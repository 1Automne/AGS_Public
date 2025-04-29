FROM python:3-alpine

WORKDIR /usr/src/agstats

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache tzdata
ENV TZ=Asia/Novosibirsk

COPY . .

CMD [ "python3", "./run.py" ]
