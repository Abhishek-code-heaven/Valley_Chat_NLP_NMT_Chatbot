import datetime as dt 
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import requests


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # requestneed =tracker.latest_message['text']
       
        dispatcher.utter_message(text=f"{dt.datetime.now()}")
        

        return []

class Actionweather(Action):

    def name(self) -> Text:
        return "action_show_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # requestneed =tracker.latest_message['text']
        url = "http://api.weatherapi.com/v1/current.json"

        querystring = {"key":"9ae08361a85a48c282f95300230203","q":"San Jose"}



        response = requests.request("GET", url, params=querystring)
        response = json.loads(response.text)
        temp = "The Temperature in San Jose is "+str(response["current"]["temp_c"])+ " "+"degree celcius and it feels like"+" "+str(response["current"]["feelslike_c"])+" "+"degree celcius"

        dispatcher.utter_message(text=f"{temp}")
        

        return []

