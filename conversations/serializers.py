from rest_framework import serializers
from .models import Conversation, Message, ConversationAnalysis

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "text", "created_at"]

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ["id", "title", "created_at", "messages"]

class ConversationCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True)
    messages = serializers.ListField(child=serializers.DictField(), allow_empty=False)

    def create(self, validated_data):
        conv = Conversation.objects.create(title=validated_data.get("title", ""))
        for m in validated_data["messages"]:
            Message.objects.create(
                conversation=conv,
                sender=m.get("sender", "user"),
                text=m.get("message") or m.get("text", "")
            )
        return conv

class ConversationAnalysisSerializer(serializers.ModelSerializer):
    conversation = ConversationSerializer()
    class Meta:
        model = ConversationAnalysis
        fields = "__all__"
