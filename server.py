from dotenv import load_dotenv
import os

# Cargar variables de entorno antes de importar servicios que las usan
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# Import business logic from the service module
from oracle_service import (
    init_oracle_game,
    validar_respuesta_bedrock
)

app = FastAPI(title="The Secret Oracle API")

# Enable CORS for frontend
# En producción, especificar la URL del frontend en Vercel
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InitResponse(BaseModel):
    image_url: str
    audio_url: str
    labels: List[Dict[str, Any]] # Sending labels to client to send back for validation (stateless)

class GuessRequest(BaseModel):
    guess: str
    labels: List[Dict[str, Any]]

@app.post("/api/oracle/init", response_model=InitResponse)
async def init_oracle():
    try:
        # Usar la función refactorizada que maneja todo el flujo
        image_url, audio_url, labels = init_oracle_game()

        return InitResponse(
            image_url=image_url,
            audio_url=audio_url,
            labels=labels
        )

    except Exception as e:
        print(f"Error in init_oracle: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/oracle/guess")
async def guess_oracle(request: GuessRequest):
    try:
        result = validar_respuesta_bedrock(request.guess, request.labels)
        return result
    except Exception as e:
        print(f"Error in guess_oracle: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
