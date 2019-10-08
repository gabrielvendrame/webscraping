import telepot
from telepot.loop import MessageLoop
import time 

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
import json
from visiter import SiteToVisit
import operator

def handle(msg):
    content_type, chat_type, chat_id  = telepot.glance(msg)
    
    iPhone_names =[
        'iPhone 5s',
        'iPhone SE',
        'iPhone 6',
        'iPhone 6 Plus',
        'iPhone 6s',
        'iPhone 6s Plus',
        'iPhone 7',
        'iPhone 7 Plus',
        'iPhone 8',
        'iPhone 8 Plus',
        'iPhone X',
        'iPhone XS',
        'iPhone XS Max',
        'iPhone XR'
    ]
    
    # username = msg['from']['username']
    
    # user_id = msg['from']['id']
    
    if content_type == 'text':
        text = msg['text']


        if text == '/searchprices':
            menu= []
            index = 0
            line = []
            for  i in range(0,len(iPhone_names)): 
                if index < 1:
                    line.append(KeyboardButton(text = iPhone_names[i]))
                    index += 1
                elif index == 1:
                    index += 1
                    line.append(KeyboardButton(text = iPhone_names[i]))
                    menu.append(line)
                    index = 0
                    line = []


            bot.sendMessage(chat_id, 'Scegli un modello',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=menu,
                                one_time_keyboard=True
                            ))


        if text== '/keepmeupdated':
            keyboard =  [[InlineKeyboardButton(text="Option 1")]]
                        
                

            bot.sendMessage(chat_id, 'Funzione in fase di sviluppo',
                            
                            reply_markup=InlineKeyboardMarkup(
                                InlineKeyboard=[[InlineKeyboardButton(text="ciao", callback_data='press')],
                                ])
                            )
                                              



        if text in iPhone_names :
            
            print("Cercato",text)

            with open('prices1.json', 'r') as input_file:
                j_data=json.load(input_file)
            with open('iPhone_type.json', 'r') as config_file:
                j_config=json.load(config_file)

            #dichiarazione variabili
            to_search=iPhone_names.index(text)
            right_search=list(j_config.keys())[to_search]
            reply_to_send=""
            global_title=[]
            global_price=[]
            global_link=[]
            indexes= sorted(range(len(global_price)), key=lambda k: global_price[k])
            
            #global_order={"Titles": [], "Links": [], "Prices": []} 


            for i in j_data:

                max=0
                for j in range(len(j_data[i][right_search])):
                    if max>=2:
                        break 
                    global_title.append(j_data[i][right_search][j][0])
                    global_link.append(j_data[i][right_search][j][1])
                    global_price.append(str(j_data[i][right_search][j][2]))
                    max+=1
            
            #Qui viene creata la Tupla contenente le varie liste
            global_order=list(map(lambda x, y,z:(x,y,z), global_title, global_price, global_link)) 

            #Qui viene ordinata la Tupla (Global order) contenente le liste
            size= lambda global_order:global_order[1]
            global_order.sort(key=size)
            print(global_title)


            # global_order["Titles"].append(global_title)
            # global_order["Links"].append(global_link)
            # global_order["Prices"].append(global_price)
            ########### Il problema è qui #############
           
            
           
            #Ordina per prezzo
            #sorted_global_order= sorted(global_order.items(), key=operator.itemgetter(1))
            #Non ordina in modo corretto, crea una lista noi vogliamo il dizionario forse
            
            
            
            

            for title,price,link in global_order: 
                title_to_send= (title)
                
                price_to_send= ("<b>"+str(price)+"€</b>")
                
                link_to_send=(link)
                
                reply_to_send+=("📱 "+title_to_send+ "\n"+ "💶 "+price_to_send+"   ")
                reply_to_send+=("<a href='"+link+"'>"+"Link"+"</a>"+"\n\n")
                reply_to_send+=("--------------------\n")



            bot.sendMessage(chat_id, reply_to_send,
                            disable_web_page_preview=True,
                            parse_mode='HTML',
                            reply_markup=ReplyKeyboardRemove()                            
                            )           
                




    
TOKEN = 'YOUR TOKEN HERE'
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)