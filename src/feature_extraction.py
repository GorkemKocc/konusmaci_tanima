# Özellik çıkarımı için fonksiyonlar burada olacak
import librosa
import numpy as np
import os
import pandas as pd

def extract_features(file_path):
    signal, sr = librosa.load(file_path, sr=22050)
    mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=13)
    mfccs = np.mean(mfccs.T, axis=0)  # Zaman ekseninde ortalama alınır
    return mfccs