from transformers import pipeline

class ReviewSummarizer:
    def __init__(self):
        self.summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-6-6",  
            max_length=130,
            min_length=30
        )
    
    def summarize(self, texts: list[str]) -> str:
        try:
            combined_text = " ".join(texts)
            if len(combined_text) > 1024:
                combined_text = combined_text[:1024]
            
            summary = self.summarizer(combined_text, do_sample=False)
            return summary[0]['summary_text']
        
        except Exception as e:
            raise Exception(f"Error in summarization: {str(e)}")
    
    def generate_tip(self, sentiment: str, aspects: list[str]) -> str:
        tips = {
            "Negative": {
                "service": "Improve staff training and customer service response times.",
                "price": "Review pricing strategy and consider competitive analysis.",
                "quality": "Implement stricter quality control measures.",
                "product": "Consider product improvements based on feedback.",
                "general": "Analyze negative feedback points for specific improvement areas."
            },
            "Neutral": {
                "general": "Focus on turning neutral experiences into positive ones."
            },
            "Positive": {
                "general": "Maintain current quality standards while monitoring feedback."
            }
        }
        
        if sentiment == "Negative":
            for aspect in aspects:
                if aspect in tips["Negative"]:
                    return tips["Negative"][aspect]
            return tips["Negative"]["general"]
        
        return tips[sentiment]["general"]
