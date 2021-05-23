import random
import requests                     #requests==2.22.0
from flask import Flask, request    #Flask==1.1.1
import os

app = Flask(__name__)
exec(open('./img_url.py').read())  #your full url

ACCESS_TOKEN = ''    #your access token
VERIFY_TOKEN = ''   #your verify token



def respond(recipient_id, type_respond, payload):
    if type_respond == 'template_button':    
        body = {
            'recipient': {
                'id': recipient_id
            },
            "message":{
                "attachment":{
                    "type":"template",
                    "payload": payload
                }
            }
        }
                
    elif (type_respond == 'quick_replies' or type_respond == 'text'):    
        body = {
           'messaging_type': 'RESPONSE',
            'recipient': {
                'id': recipient_id
            },
            'message': payload
        }
        
    response = requests.post(
        'https://graph.facebook.com/v5.0/me/messages?access_token='+ACCESS_TOKEN,
        json=body
    )

    return response.json()


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


@app.route("/", methods=['GET'])
def verify_message():
    token_sent = request.args.get("hub.verify_token")
    return verify_fb_token(token_sent)


@app.route("/", methods=['POST'])
def handle_webhook():
    output = request.get_json()
    data = output['entry'][0]['messaging'][0]
    sender_id = data['sender']['id']
    message = data['message']
    #print(message.get('text').lower())
    
    if 'start' in message.get('text').lower():
        respond(sender_id, type_respond = 'quick_replies', payload = {
            'text': 'Jakie dane chcesz zobaczyć?', 
            'quick_replies': [
                {
                    "content_type": "text",
                    "title": "ENERGIA",
                    "payload": "button-E",
                },
                {
                    "content_type": "text",
                    "title": "GAZ",
                    "payload": "button-G",
                },
                {
                    "content_type": "text",
                    "title": "INNE",
                    "payload": "button-I",
                }
            ]});  
    
    elif 'inne' in message.get('text').lower():
        respond(sender_id, type_respond = 'quick_replies', payload = {
            'text': 'Wybierz dane', 
            'quick_replies': [
                {
                    "content_type": "text",
                    "title": "PRAWA MAJĄTKOWE",
                    "payload": "button-PM",
                }, 
                {
                    "content_type": "text",
                    "title": "WĘGIEL",
                    "payload": "button-W",
                },
                {
                    "content_type": "text",
                    "title": "FARMY WIATROWE",
                    "payload": "button-FW",
                }
            ]}); 
       
    elif 'energia' in message.get('text').lower():
        respond(sender_id, type_respond = 'template_button', payload = {
            "template_type":"generic",
            "elements": [
                {
                    "title":"ENERGIA",
                    "image_url": img_energy,
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://tge.pl/",
                            "title": "Giełda Energii"
                        },
                        {
                            "type": "web_url",
                            "url": "https://www.pse.pl/obszary-dzialalnosci/rynek-energii/ceny-i-ilosc-energii-na-rynku-bilansujacym/",
                            "title": "Rynek Bilansujący"
                        },
                        {
                            "type": "web_url",
                            "url": "https://www.pse.pl/obszary-dzialalnosci/krajowy-system-elektroenergetyczny/zapotrzebowanie-kse",
                            "title": "Zapotrzebowanie KSE"
                        },
#                        {
#                            "type": "web_url",
#                            "url": "https://www.pse.pl/dane-systemowe/funkcjonowanie-kse/raporty-dobowe-z-pracy-kse/wymiana-miedzysystemowa-przeplywy-mocy",
#                            "title": "Import/Export"
#                        },                       
                    ]
                },
            ]
        });         

        
    elif 'gaz' in message.get('text').lower():
        respond(sender_id, type_respond = 'template_button', payload = {
            "template_type":"generic",
            "elements": [
                {
                    "title":"GAZ",
                    "image_url": img_gas,
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://tge.pl/",
                            "title": "Giełda Gazu"
                        },
                        {
                            "type": "web_url",
                            "url": "https://swi.gaz-system.pl/swi/public/#!/ksp/actualQuantity?lang=pl",
                            "title": "Ilość przesłanego gazu"
                        },
                        {
                            "type": "web_url",
                            "url": "https://ipi.gasstoragepoland.pl/pl/menu/transparency-template/?page=dane-operacyjne/dane-operacyjne/",
                            "title": "Napełnienie magazynów"
                        }
                    ]
                },
            ]    
        });         
    
    
    elif ('prawa majątkowe' in message.get('text').lower() or 'prawa majatkowe' in message.get('text').lower() or 'certyfikat' in message.get('text').lower()):
        respond(sender_id, type_respond = 'template_button', payload = {
            "template_type":"generic",
            "elements":[
                {
                    "title":"PRAWA MAJĄTKOWE",
                    "image_url": img_property_rights,
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://tge.pl/",
                            "title": "TGE"
                        }
                    ]
                },
            ]    
        });   
        
        
    elif ('węgiel' in message.get('text').lower() or 'wegiel' in message.get('text').lower()):
        respond(sender_id, type_respond = 'template_button', payload = {
            "template_type":"generic",
            "elements": [
                {
                    "title": "WĘGIEL",
                    "image_url": img_coal,
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://polskirynekwegla.pl/indeks-pscmi-1",
                            "title": "Indeks PSCMI 1"
                        },
                        {
                            "type": "web_url",
                            "url": "https://polskirynekwegla.pl/indeks-pscmi-2",
                            "title": "Indeks PSCMI 2"
                        }
                    ]
                },
            ]    
        });
        
        
    elif 'wiatr' in message.get('text').lower():
        respond(sender_id, type_respond = 'template_button', payload = {
            "template_type":"generic",
            "elements": [
                {
                    "title":"FARMY WIATROWE",
                    "image_url": img_wind,
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://www.pse.pl/dane-systemowe/funkcjonowanie-kse/raporty-dobowe-z-pracy-kse/generacja-zrodel-wiatrowych",
                            "title": "Generacja energii"
                        }  
                    ]
                },
            ]    
        }); 
        

    elif ('zakończ' in message.get('text').lower() or 'zakoncz' in message.get('text').lower()):
        respond(sender_id, type_respond = 'text', payload = {
            'text': 'Dzięki, że byłeś/aś z nami. \nDo zobaczenia ;)'
        });
        

    else:
        respond(sender_id, type_respond = 'quick_replies', payload = {
            'text': 'Wybierz "START", aby rozpocząć. \nWybierz "ZAKOŃCZ", aby zakończyć.', 
            'quick_replies': [
                {
                    "content_type": "text",
                    "title": "START",
                    "payload": "button-start",
                }, {
                    "content_type": "text",
                    "title": "ZAKOŃCZ",
                    "payload": "button-end",
                }
            ]});
        
    #print(message)
    #print(message.get('text').lower())
    return 'ok'


if __name__ == "__main__":
    app.run()

