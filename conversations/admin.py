from django.contrib import admin
from .models import Conversation, Message, ConversationAnalysis

# class MessageInline(admin.TabularInline):
#     model = Message
#     extra = 0

# @admin.register(Conversation)
# class ConversationAdmin(admin.ModelAdmin):
#     inlines = [MessageInline]

# @admin.register(ConversationAnalysis)
# class ConversationAnalysisAdmin(admin.ModelAdmin):
#     list_display = ("conversation", "overall_score", "sentiment", "created_at")
admin.site.register(Conversation)
admin.site.register(ConversationAnalysis)