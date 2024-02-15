class Haritalama:
    def __init__(self, x_length=100, y_length=50, depth=3):
        # Harita boyutları ve derinlik bilgisiyle birlikte haritanın başlatılması
        self.x_length = x_length
        self.y_length = y_length
        self.depth = depth
        self.map = [[[0] * depth for _ in range(x_length)] for _ in range(y_length)]

    def haritaya_ekle(self, pozisyon):
        x, y, z = pozisyon
        # Haritaya algılanan nesneyi ekle
        if 0 <= x < self.x_length and 0 <= y < self.y_length and 0 <= z < self.depth:
            self.map[y][x][z] = 1
        else:
            print("Hata: cihaz pozisyonu harita sınırlarının dışında!")

    def haritayi_goster(self):
        # Haritayı ekrana yazdır
        for y in range(self.y_length):
            for x in range(self.x_length):
                print(self.map[y][x], end=" ")
            print()

# Örnek
if __name__ == "__main__":
    harita = Haritalama()
    harita.haritaya_ekle((10, 20, 2))  # Örnek olarak (10, 20, 2) pozisyonunda bir nesne algılandı
    harita.haritayi_goster()
