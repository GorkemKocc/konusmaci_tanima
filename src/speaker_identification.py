import os
import librosa
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import joblib
from feature_extraction import extract_features

def predict_speaker(file_path, model_path, label_encoder_path, scaler_path, threshold=0.6):
    """Bir ses dosyasını analiz ederek konuşmacıyı veya Unknown'u tahmin eder."""
    model = joblib.load('models/speaker_recognition_model.pkl')
    label_encoder = joblib.load('models/label_encoder.pkl')
    scaler = joblib.load('models/scaler.pkl')

    # Ses özelliklerini çıkar ve ölçekle
    feature = extract_features(file_path)
    feature_scaled = scaler.transform([feature])

    # Modelin olasılık skorlarını al
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(feature_scaled)[0]
        classes = label_encoder.inverse_transform(np.arange(len(probabilities)))

        # Eğitim setindeki eşleşme yüzdelerini yazdır
        match_percentages = {classes[i]: probabilities[i] * 100 for i in range(len(probabilities))}
        print("Eğitim setindeki eşleşme yüzdeleri:")
        for speaker, percentage in match_percentages.items():
            print(f"{speaker}: {percentage:.2f}%")

        # En yüksek olasılığı kontrol et
        max_probability = np.max(probabilities)
        if max_probability < threshold:
            return "Unknown"

        # Tahmin edilen konuşmacı
        predicted_class = np.argmax(probabilities)
        predicted_speaker = classes[predicted_class]
        return predicted_speaker
    else:
        raise ValueError("Model, predict_proba yöntemini desteklemiyor. Farklı bir sınıflandırıcı kullanın.")

# Örnek kullanım
file_to_predict = 'test/nazlı_test/nazlı_test_3.wav'
predicted_speaker = predict_speaker(file_to_predict, 'speaker_recognition_model.pkl', 'label_encoder.pkl', 'scaler.pkl')
print(f"Predicted speaker: {predicted_speaker}")
