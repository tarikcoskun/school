import os
from dotenv import load_dotenv

from google import genai
from google.genai import errors, types

SISTEM_MESAJI = """
Sen kıdemli bir Yazılım Mimarı ve Performans Uzmanısın.

Kullanıcının gönderdiği kötü yazılmış (spagetti)
Python kodunu analiz et.

1. Değişken isimlerini anlamlı hale getir (Clean Code).
2. Algoritmanın çalışma hızını iyileştir. Örneğin O(n^2) yerine mümkünse O(n) kullan.
3. Type Hint (Tip belirteçleri) ekle.
4. Kodun mevcut işlevselliğini koru.
5. Gereksiz döngüleri ortadan kaldır.

Çıktın KESİNLİKLE sadece düzeltilmiş Python kodu olmalıdır.
Ek açıklama veya Markdown yazma.
"""

def kod_optimize_et(spagetti_kod: str):
  load_dotenv()

  api_key = os.environ["GEMINI_API_KEY"]

  print("=" * 10, "YAPAY ZEKA DESTEKLİ KOD İYİLEŞTİRME VE OPTİMİZASYON", "=" * 10)

  print("\n[AŞAMA 1] OPTİMİZE EDİLECEK SPAGETTİ KOD SİSTEME ALINDI...")
  print("\n[AŞAMA 2] REFACTORING İÇİN YAPAY ZEKAYA BAĞLANILIYOR...\n")

  try:
    with genai.Client(api_key=api_key) as client:
      response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=spagetti_kod,
        config=types.GenerateContentConfig(
          system_instruction=SISTEM_MESAJI,
          temperature=0.2
        )
      )

      temiz_kod = response.text

      if not temiz_kod:
        print("Model boş yanıt döndürdü.")
        return

      print()
      print(temiz_kod)

  except errors.APIError as e:
    print(f"\nAPI hatası: {e}")


kotu_kod = """
def bul(l):
  r = []
  for i in range(len(l)):
    if l[i] == l[j] and l[i] not in r:
      r.append(l[i])
  return r
"""


kod_optimize_et(kotu_kod)
