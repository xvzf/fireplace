FROM python:3.7

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PATH $PATH:/app

COPY entrypoint.py entrypoint.py
COPY fireplace fireplace

ENTRYPOINT ["python", "entrypoint.py"]