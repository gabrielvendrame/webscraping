import bs4
from urllib.request import urlopen as uReq
import html5lib
from bs4 import BeautifulSoup
import time
import re
import json

class SiteToVisit:
    '''
    Class definition:
        site :          {}
        url :           {}
        renderer :      {}
        page_content :  {}
        Data:
            cont :          {}
            name :          {}
            link :          {}
            img :           {}
            price :         {}
        products_data : {}

        Data Structure:
            " 5s ":         [],
            " se ":         [],
            " 6 " :         [],
            " 6 plus " :    [],
            " 6s " :        [],
            " 6s plus " :   [],
            " 7 " :         [],
            " 7 plus " :    [],
            " 8 " :         [],
            " 8 plus " :    [],
            " x " :         [],
            " xs " :        [],
            " xs max " :    [],
            " xr " :        []
        '''
    #Constructor
    def __init__(self, site, url, renderer, product_path):
        self.site = site
        self.url = url
        self.renderer = renderer
        self.page_content = None
        self.products_data = []
        self.products_path = product_path
        with open('iphone_type.json', 'r') as input_file:
                self.iphone_type=json.load(input_file)
         

    #Load Mothods
    '''
    This method loads all the data and stores it into
    PRODUCT DATA variable
    '''
    def load_products_data(self):
        #Container estrapolation
        all_cont = self.page_content.find_all(self.products_path["cont"]["container"],
                                                self.products_path["cont"]["name"])

        index = 0
        for i in all_cont:
            content = []
            
            for j in self.products_path:
                #Not a container
                if j != "cont":
                    if j == "link":
                            link = i.find(self.products_path[j]["container"],
                                    self.products_path[j]["name"], href = True)
                            try:
                                link = link["href"]
                                content.append(link)
                            except TypeError:
                                break;
                    else:
                        info = i.find(self.products_path[j]["container"],
                                        self.products_path[j]["name"])
                        if info != None:
                            #Product name
                            info = info.getText(strip=True)

                            #Parse Price data
                            if j == "price":
                                info = self.get_number_part(info)
                            content.append(info)
                            #Get link
                        
            if len(content) != 0:
                self.products_data.append(content)
        
 
        #loading json
        for i in self.iphone_type:
            for j in self.products_data:
                regex = re.compile(i)
                response = regex.search(j[0].lower())
                if response != None:
                    self.iphone_type[i].append(j)
        #Sort array
        self.order_iphone_type()


    #Load page content
    def load_page_site(self):
        if self.renderer == "selenium":
            from selenium import webdriver
            import os
            chromedriver = "./chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
            url = self.url
            driver.get(url)
            driver.find_element_by_css_selector("button.btn.btn-default.exclusive-medium").click()
            time.sleep(10)
            page_response = driver.page_source
            driver.close()
        elif self.renderer == "none":
            page = uReq(self.url)
            page_response = page.read()
            page.close()
        
        page_content = BeautifulSoup(page_response, "html5lib")
        self.page_content = page_content


    #Get number part
    '''
    From string to float
    '''
    def get_number_part(self, string):
        ret = ""
        for i in string:
            if(i in "1234567890"):
                ret += i
        return float(ret) / 100

    #Order Methods
    def order_iphone_type(self):
        for i in self.iphone_type:
            self.iphone_type[i].sort(key = lambda x: x[2],reverse = False)

    #ToString
    def __str__(self):
        ret = ""
        for i in self.iphone_type:
            ret += i + ":\n"
            for j in self.iphone_type[i]:
                ret += str(j[0])+ "  "+str(j[1])+"  "+str(j[2])+"\n"
        return ret