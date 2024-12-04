import librosa
import numpy as np

def extract_features(file_path, sr=22050, duration=5.0):
    """
    Verilen ses dosyasından özellikleri çıkarır.

    Özellikler:
    - MFCC (Mel-Frequency Cepstral Coefficients)
    - Chroma özellikleri
    - Mel-Spektrogram

    Args:
    - file_path (str): Ses dosyasının yolu
    - sr (int): Örnekleme hızı
    - duration (float): Ses dosyasının hedef uzunluğu (saniye)

    Returns:
    - np.array: Özellik vektörü
    """
    try:
        # Ses dosyasını yükle (sabit uzunluk ve örnekleme hızı ile)
        signal, sr = librosa.load(file_path, sr=sr, duration=duration)

        # Sinyali normalize et
        signal = librosa.util.normalize(signal)

        # MFCC özelliklerini çıkar
        mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=13)
        mfccs = np.mean(mfccs.T, axis=0)  # Zaman ekseninde ortalama alınır

        # Chroma özelliklerini çıkar
        chroma = librosa.feature.chroma_stft(y=signal, sr=sr)
        chroma = np.mean(chroma.T, axis=0)

        # Mel spektrogram enerji özelliklerini çıkar
        mel = librosa.feature.melspectrogram(y=signal, sr=sr)
        mel = np.mean(mel.T, axis=0)

        # Tüm özellikleri birleştir
        features = np.concatenate((mfccs, chroma, mel))
        return features

    except Exception as e:
        print(f"Özellik çıkarımı sırasında hata: {str(e)}")
        return None
