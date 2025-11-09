import datetime
import sys
from .models import Conversation, ConversationAnalysis
from .analysis_utils import compute_scores

def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    sys.stdout.write(line)
    sys.stdout.flush()
    with open("/app/cron.log", "a") as f:
        f.write(line)

def run_daily_analysis():
    log_message("Cron started.")
    pending = Conversation.objects.filter(analysis__isnull=True)
    log_message(f"Found {pending.count()} unanalysed conversations.")
    for conversation in pending:
        scores = compute_scores(conversation)
        ConversationAnalysis.objects.create(conversation=conversation, **scores)
    log_message("Analysis completed.")
