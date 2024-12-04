import numpy as np
from tensorflow.keras.models import load_model
from feature_extraction import extract_features
from sklearn.preprocessing import LabelEncoder
import os

def load_encoder(labels_path):
    """
    Konuşmacı etiketlerini yüklemek ve LabelEncoder oluşturmak için bir yardımcı fonksiyon.
    """
    if os.path.exists(labels_path):
        with open(labels_path, 'r') as f:
            labels = [line.strip() for line in f.readlines()]
        encoder = LabelEncoder()
        encoder.fit(labels)
        return encoder
    else:
        raise FileNotFoundError(f"{labels_path} bulunamadı!")

def predict_speaker_with_threshold(file_path, model, encoder, threshold=0.6):
    """
    Verilen ses dosyasını analiz ederek konuşmacıyı tahmin eden fonksiyon.
    Eğer maksimum olasılık eşik değerin altında ise, konuşmacı "Bilinmeyen" olarak değerlendirilir.
    """
    try:
        # Özellik çıkarımı
        features = extract_features(file_path)
        if features is None:
            raise ValueError(f"Özellik çıkarımı başarısız: {file_path}")
        
        features = features.reshape(1, -1)  # Model girişine uygun hale getirilir
        predictions = model.predict(features)
        
        # Maksimum olasılığı kontrol et
        max_prob = np.max(predictions)
        speaker_index = np.argmax(predictions)
        
        if max_prob >= threshold:
            speaker_name = encoder.inverse_transform([speaker_index])
            return speaker_name[0], predictions
        else:
            return "Bilinmeyen Konuşmacı", predictions
    except Exception as e:
        print(f"Hata: {file_path}, Mesaj: {str(e)}")
        return None, None

if __name__ == "__main__":
    # Model ve encoder yolları
    model_path = "models/speaker_recognition_model.h5"
    labels_path = "models/labels.txt"  # Etiketlerin kayıtlı olduğu dosya

    try:
        # Modeli yükle
        model = load_model(model_path)
        print(f"Model başarıyla yüklendi: {model_path}")
        
        # LabelEncoder'ı yükle
        encoder = load_encoder(labels_path)
        print(f"Etiketler başarıyla yüklendi: {labels_path}")

        # Tahmin yapılacak test dosyası
        test_file = "dataset/speaker2/speaker2_sample.wav"

        # Konuşmacıyı tahmin et
        predicted_speaker, predictions = predict_speaker_with_threshold(test_file, model, encoder, threshold=0.7)

        if predicted_speaker is not None:
            print(f"\nTahmin edilen konuşmacı: {predicted_speaker}")
            
            # Tüm tahminleri ve olasılıkları konsola yazdır
            print("\nTüm tahminler:")
            for i, label in enumerate(encoder.classes_):
                print(f"{label}: {predictions[0][i]:.4f}")
        else:
            print("Konuşmacı tahmin edilemedi.")
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
import numpy as np
from tensorflow.keras.models import load_model
from feature_extraction import extract_features
from sklearn.preprocessing import LabelEncoder
import os

def load_encoder(labels_path):
    """
    Konuşmacı etiketlerini yüklemek ve LabelEncoder oluşturmak için bir yardımcı fonksiyon.
    """
    if os.path.exists(labels_path):
        with open(labels_path, 'r') as f:
            labels = [line.strip() for line in f.readlines()]
        encoder = LabelEncoder()
        encoder.fit(labels)
        return encoder
    else:
        raise FileNotFoundError(f"{labels_path} bulunamadı!")

def predict_speaker_with_threshold(file_path, model, encoder, threshold=0.6):
    """
    Verilen ses dosyasını analiz ederek konuşmacıyı tahmin eden fonksiyon.
    Eğer maksimum olasılık eşik değerin altında ise, konuşmacı "Bilinmeyen" olarak değerlendirilir.
    """
    try:
        # Özellik çıkarımı
        features = extract_features(file_path)
        if features is None:
            raise ValueError(f"Özellik çıkarımı başarısız: {file_path}")
        
        features = features.reshape(1, -1)  # Model girişine uygun hale getirilir
        predictions = model.predict(features)
        
        # Maksimum olasılığı kontrol et
        max_prob = np.max(predictions)
        speaker_index = np.argmax(predictions)
        
        if max_prob >= threshold:
            speaker_name = encoder.inverse_transform([speaker_index])
            return speaker_name[0], predictions
        else:
            return "Bilinmeyen Konuşmacı", predictions
    except Exception as e:
        print(f"Hata: {file_path}, Mesaj: {str(e)}")
        return None, None

if __name__ == "__main__":
    # Model ve encoder yolları
    model_path = "models/speaker_recognition_model.h5"
    labels_path = "models/labels.txt"  # Etiketlerin kayıtlı olduğu dosya

    try:
        # Modeli yükle
        model = load_model(model_path)
        print(f"Model başarıyla yüklendi: {model_path}")
        
        # LabelEncoder'ı yükle
        encoder = load_encoder(labels_path)
        print(f"Etiketler başarıyla yüklendi: {labels_path}")

        # Tahmin yapılacak test dosyası
        test_file = "dataset/4/4_1.wav"

        # Konuşmacıyı tahmin et
        predicted_speaker, predictions = predict_speaker_with_threshold(test_file, model, encoder, threshold=0.7)

        if predicted_speaker is not None:
            print(f"\nTahmin edilen konuşmacı: {predicted_speaker}")
            
            # Tüm tahminleri ve olasılıkları konsola yazdır
            print("\nTüm tahminler:")
            for i, label in enumerate(encoder.classes_):
                print(f"{label}: {predictions[0][i]:.4f}")
        else:
            print("Konuşmacı tahmin edilemedi.")
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
