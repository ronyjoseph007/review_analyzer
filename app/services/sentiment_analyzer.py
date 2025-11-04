from transformers import pipeline
from typing import List, Dict
import logging

class SentimentAnalyzer:
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """Initialize the sentiment analyzer with a specified model"""
        try:
            self.classifier = pipeline(
                "sentiment-analysis",
                model=model_name,
                top_k=None  
            )
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize sentiment analyzer: {str(e)}")

    def analyze(self, texts: List[str]) -> Dict[str, any]:
        """
        Analyze sentiment of multiple reviews
        Returns both overall sentiment and confidence scores
        """
        try:
            if not texts:
                raise ValueError("Empty text list provided")

            results = self.classifier(texts)
            
            # Calculate sentiment scores
            positive_scores = []
            for review_scores in results:
                # Get the positive score for each review
                pos_score = next(score['score'] for score in review_scores if score['label'] == 'POSITIVE')
                positive_scores.append(pos_score)
            
            # Calculate average positive score
            avg_positive = sum(positive_scores) / len(positive_scores)
            
            # Determine overall sentiment with confidence
            if avg_positive > 0.6:
                sentiment = "Positive"
                confidence = avg_positive
            elif avg_positive < 0.4:
                sentiment = "Negative"
                confidence = 1 - avg_positive
            else:
                sentiment = "Neutral"
                confidence = 1 - abs(0.5 - avg_positive) * 2

            return {
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "review_scores": positive_scores
            }
            
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            raise Exception(f"Sentiment analysis failed: {str(e)}")
