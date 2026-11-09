# Test 05 - Güvensiz serileştirme: güvenilmeyen pickle verisi
import pickle
import socket


def oturum_verisi_al(baglanti: socket.socket):
    # Ağdan gelen, doğrulanmamış baytlar doğrudan pickle ile açılıyor
    ham_veri = baglanti.recv(4096)
    oturum = pickle.loads(ham_veri)
    return oturum
