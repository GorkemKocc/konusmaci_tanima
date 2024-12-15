from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, models
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
from feature_extraction import extract_mel_spectrogram

def create_transfer_learning_model(input_shape, num_classes):
    # VGG16 modelini yükle (önceden eğitilmiş ağırlıklarla, include_top=False demek sınıf başlıklarını dahil etmemek anlamına gelir)
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    
    # Katmanları dondur (sadece yeni katmanlar eğitilecek)
    for layer in base_model.layers:
        layer.trainable = False

    # Yeni katmanlar ekle
    model = models.Sequential([
        base_model,
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')  # Konuşmacı sayısına göre çıkış katmanı
    ])
    
    # Modeli derle
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model

def prepare_dataset(dataset_path):
    """Eğitim verilerini hazırlar ve mel-spektrogram çıkarır."""
    features = []
    labels = []

    for speaker in os.listdir(dataset_path):
        speaker_path = os.path.join(dataset_path, speaker)
        if os.path.isdir(speaker_path):
            for file_name in os.listdir(speaker_path):
                file_path = os.path.join(speaker_path, file_name)
                if file_name.endswith('.wav'):
                    #print(f"Processing {file_path}")
                    spectrogram = extract_mel_spectrogram(file_path)  # Bu, 3 kanallı mel-spektrogram
                    features.append(spectrogram)
                    labels.append(speaker)

    features = np.array(features)
    labels = np.array(labels)

    # Etiketleri encode et
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)
    return features, labels_encoded, label_encoder

def train_model():
    # Veri setini hazırla
    dataset_path = './dataset'

    X, y, label_encoder = prepare_dataset(dataset_path)

    # Eğitim ve test setlerini ayıralım
    X = X  # 4D şekil (yükseklik, genişlik, kanal) - burada zaten 3 kanallı formatta
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modeli oluştur
    input_shape = X_train.shape[1:]  # (yükseklik, genişlik, kanal)
    num_classes = len(label_encoder.classes_)
    model = create_transfer_learning_model(input_shape, num_classes)

    # Modeli eğit
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=32)
    # Modeli ve etiketleyiciyi kaydet
    model.save('models/speaker_recognition_vgg16.h5')
    joblib.dump(label_encoder, 'models/label_encoder_cnn.pkl')

    #print("Model ve label encoder başarıyla kaydedildi!")
#train_model()