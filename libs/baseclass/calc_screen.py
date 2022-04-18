from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton

from kivy.storage.jsonstore import JsonStore
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import re
import math

class CalcScreen(ThemableBehavior, MDBoxLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super(CalcScreen, self).__init__(**kwargs)
        # setup some global varables 
        self.usd_owed = 0.00
        self.gb_owed = 0.0
        self.gb_paid = 0.0
        self.exchange_rate = self.update_exchange() # Eventually this needs to be pulled from the web
        self.cus_owes_add = 0.00
        self.pay_cus_change = 0.0
        
    def calculate(self, instance):

        # Update Variables
       
        self.usd_owed = float(self.usd_owed_inTI.text)
        self.exchange_rate = float(self.gb_exchange_rateTI.text)
        self.gb_paid = float(self.num_gb_paidTI.text)

        # if the exchage rate $3.92 and you owe $10
        # 10/3.92 = 2.5510204082 GB
        # There is no change so we need to roung up to the nearest GB. However we need to keep
        # This number to calculate wheather change needs to be given or more 

        # get the raw amount of gold backs needed       
        raw_gb_owed = self.usd_owed /self.exchange_rate
        self.num_gb_owedLV.text = str(int(math.ceil(raw_gb_owed))) # always rounds up!

        #Find the $USD amount paid in gold backs!
        usd_amount_gb = self.gb_paid * self.exchange_rate 

        # Need to calcuate if change is need or if the customer needs to pay more.
        if usd_amount_gb  < self.usd_owed:
            resualts = self.usd_owed - usd_amount_gb
            self.pay_cus_changeLV.text = "0"
            self.cus_owes_addLV.text = str(round(resualts, 2))
           
        elif usd_amount_gb > self.usd_owed:
            resualts = usd_amount_gb - self.usd_owed
            self.pay_cus_changeLV.text = str(round(resualts, 2))
            self.cus_owes_addLV.text = "0"

        elif usd_amount_gb == self.usd_owed:
            # IF the amount of goldbacks owed is equal to the dollar amount then 
            # there is no change or additonal money the customer has to give.
            self.pay_cus_changeLV.text = "0"
            self.cus_owes_addLV.text = "0"  

    def update_exchange(self):
        # https://kivy.org/doc/stable/api-kivy.storage.html
        # setup database
        store = JsonStore('Goldback.json')
        
        try:
            # This gets the html of goldback to parse for the exchange rate.
            url = "https://www.goldback.com"
            result = requests.get(url)
            
            # setup are html parser
            doc = BeautifulSoup(result.text, "html.parser")
            
            # search for the text before exchange rate
            rexch = doc.find_all('div', {"class": "image-title sqs-dynamic-text"})
             
            exch = re.findall("\d+\.\d+", str(rexch))  
        
            # store value for use if offline
            store.put('exchage', value=exch[0])
             
            return exch[0]  

        except ConnectionError:
            print("Can't reach GoldBack.com!")
            return 0
            # This feature can come at a later date. For now it will defualt to zero.
            #if store.exists('exchange'):
            #    print('tite exists:', store.get('exchange'))
            #    exch = store.get('exchange')['value']
            #    return exch
