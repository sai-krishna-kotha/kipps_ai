import re
from statistics import mean

POSITIVE_WORDS = {"thank", "thanks", "great", "good", "happy", "resolved", "solved"}
NEGATIVE_WORDS = {"bad", "not", "no", "never", "angry", "sad", "problem"}
EMPATHY_WORDS = {"sorry", "apologize", "understand"}
FALLBACK_PHRASES = {"i don't know", "not sure", "cannot help", "unable to"}

def normalize(text):
    return (text or "").lower()

def compute_sentiment(messages):
    score = 0
    for m in messages:
        text = normalize(m.text)
        for word in POSITIVE_WORDS:
            if word in text:
                score += 1
        for word in NEGATIVE_WORDS:
            if word in text:
                score -= 1
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    return "neutral"

def compute_scores(conversation):
    messages = conversation.messages.all().order_by("id")
    ai_messages = [m for m in messages if m.sender == "ai"]
    user_messages = [m for m in messages if m.sender == "user"]

    # clarity
    if ai_messages:
        lengths = [len(m.text.split()) for m in ai_messages]
        avg_length = mean(lengths) if lengths else 0
        clarity_score = min(1.0, avg_length / 20)
    else:
        clarity_score = 0.0

    # relevance
    user_keywords = set(re.findall(r"\w+", " ".join(normalize(m.text) for m in user_messages)))
    relevance_matches = sum(
        1 for a in ai_messages if user_keywords & set(re.findall(r"\w+", normalize(a.text)))
    )
    relevance_score = relevance_matches / len(ai_messages) if ai_messages else 0.0

    # accuracy
    doubtful_phrases = ["i think", "maybe", "not sure"]
    doubtful_count = sum(any(p in normalize(a.text) for p in doubtful_phrases) for a in ai_messages)
    accuracy_score = 1 - (doubtful_count / len(ai_messages)) if ai_messages else 0.0

    # completeness
    completion_phrases = ["step", "first", "then", "finally", "please do"]
    completeness_count = sum(any(p in normalize(a.text) for p in completion_phrases) for a in ai_messages)
    completeness_score = completeness_count / len(ai_messages) if ai_messages else 0.0

    # empathy
    empathy_hits = sum(any(e in normalize(a.text) for e in EMPATHY_WORDS) for a in ai_messages)
    empathy_score = empathy_hits / len(ai_messages) if ai_messages else 0.0

    # fallback
    fallback_frequency = sum(any(f in normalize(a.text) for f in FALLBACK_PHRASES) for a in ai_messages)

    # sentiment & resolution
    sentiment = compute_sentiment(user_messages)
    resolved = any(
        any(word in normalize(a.text) for word in ["resolved", "fixed", "done", "success"])
        for a in ai_messages
    )
    escalation_needed = (sentiment == "negative" and not resolved) or fallback_frequency > 1

    scores = [clarity_score, relevance_score, accuracy_score, completeness_score, empathy_score]
    overall_score = sum(scores) / len(scores) if scores else 0.0

    return {
        "clarity_score": round(clarity_score, 3),
        "relevance_score": round(relevance_score, 3),
        "accuracy_score": round(accuracy_score, 3),
        "completeness_score": round(completeness_score, 3),
        "empathy_score": round(empathy_score, 3),
        "sentiment": sentiment,
        "fallback_frequency": fallback_frequency,
        "resolution": resolved,
        "escalation_needed": escalation_needed,
        "response_time_avg": 15.0,
        "overall_score": round(overall_score, 3),
    }
