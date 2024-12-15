import os
import numpy as np
from tensorflow.keras.models import load_model
import joblib
from feature_extraction import extract_mel_spectrogram



def predict_speaker_cnn(file_path, model_path, label_encoder_path, threshold=0.6):
    """Bir ses dosyasını analiz ederek konuşmacıyı ve yüzdelik olasılığını tahmin eder."""
    model = load_model(model_path)
    label_encoder = joblib.load(label_encoder_path)

    # Ses dosyasından mel spektrogram çıkar
    spectrogram = extract_mel_spectrogram(file_path)
    spectrogram = spectrogram[np.newaxis, ..., np.newaxis]  # 4D şekle dönüştür

    # Modelin tahmin skorlarını al
    probabilities = model.predict(spectrogram)[0]

    # En yüksek olasılık değerini ve sınıfını al
    max_probability = np.max(probabilities)
    predicted_index = np.argmax(probabilities)
    predicted_speaker = label_encoder.inverse_transform([predicted_index])[0]

    # Yüzdelik doğruluk değerini ekrana yazdır
    print("\nTahmin edilen konuşmacı olasılıkları:")
    for i, prob in enumerate(probabilities):
        speaker = label_encoder.inverse_transform([i])[0]
        print(f"{speaker}: {prob * 100:.2f}%")

    # Eğer en yüksek olasılık eşik değerinin altındaysa 'Unknown' döndür
    if max_probability < threshold:
        return "Unknown", max_probability * 100

    return predicted_speaker, max_probability * 100

def predict_speaker(file_to_predict):
    # Dinamik dosya yolları
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, '..\models\speaker_recognition_vgg16.h5')
    label_encoder_path = os.path.join(current_dir, '..\models\label_encoder_cnn.pkl')
    # Örnek kullanım
    #file_to_predict = './test/filiz_test/filiz_test_2.wav'
    predicted_speaker, confidence = predict_speaker_cnn(file_to_predict, model_path, label_encoder_path)
    print(f"\nTahmin edilen konuşmacı: {predicted_speaker} ({confidence:.2f}%)")