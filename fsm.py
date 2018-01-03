from transitions.extensions import GraphMachine
import vlc
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import csv



class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )


    def is_going_to_1(self, update):
        text = update.message.text
        return text.lower() == '定存'

    def is_going_to_2(self, update):
        text = update.message.text
        return text.lower() == '信貸'

    def is_going_to_3(self, update):
        text = update.message.text
        return text.lower() == '股市'

    def is_going_to_4(self, update):
        text = update.message.text
        return text.lower() == '詐騙'

    def is_going_to_5(self, update):
        text = update.message.text
        return text.lower() == '代碼'

    def on_enter_1(self, update):
        update.message.reply_text("各銀行定存利率\n")
        update.message.reply_text("http://www.taiwanrate.com/interest-rate2-tc-0.html#.WkuYL9-Wa70")
        update.message.reply_text("服務項目(輸入文字)：\n查詢銀行代碼(代碼)\n查詢各銀行利率(定存)\n查詢各銀行信貸利息(信貸)\n查詢股市(股市)\n詐騙幫助(詐騙)\n")
        self.go_back(update)

    def on_exit_1(self, update):
        print('Leaving 1')

    def on_enter_3(self, update):
        update.message.reply_text("當日股市\n")
        update.message.reply_text("https://tw.stock.yahoo.com/h/getclass.php")
        update.message.reply_text("服務項目(輸入文字)：\n查詢銀行代碼(代碼)\n查詢各銀行利率(定存)\n查詢各銀行信貸利息(信貸)\n查詢股市(股市)\n詐騙幫助(詐騙)\n")
        self.go_back(update)

    def on_exit_3(self, update):
        print('Leaving 3')

    def on_enter_2(self, update):
        update.message.reply_text("各銀行信貸利息\n")
        update.message.reply_text("https://www.money101.com.tw/%E4%BF%A1%E7%94%A8%E8%B2%B8%E6%AC%BE/%E4%B8%80%E8%88%AC%E8%B2%B8%E6%AC%BE?gclid=CjwKCAiA-KzSBRAnEiwAkmQ1570pawTWaEi6mhxqlPAar249zYbztt43apIR-DFEOIo4v-ZcedOKwhoCnHkQAvD_BwE&gclsrc=aw.ds")
        update.message.reply_text("服務項目(輸入文字)：\n查詢銀行代碼(代碼)\n查詢各銀行利率(定存)\n查詢各銀行信貸利息(信貸)\n查詢股市(股市)\n詐騙幫助(詐騙)\n")
        self.go_back(update)

    def on_exit_2(self, update):
        print('Leaving 2')

    def on_enter_5(self, update):
        update.message.reply_text("各銀行代碼\n")
        res = requests.get('http://web.thu.edu.tw/s932954/www/ruten/banklist.htm')
        res.encoding='utf-8'
        soup = BeautifulSoup(res.text, "lxml")
        bank_list = soup.find_all('td')
        count = 0
        temp_item = ""
        final_item = ""
        for item in bank_list:
            temp_item = temp_item + "--" + item.get_text()
            final_item = final_item + temp_item + "\n"
            temp_item = ""
        #tag = "銀行"
        #for drink in soup.select('{}'.format(tag)):
        #    print(drink.get_text())
        update.message.reply_text(final_item)
        update.message.reply_text("服務項目(輸入文字)：\n查詢銀行代碼(代碼)\n查詢各銀行利率(定存)\n查詢各銀行信貸利息(信貸)\n查詢股市(股市)\n詐騙幫助(詐騙)\n")
        self.go_back(update)

    def on_exit_5(self, update):
        print('Leaving 5')

    def on_enter_4(self, update):
        update.message.reply_photo("http://pic.pimg.tw/pali0621/1186583189.jpg")
        update.message.reply_photo("http://img.pcstore.com.tw/~prod/M10478352_big.jpg?pimg=static&P=1330673208")
        #instance = vlc.Instance()
        #player = instance.media_player_new()
        #media = instance.media_new('/home/user/Desktop/TOC-Project-2017/DUN DUN DUUUUN!!! (Dramatic Sound Effect).mp3')
        #player.set_media(media)
        #player.play()
        update.message.reply_text("服務項目(輸入文字)：\n查詢銀行代碼(代碼)\n查詢各銀行利率(定存)\n查詢各銀行信貸利息(信貸)\n查詢股市(股市)\n詐騙幫助(詐騙)\n")
        self.go_back(update)

    def on_exit_4(self, update):
        print('Leaving 4')
