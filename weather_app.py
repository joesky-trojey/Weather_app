"""
install geopy using "pip3 install geopy" to use geolocation(coordinates to call the weather API)
Fetch weather data and icons from Openweather
Author: Joseph Mugure
Date: Tue-Sep 26, 2023

"""
#make the resessry lib imports
import tkinter as tk
from tkinter import font, ttk, PhotoImage
from PIL import Image, ImageTk
import requests, json, geocoder, io, datetime, random

# OpenWeatherMap API key variable held here
api_key = '3d9adfed9700544cc42b339670f2cabf'

#get your current location
def get_geo_coordinates():
    location=geocoder.ip('me')
    lat=location.latlng[0]
    longit=location.latlng[1]
    return lat, longit

#get the next day for prediction display 
def get_day (date):
    date=datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date=date.date()
    weekday=date.weekday()
    #print(weekday)
    weekday_names = ["Mon-Tue", "Tue-Wed", "Wed-Thur", "Thur-Fri", "Fri-Sat", "Sat-Sun", "Sun-Mon"]
    return weekday_names[int(weekday)]
# print(get_day("2023-09-26 21:00:00")) -debug

#define function to process icon, return icon data
def weather_icon_process(icon_code,x,y):
     #create icon url based on the icon code
    icon_url=f'http://openweathermap.org/img/w/{icon_code}.png'
    print(f"Fetching Icon: {icon_url}")
    icon_resp=requests.get(icon_url)#fetch the idon using GET
    icon_data=Image.open(io.BytesIO(icon_resp.content)) #use PIL to open the image
    icon_data=icon_data.resize((x, y), Image.LANCZOS)#resize to 50x50 pixels
    # icon_photo=ImageTk.PhotoImage(icon_data)
    return icon_data #return icon data for more processing and display

geocords=get_geo_coordinates()

#get current weather infomation based on the obtained IP address using Openweather API
current_weather_API_call_url=f'https://api.openweathermap.org/data/2.5/weather?lat={geocords[0]}&lon={geocords[1]}&appid={api_key}'
#get forecast weather using opneweather API call using the url below
forecast_weather_API_call_url=f'https://api.openweathermap.org/data/2.5/forecast?lat={geocords[0]}&lon={geocords[1]}&appid={api_key}'
print("Fetching weather from: ", forecast_weather_API_call_url)

try:
    #get the data in Response object, then process it to JSON and text form
    current_weather_response=requests.get(current_weather_API_call_url)
    forecast_weather_response=requests.get(forecast_weather_API_call_url)

    current_weather_data=json.loads(current_weather_response.text)
    forecast_weather_data=json.loads(forecast_weather_response.text)

    icon_code=current_weather_data['weather'][0]['icon'] #get the icon code
    #main weather variables 
    main_weather = current_weather_data['weather'][0]['main']
    temparature=current_weather_data['main']['temp']
    description=current_weather_data['weather'][0]['description']
    pressure=current_weather_data['main']['pressure']
    humidity=current_weather_data['main']['humidity']
    windspeed=current_weather_data['wind']['speed']
    country=current_weather_data['sys']['country']
    location=current_weather_data['name']
    timezone_code=current_weather_data['timezone']


    # print(forecast_weather_data, '\n')
except Exception as e:
    print(f"Error: {str(e)}")


"""-----------------------------CREATE THE GUI USING TKINTER PYTHON LIB--------------------------------------"""
#initialize a tkinter object (to be displayed as main GUI container)
app=tk.Tk()
app.geometry("650x450")
app.resizable(0,0)
app.title('Weather App: Powered by OpenWeatherMap')
app_font =font.Font(family="Helvetica", size=13)
# app.configure(bg='blue')
app.update_idletasks()
# app.wm_attributes('-alpha',0)

app_width= int(app.winfo_width())
app_height=int(app.winfo_height())
backgrounds=['bg1.jpg', 'bg.jpg', 'bg2.jpg', 'bg3.png'] #different background images
bg_image=random.choice(backgrounds) #select background image at random
temp_background=Image.open(bg_image)
temp_background=temp_background.resize((app_width, app_height))
background_img=ImageTk.PhotoImage(temp_background)
background=tk.Label(app, image=background_img)
background.place(relheight=1, relwidth=1)

upper_frame=tk.Frame(app, width=660, height=190, background='pink',)
upper_frame.grid(row=0, column=0, padx=40, pady=5, sticky='we')

upper_left_frame=tk.Frame(upper_frame, width=150, height=190)
upper_left_frame.grid(row=2, column=4)

lower_frame=tk.Frame(app, width=660, height=190, bg='pink')
lower_frame.grid(row=1, column=0, padx=40, pady=5, sticky='ew')

# Calculate the current time in the specified timezone
utc_time = datetime.datetime.utcnow()
current_time = utc_time + datetime.timedelta(seconds=timezone_code)
current_time=current_time.strftime("%H:%M:%S")
current_date=datetime.date.today()
today=get_day(str(current_date)+" 0:0:0")
location_label=tk.Label(upper_frame, text=f"{location}, {country}, {today}, {current_time}", font=app_font, background='pink')
location_label.grid(row=0, column=4, padx=5, pady=5)

main_weather_label=tk.Label(upper_frame, text=f"{main_weather}", font=app_font, background='pink')
main_weather_label.grid(row=1, column=4, padx=5, pady=5)
main_weather_label.config(fg='green')

icon_label=ttk.Label(upper_left_frame, text='main weather')
icon_label.grid(column=0, row=0,)
icon_data=weather_icon_process(icon_code, 50, 50)
icon_photo=ImageTk.PhotoImage(icon_data)
icon_label.config(image=icon_photo, background='pink')
icon_label.image = icon_photo

temparature_label=tk.Label(upper_frame, text=f"Temparature {temparature} \u00B0F", font=app_font, background='pink')
temparature_label.grid(row=3, column=4, padx=5, pady=5)
temparature_label.config(fg='green')

pressure_label=tk.Label(upper_frame, text=f"Pressure: {pressure} hPa", font=app_font, background='pink')
pressure_label.grid(row=4, column=4, padx=5, pady=5)
pressure_label.config(fg='green')

humidity_label=tk.Label(upper_frame, text=f"Humidity {humidity} %", font=app_font, background='pink')
humidity_label.grid(row=5, column=4, padx=5, pady=5)
humidity_label.config(fg='green')

windspeed_label=tk.Label(upper_frame, text=f" Wind speed {windspeed} m/s", font=app_font, background='pink')
windspeed_label.grid(row=6, column=3, padx=5, pady=5)
windspeed_label.config(fg='green')

#forecast frame content
forecast_label=tk.Label(lower_frame, text=f"5 Day Forecast ", font=app_font, background='pink', )
forecast_label.grid(row=0, column=3, padx=5, pady=5)

for i in range(8):
    time_lable=tk.Label(lower_frame, text=f"{(datetime.datetime.strptime(forecast_weather_data['list'][i]['dt_txt'], '%Y-%m-%d %H:%M:%S')).time()}", background='pink', foreground="green")
    time_lable.grid(column=i+1, row=1, padx=3, pady=3)

#processs the hourly data and display forcast for each day
iteration=0
for i in range(5):

    next_day_forecast_label=tk.Label(lower_frame, text=f"{get_day(forecast_weather_data['list'][i*8]['dt_txt'])}: ", font=app_font, background='pink')
    next_day_forecast_label.grid(row=i+2, column=0, padx=5, pady=5)
    #Fetching icon takes a little bit of time and would probably be improved using threads to make it faster.
    for x in range(8):
        data=forecast_weather_data["list"][iteration]
        forecast=tk.Label(lower_frame, text=f"", background='pink')
        forecast_icon=weather_icon_process(data['weather'][0]['icon'], 20, 20)
        icon_photo=ImageTk.PhotoImage(forecast_icon)
        forecast.config(image=icon_photo, background='pink')
        forecast.image = icon_photo
        forecast.grid(column=x+1, row=i+2, padx=3, pady=3)
        iteration+=1
print('Rendering...')
app.update_idletasks()
print('Done')
#start the app and enter into an infinite loop 
app.mainloop()