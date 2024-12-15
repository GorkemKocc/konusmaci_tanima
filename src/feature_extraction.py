import librosa
import numpy as np

def extract_features(file_path):
    """MFCC özelliklerini çıkarır (eski özellik çıkarma)."""
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

def extract_mel_spectrogram(file_path, n_mels=128):
    """Mel spektrogram çıkarır ve 3 kanallı (RGB) formata dönüştürür."""
    y, sr = librosa.load(file_path, sr=None)
    
    # Mel spektrogramını çıkar
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    
    # Mel spektrogramını desibel (dB) cinsine dönüştür
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)

    # 3 kanal formatına dönüştür (RGB). Bu örnekte her bir kanal aynı olacak.
    rgb_spectrogram = np.repeat(log_spectrogram[..., np.newaxis], 3, axis=-1)
    
    return rgb_spectrogram