🧙‍♂️ The Secret Oracle — Greek Sphinx AI

The Secret Oracle is an artificial intelligence system capable of receiving an image (from an API), analyzing it using computer vision models from AWS Rekognition, and generating a clue, riddle, or symbolic interpretation using a language model in AWS Bedrock.
Later, the system will integrate AWS Polly to convert the clues into audio.

This project aims to create a mysterious and interactive experience where users can "interpret" what the oracle sees without receiving a literal description.

A web client will be added later.

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

⚙️ Technologies Used

Python 3.11+

AWS Rekognition → Visual image analysis

AWS Bedrock → Track/text generation

AWS Polly → Audio generation

Boto3 → AWS official SDK

Requests → Image download and API consumption

Custom API for obtaining images via pre-signed URL

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


📸 Workflow

1. The API delivers a pre-signed URL to an image.

2. The system downloads the image.

3. AWS Rekognition detects objects, scenes, and tags.

4. The system generates an intelligent prompt based on these tags.

5. AWS Bedrock produces an interpretation:

* clue

* riddle

* metaphor

* AWS Polly will convert the text to speech

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


🧠 Project Objective

To create an AI that acts as a modern oracle:

It doesn't literally describe—it interprets.

The user receives a clue based on what's in the image, but presented in an enigmatic way.

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
└── images/
    └── image.jpg

----------------------------------------------------------------------------------------------------------------------------------------------------------

🚀 How to Execute the Project

1. Clone the repository
git clone https://github.com/Juanglb28/Greek-sphinx-AI.git
cd Greek-sphinx-AI

2. Create your virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Set up AWS credentials
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION

5. Execute
aws configure

6. Run 
python main.py
----------------------------------------------------------------------------------------------------------------------------------------------------------
External links:
Unicode Characters
https://www.compart.com/en/unicode/U+1F3C6
