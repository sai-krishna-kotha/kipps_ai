# KIPPS AI – Conversation Quality Analyzer

A Django-based web app that analyzes AI–User conversations for clarity, relevance, empathy, accuracy, and completeness.  
It uses rule-based logic to score conversations and runs daily automated analysis via a cron job.

---

## Setup and Run Instructions

### 1. Clone and install
```bash
git clone <repo_url>
cd kipps_ai
pip install -r requirements.txt
```

## Docker Setup
```bash
docker build -t kipps_ai_app .
docker run -d -p 8080:8000 kipps_ai_app
docker exec -it <container_id> bash
```
then open http://localhost:8080/api/conversations in your browser or use postman for testing(I have used postman)

---

## Cron Job Setup

In `settings.py`:
```python
CRONJOBS = [
    ("0 0 * * *", "conversations.cron.run_daily_analysis")  # runs daily at 12:00 AM UTC
]
```

To register:
```bash
python manage.py crontab remove
python manage.py crontab add
service cron restart
python manage.py crontab show
```

Logs:
```bash
tail -f /app/cron.log
```
You can debug more using docker desktop i.e., by watching container files and its logs (just watch the container logs or navigate to docker container files and then app/cron.log to watch the logs of cron job)
---

## API Documentation

### 1 Upload Conversation
I have used postman for API testing
`POST /api/conversations/`
```json
{
  "title": "Order chat",
  "messages": [
    {"sender":"user","message":"Hi, I need help with my order."},
    {"sender":"ai","message":"Sure, can you please share your order ID?"},
    {"sender":"user","message":"It's 12345."},
    {"sender":"ai","message":"Thanks! Your order has been shipped and will arrive tomorrow."}
  ]
}

```

### 2️ Analyze Conversation
`POST /api/conversations/<id>/analyse/`(this is the api we calling in the cron job)

### 3️ Get Reports
`GET /api/reports/`

---

## Sample Response
```json
{
    "id": 27,
    "conversation": {
        "id": 28,
        "title": "Order chat",
        "created_at": "2025-11-11T23:34:30.060143+05:30",
        "messages": [
            {
                "id": 217,
                "sender": "user",
                "text": "Hi, I need help with my order.",
                "created_at": "2025-11-11T23:34:30.092390+05:30"
            },
            {
                "id": 218,
                "sender": "ai",
                "text": "Sure, can you please share your order ID?",
                "created_at": "2025-11-11T23:34:30.100566+05:30"
            },
            {
                "id": 219,
                "sender": "user",
                "text": "It's 12345.",
                "created_at": "2025-11-11T23:34:30.108467+05:30"
            },
            {
                "id": 220,
                "sender": "ai",
                "text": "Thanks! Your order has been shipped and will arrive tomorrow.",
                "created_at": "2025-11-11T23:34:30.115856+05:30"
            }
        ]
    },
    "clarity_score": 0.45,
    "relevance_score": 1.0,
    "accuracy_score": 1.0,
    "completeness_score": 0.0,
    "empathy_score": 0.0,
    "sentiment": "neutral",
    "fallback_frequency": 0,
    "resolution": false,
    "escalation_needed": false,
    "response_time_avg": 15.0,
    "overall_score": 0.49,
    "created_at": "2025-11-11T23:34:39.774170+05:30"
}
```

