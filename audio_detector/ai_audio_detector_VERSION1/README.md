# AI Audio Detector

A modern web application for detecting AI-generated audio using machine learning and advanced audio analysis techniques. Built with Python Flask, Librosa, and state-of-the-art audio processing libraries.

## Features

- **Modern Web Interface**: Clean, technical design with drag-and-drop file upload
- **AI Detection**: Classify audio as AI-generated or real human speech
- **Advanced Visualizations**: 
  - Waveform analysis
  - MFCC (Mel-Frequency Cepstral Coefficients) heatmaps
  - Spectrograms
  - Frequency domain analysis
- **Comprehensive Analysis**: Detailed audio metrics and technical parameters
- **Multiple Format Support**: MP3, WAV, FLAC, M4A, OGG
- **Real-time Processing**: Live feedback during analysis
- **Export Results**: Save analysis results and visualizations

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- ffmpeg (for audio processing)

### Install ffmpeg

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**On macOS:**
```bash
brew install ffmpeg
```

**On Windows:**
Download from https://ffmpeg.org/download.html and add to PATH

### Setup

1. **Clone or extract the project:**
   ```bash
   cd ai_audio_detector
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5000`

## Usage

### Web Interface

1. **Upload Audio File**:
   - Drag and drop an audio file onto the upload area
   - Or click "Browse Files" to select a file
   - Supported formats: MP3, WAV, FLAC, M4A, OGG

2. **Analysis Process**:
   - File validation and preprocessing
   - Feature extraction using Librosa
   - AI detection using machine learning model
   - Visualization generation

3. **View Results**:
   - AI vs Real classification with confidence score
   - Technical audio metrics
   - Interactive visualizations
   - Export options

### API Endpoint

The application also provides a REST API endpoint:

```bash
curl -X POST -F "file=@your_audio.wav" http://localhost:5000/api/analyze
```

Response:
```json
{
  "filename": "your_audio.wav",
  "prediction": "AI_GENERATED",
  "confidence": 0.87,
  "features": {
    "duration": 12.5,
    "sample_rate": 44100,
    "rms_energy": 0.023,
    "spectral_centroid": 2150.5,
    "spectral_bandwidth": 1200.3,
    "zero_crossing_rate": 0.089,
    "tempo": 120.0
  },
  "status": "success"
}
```

## Technical Details

### Audio Processing Pipeline

1. **Feature Extraction**:
   - MFCC (Mel-Frequency Cepstral Coefficients)
   - Spectral features (centroid, bandwidth, rolloff)
   - Temporal features (zero-crossing rate, RMS energy)
   - Rhythmic features (tempo, beat tracking)

2. **Visualizations**:
   - Time-domain waveform
   - Frequency-domain spectrogram
   - MFCC coefficient heatmaps
   - Spectral analysis plots

3. **AI Detection**:
   - Currently uses mock detection for demonstration
   - Can be easily replaced with trained models
   - Supports integration with Hugging Face models

### Libraries Used

- **Flask**: Web framework
- **Librosa**: Audio analysis and feature extraction
- **Matplotlib**: Visualization generation
- **NumPy**: Numerical computations
- **Transformers**: Machine learning model integration
- **PyTorch**: Deep learning backend

## Customization

### Adding Real AI Detection Models

Replace the `mock_deepfake_detection()` function in `app.py` with actual model inference:

```python
from transformers import pipeline

# Load actual deepfake detection model
deepfake_pipe = pipeline('audio-classification', 
                        model="MelodyMachine/Deepfake-audio-detection-V2")

def real_deepfake_detection(audio_path):
    return deepfake_pipe(audio_path)
```

### Modifying Visualizations

Add new visualization functions in `app.py`:

```python
def plot_custom_analysis(audio_path, output_img):
    y, sr = librosa.load(audio_path)
    # Your custom analysis code here
    plt.figure(figsize=(12, 6))
    # Plotting code
    plt.savefig(output_img)
    plt.close()
```

### Styling

Modify the CSS in the HTML templates to customize the appearance:
- `templates/index.html`: Upload page styling
- `templates/result.html`: Results page styling

## Project Structure

```
ai_audio_detector/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html         # Upload page template
│   └── result.html        # Results page template
├── static/                # Generated visualizations
├── uploads/               # Uploaded audio files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Performance Notes

- Processing time depends on audio file size and length
- Larger files may take longer to analyze
- Consider implementing asynchronous processing for production use
- Memory usage scales with audio file size

## Security Considerations

- File upload validation is implemented
- Uploaded files are stored locally (consider cloud storage for production)
- No authentication implemented (add as needed)
- Input sanitization for file names and paths

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section below
2. Review the code comments
3. Create an issue with detailed information

## Troubleshooting

### Common Issues

**1. "No module named 'librosa'"**
```bash
pip install librosa soundfile
```

**2. "ffmpeg not found"**
Install ffmpeg system package (see installation instructions above)

**3. "Permission denied" on uploads**
```bash
chmod 755 uploads/
chmod 755 static/
```

**4. "Port already in use"**
Change port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Performance Issues

- Reduce audio file size before upload
- Use WAV format for fastest processing
- Check available RAM for large files
- Consider using GPU acceleration for model inference

---

Built with ❤️ using Python, Flask, and modern web technologies.
