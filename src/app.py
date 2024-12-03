# Uygulamanın ana dosyası burada olacak# Kullanıcı adı ve kayıt süresi tanımlayın
import record_audio
usernames = ["speaker1", "speaker2", "speaker3"]

for username in usernames:
    record_audio.record_user_audio(username, duration=5)  # Her kullanıcıdan 5 saniyelik kayıt alıyoruz


