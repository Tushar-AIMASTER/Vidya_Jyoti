# VIDYA JYOTI:  AI-Powered Tool for Combating Misinformation 

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

### News Headline Verification
  - The news verification feature uses a multi-layered approach to analyze news headlines and provide a comprehensive authenticity score.

  - Multi-Source Verification: The system checks headlines against multiple news sources, including a NewsAPI integration for real-time news and various RSS feeds.

  - Fact-Checking: It searches for the headline and related topics on dedicated fact-checking websites to identify if the information has been previously verified or debunked.

  - Authenticity Scoring: An authenticity score from 0 to 100 is calculated based on factors like the number of matching sources, headline similarity, and the reputation of the news outlets.

  - Detailed Summary: The final result includes a detailed summary of the findings, providing context and origin information by answering the key journalistic questions: What, When, Where, and Why.

### Audio Deepfake Detection
  This feature analyzes uploaded audio files to determine if they are likely to be real human speech or AI-generated.

  - Feature Extraction: The application uses the Librosa library to extract various audio features, such as MFCCs (Mel-Frequency Cepstral Coefficients), spectral centroid, and zero-crossing rate.

  - Machine Learning Model: A pre-trained MLP (Multi-Layer Perceptron) model is used to classify the audio. The model has been trained to distinguish between real human voices and synthetic, AI-generated ones.

  - Visual Analysis: To provide a comprehensive analysis, the application generates and displays several visualizations of the audio, including a waveform, a spectrogram, and an MFCC features plot.

  - User-Friendly Interface: The web interface makes it easy to upload audio files and view the results, which include the prediction (e.g., 'REAL_HUMAN' or 'AI_GENERATED'), a confidence score, and the visual analysis.

## 🛠️ Technology Stack

### 🌐 Web Framework & Server
- **Flask:** A micro web framework for building the application's backend and handling routes.

- **Gunicorn:** A Python Web Server Gateway Interface (WSGI) HTTP server used to deploy the Flask application in a production environment.

### 📊 Data & ML
- **Scikit-learn:** A machine learning library used for building the MLP (Multi-layer Perceptron) model for deepfake detection.

- **Numpy:** A fundamental library for numerical operations, used for handling multi-dimensional arrays and mathematical functions.

- **Joblib:** A tool used for saving and loading Python objects, specifically for the trained machine learning model (rerec_MLP.pkl).

- **Transformers:** A library by Hugging Face that provides access to state-of-the-art pre-trained AI models.

### 🔊 Audio Processing
- **Librosa:** A library for audio analysis, used to extract features like MFCC, spectral centroid, and zero-crossing rate.

- **Soundfile:** A library for reading and writing sound files.

- **Matplotlib:** A plotting library used to generate visualizations of audio data, such as waveforms and spectrograms.

### 📝 News & NLP
- **Requests:** An HTTP client library used for making web requests, such as fetching content from fact-checking sites.

- **NewsAPI-python:** A library for interacting with the News API to search for news articles.

- **Feedparser:** A library for parsing RSS and Atom feeds to get news entries.

- **BeautifulSoup4:** A web scraping library that sits on top of an HTML/XML parser to extract data from web pages.

- **lxml and html5lib:** Parsers that work with BeautifulSoup to process HTML.

- **Fuzzywuzzy and python-Levenshtein:** Libraries for fuzzy string matching, used to compare headlines and find similar news articles.

- **NLTK (Natural Language Toolkit):** A suite of libraries for natural language processing tasks like tokenization and stemming.

- **python-dateutil:** An extension to Python's built-in datetime module for advanced date and time parsing.

- **Urllib3:** A powerful HTTP client for Python.


### Prerequisites

- #### 🔑 Configuration & Files
  -   .env file: The project requires a .env file with the following API keys and a secret key to function correctly.

      - NEWS_API_KEY: For the News API.

      - GNEWS_API_KEY: For the GNews API.

      - GOOGLE_API_KEY: For Google-related services.

      - SECRET_KEY: A key for Flask's session management.

- Pre-trained Model: The app.py file attempts to load a pre-trained machine learning model named rerec_MLP.pkl. This file is crucial for the deepfake audio detection feature and must be present in the project's root directory.
- #### ⚙️ Software & Library Prerequisites
  - Python 3.x: The project is written in Python, so you will need to have a compatible version installed.

  -  Python Libraries: You must install the libraries listed in the requirements.txt file. These can be installed using pip:
      -  Flask
      -  Requests
      -  BeautifulSoup4
      -  NewsAPI-python
      -  Feedparser
      -  Scikit-learn
      -  Numpy
      -  Python-dateutil
      -  NLTK
      -  Fuzzywuzzy
      -  Python-Levenshtein
      -  lxml
      -  html5lib
      -  urllib3
      -  librosa
      -  matplotlib
      -  soundfile
      -  transformers
      -  Joblib
      -  Gunicorn
## 🚀 Getting Started
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

1. **Content Analysis**: Submit text for misinformation detection
2. **Educational Mode**: Learn about common misinformation techniques
3. **Credibility Score**: Get detailed reports on content trustworthiness
4. **Fact-Checking**: Cross-reference information with reliable sources


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



## 🔒 Privacy & Security

- No personal data storage
- Anonymous content analysis
- Secure API endpoints
- GDPR compliance


## 👥 Team

- **Tushar Srivastava** - Project Lead | Full Stack Developer | Core Programmer
- **Pragati Shukla** - Frontend Developer 
- **Niharika Gupta** - Frontend Developer
- **Ankita Sharma** - Frontend Developer
- **Shivani Tripathi** - Frontend Developer

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

