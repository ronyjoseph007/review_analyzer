from transformers import pipeline


class AspectExtractor:
    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="typeform/distilbert-base-uncased-mnli"  # Smaller model - much lighter
        )
        self.aspect_categories = [
            "service quality",
            "price",
            "product quality",
            "customer support",
            "user experience"
        ]
    
    def extract(self, texts: list[str]) -> list[str]:
        try:
            combined_text = " ".join(texts)
            results = self.classifier(
                combined_text,
                candidate_labels=self.aspect_categories,
                multi_label=True
            )
            
            # Get aspects with confidence > 0.5
            found_aspects = [
                label for label, score in zip(results['labels'], results['scores'])
                if score > 0.5
            ]
            
            return found_aspects if found_aspects else ["general"]
            
        except Exception as e:
            raise Exception(f"Error in aspect extraction: {str(e)}")
