from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

# Load Pretrained Model (using a mock classifier for demo purposes)
# In production, replace with actual audio deepfake detection model
# deepfake_pipe = pipeline('audio-classification', model="MelodyMachine/Deepfake-audio-detection-V2")

def mock_deepfake_detection(audio_path):
    """
    Mock function for deepfake detection
    In production, replace this with actual model inference
    """
    # Simulate detection based on simple audio features
    y, sr = librosa.load(audio_path)

    # Extract some basic features for mock classification
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))

    # Mock classification logic (replace with real model)
    if spectral_centroid > 2000 or zero_crossing_rate > 0.1:
        return [{'label': 'AI_GENERATED', 'score': 0.87}]
    else:
        return [{'label': 'REAL_HUMAN', 'score': 0.92}]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav', 'mp3', 'flac', 'ogg', 'm4a'}

def extract_audio_features(audio_path):
    """Extract comprehensive audio features"""
    y, sr = librosa.load(audio_path)

    features = {
        'duration': len(y) / sr,
        'sample_rate': sr,
        'rms_energy': np.mean(librosa.feature.rms(y=y)),
        'spectral_centroid': np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
        'spectral_bandwidth': np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
        'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(y)),
        'tempo': librosa.beat.tempo(y=y, sr=sr)[0]
    }

    return features

def plot_waveform(audio_path, output_img):
    """Generate waveform plot"""
    y, sr = librosa.load(audio_path)

    plt.figure(figsize=(12, 4))
    plt.style.use('dark_background')
    time = np.arange(len(y)) / sr
    plt.plot(time, y, color='#00ffff', linewidth=0.5)
    plt.title('Audio Waveform', fontsize=16, color='white')
    plt.xlabel('Time (seconds)', fontsize=12, color='white')
    plt.ylabel('Amplitude', fontsize=12, color='white')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_img, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()

def plot_mfcc(audio_path, output_img):
    """Generate MFCC heatmap"""
    y, sr = librosa.load(audio_path)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    plt.figure(figsize=(12, 6))
    plt.style.use('dark_background')
    librosa.display.specshow(mfccs, x_axis='time', sr=sr, cmap='plasma')
    plt.colorbar(label='MFCC Coefficients')
    plt.title('MFCC Features', fontsize=16, color='white')
    plt.xlabel('Time (seconds)', fontsize=12, color='white')
    plt.ylabel('MFCC Coefficients', fontsize=12, color='white')
    plt.tight_layout()
    plt.savefig(output_img, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()

def plot_spectrogram(audio_path, output_img):
    """Generate spectrogram"""
    y, sr = librosa.load(audio_path)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    plt.figure(figsize=(12, 6))
    plt.style.use('dark_background')
    librosa.display.specshow(D, x_axis='time', y_axis='hz', sr=sr, cmap='magma')
    plt.colorbar(label='Amplitude (dB)')
    plt.title('Spectrogram', fontsize=16, color='white')
    plt.xlabel('Time (seconds)', fontsize=12, color='white')
    plt.ylabel('Frequency (Hz)', fontsize=12, color='white')
    plt.tight_layout()
    plt.savefig(output_img, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()

def plot_frequency_analysis(audio_path, output_img):
    """Generate frequency domain analysis"""
    y, sr = librosa.load(audio_path)

    # Compute FFT
    fft = np.fft.fft(y)
    magnitude = np.abs(fft)
    frequency = np.linspace(0, sr, len(magnitude))

    # Plot only first half (positive frequencies)
    left_frequency = frequency[:int(len(frequency)/2)]
    left_magnitude = magnitude[:int(len(magnitude)/2)]

    plt.figure(figsize=(12, 4))
    plt.style.use('dark_background')
    plt.plot(left_frequency, left_magnitude, color='#ff6b6b', linewidth=0.8)
    plt.title('Frequency Domain Analysis', fontsize=16, color='white')
    plt.xlabel('Frequency (Hz)', fontsize=12, color='white')
    plt.ylabel('Magnitude', fontsize=12, color='white')
    plt.xlim(0, 8000)  # Focus on human speech range
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_img, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Extract audio features
            features = extract_audio_features(filepath)

            # Generate visualizations
            base_name = os.path.splitext(filename)[0]
            waveform_img = os.path.join('static', f'waveform_{base_name}.png')
            mfcc_img = os.path.join('static', f'mfcc_{base_name}.png')
            spectrogram_img = os.path.join('static', f'spectrogram_{base_name}.png')
            frequency_img = os.path.join('static', f'frequency_{base_name}.png')

            plot_waveform(filepath, waveform_img)
            plot_mfcc(filepath, mfcc_img)
            plot_spectrogram(filepath, spectrogram_img)
            plot_frequency_analysis(filepath, frequency_img)

            # AI Detection (using mock function)
            detection_result = mock_deepfake_detection(filepath)

            result_data = {
                'filename': filename,
                'prediction': detection_result[0]['label'],
                'confidence': f"{detection_result[0]['score'] * 100:.1f}%",
                'features': features,
                'visualizations': {
                    'waveform': waveform_img,
                    'mfcc': mfcc_img,
                    'spectrogram': spectrogram_img,
                    'frequency': frequency_img
                }
            }

            return render_template('result.html', **result_data)

        except Exception as e:
            return jsonify({'error': f'Error processing audio: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for audio analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Extract features and run detection
            features = extract_audio_features(filepath)
            detection_result = mock_deepfake_detection(filepath)

            return jsonify({
                'filename': filename,
                'prediction': detection_result[0]['label'],
                'confidence': detection_result[0]['score'],
                'features': features,
                'status': 'success'
            })

        except Exception as e:
            return jsonify({'error': str(e), 'status': 'failed'}), 500

    return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    print("Starting AI Audio Detector...")
    print("Visit http://localhost:5000 to access the application")
    app.run(debug=True, host='0.0.0.0', port=5000)
