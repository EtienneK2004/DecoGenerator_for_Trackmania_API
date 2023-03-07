import time
import requests

import config
import wfc3d


#in seconds
SLEEP_DELAY = 3
URL_BASE = "http://web_python:80"
URL_GET_NEXT_BUILD = URL_BASE + "/build/next"
URL_UPDATE_BUILD = URL_BASE + "/build"
STATUS = {"Created": 0, "Pending": 1, "Failed": 2 , "Canceled": 3 , "OK":4 }

MyKey = config.MY_KEY

def getNextBuild():
    result = ""
    headers={"Authorization": MyKey}
    result =requests.get(URL_GET_NEXT_BUILD,headers=headers)
    if(result.status_code != 200):
        print("RIP getNextBuild")
    return result.json()

def postUpdateBuild(uuid, status):
    result = ""
    data='{ "uuid": "'+uuid+'", "status": '+str(status)+'}'
    headers={
        "Authorization": MyKey,
        "Content-Type" : "application/json",
        "Content-Length" : str(len(data))
    }
    result =requests.post(URL_UPDATE_BUILD,headers=headers, data=data)
    if(result.status_code != 200):
        print("RIP postUpdateBuild")
        print(str(result.status_code))
    return result.json()


### main

# maintenant faut coder ce truc
current_build_uuid = ""
current_build_file = ""

print("starting")

while(True):
    time.sleep(SLEEP_DELAY)

    current_build_uuid = ""
    current_build_file = ""

    print("check for build")
    #get next build
    next_build = getNextBuild()
    if(next_build.get("message")):
        print(next_build.get("message"))
        continue
    elif(len(next_build.get("uuid")) > 0):
        current_build_uuid = next_build.get("uuid")
        current_build_file = next_build.get("file_name")
    else:
        print("something is probably wrong.")
        continue

    print(current_build_uuid)
    print(current_build_file)
    #if build update status to pending
    print(">> update Build to PENDING.")
    postUpdateBuild(current_build_uuid, STATUS["Pending"])

    #run WFC
    print(">> run WFC.")
    #result = wfc3d.run("GrassRoad")
    #result = wfc3d.run("GrassMountains")
    result = wfc3d.run("GrassMountains")
    #time.sleep(10) #fake wfc

    #write result to file
    f = open("/usr/files/results/"+current_build_file, "w")
    f.write(result)
    f.close()

    #update status
    print(">> update Build to OK.")
    postUpdateBuild(current_build_uuid, STATUS["OK"])

    
    