# El Oráculo Secreto (The Secret Oracle)

Este proyecto es una aplicación web interactiva que conecta con servicios de AWS a través de un backend en Python/FastAPI.

## Tecnologías Utilizadas

### Frontend
- **React**: ^19.2.1
- **Vite**: ^7.2.4
- **Framer Motion**: ^12.23.24 (Animaciones)
- **Lucide React**: ^0.555.0 (Iconos)

### Backend (Python)
- **FastAPI**: 0.122.0
- **Uvicorn**: 0.38.0
- **Boto3**: 1.40.73 (AWS SDK)
- **Mangum**: 0.19.0 (AWS Lambda handler)
- **Pydantic**: 2.12.4

## Características
- **Mecánica de Juego**: Adivinanza de imágenes generadas/gestionadas por IA.
- **Intentos Limitados**: 3 oportunidades para adivinar.
- **Imagen Oculta**: La imagen se revela solo al ganar, perder o solicitar verlo.
- **Interfaz en Español**: Toda la UI ha sido traducida al español.

## Configuración y Ejecución

1.  **Backend**:
    ```bash
    pip install -r requirements.txt
    python server.py
    ```
2.  **Frontend**:
    ```bash
    cd Frontend
    npm install
    npm run dev
    ```
