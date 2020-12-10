FROM python:3
ENV BOT_KEY_SAVECOINS=<BOT_KEY>
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./app.py"]

