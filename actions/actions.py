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

#GUARDA EL NOMBRE PARA PODER ALMACENARLO EN LA BASE DE DATOS
class ActionGuardarNombre(Action):
    def name(self) -> Text:
        return "action_guardar_nombre"
    
    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       print(tracker.get_slot('nombre'))
       dispatcher.utter_message(response = "utter_como_te_ayudo")
       return [SlotSet('nombre',tracker.latest_message['text'])]
   
#GUARDA EL PRODUCTO PARA PODER GUARDARLO EN LA BASE DE DATOS
class ActionGuardarProducto(Action):
    def name(self) -> Text:
        return "action_guardar_producto"
    
    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       print(tracker.get_slot('producto'))
       dispatcher.utter_message(response = "action_dar_info_producto")
       return [SlotSet('producto',tracker.latest_message['text'])]

#GUARDA EL CONCEPTO PARA PODER GUARDARLO EN LA BASE DE DATOS
class ActionGuardarConcepto(Action):
    def name(self) -> Text:
        return "action_guardar_concepto"
    
    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       print(tracker.get_slot('concepto'))
       dispatcher.utter_message(response = "action_dar_info_concepto")
       return [SlotSet('concepto',tracker.latest_message['text'])]
   
#JUANCITO LO VA A VER 
def datastore(nombre, producto, concepto):
    conn=sqlite3.connect('chatbotScott')
    mycursor = conn.cursor()
    mycursor.execute("INSERT INTO USERS_SCOTT VALUES (?,?,?)",(nombre, producto, concepto))
    conn.commit()
    print(mycursor.rowcount,"registros insertados")
    

class ActionStore(Action):
    def name(self) -> Text:
        return "action_store"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        nombre=tracker.get_slot('nombre')
        producto=tracker.get_slot('producto')
        concepto=tracker.get_slot('concepto')
        
        datastore(nombre, producto, concepto)
#        dispatcher.utter_message("Gracias! La información fue guardada!.")
        print(nombre, producto, concepto)
        return []
    
class dar_info_producto(Action):
    
    def name(self) -> Text:
        return "action_dar_info_producto"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = pd.read_excel("BBDD Scotiabank.xlsx", engine='openpyxl', sheet_name='Productos')
        x = tracker.get_slot('producto')
        df = df[df['Concepto'].str.lower() == str.lower(x)]['Descripcion']
        print(df)

        #df = dict(df)
        #dispatcher.utter_custom_message(elements = df)
        return {'descripcion' : df}
    
class dar_info_concepto(Action):
    
    def name(self) -> Text:
        return "action_dar_info_concepto"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = pd.read_excel("BBDD Scotiabank.xlsx", engine='openpyxl', sheet_name='Terminos')
        
        x = tracker.get_slot('concepto')
        
        df = df[df['Concepto'].str.lower() == str.lower(x)]['Descripcion']
        print(df)
        #df = dict(df)
        return {'descripcion' : df}
    
    
    


