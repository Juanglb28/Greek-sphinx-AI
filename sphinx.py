# Librerías necesarias para interactuar con los servicios de Amazon
import boto3
import json
import requests
import os


# ----------------------------------------------------
# Función Lambda 
# ----------------------------------------------------

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"mensaje": "Oráculo operativo"})
    }



# ----------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------

API = "https://6i0b5kx1r7.execute-api.us-east-1.amazonaws.com/oraculo/random"

rekognition = boto3.client("rekognition")
bedrock = boto3.client("bedrock-runtime")
polly = boto3.client("polly")

os.makedirs("Assets/image", exist_ok=True)
os.makedirs("Assets/audio", exist_ok=True)


# ----------------------------------------------------
# Obtener URL prefirmada
# ----------------------------------------------------
def get_presigned_url():
    response = requests.get(API)
    return response.json()["presignedUrl"]


# ----------------------------------------------------
# Descargar imagen
# ----------------------------------------------------
def download_image(url):
    return requests.get(url).content


# ----------------------------------------------------
# Guardar imagen
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
# Validación inteligente con estilo mitológico
# ----------------------------------------------------
def validar_respuesta_bedrock(respuesta_usuario, etiquetas):
    lista = ", ".join([label["Name"] for label in etiquetas])

    prompt = f"""
    Adopta el rol de LA ESFINGE GRIEGA.
    Hablas en tono antiguo, poético, místico y solemne.
    Nunca uses lenguaje técnico ni menciones “etiquetas”, “IA” o “coincidencias”.

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


# ----------------------------------------------------
# Generar pistas con Bedrock
# ----------------------------------------------------
def generar_pistas(etiquetas):
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


# ----------------------------------------------------
# Generar audio (Polly)
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
    print("🔮 Solicitando imagen sagrada...")
    url = get_presigned_url()

    print("📥 Descargando visión del destino...")
    image_bytes = download_image(url)

    print("💾 Sellando la imagen en los archivos del Oráculo...")
    save_image(image_bytes)

    print("👁️ La Esfinge examina la escena...")
    etiquetas = detectar_etiquetas(image_bytes)

    print("\n🌀 Tejiendo pistas enigmáticas...")
    pistas = generar_pistas(etiquetas)
    print("\n--- PISTAS DE LA ESFINGE ---")
    print(pistas)

    print("\n🔊 Invocando la voz del Oráculo...")
    generar_audio(pistas)

    print("\n✨ El Oráculo ha hablado. Ahora, mortal... responde. ✨")

    # -----------------------------
    # VALIDACIÓN MITOLÓGICA
    # -----------------------------
    respuesta = input("\n🗣️ ¿Qué crees que oculta la imagen?: ")

    veredicto = validar_respuesta_bedrock(respuesta, etiquetas)

    print("\n📜 La Esfinge responde:")
    print(veredicto["mensaje_esfinge"])

    if veredicto["resultado"] in ["correcto", "sinonimo"]:
        print("\n🏆 Has superado el enigma de la Esfinge.")
    else:
        print("\n💀 Tu palabra no desveló el misterio...")


# ----------------------------------------------------
# EJECUCIÓN
# ----------------------------------------------------
if __name__ == "__main__":
    oraculo()
