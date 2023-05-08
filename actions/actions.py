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
from rasa_sdk.types import DomainDict
from threading import Thread
import requests
import sqlite3
import os
import openai
import json
 
import pandas as pd
import openpyxl 
#import speech_recognition as sr
#from translate import Translator
#
#

#openai.api_key = os.environ["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"]

"""class ActionChatGPT(Action):

    def name(self) -> Text:
        return "action_chat_gpt"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = tracker.latest_message['text']

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=message,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5
        )

        chat_gpt_response = response.choices[0].text.strip()
        dispatcher.utter_message(text=chat_gpt_response)
        return [] """

#GUARDA EL NOMBRE PARA PODER ALMACENARLO EN LA BASE DE DATOS
class ActionGuardarNombre(Action):
    def name(self) -> Text:
        return "action_guardar_nombre"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        
        nombre = tracker.get_slot('nombre')
        print(nombre)
        
        if nombre is not None:
            mensaje = f"Hola, {nombre}! un gusto conocerte"
        else:
            mensaje = "Hola! un gusto conocerte"
            
        dispatcher.utter_message(text = mensaje)
        
        return [SlotSet("nombre", str.upper(nombre))]
    
#GUARDA EL PRODUCTO PARA PODER GUARDARLO EN LA BASE DE DATOS
class ActionGuardarProducto(Action):
    def name(self) -> Text:
        return "action_guardar_producto"
    
    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        producto = tracker.latest_message['text']
        print(producto)
        
        mensaje = f"{str.upper(producto)} es: "
        dispatcher.utter_message(text = mensaje)
        return [SlotSet('producto', str.upper(producto))]

#GUARDA EL CONCEPTO PARA PODER GUARDARLO EN LA BASE DE DATOS
class ActionGuardarConcepto(Action):
    def name(self) -> Text:
        return "action_guardar_concepto"
    
    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        concepto = tracker.latest_message('Text')
        print(concepto)
        
        mensaje = f"{str.upper(concepto)} es: "
        dispatcher.utter_message(text = mensaje)
        
        return [SlotSet('concepto',str.upper(concepto))]
   
#
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
        #dispatcher.utter_message("Gracias a ti!!")
        print(nombre, producto, concepto)
        return []
    
class recuperar_info_producto(Action):
    
    def name(self) -> Text:
        return "action_recuperar_info_producto"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        producto = tracker.get_slot('producto')
        
        df = pd.read_excel("BBDD Scotiabank.xlsx", engine='openpyxl', sheet_name='Productos')
    
        df = df[df['PRODUCTO'].str.upper() == str.upper(producto)]
        
        if df is not None:
            df = df['DETALLE'].to_json()
            numero = df[2:4]
            json_obj = json.loads(df)
            descripcion = json_obj[numero]
        else:
            descripcion = "No hay informacion"
        
        print(descripcion)
        
        return [SlotSet('descripcion',descripcion)]
    
class dar_info(Action):
    
    def name(self) -> Text:
        return "action_dar_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        descripcion = tracker.get_slot('descripcion')
        print(descripcion)
        dispatcher.utter_message(text = descripcion)
        return []
    
class recuperar_info_concepto(Action):
    
    def name(self) -> Text:
        return "action_recuperar_info_concepto"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        concepto = tracker.get_slot('concepto')
        
        df = pd.read_excel("BBDD Scotiabank.xlsx", engine='openpyxl', sheet_name='Terminos')
        
        df = df[df['CONCEPTO'].str.upper() == str.upper(concepto)]
        
        if df is not None:
            df = df['DETALLE'].to_json()
            numero = df[2:4]
            json_obj = json.loads(df)
            descripcion = json_obj[numero]
        else:
            descripcion = "No hay informacion"
    
        print(descripcion)

        return [SlotSet('descripcion',descripcion)]
