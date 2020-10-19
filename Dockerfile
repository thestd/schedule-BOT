FROM python:3.7.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "manage.py", "run"]
