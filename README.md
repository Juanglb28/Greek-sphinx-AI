#  The Secret Oracle — Greek Sphinx AI

The Greek Sphinx is an artificial intelligence system capable of receiving an image (from an API), analyzing it using computer vision models from AWS Rekognition, and generating a clue, riddle, or symbolic interpretation using a language model in AWS Bedrock.
Later, the system will integrate AWS Polly to convert the clues into audio.

This project aims to create a mysterious and interactive experience where users can "interpret" what the oracle sees without receiving a literal description.



##  Features

- **Computer Vision**: AWS Rekognition analyzes images to detect objects and scenes
- **AI-Powered Riddles**: AWS Bedrock (Claude) generates poetic, enigmatic clues
- **Text-to-Speech**: AWS Polly converts clues into mystical audio narration
- **Web Interface**: React-based frontend with mystical UI
- **Serverless Backend**: AWS Lambda + API Gateway
- **Cloud Storage**: AWS S3 for assets
- **Modern Deployment**: Vercel for frontend, AWS Lambda for backend

##  Architecture

```
User (Browser) → Vercel (Frontend)
                      ↓
               AWS API Gateway
                      ↓
               AWS Lambda (FastAPI + Mangum)
                      ↓
    ┌─────────────────────────────────────┐
    │         Business Logic Layer        │
    │  • Image Processing (Rekognition)   │
    │  • Clue Generation (Bedrock)        │
    │  • Audio Synthesis (Polly)          │
    │  • S3 Storage Management            │
    └─────────────────────────────────────┘
                      ↓
              AWS S3 (Assets Storage)
```

##  Technologies Used

### Backend
- **Python 3.11+**
- **FastAPI**: Modern web framework
- **Mangum**: AWS Lambda adapter for FastAPI
- **AWS Rekognition**: Computer vision and image analysis
- **AWS Bedrock**: AI language model (Claude)
- **AWS Polly**: Text-to-speech synthesis
- **AWS S3**: Cloud storage for assets
- **Boto3**: AWS SDK

### Frontend
- **React 19**: UI framework
- **Vite**: Build tool and dev server
- **Framer Motion**: Animations
- **Lucide React**: Icons
- **Vercel**: Frontend deployment platform

### Infrastructure
- **AWS Lambda**: Serverless compute
- **API Gateway**: REST API management
- **AWS S3**: Static asset storage
- **Vercel**: Frontend hosting and deployment

##  Workflow

1. **Image Acquisition**: External API provides pre-signed URL
2. **Download & Analysis**: System downloads image and uses Rekognition to detect objects/tags
3. **Clue Generation**: AWS Bedrock creates poetic, enigmatic interpretations
4. **Audio Synthesis**: AWS Polly converts text clues to mystical narration
5. **Storage**: Assets uploaded to S3 with **fixed filenames** (oracle_vision.jpg, oracle_clues.mp3) to minimize storage usage
6. **User Interaction**: Frontend displays image/audio, user makes guesses
7. **Validation**: AI evaluates user responses with sphinx-like wisdom

##  Project Objective

Create an AI that acts as a modern oracle:
- **Doesn't describe literally**—interprets symbolically
- **Generates riddles and metaphors** instead of direct answers
- **Provides mystical, enigmatic experiences**
- **Combines ancient mythology with cutting-edge AI**


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🔮 Project Architecture

User → Image → API → Amazon Rekognition
                    ↓
                Tags/Objecs
                    ↓
          Dynamic Prompt → AWS Bedrock
                    ↓
                  Riddle
                    ↓
               AWS Polly → Audio



----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📁Project Structure

/Project
│ main.py
│ rekognition_utils.py
│ bedrock_utils.py
│ polly_utils.py (future)
│ requirements.txt
│ README.md
│
├── lambda_sphinx/
│   └── lambda_function.py     # AWS Lambda handler
│
├── Frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── config.js         # Environment configuration
│   │   └── components/
│   │       └── OracleEye.jsx # Mystical UI component
│   ├── vercel.json           # Vercel deployment config
│   ├── env.example          # Frontend env template
│   └── package.json
│
└── Assets/                   # Local development assets
    ├── image/
    └── audio/
```

##  Deployment Guide

### Prerequisites
- AWS Account with appropriate permissions
- Vercel Account
- Python 3.11+
- Node.js 18+

### Backend Deployment (AWS Lambda)

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd Proyecto
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or: venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure AWS**
   ```bash
   aws configure
   # Enter your AWS credentials and region
   ```

3. **Create S3 Bucket**
   ```bash
   aws s3 mb s3://oracle-assets-bucket --region us-east-1
   # Note: Update bucket name in env.example
   ```

4. **Deploy to AWS Lambda**
   ```bash
   # Install AWS SAM CLI or use AWS Console
   # Package lambda_sphinx/ directory
   # Deploy as Lambda function with API Gateway
   ```

5. **Environment Variables**
   Copy `env.example` to `.env` and configure:
   ```bash
   AWS_REGION=us-east-1
   S3_BUCKET=your-bucket-name
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

### Frontend Deployment (Vercel)

1. **Setup Frontend**
   ```bash
   cd Frontend
   npm install
   ```

2. **Configure Environment**
   Copy `env.example` to `.env.local`:
   ```
   VITE_API_URL=https://your-lambda-url.amazonaws.com/api/oracle
   ```

3. **Deploy to Vercel**
   ```bash
   npm install -g vercel
   vercel --prod
   # Or connect GitHub repo to Vercel dashboard
   ```

### Local Development

1. **Backend**
   ```bash
   # From project root
   python server.py
   # Server runs on http://localhost:8000
   ```

2. **Frontend**
   ```bash
   cd Frontend
   npm run dev
   # Frontend runs on http://localhost:5173
   ```

3. **Testing Storage Optimization**
   ```bash
   python test_storage.py
   # Verifies that files are properly overwritten
   ```

## 🔧 Configuration

### AWS Permissions Required
- `rekognition:DetectLabels`
- `bedrock:InvokeModel`
- `polly:SynthesizeSpeech`
- `s3:GetObject`, `s3:PutObject`
- `lambda:InvokeFunction`
- `apigateway:*`

### Environment Variables
- **Backend**: See `env.example`
- **Frontend**: See `Frontend/env.example`

## 🔧 Troubleshooting

### Common Issues

**Lambda Timeout**: Increase timeout in Lambda configuration (recommended: 30s)

**CORS Errors**: Ensure CORS_ORIGINS includes your Vercel domain

**S3 Access Denied**: Check bucket permissions and IAM roles

**Bedrock Model Access**: Ensure Claude model is enabled in your AWS account

### Performance Optimization

- **Rekognition**: Use specific regions for lower latency
- **Bedrock**: Consider model caching for repeated prompts
- **S3**: Enable CloudFront CDN for asset delivery
- **Storage**: Fixed filenames minimize S3 storage costs (only 2 files ever stored)

## 📚 External Resources

- [AWS Lambda with FastAPI](https://mangum.io/)
- [Vercel Deployment Guide](https://vercel.com/docs)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Unicode Characters](https://www.compart.com/en/unicode/U+1F3C6)
