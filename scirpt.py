import sys  # Sisteme erişebilmekiçin
import getopt  # Parametrelere erişebilmekiçin
from selenium import webdriver  # Selenium driver Firefox(), Chrome() vb.
from selenium.webdriver.common.keys import Keys  # Selenium parametreleri
import time  # Bilgisayarın hızını yavaşlatmak için (İnternet problemleri -_-)
import pandas as pd  # Pandas Excel kayıt ettirmek için.


class repxpertBot:
    def __init__(self, username, password, txtfile, language):
        self.username = username
        self.password = password
        self.txtfile = txtfile
        self.language = language
        self.driver = webdriver.Chrome()

    # repxpert sayfasına giriyoruz.
    def basla(self):
        driver = self.driver
        url = ""
        if self.language == "fr":
            url = "https://www.repxpert.fr/fr/login"
        elif self.language == "ru":
            url = "https://www.repxpert.ru/ru/login"
        elif self.language == "en":
            url = "https://www.repxpert.co.uk/en/login"

        driver.get(url)
        return driver

    # Login basitçe inputları bulup içerisini temizleyip gelen parametreler ile login oluyoruz.
    def loginOl(self):
        password, username = self.password, self.username
        driver = self.basla()

        e_mail = driver.find_element_by_xpath('//*[@id="j_username"]')
        passwd = driver.find_element_by_xpath('//*[@id="j_password"]')
        e_mail.clear()
        passwd.clear()
        e_mail.send_keys(str(username))
        passwd.send_keys(str(password))

        button = driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div[1]/div[2]/button')

        button.click()

        return driver

    # AramaYap login olduktan sonra txtfile içerisindeki numaraları repxpert içerisinde bulunan search sayfasına searchNo= yazıp aratıyoruz.
    # Label search kısımda bulunan listenin en başındakini alıyor.
    def aramaYap(self):
        driver = self.loginOl()
        txtfile = self.txtfile

        labels = list()

        searchURL = ""
        if self.language == "en":
            searchURL = "https://www.repxpert.co.uk/en/productcatalog/search#!?searchNo="
        elif self.language == "fr":
            searchURL = "https://www.repxpert.fr/fr/productcatalog/search#!?searchNo="
        elif self.language == "ru":
            searchURL = "https://www.repxpert.ru/ru/productcatalog/search#!?searchNo="

        for arat in txtfile:
            driver.get(searchURL + arat)
            time.sleep(0.5)
            try:
                label = driver.find_element_by_xpath(
                    '//product-tile/div/div/div[2]/div/h4')

                labels.append(label.text)
                time.sleep(0.5)
            except:
                time.sleep(0.5)
                labels.append("Null")
                print("Bulamadı")
                continue
        # time.sleep(1)

        df = pd.DataFrame({"Numbers": txtfile,
                           "Labels": labels})

        return labels, df


def parameters(argv):
    try:
        opts, args = getopt.getopt(argv, "h:u:p:i:o:l:")
    except getopt.GetoptError:
        print('script.py -u username -p password -i <inputfile.txt> -o <output.csv> -l languege(fr,en,ru) -h Help')
        sys.exit(2)
    if opts[0][0] == "-h":
        print('script.py -u username -p password -i <inputfile.txt> -o <output.csv> -l languege(fr,en,ru) -h Help')
        sys.exit(2)
    elif opts[0][0] == "-u" and opts[1][0] == "-p" and opts[2][0] == "-i" and opts[3][0] == "-o" and opts[4][0] == "-l":
        username = opts[0][1]
        password = opts[1][1]
        txtfile = open(opts[2][1], "r")
        read_file = txtfile.read().replace(" ", "").split()
        outputfile = opts[3][1]
        language = opts[4][1]
        return username, password, read_file, outputfile, language


if __name__ == "__main__":
    # Okuyacak parametreleri ayırıyoruz.
    username, password, txtfile, outputfile, language = parameters(
        sys.argv[1:])
    # Bir bot nesnesi oluşturup gerekli parametreleri giriyoruz.
    bot = repxpertBot(username, password, txtfile, language)

    # labels list şeklinde gelen ingilizce
    # df DataFrame excel kayıt ettirmek için
    labels, df = bot.aramaYap()
    # Çıktıyı Kayıt Etmek için Yorum Satırından kaldırın.
    df.to_csv(outputfile)
