# AI-Powered Tool for Combating Misinformation

An innovative Generative AI-powered solution built with Google Cloud to detect potential misinformation and educate users on identifying credible, trustworthy content.

## 🎯 Project Overview

This project addresses the critical challenge of fake news and misinformation spreading rapidly across social media and messaging platforms in India. Our solution goes beyond simple fact-checking by providing educational insights into manipulative content creation techniques, fostering a more critical and informed digital citizenry.

## 🚨 Problem Statement

The rapid spread of fake news and misinformation across digital platforms poses severe threats including:
- Social unrest and public health crises
- Widespread financial scams
- Lack of accessible verification tools
- Limited understanding of manipulative content techniques

## ✨ Key Features

News Headline Verification
The news verification feature uses a multi-layered approach to analyze news headlines and provide a comprehensive authenticity score.

Multi-Source Verification: The system checks headlines against multiple news sources, including a NewsAPI integration for real-time news and various RSS feeds.

Fact-Checking: It searches for the headline and related topics on dedicated fact-checking websites to identify if the information has been previously verified or debunked.

Authenticity Scoring: An authenticity score from 0 to 100 is calculated based on factors like the number of matching sources, headline similarity, and the reputation of the news outlets.

Detailed Summary: The final result includes a detailed summary of the findings, providing context and origin information by answering the key journalistic questions: What, When, Where, and Why.

Audio Deepfake Detection
This feature analyzes uploaded audio files to determine if they are likely to be real human speech or AI-generated.

Feature Extraction: The application uses the Librosa library to extract various audio features, such as MFCCs (Mel-Frequency Cepstral Coefficients), spectral centroid, and zero-crossing rate.

Machine Learning Model: A pre-trained MLP (Multi-Layer Perceptron) model is used to classify the audio. The model has been trained to distinguish between real human voices and synthetic, AI-generated ones.

Visual Analysis: To provide a comprehensive analysis, the application generates and displays several visualizations of the audio, including a waveform, a spectrogram, and an MFCC features plot.

User-Friendly Interface: The web interface makes it easy to upload audio files and view the results, which include the prediction (e.g., 'REAL_HUMAN' or 'AI_GENERATED'), a confidence score, and the visual analysis.

## 🛠️ Technology Stack

- **AI/ML Framework**: Google Cloud AI Platform
- **Backend**: [Your backend technology]
- **Frontend**: [Your frontend technology]
- **Database**: [Your database solution]
- **Deployment**: Google Cloud Platform
- **Additional Tools**: [List any other tools/libraries used]

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- [List other requirements]

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Tushar-AIMASTER/Vidya_Jyoti.git
cd Vidya_Jyoti
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Cloud credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python app.py
```

## 📖 Usage

### Basic Usage

1. **Content Analysis**: Submit text, images, or URLs for misinformation detection
2. **Educational Mode**: Learn about common misinformation techniques
3. **Credibility Score**: Get detailed reports on content trustworthiness
4. **Fact-Checking**: Cross-reference information with reliable sources

### API Endpoints

```bash
# Analyze text content
POST /api/analyze/text
{
  "content": "Text to analyze",
  "context": "optional context"
}

# Analyze image content
POST /api/analyze/image
{
  "image_url": "URL of image to analyze"
}

# Get educational content
GET /api/education/techniques
```

## 🏗️ Project Structure

```
ai-misinformation-detector/
├── README.md
├── requirements.txt
├── rerec_MLP.pkl
├── app.py
├── utils.py
├── news_verifier.py
├── config/
├── static/
│   ├── script.js
│   ├── style.css
│   ├── tushar.jpg
│   ├── Niharika.jpg
│   ├── pragati.jpg
│   ├── shivani.jpg
│   └── ankita.jpg
│
├── templates/
│   ├── index.html
│   ├── audio.html
│   ├── audio_result.html
└── .env


```

## 🎯 Core Components

### 1. Misinformation Detection Engine
-  text analysis
- Image verification algorithms
- Pattern recognition systems

### 2. Educational Module
- Interactive learning resources
- Technique identification guides
- Real-world case studies

### 3. Credibility Assessment
- Source verification
- Cross-referencing mechanisms
- Confidence scoring

### 4. User Interface
- Clean, intuitive design
- Multi-language support
- Accessibility features


## 🔒 Privacy & Security

- No personal data storage
- Anonymous content analysis
- Secure API endpoints
- GDPR compliance


## 👥 Team

- **[Tushar Srivastava]** - Project Lead | Full Stack Developer | Core Programmer
- **[Pragati Shukla]** - Frontend Developer 
- **[Niharika Gupta]** - Frontend Developer
- **[Ankita Sharma]** - Frontend Developer
- **[Shivani Tripathi]** - Frontend Developer

## 🙏 Acknowledgments

- Google Cloud Platform for AI/ML infrastructure
- News.org API , Gnews API and Google API



## 🚀 Future Roadmap

- [ ] Multi-platform browser extension
- [ ] Mobile application development
- [ ] Advanced deep learning models
- [ ] Regional language support expansion
- [ ] Integration with social media platforms
- [ ] Real-time monitoring dashboard

