import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from feature_extraction import extract_features  # extract_features fonksiyonunu import ediyoruz

def prepare_dataset(dataset_path):
    data = []
    labels = []
    speakers = os.listdir(dataset_path)
    
    for speaker in speakers:
        speaker_folder = os.path.join(dataset_path, speaker)
        if os.path.isdir(speaker_folder):
            for filename in os.listdir(speaker_folder):
                if filename.endswith(".wav"):
                    file_path = os.path.join(speaker_folder, filename)
                    features = extract_features(file_path)
                    data.append(features)
                    labels.append(speaker)
    return np.array(data), np.array(labels)

# Veri setini hazırla
X, y = prepare_dataset("dataset")

# Etiketleri sayısal değerlere dönüştür
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)

# Eğitim ve test setlerine ayır
X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)

# Modeli tanımla
model = Sequential([
    Dense(256, activation='relu', input_shape=(X.shape[1],)),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dense(len(np.unique(y)), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Modeli eğit
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Modeli kaydet
model.save("models/speaker_recognition_model.h5")
