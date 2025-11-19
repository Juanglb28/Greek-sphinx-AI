# Librería necesaria para interactuar con los servicios de Amazon
import boto3
# librería para convertir JSON → Python
import json
# librería de Python para hacer peticiones HTTP
import requests
# OS es una librería que permite interactuar con el sistema operativo.
import os


# ----------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------

# Api para recibir imagenes aleatorías
API = "https://6i0b5kx1r7.execute-api.us-east-1.amazonaws.com/oraculo/random"

rekognition = boto3.client("rekognition")
bedrock = boto3.client("bedrock-runtime")
polly = boto3.client("polly")


# Crear carpetas si no existen
os.makedirs("Assets/image", exist_ok=True)
os.makedirs("Assets/audio", exist_ok=True)


# ----------------------------------------------------
# Obtener URL prefirmada
# ----------------------------------------------------
def get_presigned_url():
    response = requests.get(API)
    data = response.json()
    return data["presignedUrl"]


# ----------------------------------------------------
# Descargar imagen
# ----------------------------------------------------
def download_image(url):
    response = requests.get(url)
    return response.content


# ----------------------------------------------------
# Guardar imagen en Assets/image
# ----------------------------------------------------
def save_image(image_bytes, filename="imagen.jpg"):
    path = os.path.join("Assets/image", filename)
    with open(path, "wb") as f:
        f.write(image_bytes)
    return path


# ----------------------------------------------------
# Procesar imagen con Rekognition
# ----------------------------------------------------
def detectar_etiquetas(image_bytes):
    response = rekognition.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=10,
        MinConfidence=70
    )
    return response["Labels"]


# ----------------------------------------------------
# Generar pistas con Bedrock Claude
# ----------------------------------------------------
def generar_pistas(etiquetas):
    lista = ", ".join([label["Name"] for label in etiquetas])

    prompt = f"""
    Eres La ESFINGE GRIEGA .
    Debes generar pistas cortas, misteriosas y únicas.
    No reveles directamente el objeto.
    Etiquetas detectadas por Rekognition: {lista}
    Entrega exactamente 3 pistas.
    Si el usuario acierta, aumenta la dificultad para una nueva pregunta
    """

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 150,
        "temperature": 0.8,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps(payload)
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


# ----------------------------------------------------
# Generar audio con Polly (voz femenina)
# ----------------------------------------------------
def generar_audio(texto, filename="oraculo.mp3"):
    response = polly.synthesize_speech(
        Text=texto,
        OutputFormat="mp3",
        VoiceId="Lucia"
    )

    audio_stream = response["AudioStream"].read()

    path = os.path.join("Assets/audio", filename)

    with open(path, "wb") as f:
        f.write(audio_stream)

    return path


# ----------------------------------------------------
# FLUJO COMPLETO DEL ORÁCULO
# ----------------------------------------------------

def oraculo():
    print("🔮 Solicitando imagen al portal del destino...")
    url = get_presigned_url()

    print("📥 Descargando imagen...")
    image_bytes = download_image(url)

    print("💾 Guardando imagen en Assets/image...")
    image_path = save_image(image_bytes)
    print("Imagen guardada en:", image_path)

    print("👁️ Analizando imagen con Rekognition...")
    etiquetas = detectar_etiquetas(image_bytes)
    print("Etiquetas:", [e["Name"] for e in etiquetas])

    print("\n🌀 Generando pistas con Bedrock...")
    pistas = generar_pistas(etiquetas)
    print("Pistas generadas:\n", pistas)

    print("\n🔊 Generando audio con Polly...")
    audio_path = generar_audio(pistas)
    print("Audio guardado en:", audio_path)

    print("\n✨ Proceso completado. El Oráculo ha hablado ✨")


# ----------------------------------------------------
# EJECUCIÓN
# ----------------------------------------------------

if __name__ == "__main__":
    oraculo()
