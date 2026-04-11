# YOLOv8-OBB Cube Detection Project

Bu proje, TEKNOFEST Robolig kapsamında bir robotun **küp (cube) nesnesini tespit etmesi ve konum/açı bilgisine göre yakalaması** amacıyla geliştirilmiştir.

---

## 🚀 Proje Amacı

- Kameradan gelen görüntüde küpü tespit etmek
- Küpün:
  - konumunu (cx, cy)
  - açısını (angle)
  - boyutunu (area)
- robotik kola iletmek
- nesneyi doğru açıyla yakalamak

---

## 🧠 Kullanılan Teknoloji

- YOLOv8-OBB (Oriented Bounding Box)
- Python
- OpenCV
- Ultralytics

---

## 📦 Dataset

Kullanılan dataset:
- Roboflow üzerinden alınmıştır
- Cube ve pillar sınıfları içeriyordu

### Yapılan işlemler:
- Sadece **cube** sınıfları bırakıldı
- Tüm cube sınıfları tek sınıfa indirildi:
  ```yaml
  names:
    0: cube
````

---

## 📁 Proje Yapısı

```text
cube.v3i.yolov8-obb/
├── train/
├── valid/
├── test/
├── runs/
├── data.yaml
├── live_test.py
```

---

## ⚙️ Kurulum

### 1. Sanal ortam oluştur

```bash
py -3.13 -m venv .venv
```

### 2. Ortamı aktif et

```bash
.\.venv\Scripts\activate
```

### 3. Gerekli paketler

```bash
pip install ultralytics opencv-python
```

---

## 🏋️ Model Eğitimi

```bash
.\.venv\Scripts\yolo.exe task=obb mode=train model=yolov8n-obb.pt data=data.yaml epochs=50 imgsz=640
```

### Çıktı:

```text
runs/obb/train/weights/best.pt
```

---

## 🔍 Test (Görsel)

```bash
.\.venv\Scripts\yolo.exe task=obb mode=predict model=runs/obb/train/weights/best.pt source=test/images save=True
```

---

## 🎥 Canlı Kamera Testi

```bash
python live_test.py
```

---

## 📊 Model Çıktıları

Her tespit için:

* `cx` → merkez x koordinatı
* `cy` → merkez y koordinatı
* `angle` → nesnenin açısı
* `confidence` → model güveni
* `area` → nesne büyüklüğü

---

## 🤖 Robot Kontrol Mantığı

Ekran 3 bölgeye ayrılır:

```text
| SOL | ORTA | SAĞ |
```

### Karar mekanizması:

* cx < sol eşik → sola dön
* cx > sağ eşik → sağa dön
* ortadaysa → ileri git

### Kavrama:

* angle → kol açısını ayarla
* area büyükse → nesne yakın → kavra

---

## 🎯 Kritik Noktalar

* OBB sayesinde nesnenin açısı hesaplanır
* Tek sınıf (cube) kullanımı performansı artırır
* Gerçek ortam verisi ile fine-tune önerilir

---

## 🔜 Geliştirme Adımları

* PID ile hassas hizalama
* Derinlik (depth) entegrasyonu
* ROS entegrasyonu
* Gerçek zamanlı robot kontrolü

---

## 👨‍💻 Geliştirici Notu

Bu proje, yapay zekâ ile robotik sistemlerin entegrasyonuna yönelik bir çalışmadır.
Model çıktıları doğrudan robot kontrolüne bağlanacak şekilde tasarlanmıştır.

---

## 🏁 Sonuç

✔ Küp tespiti başarılı
✔ Açı bilgisi elde edildi
✔ Robotik entegrasyon için hazır çıktı üretildi

```