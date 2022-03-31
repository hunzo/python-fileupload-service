FROM python:3.9-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./app.py /code

RUN mkdir -p /code/upload

RUN apk update --no-cache \
	&& apk add tzdata 

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV TZ=Asia/Bangkok

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]