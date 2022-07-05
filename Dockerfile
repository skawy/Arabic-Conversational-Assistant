FROM python:3.7-slim

RUN pip install --no-cashe-dir --upgrade pip
RUN python -m pip install rasa == 2.8

WORKDIR /app

COPY . .

RUN rasa train nlu

USER 1001

ENTRYPOINT [ "rasa" ]

CMD [ "run", "--enable-api","--port","8080" ]
