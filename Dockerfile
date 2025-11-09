FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD bash -c "service cron start && python manage.py migrate && python manage.py crontab add && python manage.py runserver 0.0.0.0:8000"
