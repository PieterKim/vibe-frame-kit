"""Safe contract demo: deterministic mock only, no AI SDK or network calls."""
from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, StringConstraints, ValidationError

class SummarizeRequest(BaseModel):
    text: Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1)]

class SummarizeResponse(BaseModel):
    summary: str
    action_items: list[str]
    message: str

class ProviderError(Exception):
    """Adapter-normalized upstream rejection or unusable provider response."""

def mock_summary(text):
    return {"summary": text, "action_items": [], "message": "mock; not an AI quality evaluation"}

def create_app(service=mock_summary):
    app = FastAPI()
    @app.post("/api/summarize", response_model=SummarizeResponse)
    def summarize(request: SummarizeRequest):
        try:
            result = service(request.text)
            try:
                return SummarizeResponse.model_validate(result)
            except ValidationError as error:
                raise ProviderError("Unusable provider response") from error
        except (TimeoutError, ConnectionError, ProviderError):
            raise HTTPException(status_code=502, detail="Summary provider unavailable") from None
    return app

app = create_app()
