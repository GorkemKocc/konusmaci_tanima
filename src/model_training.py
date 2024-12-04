import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
from feature_extraction import extract_features
import matplotlib.pyplot as plt


def prepare_dataset(dataset_path):
    """Eğitim verilerini hazırlar."""
    features = []
    labels = []

    for speaker in os.listdir(dataset_path):
        speaker_path = os.path.join(dataset_path, speaker)
        if os.path.isdir(speaker_path):
            for file_name in os.listdir(speaker_path):
                file_path = os.path.join(speaker_path, file_name)
                if file_name.endswith('.wav'):
                    print(f"Processing {file_path}")
                    feature = extract_features(file_path)
                    features.append(feature)
                    labels.append(speaker)

    # "Unknown" için rastgele gürültü özellikleri oluştur
    unknown_features = np.random.normal(size=(50, 13))  # 50 bilinmeyen örnek
    features.extend(unknown_features)
    labels.extend(['Unknown'] * len(unknown_features))

    return np.array(features), np.array(labels)

# Veri setini hazırla
dataset_path = 'dataset'
X, y = prepare_dataset(dataset_path)

# Etiketleri encode et
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Verileri ölçekle
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Eğitim ve test setlerini ayır
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

# Model oluştur ve eğit
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# Model doğruluğunu kontrol et
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy * 100:.2f}%")

save_dir = 'models'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Modeli, etiketleri ve ölçekleyiciyi kaydet
joblib.dump(model, os.path.join(save_dir, 'speaker_recognition_model.pkl'))
joblib.dump(label_encoder, os.path.join(save_dir, 'label_encoder.pkl'))
joblib.dump(scaler, os.path.join(save_dir, 'scaler.pkl'))
