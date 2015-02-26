from PIL import Image

resim = Image.open('sample_shredded.jpg')
data = resim.getdata()
sutun_sayisi = 20
unshredded = Image.new("RGBA", resim.size)
her_bir_parcanin_genisligi = unshredded.size[0] / sutun_sayisi
yukseklik = resim.size[1]
ciftler = {}
kontrol = -1
j=0

#test


def kontrol():
    print "sutun_sayisi:%s"%sutun_sayisi
    print "her_bir_parcanin_genisligi:%s"%her_bir_parcanin_genisligi
    print "yukseklik:%s"%yukseklik
    print "sonuc:%d " %(yukseklik * her_bir_parcanin_genisligi * 20)


def Kac_Pixel(x,y):
    genislik , yukseklik = resim.size
    pixel = data[y * genislik + x]
    #print pixel #test
    return pixel


def get_shred(kacinci_sutun):
    x1 = her_bir_parcanin_genisligi * kacinci_sutun
    y1 = 0
    x2 = her_bir_parcanin_genisligi + x1
    y2 = yukseklik
    shred  = Image.new("RGBA", (her_bir_parcanin_genisligi, yukseklik))
    return shred


def pixel_islemler():
    r, g, b = 0, 0 ,0
    sol_pixel, sag_pixel = [], []
    sag_sirali , sol_sirali = [], []
    sag_sirasiz , sol_sirasiz = [], []
    j = 1
    t = 1
    en_iyi_eslesme = 0
    taraf = 1 # 1 = sag anlamina gelsin

    while j<20:
        sonuc = 0

        if(taraf == 1): ##sagina eklenecek ise
            x1 = her_bir_parcanin_genisligi * t
            x2 = (her_bir_parcanin_genisligi * j) +1

        else:
            x1 = her_bir_parcanin_genisligi * t
            if j<18:
                x2 = x1 + (her_bir_parcanin_genisligi * (j + 1))

        for i in range(yukseklik):
            y1, y2 = i, i
            sol_pixel = Kac_Pixel(x1,y1)
            sag_pixel = Kac_Pixel(x2,y2)


            r = abs(sol_pixel[0]-sag_pixel[0])
            g = abs(sol_pixel[1]-sag_pixel[1])
            b = abs(sol_pixel[2]-sag_pixel[2])

            sonuc = sonuc + r + g + b

        if taraf == 1:
            sag_sirasiz.append(sonuc)
            sag_sirali.append(sonuc)
            sag_sirali.sort()
        else:
            sol_sirasiz.append(sonuc)
            sol_sirali.append(sonuc)
            sol_sirali.sort()

        j = j + 1

        if j == 20 :

            if taraf == 0: #sol anlaminda

                 while j<19:

                    if sag_sirali[0] == sag_sirasiz[j]:
                        en_iyi_eslesme = j + 1
                        print "en iyi eslesme shredi sagda", en_iyi_eslesme, "taraf sag", "deger", sag_sirali[0]

                    if sol_sirali[0] == sol_sirasiz[j]:
                        en_iyi_eslesme = j + 1
                        print "en iyi eslesme shredi solda", en_iyi_eslesme, "taraf sol", "deger", sol_sirali[0]

                    j=j+1

                 # if t==sutun_sayisi-1:
                 #    break
                 # else:
                 #    taraf = 1
                 #    j = 1
                 #    t = t + 1

            else:
                j = 1
                taraf=0

    # j = 0
    # while j<19:
    #     if sag_sirali[0] == sag_sirasiz[j]:
    #         en_iyi_eslesme = j + 1
    #         print "en iyi eslesme shredi sagda", en_iyi_eslesme, "taraf sag", "deger", sag_sirali[0]
    #     if sol_sirali[0] == sol_sirasiz[j]:
    #         en_iyi_eslesme = j + 1
    #         print "en iyi eslesme shredi solda", en_iyi_eslesme, "taraf sol", "deger", sol_sirali[0]
    #     j=j+1

pixel_islemler()
kontrol()
Kac_Pixel(20,30)