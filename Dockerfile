FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ADD requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

ADD data /app/data
ADD static /app/static
ADD templates /app/templates
ADD main.py /app/main.py
ADD utils.py /app/utils.py
ADD favicon.ico /app/favicon.ico
ENV HOST=0.0.0.0
ENV PORT=5000
ENV MAX_WORKERS=1


