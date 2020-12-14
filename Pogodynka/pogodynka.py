import tkinter as tk
from tkinter import *
from tkinter import messagebox
import urllib
import requests
from PIL import Image, ImageTk
import time

app = tk.Tk()
app.title("Pogodynka")

HEIGHT = 500
WIDTH = 600

photo = PhotoImage(file="icons/01d.png")
app.iconphoto(False, photo)


def unix_to_local_conversion(api_time):
    return time.strftime("%I:%M %p", time.localtime(int(api_time)))


def format_response(weather_json):
    try:
        city = weather_json['name']
        conditions = weather_json['weather'][0]['description']
        temp = weather_json['main']['temp']
        feels = weather_json['main']['feels_like']
        sunrise = unix_to_local_conversion(int(weather_json['sys']['sunrise']))
        sunset = unix_to_local_conversion(int(weather_json['sys']['sunset']))
        values = 'Miasto: %s \nWarunki: %s \nTemperatura (°C): %s\nTemp. odczuwalna(°C): %s\nWschód słońca: %s' \
                    '\nZachód słonca: %s'\
                    % (city, conditions, temp, feels, sunrise, sunset)
    except:
        tk.messagebox.showwarning(
            title="Błąd!", message="Sprawdź nazwę miasta!"
        )
    return values


def get_weather(city):
    weather_key = '542591da57b70f1863ce1c7fd54cfe98'
    lang = 'pl'
    url_encoded_city_name = urllib.parse.quote(city)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={url_encoded_city_name}&appid={weather_key}&lang={lang}&units=metric"
    response = requests.get(url)
    weather_json = response.json()

    results['text'] = format_response(response.json())

    icon_name = weather_json['weather'][0]['icon']
    open_image(icon_name)


def open_image(icon):
    size = 75
    img = ImageTk.PhotoImage(Image.open('./icons/'+icon+'.png').resize((size, size)))
    weather_icon.delete("all")
    weather_icon.create_image(0,0, anchor='nw', image=img)
    weather_icon.image = img


C = tk.Canvas(app, height=HEIGHT, width=WIDTH, bg="#00396B")
background_label = tk.Label(app, bg="#00396B")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

C.pack()

frame = tk.Frame(app,  bg='#EB9600', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

textbox = tk.Entry(frame, font=40)
textbox.place(relwidth=0.65, relheight=1)

submit = tk.Button(frame, text='Sprawdź pogodę', bg="#006AEB", fg="white", highlightcolor='#006AEB',
                   font=("Arial Bold", 12),command=lambda: get_weather(textbox.get()))
submit.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(app, bg='#EB9600', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')


bg_color = '#47A0EE'
results = tk.Label(lower_frame, anchor='nw', justify='left', bd=4)
results.config(font=40, bg=bg_color)
results.place(relwidth=1, relheight=1)

weather_icon = tk.Canvas(results, bg=bg_color, bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)

app.mainloop()
