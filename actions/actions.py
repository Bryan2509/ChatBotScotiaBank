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

import pandas as pd
import openpyxl 
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
       dispatcher.utter_message(response = "utter_como_te_ayudo")
       return [SlotSet('nombre',tracker.latest_message['text'])]

def datastore(nombre):
    conn=sqlite3.connect('Scott.db')
    mycursor = conn.cursor()
    mycursor.execute("""CREATE TABLE IF NOT EXISTS user_scott (Name TEXT, nu_documento TEXT);""")
    mycursor.execute("INSERT INTO my_info VALUES (?)",(nombre))
    conn.commit()
    print(mycursor.rowcount,"registros insertados")
    

class ActionStore(Action):
    def name(self) -> Text:
        return "action_store"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        x=tracker.get_slot('nombre')
        datastore(x)
        dispatcher.utter_message("Gracias! La información fue guardada!.")
        print(x)
        return []
    
class dar_info_producto(Action):
    
    def name(self) -> Text:
        return "action_dar_info_producto"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dfhoja1 = pd.read_excel("BBDD Scotiabank.xlsx", engine='openpyxl', sheet_name='Hoja 1')
        dfhoja2 = pd.read_excel("BBDD Scotiabank.xlsx", engine='openpyxl', sheet_name='Hoja 2')
        
        x = tracker.get_slot('concepto')
        
        df = dfhoja1[dfhoja1['Concepto'].str.lower() == x]['Descripcion']
        if df.empty:
            df = dfhoja2[dfhoja2['Concepto'].str.lower() == x]['Descripcion']
        
        df = dict(df)
        print(df)
        dispatcher.utter_elements(elements = Dict[df['Description'], Any])
        
        return df