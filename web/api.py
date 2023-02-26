#################################
#~~~~~~ App ENSIIE- NOSQL ~~~~~~# 
#################################

# Import framework
from flask import Flask,render_template, request, redirect, url_for, session
import logging
import os
import datetime
from datetime import datetime, timedelta
import json
#from flask_restful import Resource, Api 
import psycopg2
import uuid

import config

import entity.Build as Build
import entity.repository.buildRepository as buildRepository
import model.WFCResultOutputDto as WFCResultOutputDto
import model.WFCServerOutputDto as WFCServerOutputDto
from StatusEnum import status as BuildStatus

# global variables
ServerKeys = config.SERVER_KEYS

# initialisation de l'application
app = Flask(__name__)


#### FUNCTIONS ####
def checkAutorisation(token):
	return token in ServerKeys

#### HEALTHCHECK ####
#only used to check database status			
@app.route('/psql')
def postgres():
	try:
		conn = psycopg2.connect(
			host="psql",    #nom du service compose
			database="postgres",
			user="postgres",
			password="postgres",
			port='5432')
		conn.close()
		return {
		'psql': ['connexion:', 'OK']
		}
	except:
		return {
			'psql': ['fail']
		}

#### TEMPLATED PAGE ####
@app.route('/')
def index():
	return redirect(url_for('home'))

@app.route('/home', methods = ['GET'])
def home():
		data = {}
		return render_template("home.html", data=data)


#### TM CLIENT API ENDPOINTS ####
"""
{
	"account_id": "string",
	"blockset_name": "string",
	"subset": ["string"],
	"size": [x,y,z]
}
return
{
	"uuid": "string",
	"status": StatusEnum,
	"JsonBlocks": [
		{
			"Coord": [x,y,z],
			"BlockModelName": "string",
			"Dir": int(0|1|2|3),
			"Color": int(0|1|2|3|4),
			"Mode": 0, //0 = Normal, 1= AirMode with MixMapping
		},
		...
	]
}
"""

# Create a new wfc generation with parameters
@app.route("/generate", methods=["POST"])
def getGenerate():
		
	build = Build.Build()
	build.uuid = str(uuid.uuid4())

	#check if uuid is unique
	isUnique = False
	while not isUnique :
		tmpBuild = buildRepository.findByUuid(build.uuid)
		if tmpBuild == False:
			isUnique = True

	build.account_id = request.json.get('account_id')
	build.status = BuildStatus["Created"]
	build.setResultFileName()
	
	#> TODO add wfc parameters to Build class
	blockset_name = request.json.get('blockset_name')
	subset = request.json.get('subset')
	size = request.json.get('size')

	buildRepository.persist(build)

	response = WFCResultOutputDto.WFCResultOutputDto()
	response.uuid = build.uuid
	response.status = build.status

	return response.json()

# [FOR TM USER]
@app.route("/build/<uuid>", methods=["GET"])
def getBuildResult(uuid):
	#get build
	build = buildRepository.findByUuid(uuid)
	print("build")
	print(build)
	response = WFCResultOutputDto.WFCResultOutputDto()

	if build is False :
		response.status = -1
		return response.json()

	response.uuid = build.uuid
	response.status = build.status
	if(not response.status == BuildStatus["OK"]):
		return response.json()
		
	#read file
	f = open("/usr/files/results/" + build.file_name, "r")
	#print(f.read())
	#json_value = json.loads(f.read())
	response.JsonBlocks = json.loads(f.read())

	#return WFCResultOutputDto
	return response.json()

#### WFC SERVER API ENDPOINTS (need Authorization) ####

# [FOR WFC SERVER]
@app.route("/build/next", methods=["GET"])
def getNextBuild():
	#check Authorization Header
	if not checkAutorisation(request.headers.get('Authorization')) :
		return { "message" : "Access denied." }
	
	#get next Created Build by older date
	build = buildRepository.findNextBuildByCreatedDate()

	if build is False:
		return {"message":"no more build to process."}

	response = WFCServerOutputDto.WFCServerOutputDto()
	response.uuid = build.uuid
	response.status = build.status
	response.file_name = build.file_name
	
	#return build
	return response.json()

# [FOR WFC SERVER]
@app.route("/build", methods=["POST"])
def updateBuildStatus():
	#check Authorization Header
	if not checkAutorisation(request.headers.get('Authorization')) :
		return { "message" : "Access denied." }

	#get body uuid and status
	print(request.json)
	build_uuid = request.json.get('uuid')
	status = request.json.get('status')
		
	#get build from db
	build = buildRepository.findByUuid(build_uuid)
	if build is False:
		return {"message":"build does not exist."}

	#set status and finish date
	build.status = status
	build.setFinishDate()

	#persist
	buildRepository.persist(build)

	#return 200
	response = WFCServerOutputDto.WFCServerOutputDto()
	response.uuid = build.uuid
	response.status = build.status
	response.file_name = build.file_name
	return response.json()



# App launch
if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=80, debug=True)