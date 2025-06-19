from django.shortcuts import render
from paho.mqtt import client as mqtt_client
from .models import House, Apartment, Intercom
from django.shortcuts import get_object_or_404
import uuid
import json
from django.forms.models import model_to_dict


def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt():
    client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2, client_id=client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker_address, port, keepalive=10)
    return client


broker_address = 'm4.wqtt.ru'
port = 13408
client_id = f'python-mqtt-{uuid.uuid4()}'
username = 'u_FAVYQ5'
password = 'Fa3sAjwH'
client = connect_mqtt()
client.loop_start()


def index(request):
    context = {
        "intercoms": Intercom.objects.all()
        }
    return render(request, "index.html", context)

apartment_number = ""

def intercom(request, pk):
    global apartment_number
    call_apartment = None
    is_open = False
    intercom_message = "ДОМОФОН"
    intercom = get_object_or_404(Intercom, pk=pk)
    if request.method == "POST":
        button = request.POST.get("button")
        if button == "call":
            apartments = Apartment.objects.filter(house=intercom.house)
            apartment_number = apartment_number.lstrip("0")

            for apartment in apartments:
                if str(apartment.number) == apartment_number:
                    call_apartment = apartment
                    break

            apartment_number = ""
        elif button == "del" or button == "open":
            apartment_number = ""
        else:
            apartment_number += button

        intercom_dict = model_to_dict(intercom)
        message = {
            "id": str(uuid.uuid4()),
            "intercom": intercom_dict,
            "button": button,
        }
    
        if button == "call":
            message["apartment"] = apartment
    
        message = json.dumps(message, default=str)

        if button == "call":
            client.publish("call", message)
        elif button.isnumeric():
            client.publish("buttons", message)
        elif button == "open":
            client.publish("open", message)

        if apartment_number.isnumeric():
            intercom_message = apartment_number
        elif call_apartment:
            intercom_message = "ИДЕТ ЗВОНОК"
        elif not call_apartment and apartment_number == "" and button == "call":
            intercom_message = "ВХОД ЗАПРЕЩЕН"
        elif button == "open":
            intercom_message = "ИДЕТ ОТКРЫТИЕ"
            is_open = True
        
        if len(apartment_number) > 4:
            apartment_number = ""
            intercom_message = "ВХОД ЗАПРЕЩЕН" 
    
    if request.method == "GET":
        apartment_number = ""

    context = {
        "intercom": intercom,
        "is_open": is_open,
        "house": intercom.house,
        "intercom_message": intercom_message,
        "apartments": Apartment.objects.filter(house=intercom.house)
    }

    return render(request, "intercom.html", context) 