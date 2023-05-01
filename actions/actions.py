# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
import sqlite3
#import speech_recognition as sr
#from translate import Translator
#
#
class ActionGuardarNombre(Action):
    def name(self) -> Text:
        return "action_guardar_nombre"
    
    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       print(tracker.get_slot('nombre'))
       return [SlotSet('nombre',tracker.latest_message['text'])]
   
class ActionGuardarDocumento(Action):
    def name(self) -> Text:
        return "action_guardar_documento"
    
    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       print(tracker.get_slot('documento'))
       return [SlotSet('documento',tracker.latest_message['text'])]

def datastore(nombre, nu_documento):
    conn=sqlite3.connect('Scott.db')
    mycursor = conn.cursor()
    mycursor.execute("""CREATE TABLE IF NOT EXISTS user_scott (Name TEXT, nu_documento TEXT);""")
    mycursor.execute("INSERT INTO my_info VALUES (?,?)",(nombre, nu_documento))
    conn.commit()
    print(mycursor.rowcount,"registros insertados")
    

class ActionStore(Action):
    def name(self) -> Text:
        return "action_store"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        x=tracker.get_slot('nombre')
        y=tracker.get_slot('documento')
        datastore(x,y)
        dispatcher.utter_message("Gracias! La información fue guardada!.")
        print(x)
        print(y)
        return []