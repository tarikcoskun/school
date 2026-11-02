import sqlite3, os, re, time, random
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

import pandas as pd
from google import genai
from google.genai import errors, types

MAKS_DENEME = 3
MAKS_SATIR = 20
RAPOR_DOSYASI = Path(__file__).parent / "sql_asistan_raporu.txt"

KAYIT_SAYISI = 1000
SEHIRLER = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"]
ADLAR = ["Ahmet", "Ayşe", "Mehmet", "Fatma", "Mustafa", "Zeynep", "Ali", "Elif", "Can", "Deniz"]
SOYADLAR = ["Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Aydın", "Öztürk", "Arslan", "Doğan"]

YASAKLI_KOMUTLAR = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]

SISTEM_MESAJI = f"""
Aşağıdaki veritabanı şemasına göre kullanıcının doğal dille istediği
veriyi çekecek SQLite uyumlu SQL sorgusunu yaz.

Şema:
musteriler(musteri_id, ad_soyad, sehir)
siparisler(siparis_id, musteri_id, tutar, tarih)

sehir sütununun alabileceği değerler: {", ".join(SEHIRLER)}

Kurallar:
Veri okuma talepleri için SELECT komutu kullan.
Talep veri silme, güncelleme veya ekleme içeriyorsa onu SELECT'e çevirme ve reddetme,
istenen SQL komutunu aynen yaz. Bu komutlar ayrı bir güvenlik katmanında denetlenir.
Örnek: "Tüm siparişleri sil" talebinin çıktısı: DELETE FROM siparisler
Kullanıcı açıkça bir tablo veya sütun adı yazdıysa şemada olmasa bile o adı kullan.
SQLite hata verirse hata sana bildirilir ve sorguyu şemaya göre düzeltirsin.
Çıktıda markdown etiketi ve açıklama olmasın.
"""

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE musteriler (musteri_id INT, ad_soyad TEXT, sehir TEXT)")
cursor.execute("CREATE TABLE siparisler (siparis_id INT, musteri_id INT, tutar REAL, tarih TEXT)")

musteriler = [
  (i, f"{random.choice(ADLAR)} {random.choice(SOYADLAR)}", random.choice(SEHIRLER))
  for i in range(1, KAYIT_SAYISI + 1)
]
siparisler = [
  (i, random.randint(1, KAYIT_SAYISI), round(random.uniform(100, 10000), 2), "2026-01-01")
  for i in range(1, KAYIT_SAYISI + 1)
]
cursor.executemany("INSERT INTO musteriler VALUES (?, ?, ?)", musteriler)
cursor.executemany("INSERT INTO siparisler VALUES (?, ?, ?, ?)", siparisler)
conn.commit()


def yasakli_komut_bul(sql_kodu: str) -> str | None:
  eslesme = re.search(rf"\b({'|'.join(YASAKLI_KOMUTLAR)})\b", sql_kodu, re.IGNORECASE)
  return eslesme.group(1).upper() if eslesme else None


def guvenlik_kontrolu(sql_kodu: str) -> bool:
  komut = yasakli_komut_bul(sql_kodu)

  if komut:
    print(f"[GÜVENLİK ENGELİ] Zararlı SQL tespit edildi: '{komut}' komutuna izin verilmiyor!")
    return False

  if not re.search(r"^\s*SELECT\b", sql_kodu, re.IGNORECASE):
    print("[GÜVENLİK ENGELİ] Sadece SELECT sorgularına izin veriliyor!")
    return False

  if ";" in sql_kodu.strip().rstrip(";"):
    print("[GÜVENLİK ENGELİ] Tek seferde birden fazla SQL komutuna izin verilmiyor!")
    return False

  print("[GÜVENLİK] Denetim Başarılı (Sadece SELECT).")
  return True


def clean_sql(raw_sql: str) -> str:
  eslesme = re.search(r"```(?:sql)?\s*(.*?)\s*(?:```|$)", raw_sql, re.IGNORECASE | re.DOTALL)
  return eslesme.group(1).strip() if eslesme else raw_sql.strip()


def sonuc_tablosu_yazdir(satirlar: list, sutunlar: list):
  df = pd.DataFrame(satirlar, columns=sutunlar)

  if df.empty:
    print("Sorgu sonucunda kayıt bulunamadı.")
    return

  print(df.head(MAKS_SATIR).to_markdown(index=False, tablefmt="psql", floatfmt=".2f"))

  if len(df) > MAKS_SATIR:
    print(f"... toplam {len(df)} satırın ilk {MAKS_SATIR} satırı gösterildi.")


def sql_asistani_calistir(kullanici_talebi: str) -> dict:
  load_dotenv()

  api_key = os.environ["GEMINI_API_KEY"]

  sonuc = {
    "talep": kullanici_talebi,
    "durum": "BASARISIZ",
    "deneme": 0,
    "sql": "",
    "icra_suresi": None,
    "gemini_sureleri": [],
    "yasakli_komut": None,
    "son_hata": None,
  }

  istek = kullanici_talebi
  deneme = 0

  try:
    with genai.Client(api_key=api_key) as client:
      while deneme < MAKS_DENEME:
        deneme += 1
        sonuc["deneme"] = deneme

        print(f"[GEMINI] SQL Üretiliyor... (Deneme {deneme}/{MAKS_DENEME})")

        baslangic = time.perf_counter()
        response = client.models.generate_content(
          model="gemini-3.5-flash-lite",
          contents=istek,
          config=types.GenerateContentConfig(
            system_instruction=SISTEM_MESAJI,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            temperature=0,
          )
        )
        sonuc["gemini_sureleri"].append(time.perf_counter() - baslangic)

        if not response.text:
          print("Model boş yanıt döndürdü.")
          sonuc["son_hata"] = "Model boş yanıt döndürdü."
          return sonuc

        sql = clean_sql(response.text)
        sonuc["sql"] = sql
        print(f"[SQL] {sql}")

        if not guvenlik_kontrolu(sql):
          sonuc["durum"] = "ENGELLENDI"
          sonuc["yasakli_komut"] = yasakli_komut_bul(sql)
          return sonuc

        try:
          icra_baslangic = time.perf_counter()
          imlec = conn.execute(sql)
          satirlar = imlec.fetchall()
          sonuc["icra_suresi"] = time.perf_counter() - icra_baslangic

          print(f"[SONUÇ] (İcra Süresi: {sonuc['icra_suresi']:.3f} sn)")
          sonuc_tablosu_yazdir(satirlar, [sutun[0] for sutun in imlec.description])

          sonuc["durum"] = "BASARILI"
          return sonuc

        except sqlite3.Error as e:
          print(f"[VERİTABANI HATASI] {e}")
          sonuc["son_hata"] = str(e)

          istek = f"""
Kullanıcı talebi: {kullanici_talebi}

Ürettiğin sorgu:
{sql}

SQLite bu sorguda şu hatayı verdi:
{e}

Şemaya uygun olacak şekilde sorguyu düzelt.
"""

      print(f"[HATA] Sorgu {MAKS_DENEME} denemede düzeltilemedi.")

  except errors.APIError as e:
    print(f"\nAPI hatası: {e}")
    sonuc["son_hata"] = f"API hatası {e.code} {e.status}"

  return sonuc


def test_satiri_olustur(numara: int, sonuc: dict) -> str:
  if sonuc["durum"] == "ENGELLENDI":
    neden = f"{sonuc['yasakli_komut']} engellendi" if sonuc["yasakli_komut"] else "SELECT dışı yanıt engellendi"
    satir = f"[TEST {numara}] Güvenlik Engeli: BAŞARILI ({neden})"
  elif sonuc["durum"] == "BASARILI" and sonuc["deneme"] > 1:
    satir = (f"[TEST {numara}] Hata Düzeltme: {sonuc['deneme']}. denemede çözüldü "
             f"({sonuc['son_hata']}) | İcra Süresi: {sonuc['icra_suresi']:.3f} saniye")
  elif sonuc["durum"] == "BASARILI":
    satir = f"[TEST {numara}] {KAYIT_SAYISI} Veride İcra Süresi: {sonuc['icra_suresi']:.3f} saniye | Durum: BAŞARILI"
  else:
    satir = f"[TEST {numara}] {sonuc['deneme']} denemede çözülemedi | Durum: BAŞARISIZ ({sonuc['son_hata']})"

  return f"{satir}\n  Talep: {sonuc['talep']}\n  SQL  : {sonuc['sql']}"


def rapor_yaz(sonuclar: list):
  basarili = [s for s in sonuclar if s["durum"] == "BASARILI"]
  engellenen = [s for s in sonuclar if s["durum"] == "ENGELLENDI"]
  duzeltilen = [s for s in basarili if s["deneme"] > 1]
  gemini_sureleri = [sure for s in sonuclar for sure in s["gemini_sureleri"]]

  satirlar = [
    "AKILLI SQL ASİSTANI PERFORMANS VE GÜVENLİK RAPORU",
    "-" * 50,
    f"Çalıştırma Tarihi   : {date.today()}",
    f"Veritabanı Hacmi    : {KAYIT_SAYISI:,} Müşteri / {KAYIT_SAYISI:,} Sipariş".replace(",", "."),
    f"Toplam Test Talebi  : {len(sonuclar)}",
    f"Başarılı İcra       : {len(basarili)}",
    f"Engellenen Saldırı  : {len(engellenen)}",
    f"Hata Düzeltme Sayısı: {len(duzeltilen)}",
    "",
    "TEST DETAYLARI:",
  ]
  satirlar += [test_satiri_olustur(i, s) for i, s in enumerate(sonuclar, 1)]
  satirlar += ["", "KISA YORUM VE DEĞERLENDİRME:"]

  if gemini_sureleri:
    ortalama = sum(gemini_sureleri) / len(gemini_sureleri)
    satirlar.append(f"SQL üretimi ortalama {ortalama:.2f} saniye sürdü")

  if basarili:
    ortalama = sum(s["icra_suresi"] for s in basarili) / len(basarili)
    satirlar.append(f"Üretilen SQL'lerin SQLite üzerindeki icra süresi ortalama {ortalama * 1000:.2f} ms'dir.")

  if engellenen:
    satirlar.append(f"Güvenlik filtresi {len(engellenen)} talebi veritabanına ulaşmadan engellemiştir.")

  if duzeltilen:
    satirlar.append(f"Self-Correction döngüsü {len(duzeltilen)} hatalı sorguyu otomatik düzeltmiştir.")

  RAPOR_DOSYASI.write_text("\n".join(satirlar) + "\n", encoding="utf-8")


if __name__ == "__main__":
  print(f"[BİLGİ] Veritabanı oluşturuldu. {KAYIT_SAYISI:,} müşteri ve {KAYIT_SAYISI:,} sipariş yüklendi.".replace(",", "."))

  sonuclar = []

  while True:
    print("-" * 70)
    talep = input("Soru Girin (Çıkış için 'q'): ").strip()

    if talep.lower() == "q":
      break

    if not talep:
      continue

    sonuclar.append(sql_asistani_calistir(talep))
    rapor_yaz(sonuclar)

  if sonuclar:
    print(f"[BİLGİ] Rapor kaydedildi: {RAPOR_DOSYASI}")
