# Test 03 - Komut enjeksiyonu: girdinin kabuk komutunda kullanımı
import os
import subprocess


def ping_at(hedef):
    # Kullanıcı girdisi doğrudan kabuğa gidiyor
    os.system("ping -c 4 " + hedef)


def ping_at_2(hedef):
    subprocess.run(f"ping -c 4 {hedef}", shell=True)
