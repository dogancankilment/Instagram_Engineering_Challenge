import sys
import PIL.Image
#from PIL import Image

# calistirmak icin python unshredder.py image_file.jpg


def pixel_islemleri(image, shred_width, left_shred, right_shred):

    """

    Argumanlar:

    image : resim
    shred_width : her bir parcanin genisligi
    left_shred : sol parcada index olarak kullanilacak
    right_shred : sag parcada index olarak kullanilacak

    """

    w, h = image.size
    data = image.getdata()

    return sum([abs(data[y * w + (left_shred + 1) * shred_width - 1] -
                    data[y * w + right_shred * shred_width])
                for y in xrange(h)])


def unshred(image, shred_width):

    """
    Bu fonksiyonun esas amaci soldan saga dogru gelecek olan shred listesini
    Unshred yapilmis olan resme yerlestirmelidir.

    Argumanlar:
    image : resim
    shred_width : shred genisligi
    return :
    Buradan geri donecek deger (return yapacak sey)
    Unshred yapilmis olan resmi olusturacak shred listesini tutacak
    """


    def unshred_islemi(yerlestirme, shreds_left, unshred_order):

        """
        inner fonksiyonu tek basamakta unshredding islemini gerceklestirecek.

        Argumanlar:
        yerlestirme -- (left_shred, right_shred, stitching_cost) dizilerini tutan
                      ve bu fonksiyon tarafindan siralanmis tum olasi listeler
        shreds_left -- unshred islemine tabi tutulacak sol parca
        unshred_order -- sirasiyla soldan saga dizilmis olan unshredded resmi elde etmek
                        icin gerekli olan parcalari tutacak

        Bu fonksiyon ozyinelemeli olarak calisarak geri deger dondurecektir.
        Her adimda yeni bir parca siraya koyularak esas olmasi gereken yer bulanacaktir.
        Bu parca yerlestirildikten sonra bir sonraki parcayi bulmak icin
        Hesaplama sonucunda en dusuk degere sahip olan parcayi yerlestirebilmek icin
        en son gecerli olan unshredded resmin solundaki parca ile karsilastirildiktan sonra
        unshred order listesinin basina eklenmeli. Bu sayede liste basina
        ekledigimiz yeni parca gecerli olan unshredded resmimizin sag parcasi olacaktir.

        Eger baslangicta unshred order listemiz bos ise yerlestirmeye baslarken
        en dusuk degerli olan parcayi alip, cift tarafli bakarak yerlestirmeye devam etmeliyiz.
        Zaten cift tarafli bakacagimiz icin resim en sonunda ortaya cikacaktir.
        """

        if shreds_left == 0:

            return unshred_order

        else:

            if not unshred_order: #liste ilk adimda bos ise

                best = yerlestirme[0]
                unshred_order_next = [best[0], best[1]]
                shreds_left_next = shreds_left - 2

            else:

                #en iyi liste basina eklenebilecek deger
                best_prepend = filter(lambda x: x[1] == unshred_order[0], yerlestirme)

                #en iyi tercih
                best_append = filter(lambda x: x[0] == unshred_order[-1], yerlestirme)

                if best_prepend and best_append and \
                                best_prepend[0][2] < best_append[0][2] or best_prepend:

                    unshred_order_next = [best_prepend[0][0]] + unshred_order

                elif best_append:

                    unshred_order_next = unshred_order + [best_append[0][1]]

                else:

                    raise Exception("Yapilamadi")

                shreds_left_next = shreds_left - 1

                """

                Simdi elimizde olanlar
                unshred_order_next[0] : sol parca ve sol parcayla devam eden
                unshred_order_next[-1] : unshred_order_next'in
                                        son elemani - sag parca gibi

                """

            yerlestirme_next = filter(lambda x: x[0] != unshred_order_next[0] and
                                                x[1] != unshred_order_next[-1], yerlestirme)

            return unshred_islemi(yerlestirme_next, shreds_left_next, unshred_order_next)

    shreds = image.size[0] / shred_width

    # cmp karsilastirma islemi yapmamizi sagliyor
    # Eger geri donen deger negatif ise if x < y, sifir ise if x == y ve
    # tam anlamiyla pozitif ise if x > y.
    yerlestirme = sorted([(sol, sag, pixel_islemleri(image, shred_width, sol, sag))
                          for sol in xrange(shreds) for sag in xrange(shreds)
                          if sol != sag], cmp=lambda x, y: x[2] - y[2])

    return unshred_islemi(yerlestirme, shreds, [])


if __name__ == "__main__":

    # kullanicinin girdi olarak yazdigi resmi
    # isleme tabi tutacagiz
    image = PIL.Image.open(sys.argv[1])

    shred_width = 32 #her bir parcanin genisligi
    unshred_order = unshred(image.convert("L"), shred_width) #monochrome gri tonlama

    # image_file = image_file.convert('1') # resmi siyah ve beyaz agirlikli haline cevirir.
    # convert farkli versiyonlarda calisabiliyor.
    # resmi siyah beyaz yapiyor

    unshredded = PIL.Image.new("RGB", image.size)

    for i, shred in enumerate(unshred_order):
        x1, y1 = shred_width * shred, 0
        x2, y2 = x1 + shred_width, image.size[1]
        unshredded.paste(image.crop((x1, y1, x2, y2)), (i * shred_width, 0))
        # step by step gormemizi sagliyor
        # unshredded.save(str(i)+"unshredded.png", "PNG")

    unshredded.save("unshredded.png", "PNG")
    #unshredded.save("unshredded.jpg")