from django.shortcuts import render
from paho.mqtt import client as mqtt_client
from .models import House, Apartment, Intercom
from django.shortcuts import get_object_or_404, redirect
from asyncio import SelectorEventLoop
from concurrent.futures import ThreadPoolExecutor
import uuid
import json
from django.forms.models import model_to_dict


loop = SelectorEventLoop()
executor = ThreadPoolExecutor()

# broker = 'broker.emqx.io'
# broker = 'test.mosquitto.org'
# port = 1883
# topic = "python/mqtt"
# client_id = f'python-mqtt-{uuid.uuid4()}'

# # username = 'emqx'
# # password = 'public'
# username = 'mosquitto'
# password = '123'

broker_address = 'm4.wqtt.ru'
port = 13408
client_id = f'python-mqtt-{uuid.uuid4()}'
username = 'u_FAVYQ5'
password = 'Fa3sAjwH'


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
    # has_called = False
    call_apartment = None

    intercom = get_object_or_404(Intercom, pk=pk)
    if request.method == "POST":
        if request.POST.get("open_button"):
            return 
        button = request.POST.get("button")
        client.publish(f"buttons", button)
        if button == "call":
            apartments = Apartment.objects.filter(house=intercom.house)
            apartment_number = apartment_number.lstrip("0")
            for apartment in apartments:
                if str(apartment.number) == apartment_number:
                    call_apartment = apartment
                    break
            apartment_number = ""
            if not call_apartment:
                print("Неправильно набран номер")
                # return redirect("intercom:call")
        elif button == "del":
            apartment_number = ""
        else:
            apartment_number += button
    intercom_dict = model_to_dict(intercom)
    message = {
        "id": str(uuid.uuid4()),
        "intercom_id": intercom.id,
        "intercom": intercom_dict,
    }
    message = json.dumps(message, default=str)
    client.publish("buttons", message)

    if apartment_number.isnumeric():
        intercom_message = apartment_number
    elif call_apartment:
        intercom_message = "ИДЕТ ЗВОНОК"
    elif not call_apartment and apartment_number == "":
        intercom_message = "ДОМОФОН"


    context = {
        "intercom": intercom,
        "is_open": False,
        "house": intercom.house,
        "intercom_message": intercom_message,
        "apartments": Apartment.objects.filter(house=intercom.house)
    }
    return render(request, "intercom.html", context)


def open(request):
    client.publish("call", )
    return render(request, "open.html")


def call(request):
    context = {}
    return render(request, "call.html", context)