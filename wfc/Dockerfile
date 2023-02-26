FROM python:3-onbuild
COPY ./server /usr/src/app
RUN pip install -r requirements.txt
CMD ["python", "-u", "server.py"]