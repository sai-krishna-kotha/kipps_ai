from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, ConversationAnalysis
from .serializers import (
    ConversationCreateSerializer,
    ConversationSerializer,
    ConversationAnalysisSerializer,
)
from .analysis_utils import compute_scores

@api_view(["POST"])
def upload_conversation(request):
    serializer = ConversationCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    conversation = serializer.save()
    return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def analyze_conversation(request, conv_id):
    try:
        conversation = Conversation.objects.get(id=conv_id)
    except Conversation.DoesNotExist:
        return Response({"detail": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
    scores = compute_scores(conversation)
    analysis, _ = ConversationAnalysis.objects.update_or_create(
        conversation=conversation, defaults=scores
    )
    return Response(ConversationAnalysisSerializer(analysis).data)

@api_view(["GET"])
def list_analyses(request):
    analyses = ConversationAnalysis.objects.select_related("conversation").order_by("-created_at")
    serializer = ConversationAnalysisSerializer(analyses, many=True)
    return Response(serializer.data)
