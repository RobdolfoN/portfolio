import paho.mqtt.client as mqtt
import json
import django
import os
import time
from datetime import datetime
from django.core.management.base import BaseCommand
from portfolioapp.models import Flight

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')
django.setup()

class Command(BaseCommand):
    help = 'Runs the MQTT client to subscribe to OpenSky data'

    def handle(self, *args, **kwargs):
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))
            client.subscribe("opensky/#")

        def on_message(client, userdata, msg):
            try:
                payload = json.loads(msg.payload.decode('utf-8'))
                self.process_flight_data(payload)
            except Exception as e:
                print(f"Error decoding message: {e}")

        def process_flight_data(self, data):
            icao24 = data.get('icao24')
            callsign = data.get('callsign', '').strip()
            on_ground = data.get('on_ground', False)
            time_position = data.get('time_position', 0)
            airline = callsign[:3]  # Assuming first 3 characters of callsign represent the airline

            if on_ground:
                actual_arrival = datetime.fromtimestamp(time_position)
                flight = Flight.objects.filter(icao24=icao24, status__isnull=True).first()
                if flight:
                    expected_arrival = flight.expected_arrival
                    status = 'on_time' if actual_arrival <= expected_arrival else 'delayed'
                    flight.actual_arrival = actual_arrival
                    flight.status = status
                    flight.save()
                    print(f"Flight {callsign} ({icao24}) arrived {'on time' if status == 'on_time' else 'delayed'}.")

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("mqtt.opensky-network.org", 1883, 60)
        client.loop_forever()
