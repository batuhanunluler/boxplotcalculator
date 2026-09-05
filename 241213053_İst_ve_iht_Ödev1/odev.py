import csv
import os
import matplotlib.pyplot as plt

dosya_adi = "veri.csv"
su_anki_dizin = os.path.dirname(os.path.abspath(__file__))
tam_yol = os.path.join(su_anki_dizin, dosya_adi)

var1 = []
var2 = []
var3 = []

try: 
    with open (dosya_adi, mode='r', encoding='utf-8' ) as dosya:
        okuyucu = csv.reader(dosya, delimiter=',')
        basliklar = next(okuyucu)

        for satir in okuyucu:
            if len(satir) < 3:
                continue

            var1.append(float(satir[1]))
            var2.append(float(satir[2]))
            var3.append(float(satir[3]))

    print ("Veri okuma basarili!")
    print (f"Toplam okunan gozlem (satIr) sayisi: {len(var1)}")
    print ("Degisken 1'in verileri:" , var1)

except FileNotFoundError:
    print (f"Hata: {dosya_adi} dosyasi bulunamadi! odev.py ile ayni klasorde olup olmadigini kontrol edin!")
except Exception as e:
    print (f"Beklenmeyen Hata!: {e}")

def manuel_siralama (liste):
    n = len(liste)

    for i in range (n-1):
        for j in range(n-i-1):
            if liste[j] > liste[j+1]:
                liste[j], liste[j+1] = liste[j+1] , liste[j]
    return liste

def aykiri_analizi(liste):
    sirali = manuel_siralama(liste[:])
    n = len(sirali)

    q1 = sirali[int(n * 0.25)]
    q3 = sirali[int(n* 0.75)]
    iqr = q3 - q1

    alt_sinir = q1 - (1.5*iqr)
    ust_sinir = q3 + (1.5*iqr)

    aykirilar = []
    temiz_liste = []

    for x in liste:
        if x < alt_sinir or x > ust_sinir:
            aykirilar.append(x)
        else:
            temiz_liste.append(x)
    return aykirilar, temiz_liste, q1, q3, iqr, alt_sinir, ust_sinir
def merkezi_egilim_hesapla (liste):
    n = 0
    toplam = 0
    for x in liste:
        toplam += x
        n += 1
    ortalama = toplam / n

    sirali = manuel_siralama(liste[:])
    orta = n // 2
    if n % 2 == 0:
        medyan = (sirali[orta-1] + sirali[orta]) / 2
    else:
        medyan = sirali[orta]
    
    en_yuksek_frekans = 0
    mod = sirali[0]
    for i in range(n):
        sayac = 0
        for j in range(n):
            if sirali[i] == sirali[j]:
                sayac += 1
        if sayac > en_yuksek_frekans:
            en_yuksek_frekans = sayac
            mod = sirali[i]
    return ortalama, medyan, mod

def merkezi_dagilim_hesapla(liste, ortalama, q1, q3):
    n = 0
    for _ in liste: n+=1

    maksi=liste[0]
    mini=liste[0]
    for x in liste:
        if x > maksi: maksi=x
        if x < mini: mini=x
    aralik = maksi - mini

    mutlak_toplam=0
    for x in liste:
        fark = x-ortalama
        if fark < 0:
            fark = -fark
        mutlak_toplam += fark
    ort_mutlak_sapma = mutlak_toplam / n

    kare_fark_toplam = 0
    for x in liste:
        kare_fark_toplam += (x-ortalama) ** 2
    
    varyans = kare_fark_toplam / (n-1)
    std_sap = varyans ** 0.5

    degisim_kats = (std_sap / ortalama) * 100

    iqr = q3 -q1

    return aralik, ort_mutlak_sapma, varyans, std_sap, degisim_kats, iqr
sonuc_dosyayolu = os.path.join(su_anki_dizin, 'sonuc.txt')

with open (sonuc_dosyayolu, "w" , encoding="utf-8") as f:
    f.write("--- SONUCLAR ---\n\n")

    degiskenler = [var1, var2, var3]
    isimler = ["Degisken 1", "Degisken 2" , "Degisken 3"]

    boxplot_verileri = []

    for i in range (3):
        mevcutveri = degiskenler[i]
        isim = isimler[i]

        boxplot_verileri.append(mevcutveri)

        aykirilar, temiz_veri, q1, q3, iqr, alt, ust = aykiri_analizi(mevcutveri)
        ort, med, mod = merkezi_egilim_hesapla(temiz_veri)
        aralik, oms, varyans, std, dk, iqr_temiz = merkezi_dagilim_hesapla(temiz_veri, ort, q1, q3)

        rapor = f"""
========== {isim} =========
Aykiri Degerler {aykirilar if len(aykirilar) > 0 else 'Yok!'}

--- Merkezi Egilim (Aykirilar Haric) ---
Aritmetik Ort.: {ort:.2f}
Medyan: {med:.2f}
Mod: {mod:.2f}

---Merkezi Dagilim (Aykirilar Haric)---
Degisim Ar.:{aralik:.2f}
Ort. Mutlak Sapma: {oms:.2f}
Varyans: {varyans:.2f}
Std. Sapma: {std:.2f}
Degisim Kats.: %{dk:.2f}
IQR (Ceyrekler Acikligi): {iqr_temiz:.2f}
"""
        print(rapor)
        f.write(rapor)
print (f"\nBASARILI Tum istatistiksel sonuclar '{sonuc_dosyayolu}' dosyasina kaydedildi!")

print("Grafik ekrana getiriliyor. Grafik kapatildiginda program kapanir...")

plt.boxplot(boxplot_verileri)
plt.xticks([1, 2, 3], isimler)
plt.title("Kutu (Boxplot) Cizimi")
plt.ylabel ("Degerler")

plt.show()