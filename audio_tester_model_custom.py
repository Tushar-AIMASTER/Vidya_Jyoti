import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os,sys
import librosa.display
import librosa.display


class AudioDeepfakeDetector:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.scaler = StandardScaler()

    def extract_features(self, audio_file_path):
        """Extract MFCC and spectral features from audio"""
        y, sr = librosa.load(audio_file_path, duration=30)

        # MFCC features (most important for deepfake detection)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)

        # Additional spectral features
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))

        # Combine features
        features = np.concatenate([
            mfcc_mean, mfcc_std,
            [spectral_centroid, spectral_bandwidth, zero_crossing_rate]
        ])

        return features

    def train_model(self, real_audio_files, fake_audio_files):
        """Train the detection model"""
        features = []
        labels = []

        # Process real audio files
        for file in real_audio_files:
            feature = self.extract_features(file)
            features.append(feature)
            labels.append(0)  # 0 = real

        # Process fake audio files
        for file in fake_audio_files:
            feature = self.extract_features(file)
            features.append(feature)
            labels.append(1)  # 1 = fake

        # Train model
        X = np.array(features)
        y = np.array(labels)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

        print("Model trained successfully!")

    def detect(self, audio_file_path):
        """Detect if audio is AI-generated"""
        features = self.extract_features(audio_file_path)
        features_scaled = self.scaler.transform(features.reshape(1, -1))

        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]

        return {
            'is_fake': bool(prediction),
            'confidence': float(probability[1] if prediction else probability[0]),
            'probabilities': {
                'real': float(probability[0]),
                'fake': float(probability[1])
            }
        }


# Usage example
detector = AudioDeepfakeDetector()
detector.train_model("D:/python_Projects/Dataset/training/real", "D:/python_Projects/Dataset/training/fake")  # Train first
result = detector.detect("test_audio.wav")
