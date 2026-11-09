# Test 06 - Güvenli Python kodu: bilinçli olarak açık içermeyen örnek
import json
import os
import sqlite3
from pathlib import Path

DB_PATH = os.environ.get("APP_DB_PATH", "uygulama.db")
BASE_DIR = Path("/var/www/uygulama/yuklemeler").resolve()


def kullanici_getir(kullanici_adi: str):
    # Parametreli sorgu kullanılıyor
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT id, ad FROM kullanicilar WHERE ad = ?", (kullanici_adi,))
        return cur.fetchone()


def dosya_oku(filename: str) -> bytes:
    # Yol çözümlenip güvenli klasörün içinde kaldığı doğrulanıyor
    hedef = (BASE_DIR / filename).resolve()
    if not hedef.is_relative_to(BASE_DIR):
        raise PermissionError("İzin verilen klasörün dışına erişilemez.")
    return hedef.read_bytes()


def ayar_yukle(ham_veri: str) -> dict:
    # Güvenilmeyen veri pickle yerine JSON ile ayrıştırılıyor
    veri = json.loads(ham_veri)
    if not isinstance(veri, dict):
        raise ValueError("Ayarlar bir JSON nesnesi olmalıdır.")
    return veri


def ortalama(sayilar: list[float]) -> float:
    if not sayilar:
        return 0.0
    return sum(sayilar) / len(sayilar)
