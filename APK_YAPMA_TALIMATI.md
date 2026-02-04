# Nexus APK Derleme Kılavuzu (Google Colab)

Windows bilgisayarlarda APK yapmak zordur. En kolay ve hızlı yöntem Google'ın ücretsiz bilgisayarlarını (Colab) kullanmaktır. Kodlarını GitHub'a yüklediğin için işlem çok basit!

### Adım 1: Google Colab'ı Aç
Şu adrese git: [https://colab.research.google.com/](https://colab.research.google.com/)

### Adım 2: Yeni Not Defteri Aç
"Yeni Not Defteri" (New Notebook) butonuna bas.

### Adım 3: Kodları Yapıştır
Açılan boş sayfadaki kod kutusuna **aşağıdaki kodların tamamını kopyalayıp yapıştır**:

```python
# 1. Gerekli Araçları Yükle
!pip install buildozer cython
!sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 2. Senin GitHub Projeni Çek
!git clone https://github.com/ibomiri431-oss/CuuP.git

# 3. Android Proje Klasörüne Gir
%cd CuuP/AndroidProject

# 4. APK'yı Derle (Bu işlem 10-15 dakika sürebilir)
!buildozer android debug

# 5. Derleme Bitince APK'yı İndirmen İçin Hazırla
print("\n\n✅ İŞLEM TAMAMLANDI! Sol taraftaki dosya simgesine tıkla.")
print("CuuP > AndroidProject > bin klasörüne git.")
print(".apk dosyasını sağ tıklayıp İNDİR diyebilirsin.")
```

### Adım 4: Çalıştır
Kutucuğun solundaki **Play (▶️)** butonuna bas ve arkana yaslan.

Yaklaşık 10-15 dakika sürecek. İşlem bitince:
1.  Ekranın solundaki **Dosya (Klasör)** simgesine tıkla.
2.  `CuuP` > `AndroidProject` > `bin` yolunu izle.
3.  Orada **`nexus-1.0-debug.apk`** göreceksin.
4.  Sağ tıkla ve **İndir** de.

Tebrikler! Kendi yaptığın uygulama artık telefonunda. 🚀
