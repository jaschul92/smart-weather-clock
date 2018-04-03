import os
import sys
import requests
import json
import sched, time
from threading import Thread, Event
#from Tkinter import *

WEATHER_BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
GEOLOCATION_BASE_URL = 'http://freegeoip.net/json'
API_KEY = str(os.environ.get('WEATHER_API_KEY'))

class Weather():
   def __init__(self):
      self.city = ''
      self.temp = ''
      self.min_temp = ''
      self.max_temp = ''
      self.cloud = ''
      self.get_weather()

   def get_weather(self):
      try:
         lat,lon = get_location()
         request_url = WEATHER_BASE_URL+'?lat='+lat+'&lon='+lon+'&APPID='+API_KEY
         resp = requests.get(request_url)
         data = json.loads(resp.text)
         print(data)
         
         city = data['name']
         weather_data = data['weather']
         cloud_condition = weather_data[0]['main']
         temp_data = data['main']
         temp = kelvin_to_farenheit(int(temp_data['temp']))
         min_temp = kelvin_to_farenheit(int(temp_data['temp_min']))
         max_temp = kelvin_to_farenheit(int(temp_data['temp_max']))

         if self.city != city:
            self.city = city
         if self.cloud != cloud_condition:
            self.cloud = cloud_condition
         if self.temp != str(temp):
            self.temp = str(temp)
         if self.min_temp != str(min_temp):
            self.min_temp = str(min_temp)
         if self.max_temp != str(max_temp):
            self.max_temp = str(max_temp)

      except Exception as e:
         print("Error: %s. Cannot get weather" %e)
      
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

def get_location():
   r = requests.get(GEOLOCATION_BASE_URL)
   j = json.loads(r.text)
   lat = str(j['latitude'])
   lon = str(j['longitude'])

   return lat,lon

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
