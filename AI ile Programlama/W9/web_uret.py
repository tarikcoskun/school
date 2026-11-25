import os

from dotenv import load_dotenv
from google import genai

SISTEM_MESAJI = """
Sen bir web geliştiricisisin. Kullanıcının talebine göre bir üyelik sistemi için üç HTML sayfası üret.

Yanıtın sadece aşağıdaki üç etiketten ve altlarındaki HTML kodundan oluşsun, başka açıklama yazma:
===INDEX.HTML===
(index.html kodu)
===FORGOT_PASSWORD.HTML===
(forgot_password.html kodu)
===SIGNUP.HTML===
(signup.html kodu)

Sayfalar:
1. index.html: E-posta alanı, şifre alanı, "Giriş Yap" butonu, "Şifremi Unuttum" bağlantısı
   (forgot_password.html), "Üye Ol" bağlantısı (signup.html).
2. forgot_password.html: "Şifremi Unuttum" başlığı, e-posta alanı, "Şifre Sıfırlama Bağlantısı Gönder"
   butonu, "Giriş sayfasına dön" bağlantısı (index.html).
3. signup.html: Ad Soyad, e-posta, şifre ve şifre tekrar alanları, "Üye Ol" butonu,
   "Giriş sayfasına dön" bağlantısı (index.html).

Tasarım:
- Sade ve basit, karanlık temalı, mobil uyumlu bir tasarım yap. CSS kısa olsun.
- Gradyan, animasyon, ikon, SVG, bulanıklık efekti ve harici yazı tipi kullanma.
- Butonlar ve bağlantılar için tek bir vurgu rengi kullan. Butonlarda hover olunca hafif parlama olsun.
- CSS'i <style>, JavaScript'i <script> etiketi içinde aynı HTML dosyasına yaz. Harici dosya kullanma.
- Üç sayfa aynı tasarımı kullansın. Metinler Türkçe olsun.

JavaScript:
- Boş alan, e-posta formatı ve signup.html'de şifre eşleşme kontrolü yap.
- Hataları alanın altında kırmızı yazıyla göster. Her şey doğruysa yeşil bir başarı mesajı göster.
- Şifre alanlarında "Göster" / "Gizle" düğmesi olsun.
"""

dosyalar = {
    "index.html": "===INDEX.HTML===",
    "forgot_password.html": "===FORGOT_PASSWORD.HTML===",
    "signup.html": "===SIGNUP.HTML===",
}


def html_ayikla(sonuc, etiket):
    baslangic = sonuc.find(etiket)
    if baslangic == -1:
        return None
    baslangic += len(etiket)

    bitis = len(sonuc)
    for diger_etiket in dosyalar.values():
        konum = sonuc.find(diger_etiket, baslangic)
        if konum != -1 and konum < bitis:
            bitis = konum

    html_kodu = sonuc[baslangic:bitis]
    html_kodu = html_kodu.replace("```html", "").replace("```", "").strip()
    return html_kodu


def main():
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    tasarim_talebi = input("Web sitesi tasarım talebinizi yazın: ")

    print("Sayfalar oluşturuluyor, lütfen bekleyin...")
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=SISTEM_MESAJI + "\n\nKullanıcı talebi:\n" + tasarim_talebi,
        config={"temperature": 0.5, "max_output_tokens": 32000},
    )
    sonuc = response.text

    for dosya_adi, etiket in dosyalar.items():
        html_kodu = html_ayikla(sonuc, etiket)
        if html_kodu is None:
            print(dosya_adi, "için etiket bulunamadı.")
            continue

        with open(dosya_adi, "w", encoding="utf-8") as dosya:
            dosya.write(html_kodu)
        print(dosya_adi, "kaydedildi.")


main()
