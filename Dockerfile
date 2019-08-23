FROM python:3.7.4-alpine3.10 as base
RUN apk add --no-cache build-base
COPY ./requirements.txt /requirements.txt
RUN pip3 install --target="/install" -r /requirements.txt


FROM python:3.7.4-alpine3.10
ENV PYTHONUNBUFFERED 1
COPY --from=base /install /usr/local/lib/python3.7/site-packages
RUN mkdir /app
WORKDIR /app
COPY ./ ./
ENTRYPOINT ["python3", "manage.py", "run"]

