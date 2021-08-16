FROM python:slim

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

ENV BOTTOKEN = 'ENTER CONFIG HERE'

EXPOSE 80

CMD echo $BOTTOKEN > config.txt

ENTRYPOINT [ "python", "app.py" ]
