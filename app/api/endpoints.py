from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import ReviewRequest, AnalysisResponse
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.aspect_extractor import AspectExtractor
from app.services.summarizer import ReviewSummarizer
import asyncio

router = APIRouter(tags=["analyze"])

# Module-level cache for lazy-loaded models
_models_cache = {}

async def get_models(request: Request):
    """Lazily load models on first request"""
    global _models_cache
    
    if not _models_cache:
        # Load models only once, on first request
        loop = asyncio.get_event_loop()
        _models_cache['sentiment_analyzer'] = await loop.run_in_executor(None, SentimentAnalyzer)
        _models_cache['aspect_extractor'] = await loop.run_in_executor(None, AspectExtractor)
        _models_cache['review_summarizer'] = await loop.run_in_executor(None, ReviewSummarizer)
    
    return _models_cache

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_reviews(request: ReviewRequest, fastapi_request: Request):
    """
    Accepts a list of review texts and returns:
    - overall sentiment (Positive/Neutral/Negative)
    - detected aspects (list)
    - short summary (2-3 lines)
    - an actionable improvement tip
    """
    try:
        if not request.texts:
            raise HTTPException(status_code=400, detail="`texts` must be a non-empty list of strings")

        # Lazily load models
        models = await get_models(fastapi_request)
        sentiment_analyzer = models['sentiment_analyzer']
        aspect_extractor = models['aspect_extractor']
        review_summarizer = models['review_summarizer']

        sent_result = sentiment_analyzer.analyze(request.texts)
        sentiment = sent_result.get("sentiment") if isinstance(sent_result, dict) else sent_result

        aspects = aspect_extractor.extract(request.texts)
        summary = review_summarizer.summarize(request.texts)
        tip = review_summarizer.generate_tip(sentiment, aspects)

        return AnalysisResponse(
            sentiment=sentiment,
            aspects=aspects,
            summary=summary,
            improvement_tip=tip
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))