"""
Sentiment analysis for conversations
"""
import logging
from textblob import TextBlob

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Analyze sentiment of user messages
    Returns score between -1 (negative) and 1 (positive)
    """
    
    @staticmethod
    def analyze(text: str) -> dict:
        """Analyze sentiment of text"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Determine sentiment label
            if polarity > 0.1:
                sentiment = "positive"
            elif polarity < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "requires_escalation": sentiment == "negative" and abs(polarity) > 0.5
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {
                "sentiment": "unknown",
                "polarity": 0.0,
                "subjectivity": 0.0,
                "requires_escalation": False
            }

sentiment_analyzer = SentimentAnalyzer()
