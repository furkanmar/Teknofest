import cv2
"""from PIL import Image

from goruntu_isleme1 import get_limits


yellow = [0, 255, 255]  # yellow in BGR colorspace
cap = cv2.VideoCapture(2)
while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=yellow)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()"""



# Laptop kamerasını kullanmak için 0 endeksini kullanıyoruz
"""camera_index = 0


cap = cv2.VideoCapture(camera_index)


if not cap.isOpened():
    print("Kamera bağlantısı kurulamadı. Lütfen bağlantıyı kontrol edin.")
    exit()

# Video döngüsü
while True:
    # Kameradan bir kare alın
    ret, frame = cap.read()

    
    if not ret:
        print("Kare alınamadı. Çıkış yapılıyor...")
        break

    # Alınan kareyi göster
    cv2.imshow('Laptop Kamera', frame)

    # 'q' tuşuna basıldığında döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Video yakalama nesnesini ve pencereyi serbest bırakın
cap.release()
cv2.destroyAllWindows()"""

from PIL import Image

from goruntu_isleme1 import get_limits

yellow = [0, 255, 255]

# Notebook kamerası için genellikle 0 endeksini kullan
camera_index = 0

# Video yakalama nesnesi
cap = cv2.VideoCapture(camera_index)

while True:

    ret, frame = cap.read()

    # Kare alınamazsa döngüyü sonlandır
    if not ret:
        print("Kare alınamadı. Çıkış yapılıyor...")
        break

    # Görüntüyü HSV renk uzayına dönüştürün
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Sarı renk sınırlarını alın
    lowerLimit, upperLimit = get_limits(color=yellow)

    # Maskelenmiş görüntüyü elde etmek için renk sınırlarını kullanarak bir maske oluşturun
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    # Maskelenmiş görüntüdeki sınırları alın
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    # Eğer sınırlar varsa, sınırları çerçeveleyin
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    # Görüntüyü gösterin
    cv2.imshow('frame', frame)

    # 'q' tuşuna basıldığında döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Video yakalama nesnesini ve pencereyi serbest bırakın
cap.release()
cv2.destroyAllWindows()

