import os
import sys
from record_audio import record_audio, record_test_audio  # Ses kaydı için gerekli fonksiyon
from model_training import train_model  # Model eğitimi için gerekli fonksiyon
from predict_speaker import predict_speaker  # Kullanıcı tanıma için gerekli fonksiyon
import time 

def create_user_directory(isTest, username):
    """
    Kullanıcıya özel bir klasör oluşturur.
    """
    if(isTest):
        user_dir = f"test/{username}"
    else:
        user_dir = f"dataset/{username}"
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

def yeni_kullanici_kaydi():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n--- Yeni Kullanıcı Kaydı ---")
    username = input("Yeni kullanıcının ismini girin (Ana menüye dönmek için Enter'a basın): ").strip()
    if not username:
        print("Ana menüye dönülüyor...")
        time.sleep(0.5)
        return
    create_user_directory(False,username)
    record_audio(username)  # Yeni ses kaydını oluştur
    print("Model yeniden eğitiliyor...")
    train_model()  # Modeli yeniden eğit
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Model eğitimi tamamlandı.")
    input("Devam etmek için bir tuşa basın.")

def kullanici_tanima():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n--- Kullanıcı Tanıma ---")
    print("1. Mevcut test dosyalarını kullan")
    print("2. Yeni test dosyası ekle")
    secim = input("Seçiminizi yapın (1/2 ya da Ana menüye dönmek için Enter'a basın): ").strip()
    if not secim:
        print("Ana menüye dönülüyor...")
        time.sleep(0.5)
        return
    
    if secim == "1":
        test_root = "test"
        # Klasörleri listele
        user_folders = [folder for folder in os.listdir(test_root) if os.path.isdir(os.path.join(test_root, folder))]
        if not user_folders:
            print("Test klasöründe alt klasör bulunamadı.")
            return

        print("\nMevcut kullanıcı klasörleri:")
        for idx, folder in enumerate(user_folders):
            print(f"{idx + 1}. {folder}")
        
        try:
            # Klasör seçimi
            folder_index = input("Bir klasör seçin (numara ya da Ana menüye dönmek için Enter'a basın): ")
            if not folder_index:
                print("Ana menüye dönülüyor...")
                time.sleep(0.5)
                return
            else:
                folder_index = int(folder_index) - 1
            os.system('cls' if os.name == 'nt' else 'clear')
            if 0 <= folder_index < len(user_folders):
                selected_folder = user_folders[folder_index]
                folder_path = os.path.join(test_root, selected_folder)

                # Klasör içindeki ses dosyalarını listele
                audio_files = [file for file in os.listdir(folder_path) if file.endswith(".wav")]
                if not audio_files:
                    print("Bu klasörde ses dosyası bulunamadı.")
                    return
                
                print(f"\n{selected_folder} klasöründeki ses dosyaları:")
                for idx, file in enumerate(audio_files):
                    print(f"{idx + 1}. {file}")
                
                # Dosya seçimi
                file_index = input("Bir dosya seçin (numara ya da Ana menüye dönmek için Enter'a basın): ")
                if not file_index:
                    print("Ana menüye dönülüyor...")
                    time.sleep(0.5)
                    return
                else:
                    file_index = int(file_index) - 1
                if 0 <= file_index < len(audio_files):
                    selected_file = os.path.join(folder_path, audio_files[file_index])
                    print("Kullanıcı tanımlanıyor..." + selected_file)
                    predict_speaker(selected_file)  # Tanıma işlemi
                    input("Devam etmek için bir tuşa basın.")
                else:
                    print("Geçersiz dosya seçimi.")
            else:
                print("Geçersiz klasör seçimi.")
        except ValueError:
            print("Geçersiz giriş. Lütfen sayı girin.")
    elif secim == "2":
        print("\n--- Yeni Test Kaydı ---")
        username = input("Yeni test dosyası için ismini girin (Ana menüye dönmek için Enter'a basın): ").strip()
        if not username:
            print("Ana menüye dönülüyor...")
            time.sleep(0.5)
            return
        create_user_directory(True,username)
        record_test_audio(username)
        print("Ses kaydı tamamlandı.")
        predict_speaker(f"test/{username}/{username}_test.wav")
        input("Devam etmek için bir tuşa basın.")
    else:
        print("Geçersiz seçim.")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n==== Ses Tanıma Uygulaması ====")
        print("1. Yeni Kullanıcı Kaydı")
        print("2. Kullanıcı Tanıma")
        print("3. Çıkış")
        
        choice = input("Bir seçenek girin: ").strip()
        
        match choice:
            case "1":
                yeni_kullanici_kaydi()
            case "2":
                kullanici_tanima()
            case "3":
                print("Programdan çıkılıyor...")
                sys.exit(0)
            case _:
                print("Geçersiz seçim, lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()


