FROM python:3.9-slim-buster

ADD requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

ADD data ./data
ADD static ./static
ADD templates ./templates
ADD main.py ./main.py
ADD utils.py ./utils.py
ADD favicon.ico ./favicon.ico
ENV HOST=0.0.0.0
ENV PORT=5000

EXPOSE 8080
ENTRYPOINT python main.py


