import sounddevice as sd
from scipy.io.wavfile import write
import time
import os

def record_test_audio(test_user, duration=5, sample_rate=22050):
    # Kullanıcı için klasör oluştur
    user_dir = f"test/{test_user}"
    os.makedirs(user_dir, exist_ok=True)

    print(f"\nTest Kullanıcısı: {test_user} için test kaydı hazırlanıyor...\n")
    print(f"{test_user}, lütfen 5 saniye boyunca konuşunuz:")
    input("Hazır olduğunuzda Enter'a basarak kayda başlayın...")

    # Kayıt işlemini başlat
    print("Test kaydı başladı...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)

    # Geri sayım göstergesi
    for remaining in range(duration, 0, -1):
        print(f"Kalan süre: {remaining} saniye", end="\r")
        time.sleep(1)

    sd.wait()  # Kayıt tamamlanana kadar bekleyin

    # Dosya adını belirle
    file_path = f"{user_dir}/{test_user}_test.wav"

    # Kayıt dosyasını kaydedin
    write(file_path, sample_rate, audio)
    print(f"\nTest kaydı tamamlandı ve {file_path} olarak kaydedildi.")

    print(f"\n{test_user} için test ses kaydı başarıyla tamamlandı!")

def record_audio(username, duration=5, sample_rate=22050):
    """
    Kullanıcıdan 3 farklı ses kaydı alır ve her birini belirtilen klasöre kaydeder.
    """
    # Kullanıcının okuyacağı örnek metinler
    example_texts = [
    "Merhaba, bu benim ses kaydım. Konuşmacı tanıma uygulaması için kullanıyorum.",
    "Bugün hava çok güzel ve güneş parlıyor.",
    "Kahvaltıda çay içtim ve peynir yedim.",
    "Yeni bir kitap aldım ve okumaya başladım.",
    "Bilgisayarımı açtım ve çalışmaya başladım.",
    "Yürüyüş yapmak iyi hissettiriyor ve enerji veriyor.",
    "Telefonumun şarjı azalmış ve hemen taktım.",
    "Arkadaşlarımla buluştum ve güzel bir sohbet ettik.",
    "Marketten ekmek almayı unuttum ve geri döndüm.",
    "Televizyonda haberleri izledim ve ilginç bilgiler öğrendim.",
    "Yemek yapmak oldukça eğlenceli ve rahatlatıcı."
    ]

    for i, text in enumerate(example_texts, start=1):
        print(f"\n{username} Kayıt {i}. Örnek için hazırlanıyor... \n\n")
        print(f"{username}, lütfen kaydı başlatıp aşağıdaki metni okuuyunuz:")
        print(f"Metin: {text}")
        input("Hazır olduğunuzda Enter'a basarak kayda başlayın...")

        # Kayıt işlemini başlat
        print(f"Kayıt {i} başladı...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        
        # Geri sayım göstergesi
        for remaining in range(duration, 0, -1):
            print(f"Kalan süre: {remaining} saniye", end="\r")
            time.sleep(1)

        sd.wait()  # Kayıt tamamlanana kadar bekleyin

        # Dosya adını belirle
        file_path = f"dataset/{username}/{username}_{i}.wav"

        # Kayıt dosyasını kaydedin
        write(file_path, sample_rate, audio)
        print(f"\nKayıt {i} tamamlandı ve {file_path} olarak kaydedildi.")

    print(f"\n{username} için örnek ses kaydı başarıyla tamamlandı!")


