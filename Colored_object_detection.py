import cv2
import numpy as np
import time  # Eklenen kütüphane

def detect_color(image, target_color):
    # Resmi BGR'den HSV'ye dönüştür
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Renk tespiti için renk aralıklarını tanımla (mavi, yeşil, sarı ve kırmızı)
    color_ranges = {
        'blue': ([100, 50, 50], [120, 255, 255]),  # Adjusted for blue
        'green': ([40, 50, 50], [80, 255, 255]),
        'yellow': ([20, 100, 100], [30, 255, 255]),
        'red': ([0, 100, 100], [10, 255, 255]) + ([170, 100, 100], [180, 255, 255]),  # Adjusted for red (considering wrap-around)
    }

    # Hedef rengin renk aralığını al
    target_range = color_ranges.get(target_color.lower())

    if target_range is None:
        return None, None  # Hem tespit edilen rengi hem de sınırlayıcı kutuyu için None döndür

    # HSV görüntüsündeki renk aralığına dayalı bir maske oluştur
    mask = cv2.inRange(hsv_image, np.array(target_range[0]), np.array(target_range[1]))

    # Maskeyi uygula ve konturları bul
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_color = None
    bounding_box = None

    for contour in contours:
        # Küçük konturları filtrele
        if cv2.contourArea(contour) > 5000:  # Bu eşik değeri ihtiyaca göre ayarlayın
            # Kontur etrafında sınırlayıcı dikdörtgeni al
            x, y, w, h = cv2.boundingRect(contour)

            # İlgili bölgenin (ROI) ilgisini çek
            roi = masked_image[y:y+h, x:x+w]

            # HSV uzayındaki ROI'nin ortalama rengini hesapla
            mean_color_hsv = cv2.mean(roi)[:3]

            # Ortalama renk, hedef renk aralığına yakın mı kontrol et
            if target_color.lower() == 'red' and (mean_color_hsv[0] > 170 or mean_color_hsv[0] < 10):
                detected_color = target_color
                bounding_box = (x, y, w, h)
                return detected_color, bounding_box
            elif target_color.lower() != 'red' and mean_color_hsv[0] > target_range[0][0] and mean_color_hsv[0] < target_range[1][0]:
                detected_color = target_color
                bounding_box = (x, y, w, h)
                return detected_color, bounding_box

    return detected_color, bounding_box

def draw_circle(image, center, bgr_color):
    # Belirtilen renkte merkezin etrafına dolu bir daire çiz
    cv2.circle(image, center, 50, bgr_color, -1)

# Kamera bağlantısını başlat
cap = cv2.VideoCapture(0)

# Renk sırasını tanımla
color_sequence = ['red', 'blue', 'yellow', 'green']

for target_color in color_sequence:
    # Kameradan bir kare yakala
    ret, image = cap.read()

    # Kare başarıyla yakalandı mı kontrol et
    if not ret:
        break

    cv2.putText(image, f"Searching for {target_color} object...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Frame', image)
    cv2.waitKey(1000)  # 1 saniye beklemek için

    start_time = time.time()  # Başlangıç zamanını kaydet

    while True:
        # Kameradan bir kare yakala
        ret, frame = cap.read()
        if not ret:
            break

        # Rengi tespit et ve sınırlayıcı kutuyu al
        detected_color, bounding_box = detect_color(frame, target_color)

        if detected_color is not None:
            # Kameradaki renkli nesneyi daha büyük bir font ile göster
            cv2.putText(frame, f"{detected_color.capitalize()} object found!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
            
            # Sınırlayıcı kutudaki her şeyin tespit edilen renkte olduğunu belirten bir mesajı göster
            cv2.putText(frame, f"Everything in the bounding box is {detected_color.capitalize()}.", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
            
            if bounding_box is not None:
                # Sınırlayıcı kutunun merkezine (örneğin: yeşil daire) bir daire çiz
                draw_circle(frame, (bounding_box[0] + bounding_box[2] // 2, bounding_box[1] + bounding_box[3] // 2), (0, 255, 0))
            
            cv2.imshow('Frame', frame)
            elapsed_time = time.time() - start_time
            if elapsed_time >= 3:  # 3 saniye beklemek için
                break

        # Çerçeveyi göster
        cv2.imshow('Frame', frame)

        # 'q' tuşuna basıldığında döngüyü kır
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Kamera bağlantısını serbest bırak ve pencereyi kapat
cap.release()
cv2.destroyAllWindows()
