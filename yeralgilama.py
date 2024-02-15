class YerAlgılama:
    def __init__(self):
        # Algılama için gerekli başlangıç durumlarını buradan başlatırım
        pass

    def algila(self, pozisyon):
        # Algılama algoritmasını buradan yazarım
        # örnek olarak nesne olsun
        return pozisyon

# Örnek haritalama ile buradan bağlayabilirim
if __name__ == "__main__":
    algilayici = YerAlgılama()
    algilanan_pozisyon = algilayici.algila((10, 20, 2))  # Örnek olarak (10, 20, 2) pozisyonunda bir nesne algılandı
    print("Algılanan pozisyon:", algilanan_pozisyon)
