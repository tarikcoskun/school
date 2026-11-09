# Test 02 - Sabit parola: kaynak koda gömülü gizli bilgi
import psycopg2

DB_HOST = "10.0.0.15"
DB_USER = "admin"
DB_PASSWORD = "Sirket2024!"          # Parola kaynak kodda açık metin
API_KEY = "sk_live_51Hx9...abc"      # Gizli anahtar kodda

conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname="musteri")
