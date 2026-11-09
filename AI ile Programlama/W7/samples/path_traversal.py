# Test 04 - Path Traversal: kontrolsüz dosya yolu birleştirme
BASE_DIR = "/var/www/uygulama/yuklemeler/"


def dosya_indir(filename):
    # filename kullanıcıdan (ör. URL parametresi) geliyor ve doğrudan klasör yoluna ekleniyor.
    # "../../../etc/passwd" gibi bir değer beklenen klasörün dışına çıkabilir.
    with open(BASE_DIR + filename, "rb") as f:
        return f.read()
