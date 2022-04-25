# Author: Dakota James Owen keeler
# Email:  DakotaJKeeler@protonmail.com
# Purpose: The aim of this application is to make it easier to spend and use goldback. 

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.



import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore
from kivy.base import runTouchApp

from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import re
import math


# I never want to write the word self again.............. :(

class AboutGBWindow():
    def __init__(self, **kwargs):
        super(AboutGBWindow, self).__init__(**kwargs)

class HowToSpend():
    def __init__(self, **kwargs):
        super(HowToSpend, self).__init__(**kwargs)

class FeaturedBusinss():
    def __init__(self, **kwargs):
        super(FeaturedBusinss, self).__init__(**kwargs)

class AboutApp():
    def __init__(self, **kwargs):
        super(AboutApp, self).__init__(**kwargs)
        
        Window.clearcolor = (1,1,1,1)
        self.cols = 1

        self.test = Label(text="This is a test")
        self.add_widget(self.test)



class Calc(GridLayout):
    def __init__(self, **kwargs):
        super(Calc, self).__init__(**kwargs)
        self.cols = 1
        Window.clearcolor = (1, 1, 1, 1) # Change background color

        # setup some global varables 
        self.usd_owed = 0.00
        self.gb_owed = 0.0
        self.gb_paid = 0.0
        self.exchange_rate = self.update_exchange() # Eventually this needs to be pulled from the web
        self.cus_owes_add = 0.00
        self.pay_cus_change = 0.0

        self.titleL = Label(text="Goldback Transaction Calculator",  color=[0, 0, 0, 1])
        self.add_widget(self.titleL)

        self.usd_owedL = Label(text="Amount Owed in $USD",  color=[0, 0, 0, 1])
        self.usd_owed_inTI = TextInput(multiline=False, text=str(self.usd_owed))
        self.add_widget(self.usd_owedL)
        self.add_widget(self.usd_owed_inTI)

        self.gb_exchange_rateL = Label(text="Goldback Exchange Rate",  color=[0, 0, 0, 1])
        self.gb_exchange_rateTI = TextInput(multiline=False, text=str(self.exchange_rate))
        self.add_widget(self.gb_exchange_rateL)
        self.add_widget(self.gb_exchange_rateTI)

        self.num_gb_owedL = Label(text="Number of Goldbacks Owed",  color=[0, 0, 0, 1])
        self.num_gb_owedLV = Label(text=str(self.gb_owed),  color=[0, 0, 0, 1])
        self.add_widget(self.num_gb_owedL)
        self.add_widget(self.num_gb_owedLV)

        self.num_gb_paidL = Label(text="Goldbacks Paid By The Customer",  color=[0, 0, 0, 1])
        self.num_gb_paidTI = TextInput(multiline=False, text=str(self.gb_owed))
        self.add_widget(self.num_gb_paidL)
        self.add_widget(self.num_gb_paidTI)

        self.cus_owes_addL = Label(text="Customer Owes You an Additional",  color=[0, 0, 0, 1])
        self.cus_owes_addLV = Label(text=str(self.cus_owes_add),  color=[0, 0, 0, 1])
        self.add_widget(self.cus_owes_addL)
        self.add_widget(self.cus_owes_addLV)

        self.pay_cus_changeL = Label(text="Pay The Customer This in Change",  color=[0, 0, 0, 1])
        self.pay_cus_changeLV = Label(text=str(self.pay_cus_change),  color=[0, 0, 0, 1])
        self.add_widget(self.pay_cus_changeL)
        self.add_widget(self.pay_cus_changeLV)


        self.calc_bt = Button(text="Calculate")
        self.calc_bt.bind(on_press=self.calculate)
        self.add_widget(self.calc_bt)

        self.noticeL = Label(text="GOLDBACK EXCHANGE RATE CAN BE MANUALLY ADJUSTED.",  color=[0, 0, 0, 1])
        self.add_widget(self.noticeL)
     

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
            

    
        

        #gb_exchange_rate = 0.0
        
class GoldBack(App):
    def build(self):
        return Calc() 

         

if __name__ == "__main__":
    runTouchApp(GoldBack().run())
