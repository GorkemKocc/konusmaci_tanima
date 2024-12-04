import librosa
import numpy as np

def extract_features(file_path):
    """Ses dosyasından özellikler çıkarır."""
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)