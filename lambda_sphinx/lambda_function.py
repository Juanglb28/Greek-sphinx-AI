"""
AWS Lambda handler for The Secret Oracle API
Usa Mangum para adaptar FastAPI a AWS Lambda
"""

# Instalar dependencias si es necesario:
# pip install -r ../requirements.txt

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Dict, Any
import os

# Importar lógica de negocio
from oracle_service import (
    init_oracle_game,
    validar_respuesta_bedrock
)

# Crear aplicación FastAPI
app = FastAPI(
    title="The Secret Oracle API",
    description="API del Oráculo Secreto para AWS Lambda",
    version="1.0.0"
)

# Configurar CORS para Vercel frontend
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://your-vercel-app.vercel.app").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Modelos Pydantic
class InitResponse(BaseModel):
    image_url: str
    audio_url: str
    labels: List[Dict[str, Any]]

class GuessRequest(BaseModel):
    guess: str
    labels: List[Dict[str, Any]]

class GuessResponse(BaseModel):
    resultado: str
    mensaje_esfinge: str

# Endpoints de la API
@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy", "service": "oracle-api"}

@app.post("/api/oracle/init", response_model=InitResponse)
async def init_oracle():
    """Inicializa un nuevo juego del oráculo"""
    try:
        image_url, audio_url, labels = init_oracle_game()
        return InitResponse(
            image_url=image_url,
            audio_url=audio_url,
            labels=labels
        )
    except Exception as e:
        print(f"Error in init_oracle: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/oracle/guess", response_model=GuessResponse)
async def guess_oracle(request: GuessRequest):
    """Valida la respuesta del usuario"""
    try:
        result = validar_respuesta_bedrock(request.guess, request.labels)
        return GuessResponse(**result)
    except Exception as e:
        print(f"Error in guess_oracle: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Handler para AWS Lambda
handler = Mangum(app, lifespan="off")

# Para desarrollo local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
