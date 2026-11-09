# Test 01 - SQL Injection: parametresiz sorgu oluşturma
import sqlite3


def kullanici_getir(kullanici_adi, parola):
    conn = sqlite3.connect("uygulama.db")
    cur = conn.cursor()
    # Girdi doğrudan sorgu metnine ekleniyor
    sorgu = f"SELECT * FROM kullanicilar WHERE ad = '{kullanici_adi}' AND parola = '{parola}'"
    cur.execute(sorgu)
    return cur.fetchone()
