#!/usr/bin/env python3

from hermes_python.hermes import Hermes, MqttOptions
import datetime
import random
import toml


USERNAME_INTENTS = "anga97"
MQTT_BROKER_ADDRESS = "localhost:1883"
MQTT_USERNAME = None
MQTT_PASSWORD = None


def user_intent(intentname):
    return USERNAME_INTENTS + ":" + intentname


def subscribe_intent_callback(hermes, intent_message):
    intentname = intent_message.intent.intent_name

    if intentname == user_intent("UniversityName"):
        result_sentence = "Die Hochschule heißt TH-Nürnberg"
        current_session_id = intent_message.session_id
        hermes.publish_end_session(current_session_id, result_sentence)

    elif intentname == user_intent("SnipsHello"):
        result_sentence = "Hallo ich bin Snips. Ich bin eine Anwendung, welche die Steuerung von Systemen über Spracheingaben ermöglicht. Im Bild links oben sehen sie den Mikrocontroller auf dem ich derzeit installiert bin. Links unten finden sie eine Beschreibung des Aufbaus des Linux Systems auf dem ich laufe. Rechts oben finden sie die geparste Spracheingabe und mit welcher Sicherheit ich die Eingabe verstanden habe. Ich wünsche noch einen schönen Tag."
        current_session_id = intent_message.session_id
        hermes.publish_end_session(current_session_id, result_sentence)

    elif intentname == user_intent("Sender"):
        result_sentence = "Diese Funktion ist noch nicht vorhanden, wird aber bald hinzugefügt."
        radiosender = intent_message.slots.radiosender.first().value
        result_sentence = "Stelle den Sender {radiosender} ein"
        current_session_id = intent_message.session_id
        hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    snips_config = toml.load('/etc/snips.toml')
    if 'mqtt' in snips_config['snips-common'].keys():
        MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
    if 'mqtt_username' in snips_config['snips-common'].keys():
        MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
    if 'mqtt_password' in snips_config['snips-common'].keys():
        MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']

    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intents(subscribe_intent_callback).start()
