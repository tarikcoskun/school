import os
import time
from dotenv import load_dotenv

from google import genai
from google.genai import errors, types

SEMA = """
1. Musteriler tablosu: musteri_id, ad_soyad, e_posta, sehir
2. Siparisler tablosu: siparis_id, musteri_id, tutar, siparis_tarihi
"""

SISTEM_MESAJI = f"""
Sen kıdemli bir SQL uzmanısın.

Veri tabanı şeması:
{SEMA}

Kullanıcının talebini SQL sorgusuna dönüştür.
Çıktı KESİNLİKLE sadece SQL kodu olmalıdır.
Ek açıklama veya Markdown yazma.
"""

def sql_sorgusu_uret(talep: str):
  load_dotenv()

  api_key = os.environ["GEMINI_API_KEY"]

  print("=" * 70)
  print("YAPAY ZEKA DESTEKLİ DOĞAL DİLDEN SQL ÜRETİCİ".center(70, " "))
  print("=" * 70)

  print("\n[AŞAMA 1] VERİ TABANI ŞEMASI VE KULLANICI TALEBİ ALINDI...")
  print("\n[AŞAMA 2] SQL ÇEVİRİSİ İÇİN YAPAY ZEKAYA BAĞLANILIYOR...\n")

  baslangic = time.perf_counter()

  try:
    with genai.Client(api_key=api_key) as client:
      baglanti_sonrasi = time.perf_counter()

      response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=talep,
        config=types.GenerateContentConfig(
          system_instruction=SISTEM_MESAJI,
          automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
          temperature=0,
        )
      )

      bitis = time.perf_counter()

      sql = response.text

      if not sql:
        print("Model boş yanıt döndürdü.")
        return

      print("=" * 70)
      print("ÜRETİLEN SQL SORGUSU".center(70, " "))
      print("=" * 70)
      print(sql)

      print(f"\nİstemci kurulum süresi: "
            f"{baglanti_sonrasi - baslangic:.2f} saniye")
      print(f"API yanıt süresi: {bitis - baglanti_sonrasi:.2f} saniye")
      print(f"Toplam süre: {bitis - baslangic:.2f} saniye")

  except errors.APIError as e:
    print(f"\nAPI hatası: {e}")


talep = """
Son bir hafta içinde 10.000 TL altında alışveriş yapan
Ankara ve Edirne'deki müşterilerin id, ad soyad, şehir ve en yüksek tutarlı harcamasını getir.
"""

sql_sorgusu_uret(talep)
