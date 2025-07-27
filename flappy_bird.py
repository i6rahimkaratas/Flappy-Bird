import pygame
import random
import sys

EKRAN_GENISLIGI = 400
EKRAN_YUKSEKLIGI = 600
FPS = 60  

SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
SARI = (255, 255, 0)  

KUS_X = 50
KUS_GENISLIK = 40
KUS_YUKSEKLIK = 40
YERCEKIMI = 0.4
ZIPLAMA_GUCU = -8

BORU_GENISLIK = 50
BORU_BOSLUK = 150  
BORU_HIZI = -3
BORU_EKLEME_ARALIGI = 1500 




class Kus(pygame.sprite.Sprite):
    """Oyuncunun kontrol ettiği kuşu temsil eden sınıf."""
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load("sarikus.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (KUS_GENISLIK, KUS_YUKSEKLIK))
        self.rect = self.image.get_rect()
        self.rect.x = KUS_X
        self.rect.y = EKRAN_YUKSEKLIGI // 2

       
        self.hiz_y = 0

    def zipla(self):
        
        self.hiz_y = ZIPLAMA_GUCU

    def update(self):
       
        self.hiz_y += YERCEKIMI
        self.rect.y += self.hiz_y

        
        if self.rect.top < 0:
            self.rect.top = 0
            self.hiz_y = 0


class Boru(pygame.sprite.Sprite):
    
    def __init__(self, x, y, yukseklik, ters=False):
        super().__init__()
        self.image = pygame.Surface([BORU_GENISLIK, yukseklik])
        self.image.fill(BEYAZ)
        self.rect = self.image.get_rect()
        self.rect.x = x

        
        if ters:
            self.rect.bottom = y
        else:
            self.rect.top = y

    def update(self):
        
        self.rect.x += BORU_HIZI
        
        if self.rect.right < 0:
            self.kill()




def oyun():
    
    pygame.init()

    
    ekran = pygame.display.set_mode((EKRAN_GENISLIGI, EKRAN_YUKSEKLIGI))
    pygame.display.set_caption("Siyah Beyaz Flappy Bird")
    saat = pygame.time.Clock()

    
    tum_spritelar = pygame.sprite.Group()
    borular = pygame.sprite.Group()

    
    kus = Kus()
    tum_spritelar.add(kus)

    
    BORU_EKLE_EVENTI = pygame.USEREVENT + 1
    pygame.time.set_timer(BORU_EKLE_EVENTI, BORU_EKLEME_ARALIGI)

    
    skor = 0
    font = pygame.font.Font(None, 74)
    oyun_bitti = False
    oyun_basladi = False

    
    gecilen_borular = []

    
    calisiyor = True
    while calisiyor:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                calisiyor = False

            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or \
               event.type == pygame.MOUSEBUTTONDOWN:
                if not oyun_bitti:
                    oyun_basladi = True
                    kus.zipla()
                else:
                    
                    return oyun()

            
            if event.type == BORU_EKLE_EVENTI and not oyun_bitti and oyun_basladi:
                
                bosluk_y = random.randint(150, EKRAN_YUKSEKLIGI - 150)

                
                alt_boru = Boru(EKRAN_GENISLIGI, bosluk_y + BORU_BOSLUK // 2, EKRAN_YUKSEKLIGI)
                
                ust_boru = Boru(EKRAN_GENISLIGI, bosluk_y - BORU_BOSLUK // 2, EKRAN_YUKSEKLIGI, ters=True)

                tum_spritelar.add(alt_boru, ust_boru)
                borular.add(alt_boru, ust_boru)

                
                gecilen_borular.append((alt_boru, ust_boru, False))


        if not oyun_bitti:
            
            if oyun_basladi:
                tum_spritelar.update()

            
            for alt_boru, ust_boru, gecildi in gecilen_borular:
                if not gecildi and alt_boru.rect.centerx < kus.rect.centerx:
                    skor += 1
                    
                    gecilen_borular[gecilen_borular.index((alt_boru, ust_boru, gecildi))] = (alt_boru, ust_boru, True)


            
            if pygame.sprite.spritecollide(kus, borular, False):
                oyun_bitti = True

            
            if kus.rect.bottom >= EKRAN_YUKSEKLIGI:
                oyun_bitti = True
                kus.rect.bottom = EKRAN_YUKSEKLIGI 


        
        ekran.fill(SIYAH)
        tum_spritelar.draw(ekran)

       
        skor_yazisi = font.render(str(skor), True, BEYAZ)
        ekran.blit(skor_yazisi, (EKRAN_GENISLIGI / 2 - skor_yazisi.get_width() / 2, 50))

        
        if oyun_bitti:
            bitis_fontu = pygame.font.Font(None, 50)
            bitis_yazisi = bitis_fontu.render("Oyun Bitti", True, BEYAZ)
            tekrar_yazisi = bitis_fontu.render("", True, BEYAZ)

            ekran.blit(bitis_yazisi, (EKRAN_GENISLIGI/2 - bitis_yazisi.get_width()/2, EKRAN_YUKSEKLIGI/2 - 50))
            ekran.blit(tekrar_yazisi, (EKRAN_GENISLIGI/2 - tekrar_yazisi.get_width()/2, EKRAN_YUKSEKLIGI/2))

        
        if not oyun_basladi:
            baslangic_fontu = pygame.font.Font(None, 40)
            baslangic_yazisi = baslangic_fontu.render("Baslamak icin ZIPLA", True, BEYAZ)
            ekran.blit(baslangic_yazisi, (EKRAN_GENISLIGI/2 - baslangic_yazisi.get_width()/2, EKRAN_YUKSEKLIGI/1.5))


        
        pygame.display.flip()

       
        saat.tick(FPS)

    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    oyun()