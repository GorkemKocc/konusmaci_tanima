import sounddevice as sd
from scipy.io.wavfile import write
import time
import os

def create_user_directory(username):
    user_dir = f"dataset/{username}"
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

def record_user_audio(username, duration=5, sample_rate=22050):
    # Kayıt için kullanıcıya bir metin gösterin
    create_user_directory(username)
    print(f"{username}, lütfen aşağıdaki metni okuyarak kaydı başlatın:")
    print("Merhaba, bu benim ses kaydım. Konuşmacı tanıma uygulaması için kullanıyorum.")
    input("Hazır olduğunuzda Enter'a basarak kayda başlayın...")

    # Kayıt işlemini başlatın
    print("Kayıt başladı...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    
    # Kayıt devam ederken geri sayım göster
    for remaining in range(duration, 0, -1):
        print(f"Kalan süre: {remaining} saniye", end="\r")
        time.sleep(1)

    sd.wait()  # Kayıt tamamlanana kadar bekleyin
    file_path = f"dataset/{username}/{username}_sample.wav"
    
    # Dosyayı kaydedin
    write(file_path, sample_rate, audio)  # Dosyayı kaydet
    print(f"\nKayıt tamamlandı ve {file_path} olarak kaydedildi.")
    return file_path
