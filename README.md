# Review Analyzer API

A FastAPI-based service that analyzes customer reviews using HuggingFace transformers.

## Features
- Sentiment Analysis
- Aspect Detection
- Review Summarization
- Improvement Tips Generation

## Requirements
- Python 3.10+
- See requirements.txt for dependencies

## Setup
1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```



## Example Usages
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "texts": [
         "Great service, but the price was too high",
         "The product quality is excellent",
         "Customer support needs improvement"
       ]
     }'
```
## swaggger ui
```bash
Go to http://127.0.0.1:8000/docs

Click "Try it out" on /analyze endpoint

Paste request JSON

Click "Execute"
```

Example Response:
```json
{
  "sentiment": "Neutral",
  "aspects": ["service quality", "price", "product quality"],
  "summary": "Mixed reviews with positive feedback on product quality and service, but concerns about pricing.",
  "improvement_tip": "Review pricing strategy and consider competitive analysis."
}
```