#to avoid ssl issue
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

#Code
import json
import time
from visiter import SiteToVisit
import datetime


#Create product path
def create_product_path( product_path):
    ret = {}
    for i in product_path:
        variable = i["variable"]
        container = i["container"]
        name = i["name"]
        ret[variable] = {"container" : container, "name" : name}
    return ret

#Load json file and save objects
def create_objects_from_json_file(path):
    SiteToVisitList = []
    with open(file=path,mode='r') as file_handler:
        #print(file_handler)
        obj_handler = json.load(file_handler)
        for i in obj_handler:
            site = i["site"]
            url  = i["url"]
            renderer = i["renderer"]
            estract_data_info = i["estract_data_info"]
            product_path = create_product_path(estract_data_info)
            exo_site = SiteToVisit(site = site, url = url, renderer = renderer, product_path = product_path)
            SiteToVisitList.append(exo_site)
    return SiteToVisitList

#Main Code
if __name__ == "__main__":
    while True:

        #Join results and prepare for Json
        site_to_insert=[]
        data_to_insert=[]
        dictionary={}
        
        SiteToVisitList = create_objects_from_json_file("./site_data.json")
        for i in SiteToVisitList:
            try:
                i.load_page_site()
                i.load_products_data()
                site_to_insert.append(i.site)
                data_to_insert.append(i.iphone_type)
                print(datetime.datetime.now(), "Fatto", i.site)
            except Exception:
                print("Errore generico (probabile connessione lenta)")

                continue
           
            

        y=0    
        for x in site_to_insert:
            dictionary[x]=data_to_insert[y]
            y=y+1
        #In this way every time should overwrite the file
        with open('prices1.json', 'w') as outfile:
            json.dump(dictionary, outfile)
        print(datetime.datetime.now(), "JSON Aggiornato")
        #Runs every 3 hours 
        time.sleep(10800)