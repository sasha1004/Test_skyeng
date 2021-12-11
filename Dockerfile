FROM python:3.9-slim-buster

ADD requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

ADD data ./data
ADD static ./static
ADD templates ./templates
ADD main.py ./main.py
ADD utils.py ./utils.py
ADD fastapi.svg ./fastapi.svg
ENV HOST=0.0.0.0
ENV PORT=8080

EXPOSE 8080
ENTRYPOINT python main.py


