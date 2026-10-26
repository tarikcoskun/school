"""İki girişli hardlim perceptron. Çalıştırma: python perceptron_AND_OR_XOR.py

Harici paket gerektirmez; grafik için standart tkinter modülünü kullanır.
hardlim(0) = 1 kabul edilir.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import math
import random


def perceptron(x1, x2, w1, w2, b):
    net = w1 * x1 + w2 * x2 + b
    return net, int(net >= 0)


def hedef_degeri(kapi, x1, x2):
    if kapi == "AND":
        return int(bool(x1) and bool(x2))
    if kapi == "OR":
        return int(bool(x1) or bool(x2))
    return int(bool(x1) != bool(x2))


class Uygulama:
    def __init__(self, root):
        self.root = root
        self.egitim = False
        self.zamanlayici = None
        self.hata_gecmisi = []
        self.hata_penceresi = None
        self.ornekler = ((0, 0), (0, 1), (1, 0), (1, 1))
        root.protocol("WM_DELETE_WINDOW", self.kapat)
        root.title("AND / OR / XOR — hardlim perceptron")
        secim_paneli = ttk.Frame(root, padding=8)
        secim_paneli.pack(fill="x")
        ttk.Label(secim_paneli, text="Mantık kapısı:").pack(side="left", padx=4)
        self.kapi = tk.StringVar(value="AND")
        secici = ttk.Combobox(secim_paneli, textvariable=self.kapi,
                             values=("AND", "OR", "XOR"), state="readonly", width=8)
        secici.pack(side="left")
        secici.bind("<<ComboboxSelected>>", self.kapi_sec)
        self.aciklama = ttk.Label(root, padding=8, wraplength=710)
        self.aciklama.pack(fill="x")
        panel = ttk.Frame(root, padding=12)
        panel.pack(fill="x")
        self.girdiler = {}
        for sutun, (isim, deger) in enumerate(
            [("x1", "1"), ("x2", "1"), ("w1", "1"), ("w2", "1"), ("b", "-1.5")]
        ):
            ttk.Label(panel, text=isim).grid(row=0, column=sutun)
            if isim in ("x1", "x2"):
                alan = ttk.Combobox(panel, values=("0", "1"), state="readonly", width=8)
                alan.set(deger)
            else:
                alan = ttk.Entry(panel, width=10)
                alan.insert(0, deger)
            alan.grid(row=1, column=sutun, padx=4)
            self.girdiler[isim] = alan
        ttk.Button(panel, text="Hesapla ve çiz", command=self.hesapla).grid(
            row=1, column=5, padx=10
        )
        self.sonuc = ttk.Label(root, padding=8, justify="left")
        self.sonuc.pack(fill="x")
        ttk.Button(root, text="Başlangıç ağırlıklarını yükle", command=self.agirliklari_yukle).pack()
        self.tablo = ttk.Treeview(root, columns=("x1", "x2", "net", "beklenen", "cikti", "durum"),
                                 show="headings", height=4)
        for isim, baslik in zip(self.tablo["columns"],
                                ("x1", "x2", "Net", "AND hedefi", "Çıktı", "Kontrol")):
            self.tablo.heading(isim, text=baslik)
            self.tablo.column(isim, width=110, anchor="center")
        self.tablo.pack(padx=12, pady=4)
        self.tablo.bind("<<TreeviewSelect>>", self.satir_sec)
        self.kontrol = ttk.Label(root)
        self.kontrol.pack()
        egitim_panel = ttk.Frame(root, padding=6)
        egitim_panel.pack(fill="x")
        ttk.Label(egitim_panel, text="Öğrenme oranı η:").pack(side="left")
        self.eta = ttk.Entry(egitim_panel, width=5)
        self.eta.insert(0, "0.2")
        self.eta.pack(side="left")
        ttk.Label(egitim_panel, text="En fazla tur:").pack(side="left", padx=4)
        self.tur_siniri = ttk.Entry(egitim_panel, width=5)
        self.tur_siniri.insert(0, "100")
        self.tur_siniri.pack(side="left")
        dugme_panel = ttk.Frame(root, padding=4)
        dugme_panel.pack(fill="x")
        for baslik, komut in (("Mevcut değerlerle başlat", self.baslat),
                              ("Rastgele başlat", lambda: self.baslat(True)),
                              ("Bir adım", self.adim),
                              ("Otomatik", self.oto_baslat),
                              ("Duraklat", self.duraklat),
                              ("Hata grafiği", self.hata_grafigini_ac)):
            ttk.Button(dugme_panel, text=baslik, command=komut).pack(side="left", padx=2)
        self.egitim_bilgisi = ttk.Label(root, padding=6, justify="left", wraplength=720,
                                       text="Başlat → Bir adım: her tıklama bir örneği işler. "
                                            "Bir tur dört örnektir. e = hedef − çıktı.")
        self.egitim_bilgisi.pack(fill="x")
        gecmis_panel = ttk.Frame(root)
        gecmis_panel.pack(fill="x", padx=12)
        self.gecmis = tk.Text(gecmis_panel, height=5, width=95, state="disabled")
        kaydirma = ttk.Scrollbar(gecmis_panel, command=self.gecmis.yview)
        self.gecmis.config(yscrollcommand=kaydirma.set)
        self.gecmis.pack(side="left", fill="x", expand=True)
        kaydirma.pack(side="right", fill="y")
        self.canvas = tk.Canvas(root, width=720, height=300, bg="white")
        self.canvas.pack(padx=12, pady=8)
        self.legend = ttk.Label(
            root,
            text="Mavi: y=1   |   Turuncu: y=0   |   Siyah: karar sınırı   |   Kırmızı: verilen giriş\n"
                 "Karar sınırı: w1·x1 + w2·x2 + b = 0. Sınır üzerindeki noktaların çıktısı 1'dir.",
            padding=8, justify="left"
        )
        self.legend.pack(fill="x")
        root.bind("<Return>", lambda event: self.hesapla())
        self.kapi_sec()

    def kapi_sec(self, event=None):
        self.egitimi_bitir()
        self.hata_gecmisi = []
        self.hata_grafigini_ciz()
        kapi = self.kapi.get()
        aciklamalar = {
            "AND": "AND: Yalnızca iki giriş de 1 olduğunda çıktı 1 olur.",
            "OR": "OR: En az bir giriş 1 olduğunda çıktı 1 olur.",
            "XOR": "XOR hedefi: Girişler farklı olduğunda çıktı 1 olur. Aynı tek perceptron kullanılır. "
                   "XOR doğrusal ayrılabilir olmadığından dört hedefin tamamı sağlanamaz.",
        }
        self.aciklama.config(text=aciklamalar[kapi])
        self.tablo.heading("beklenen", text=f"{kapi} hedefi")
        # XOR seçilirken kullanıcının mevcut ağırlıklarını koru.
        if kapi != "XOR":
            self.agirliklari_yukle()
            return
        self.hesapla()

    def agirliklari_yukle(self):
        self.egitimi_bitir()
        self.hata_gecmisi = []
        self.hata_grafigini_ciz()
        # XOR için de aynı tek nörona başlangıç değerleri verilir.
        bias = "-1.5" if self.kapi.get() == "AND" else "-0.5"
        for isim, deger in (("w1", "1"), ("w2", "1"), ("b", bias)):
            self.girdiler[isim].delete(0, tk.END)
            self.girdiler[isim].insert(0, deger)
        self.hesapla()

    def model(self, x1, x2, w1, w2, b):
        return perceptron(x1, x2, w1, w2, b)

    def duraklat(self):
        if self.zamanlayici is not None:
            self.root.after_cancel(self.zamanlayici)
            self.zamanlayici = None

    def egitimi_bitir(self):
        self.duraklat()
        self.egitim = False
        for isim in ("w1", "w2", "b"):
            self.girdiler[isim].config(state="normal")
        self.eta.config(state="normal")
        self.tur_siniri.config(state="normal")
        if hasattr(self, "egitim_bilgisi"):
            self.egitim_bilgisi.config(text="Eğitim başlatılmadı. Başlangıç değerlerini seçip Başlat'a basın.")

    def kapat(self):
        self.duraklat()
        self.root.destroy()

    def kaydet(self, metin):
        self.egitim_bilgisi.config(text=metin)
        self.gecmis.config(state="normal")
        self.gecmis.insert(tk.END, metin + "\n\n")
        self.gecmis.see(tk.END)
        self.gecmis.config(state="disabled")

    def toplam_hata(self):
        # |hedef - çıktı|: 0/1 çıktılarda hatalı örnek sayısına eşittir.
        return sum(abs(hedef_degeri(self.kapi.get(), a, b) -
                       perceptron(a, b, *self.agirliklar)[1])
                   for a, b in self.ornekler)

    def hata_grafigini_ac(self):
        if self.hata_penceresi is not None and self.hata_penceresi.winfo_exists():
            self.hata_penceresi.deiconify()
            self.hata_penceresi.lift()
            return
        self.hata_penceresi = tk.Toplevel(self.root)
        self.hata_penceresi.title("Perceptron — hata değişimi")
        self.hata_penceresi.protocol("WM_DELETE_WINDOW", self.hata_penceresi.withdraw)
        ttk.Label(self.hata_penceresi, padding=8,
                  text="Toplam hata = Σ|hedef − çıktı| (dört örneğin tamamı).\n"
                       "Her adım sonunda mevcut ağırlıklarla ölçülür; sıfırda eğitim durur.").pack(fill="x")
        self.hata_canvas = tk.Canvas(self.hata_penceresi, width=720, height=280, bg="white")
        self.hata_canvas.pack(fill="both", expand=True, padx=8, pady=8)
        self.hata_canvas.bind("<Configure>", lambda event: self.hata_grafigini_ciz())
        self.hata_grafigini_ciz()

    def hata_grafigini_ciz(self):
        if self.hata_penceresi is None or not self.hata_penceresi.winfo_exists():
            return
        c = self.hata_canvas
        c.delete("all")
        genislik = max(720, c.winfo_width())
        yukseklik = max(280, c.winfo_height())
        sol, ust, sag, alt = 65, 35, genislik - 25, yukseklik - 45
        son_adim = max(1, len(self.hata_gecmisi) - 1)
        def nokta(adim, hata):
            return sol + (sag - sol) * adim / son_adim, alt - (alt - ust) * hata / 4
        for hata in range(5):
            _, y = nokta(0, hata)
            c.create_line(sol, y, sag, y, fill="#bbf7d0" if hata == 0 else "#e5e7eb")
            c.create_text(sol - 15, y, text=str(hata))
        for adim in sorted({round(son_adim * i / 5) for i in range(6)}):
            x, _ = nokta(adim, 0)
            c.create_text(x, alt + 15, text=str(adim))
        c.create_line(sol, ust, sol, alt, sag, alt, width=2)
        c.create_text((sol + sag) / 2, yukseklik - 10, text="Eğitim adımı (0: başlangıç)")
        c.create_text(18, (ust + alt) / 2, text="Toplam hata", angle=90)
        c.create_text((sol + sag) / 2, 15, text=f"{self.kapi.get()} — hata değişimi")
        noktalar = [nokta(i, hata) for i, hata in enumerate(self.hata_gecmisi)]
        if len(noktalar) > 1:
            c.create_line(*[v for p in noktalar for v in p], fill="#2563eb", width=2)
        if noktalar:
            x, y = noktalar[-1]
            c.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#16a34a" if self.hata_gecmisi[-1] == 0 else "#2563eb")
            c.create_text(sag, ust + 12, anchor="ne", text=f"Son hata: {self.hata_gecmisi[-1]}/4")
        else:
            c.create_text((sol + sag) / 2, (ust + alt) / 2, text="Grafik için eğitimi başlatın.")

    def baslat(self, rastgele=False):
        try:
            eta = float(self.eta.get().replace(",", "."))
            sinir = int(self.tur_siniri.get())
            agirliklar = ([random.uniform(-1, 1) for _ in range(3)] if rastgele else
                         [float(self.girdiler[k].get().replace(",", "."))
                          for k in ("w1", "w2", "b")])
            if not 0 < eta <= 1 or sinir < 1 or not all(math.isfinite(w) for w in agirliklar):
                raise ValueError
            if not all(math.isfinite(perceptron(a, b, *agirliklar)[0]) for a, b in self.ornekler):
                raise ValueError
        except (ValueError, OverflowError):
            messagebox.showerror("Eğitim ayarları", "Sonlu ağırlıklar, 0 < η ≤ 1 ve pozitif tam sayı tur sınırı girin.")
            return
        self.duraklat()
        self.ogrenme, self.sinir = eta, sinir
        self.agirliklar = agirliklar
        self.eta.config(state="readonly")
        self.tur_siniri.config(state="readonly")
        self.indeks, self.tur, self.hatalar, self.adim_no = 0, 1, 0, 0
        self.egitim = True
        self.gecmis.config(state="normal")
        self.gecmis.delete("1.0", tk.END)
        self.gecmis.config(state="disabled")
        self.alanlari_guncelle()
        self.hata_gecmisi = [self.toplam_hata()]
        self.hata_grafigini_ac()
        self.hata_grafigini_ciz()
        metin = (f"{self.kapi.get()} eğitimi başladı. η={eta:g}, en fazla {sinir} tur.\n"
                 f"Başlangıç (w1, w2, b) = {tuple(round(w, 4) for w in self.agirliklar)}\n"
                 f"Toplam hata: {self.hata_gecmisi[-1]}/4.")
        if self.hata_gecmisi[-1] == 0:
            self.egitimi_bitir()
            metin += " Hata sıfır; başlangıç ağırlıkları zaten doğru. Eğitim durdu."
        self.kaydet(metin)

    def alanlari_guncelle(self):
        for isim, deger in zip(("w1", "w2", "b"), self.agirliklar):
            alan = self.girdiler[isim]
            alan.config(state="normal")
            alan.delete(0, tk.END)
            alan.insert(0, repr(deger))
            alan.config(state="readonly")
        self.hesapla()

    def adim(self):
        self.duraklat()
        if not self.egitim:
            return
        a, b = self.ornekler[self.indeks]
        hedef = hedef_degeri(self.kapi.get(), a, b)
        once = self.agirliklar[:]
        net, cikti = perceptron(a, b, *once)
        hata = hedef - cikti
        delta = [self.ogrenme * hata * x for x in (a, b, 1)]
        self.agirliklar = [w + dw for w, dw in zip(once, delta)]
        self.hatalar += int(hata != 0)
        self.adim_no += 1
        self.girdiler["x1"].set(str(a))
        self.girdiler["x2"].set(str(b))
        self.alanlari_guncelle()
        metin = (f"Adım {self.adim_no} | Tur {self.tur} | Örnek ({a}, {b}), hedef={hedef}\n"
                 f"1. net = ({once[0]:.4f})·{a} + ({once[1]:.4f})·{b} + ({once[2]:.4f}) = {net:.4f}\n"
                 f"2. hardlim(net) = {cikti}; e = {hedef} − {cikti} = {hata}\n"
                 f"3. Δw1 = η·e·x1 = {delta[0]:+.4f}; Δw2 = η·e·x2 = {delta[1]:+.4f}; Δb = η·e = {delta[2]:+.4f}\n"
                 f"4. Yeni (w1, w2, b) = ({self.agirliklar[0]:.4f}, {self.agirliklar[1]:.4f}, {self.agirliklar[2]:.4f}). "
                 "Grafik güncellendi.")
        self.indeks += 1
        toplam = self.toplam_hata()
        self.hata_gecmisi.append(toplam)
        self.hata_grafigini_ciz()
        metin += f"\nDört örnekte toplam hata: {toplam}/4."
        if toplam == 0:
            self.egitimi_bitir()
            metin += f" {self.kapi.get()} öğrenildi: toplam hata sıfır. Eğitim durdu."
        elif self.indeks == len(self.ornekler):
            metin += f"\nTur tamamlandı: {self.hatalar} hatalı örnek."
            if self.tur >= self.sinir:
                self.egitimi_bitir()
                metin += " Tur sınırına ulaşıldı; öğrenme tamamlanmadı."
                if self.kapi.get() == "XOR":
                    metin += " XOR tek perceptron ile öğrenilemez; doğrusal ayrılabilir değildir."
            else:
                self.tur += 1
                self.indeks, self.hatalar = 0, 0
        self.kaydet(metin)

    def oto_baslat(self):
        if not self.egitim:
            self.baslat()
        if self.egitim and self.zamanlayici is None:
            self.oto_adim()

    def oto_adim(self):
        self.zamanlayici = None
        self.adim()
        if self.egitim:
            self.zamanlayici = self.root.after(900, self.oto_adim)

    def satir_sec(self, event):
        secim = self.tablo.selection()
        if secim:
            a, b = self.tablo.item(secim[0], "values")[:2]
            self.girdiler["x1"].set(a)
            self.girdiler["x2"].set(b)
            self.hesapla()

    def hesapla(self):
        try:
            x1, x2, w1, w2, b = (
                float(self.girdiler[k].get().replace(",", "."))
                for k in ("x1", "x2", "w1", "w2", "b")
            )
            # NaN ve sonsuz değerleri kütüphane kullanmadan reddet.
            for v in (x1, x2, w1, w2, b):
                if v != v or abs(v) == float("inf"):
                    raise ValueError
            net, y = self.model(x1, x2, w1, w2, b)
            if net != net or abs(net) == float("inf"):
                raise ValueError
            self.sonuc.config(text=(
                f"net = ({w1:g})·({x1:g}) + ({w2:g})·({x2:g}) + ({b:g}) = {net:g}\n"
                f"hardlim(net) = 1, net ≥ 0 ise; 0, net < 0 ise.  Çıktı: y = {y}"
            ))
            self.ciz(x1, x2, w1, w2, b)
            # Sabit kimliklerle güncellemek seçim olaylarının döngüye girmesini önler.
            dogru = 0
            for a, d in ((0, 0), (0, 1), (1, 0), (1, 1)):
                n, cikti = self.model(a, d, w1, w2, b)
                hedef = hedef_degeri(self.kapi.get(), a, d)
                dogru += int(cikti == hedef)
                kimlik = f"{a}{d}"
                degerler = (a, d, f"{n:g}", hedef, cikti,
                            "Doğru" if cikti == hedef else "Hatalı")
                if self.tablo.exists(kimlik):
                    self.tablo.item(kimlik, values=degerler)
                else:
                    self.tablo.insert("", "end", iid=kimlik, values=degerler)
            self.kontrol.config(text=f"{self.kapi.get()} doğrulaması: {dogru}/4 doğru. "
                                "Tablodaki bir satıra tıklayarak giriş seçebilirsiniz.")
        except (ValueError, OverflowError):
            messagebox.showerror("Geçersiz giriş", "Sonlu sayılar girin; çok büyük değerler kullanmayın.")

    def ciz(self, x1, x2, w1, w2, b):
        asil_agirliklar = (w1, w2, b)
        # Pozitif ölçekleme karar sınırını değiştirmez; çizimde taşmayı önler.
        olcek = max(abs(w1), abs(w2), abs(b))
        if olcek:
            w1, w2, b = w1 / olcek, w2 / olcek, b / olcek
        c = self.canvas
        c.delete("all")
        sol, ust, genislik, yukseklik = 65, 30, 610, 230
        limit = 1.5

        def ekran(x, y):
            return (sol + (x / limit + 1) * genislik / 2,
                    ust + (1 - y / limit) * yukseklik / 2)

        # Her yatay şeridi karar sınırına göre böl: harici çizim paketi yok.
        for satir in range(yukseklik):
            y = (1 - 2 * (satir + 0.5) / yukseklik) * limit
            if w1 == 0:
                renk = "#dbeafe" if w2 * y + b >= 0 else "#ffedd5"
                c.create_rectangle(sol, ust + satir, sol + genislik,
                                   ust + satir + 1, fill=renk, outline="")
            else:
                kesim = -(w2 * y + b) / w1
                px = sol + (max(-1, min(1, kesim / limit)) + 1) * genislik / 2
                renkler = ("#ffedd5", "#dbeafe") if w1 > 0 else ("#dbeafe", "#ffedd5")
                c.create_rectangle(sol, ust + satir, px, ust + satir + 1,
                                   fill=renkler[0], outline="")
                c.create_rectangle(px, ust + satir, sol + genislik, ust + satir + 1,
                                   fill=renkler[1], outline="")

        for i in range(-4, 5):
            deger = limit * i / 4
            px, py = ekran(deger, deger)
            c.create_line(px, ust, px, ust + yukseklik, fill="#cccccc")
            c.create_line(sol, py, sol + genislik, py, fill="#cccccc")
            c.create_text(px, ust + yukseklik + 16, text=f"{deger:.2g}")
            c.create_text(sol - 28, py, text=f"{deger:.2g}")
        ox, oy = ekran(0, 0)
        c.create_line(sol, oy, sol + genislik, oy, width=2, arrow="last")
        c.create_line(ox, ust + yukseklik, ox, ust, width=2, arrow="last")
        c.create_text(sol + genislik + 15, oy, text="x1")
        c.create_text(ox, ust - 15, text="x2")

        # Doğrunun görünür pencerenin kenarlarıyla kesişimlerini bul.
        noktalar = []
        if w2 != 0:
            for x in (-limit, limit):
                y = -(w1 * x + b) / w2
                if -limit <= y <= limit:
                    noktalar.append(ekran(x, y))
        if w1 != 0:
            for y in (-limit, limit):
                x = -(w2 * y + b) / w1
                if -limit <= x <= limit:
                    nokta = ekran(x, y)
                    if nokta not in noktalar:
                        noktalar.append(nokta)
        if len(noktalar) >= 2:
            c.create_line(*noktalar[0], *noktalar[1], width=3)
        if w1 == 0 and w2 == 0:
            c.create_text(sol + genislik / 2, ust + 18,
                          text=f"Ağırlıklar sıfır: tüm girişler için y = {int(b >= 0)}")
        elif len(noktalar) < 2:
            c.create_text(sol + genislik / 2, ust + 18,
                          text="Karar sınırı bu görüntüleme aralığının dışında.")

        for a, d in ((0, 0), (0, 1), (1, 0), (1, 1)):
            px, py = ekran(a, d)
            _, cikti = self.model(a, d, *asil_agirliklar)
            renk = "#2563eb" if cikti else "#ea580c"
            c.create_oval(px - 7, py - 7, px + 7, py + 7, fill=renk, outline="black")
            c.create_text(px, py - 20, text=f"({a}, {d}) → {cikti}")
        px, py = ekran(x1, x2)
        c.create_oval(px - 11, py - 11, px + 11, py + 11, outline="red", width=3)


if __name__ == "__main__":
    pencere = tk.Tk()
    Uygulama(pencere)
    pencere.mainloop()
