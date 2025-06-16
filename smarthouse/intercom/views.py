from django.shortcuts import render
import random
from paho.mqtt import client as mqtt_client
import time
from .models import House, Apartment, Intercom
from django.shortcuts import get_object_or_404
from asyncio import SelectorEventLoop
from concurrent.futures import ThreadPoolExecutor
import uuid
import json
from django.forms.models import model_to_dict


loop = SelectorEventLoop()
executor = ThreadPoolExecutor()

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

username = 'emqx'
password = 'public'


def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt():
    client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2, client_id=client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port, keepalive=10)
    return client


client = connect_mqtt()
client.loop_start()

def publish(client: mqtt_client.Client):
    msg_count = 0
    while True:
        # await asyncio.sleep(3)
        time.sleep(3)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def index(request):
    # client.publish(topic, "hello")
    # publish(client)
    # task = asyncio.create_task(publish)
    # asyncio.run(task(client))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(task)
    # await loop.run_in_executor(executor, client.publish, topic, "hello")
    context = {
        "intercoms": Intercom.objects.all()
        }
    return render(request, "index.html", context)


def intercom(request, pk):
    intercom = get_object_or_404(Intercom, pk=pk)
    intercom_dict = model_to_dict(intercom)
    message = {
        "id": str(uuid.uuid4()),
        "intercom_id": intercom.id,
        "intercom": intercom_dict,
    }
    message = json.dumps(message, default=str)
    client.publish(topic, message)
    context = {
        "intercom": intercom,
        "house": intercom.house,
        "apartments": Apartment.objects.filter(house=intercom.house)
    }
    return render(request, "intercom.html", context)


def open(request):
    context = {}
    return render(request, "open.html", context)


def call(request):
    context = {}
    return render(request, "call.html", context)