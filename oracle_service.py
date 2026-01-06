# Oracle Service - Lógica de negocio separada
import boto3
import json
import requests
import os
from typing import List, Dict, Any, Tuple

# ----------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------

# ----------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------

API = "https://6i0b5kx1r7.execute-api.us-east-1.amazonaws.com/oraculo/random"

# Configuración S3
S3_BUCKET = os.getenv("S3_BUCKET", "oracle-assets-bucket")
S3_REGION = os.getenv("S3_REGION", os.getenv("AWS_REGION", "us-east-1"))

# Inicializar clientes AWS
rekognition = boto3.client("rekognition")
bedrock = boto3.client("bedrock-runtime")
polly = boto3.client("polly")
s3 = boto3.client("s3", region_name=S3_REGION)

# ----------------------------------------------------
# Funciones de negocio
# ----------------------------------------------------

def get_presigned_url() -> str:
    """Obtiene URL prefirmada de la API externa"""
    response = requests.get(API)
    response.raise_for_status()
    return response.json()["presignedUrl"]

def download_image(url: str) -> bytes:
    """Descarga imagen desde URL"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def upload_to_s3(data: bytes, key: str, content_type: str = "image/jpeg") -> str:
    """Sube datos a S3 y retorna una URL prefirmada para lectura"""
    # 1. Upload without ACL (works with Bucket Owner Enforced)
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=data,
        ContentType=content_type
        # Removed ACL='public-read'
    )
    
    # 2. Generate Presigned URL for reading (valid for 1 hour)
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': key},
        ExpiresIn=3600
    )
    return url

def save_image_to_s3(image_bytes: bytes, filename: str) -> str:
    """Guarda imagen en S3 y retorna URL"""
    key = f"images/{filename}"
    return upload_to_s3(image_bytes, key, "image/jpeg")

def save_audio_to_s3(audio_bytes: bytes, filename: str) -> str:
    """Guarda audio en S3 y retorna URL"""
    key = f"audio/{filename}"
    return upload_to_s3(audio_bytes, key, "audio/mpeg")

def detectar_etiquetas(image_bytes: bytes) -> List[Dict[str, Any]]:
    """Detecta etiquetas en imagen usando Rekognition"""
    response = rekognition.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=10,
        MinConfidence=70
    )
    return response["Labels"]

def validar_respuesta_bedrock(respuesta_usuario: str, etiquetas: List[Dict[str, Any]]) -> Dict[str, str]:
    """Valida respuesta del usuario usando Bedrock"""
    lista = ", ".join([label["Name"] for label in etiquetas])

    prompt = f"""
    Adopta el rol de LA ESFINGE GRIEGA.
    Hablas en tono antiguo, poético, místico y solemne.
    Nunca uses lenguaje técnico ni menciones "etiquetas", "IA" o "coincidencias".

    Tu tarea es evaluar si la respuesta del mortal coincide con la verdad
    oculta detrás de estas descripciones del objeto: {lista}.

    Clasifica la respuesta en:
    - "correcto": si acertó o dijo un sinónimo equivalente.
    - "sinonimo": si su palabra es equivalente, relacionada o válida.
    - "cercano": si intuye parte de la esencia pero no del todo.
    - "incorrecto": si no guarda relación.

    Devuelve SIEMPRE solo un JSON así:

    {{
        "resultado": "correcto" | "sinonimo" | "cercano" | "incorrecto",
        "mensaje_esfinge": "tu mensaje místico, máximo 2 líneas"
    }}

    Respuesta del mortal: "{respuesta_usuario}"
    """

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "temperature": 0.7,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps(payload)
    )

    raw = json.loads(response["body"].read())["content"][0]["text"]

    try:
        return json.loads(raw)
    except:
        return {
            "resultado": "incorrecto",
            "mensaje_esfinge": "Tus palabras se pierden como bruma en el abismo. Intenta de nuevo."
        }

def generar_pistas(etiquetas: List[Dict[str, Any]]) -> str:
    """Genera pistas enigmáticas usando Bedrock"""
    lista = ", ".join([label["Name"] for label in etiquetas])

    prompt = f"""
    Eres LA ESFINGE GRIEGA.
    Ofrece exactamente 3 pistas en estilo enigmático, poético y simbólico.
    No reveles directamente el objeto.
    Basado en estas descripciones del mundo humano: {lista}
    """

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 160,
        "temperature": 0.8,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps(payload)
    )

    return json.loads(response["body"].read())["content"][0]["text"]

def generar_audio(texto: str) -> bytes:
    """Genera audio usando Polly"""
    response = polly.synthesize_speech(
        Text=texto,
        OutputFormat="mp3",
        VoiceId="Lucia"
    )
    return response["AudioStream"].read()

def init_oracle_game() -> Tuple[str, str, List[Dict[str, Any]]]:
    """Inicializa un nuevo juego del oráculo

    Returns:
        Tuple con (image_url, audio_url, labels)
    """
    # 1. Obtener imagen
    url = get_presigned_url()
    image_bytes = download_image(url)

    # 2. Usar nombres fijos para sobrescribir archivos y minimizar almacenamiento
    # Esto mantiene solo 2 archivos en S3: oracle_vision.jpg y oracle_clues.mp3
    # reduciendo costos de almacenamiento significativamente
    image_filename = "oracle_vision.jpg"
    audio_filename = "oracle_clues.mp3"

    # 3. Detectar etiquetas
    labels = detectar_etiquetas(image_bytes)

    # 4. Generar pistas
    clues = generar_pistas(labels)

    # 5. Generar audio
    audio_bytes = generar_audio(clues)

    # 6. Subir a S3 (sobrescribiendo archivos existentes)
    image_url = save_image_to_s3(image_bytes, image_filename)
    audio_url = save_audio_to_s3(audio_bytes, audio_filename)

    return image_url, audio_url, labels

# ----------------------------------------------------
# Funciones de compatibilidad (legacy)
# ----------------------------------------------------

def save_image(image_bytes: bytes, filename: str = "oracle_vision.jpg") -> str:
    """Función legacy para compatibilidad - ahora usa S3 con nombre fijo"""
    # Esta función se mantiene por compatibilidad pero ahora usa S3 con nombre fijo
    key = f"images/{filename}"
    return upload_to_s3(image_bytes, key, "image/jpeg")

# ----------------------------------------------------
# Función Lambda (legacy)
# ----------------------------------------------------

def lambda_handler(event, context):
    """Handler legacy para Lambda"""
    return {
        "statusCode": 200,
        "body": json.dumps({"mensaje": "Oráculo operativo"})
    }
