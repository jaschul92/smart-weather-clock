import os
import sys
import requests
import json
import sched, time
from threading import Thread, Event
#from Tkinter import *

WEATHER_BASE_URL = 'https://api.darksky.net/forecast/'
GEOLOCATION_BASE_URL = 'http://freegeoip.net/json'
API_KEY = '0de17eb41ac7bb9b6a09b74245da3039'

class Weather():
   def __init__(self):
      self.forecast = ''
      self.temp = ''
      self.cloud_condition = ''
      self.get_weather()

   def get_weather(self):
      try:
         lat, lon = self.get_location()
         request_url = WEATHER_BASE_URL+API_KEY+'/'+lat+','+lon
         resp = requests.get(request_url)
         data = json.loads(resp.text)
         curr_temp = str(int(data['currently']['temperature']))+u'\N{DEGREE SIGN}'
         curr_cloud_condition = data['currently']['summary']
         curr_forecast = data['hourly']['summary']
         curr_icon = data['currently']['icon']

         if curr_temp != self.temp:
            self.temp = curr_temp
         if curr_cloud_condition != self.cloud_condition:
            self.cloud_condition = curr_cloud_condition
         if curr_forecast != self.forecast:
            self.forecast = curr_forecast

      except Exception as e:
         print("Error: %s. Cannot get weather" %e)

   def get_location(self):
      try:
         r = requests.get(GEOLOCATION_BASE_URL)
         j = json.loads(r.text)
         lat = str(j['latitude'])
         lon = str(j['longitude'])
         return lat,lon

      except Exception as e:
         print("Errro %s. Cannot get current location" %e)
      
class Window():
   def __init__(self):
      self.tk = Tk()
      self.tk.configure(background = 'gray')
      self.state = False
      self.tk.bind("<Return>", self.toggle_fullscreen)
      self.tk.bind("<Escape>", self.end_fullscreen)

   def toggle_fullscreen(self, event=None):
      self.state = not self.state
      self.tk.attributes("-fullscreen", self.state)
      return "break"

   def end_fullscreen(self, event=None):
      self.state = False
      self.tk.attributes("-fullscreen", False)
      return "break"
      

class MyThread(Thread):
   def __init__(self, event):
      Thread.__init__(self)
      self.stopped = event

   def run(self):
      while not self.stopped.wait(5.0):
         w = Weather()
         print(w.temp)
         print(w.cloud_condition)
         print(w.forecast)
         
def kelvin_to_farenheit(k_temp):
   return int((k_temp - 273.15)*1.8 + 32.00)

def main():
   stop_flag = Event()
   thread = MyThread(stop_flag)
   thread.start()

   #w = Weather()
   #win = Window()
   #win.tk.mainloop()
   
if __name__ == "__main__":
    main()
