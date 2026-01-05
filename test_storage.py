#!/usr/bin/env python3
"""
Script de prueba para verificar el comportamiento de almacenamiento
"""

import os
from oracle_service import init_oracle_game

# Configurar variables de entorno para pruebas locales
os.environ['AWS_REGION'] = 'us-east-1'
os.environ['S3_BUCKET'] = 'test-bucket'  # Cambiar por bucket real para pruebas

def test_storage_optimization():
    """Prueba que los nombres de archivo sean consistentes"""
    print("🧪 Probando optimización de almacenamiento...")

    try:
        # Simular múltiples llamadas
        for i in range(3):
            print(f"\n🔄 Iteración {i+1}")
            image_url, audio_url, labels = init_oracle_game()

            print(f"📸 URL de imagen: {image_url}")
            print(f"🔊 URL de audio: {audio_url}")
            print(f"🏷️  Número de etiquetas detectadas: {len(labels)}")

            # Verificar que las URLs contengan los nombres fijos
            assert "oracle_vision.jpg" in image_url
            assert "oracle_clues.mp3" in audio_url

        print("\n✅ Prueba exitosa: Los archivos se sobrescriben correctamente")
        print("💰 Optimización de almacenamiento implementada")

    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        print("Nota: Asegúrate de configurar AWS credentials y bucket válidos")

if __name__ == "__main__":
    test_storage_optimization()
