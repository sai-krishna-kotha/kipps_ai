from django.db import models

class Conversation(models.Model):
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.title or 'untitled'}"

class Message(models.Model):
    SENDER_CHOICES = (("user", "user"), ("ai", "ai"))
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:40]}"

class ConversationAnalysis(models.Model):
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name="analysis")
    clarity_score = models.FloatField()
    relevance_score = models.FloatField()
    accuracy_score = models.FloatField()
    completeness_score = models.FloatField()
    empathy_score = models.FloatField()
    sentiment = models.CharField(max_length=20)
    fallback_frequency = models.IntegerField()
    resolution = models.BooleanField()
    escalation_needed = models.BooleanField()
    response_time_avg = models.FloatField()
    overall_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for conv {self.conversation.id} - score {self.overall_score:.2f}"
