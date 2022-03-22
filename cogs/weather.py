import os
import time
import requests
import typing
import discord
from discord.ext import commands

class Weather(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Weather system is online.')
        time.sleep(0.25)

    @commands.command(pass_context = True)
    async def weather(self, ctx, *, args: typing.Optional[str] = None):
        if not args:
            await ctx.send('You need to give me your location (e.g. \"$weather New York\")')
            return
        #Important information to complete the task.
        weather_Key = os.environ['Weather API']
        current_weather_url = "http://api.weatherapi.com/v1/current.json?key=" + weather_Key + "&q="
        userLocation = args

        #Check if the location is properly provided by the user.
        if(len(userLocation) > 1):
            print('\nAcquiring weather data based on the location provided by the user: {0}'.format(userLocation))
            current_weather_link = requests.get(current_weather_url + str(userLocation) + "&aqi=yes&alert=yes")
            current_weather_data = current_weather_link.json()

        if(current_weather_link.headers['CDN-RequestPullCode'] == "200"):
            #Harvest data from the Weather API file.
            print('Starting to collect data...')
            #Location information.
            location_city = current_weather_data["location"]["name"]
            location_state = current_weather_data["location"]["region"]
            location_country = current_weather_data["location"]["country"]
            #Temperature information
            temp_c = current_weather_data["current"]["temp_c"]
            temp_f = current_weather_data["current"]["temp_f"]
            #Condition information
            feelslike_c = current_weather_data["current"]["feelslike_c"]
            feelslike_f = current_weather_data["current"]["feelslike_f"]
            gust_mph = current_weather_data["current"]["gust_mph"]
            gust_kph = current_weather_data["current"]["gust_kph"]
            wind_dir = current_weather_data["current"]["wind_dir"]
            condition_text = current_weather_data["current"]["condition"]["text"]
            condition_icon = "https:" + current_weather_data["current"]["condition"]["icon"]
            vis_mi = current_weather_data["current"]["vis_miles"]
            vis_km = current_weather_data["current"]["vis_km"]
            humidity = current_weather_data["current"]["humidity"]
            uv_level = current_weather_data["current"]["uv"]
            #Air quality information
            us_epa_index = current_weather_data["current"]["air_quality"]["us-epa-index"]
            co_index = current_weather_data["current"]["air_quality"]["co"]
            ozone_index = current_weather_data["current"]["air_quality"]["o3"]
            pm2_5 = current_weather_data["current"]["air_quality"]["pm2_5"]
            pm10 = current_weather_data["current"]["air_quality"]["pm10"]

            #Rounding values to two decimal digits
            print('Data has been collected. Now starting to round decimal numbers...')
            co_index = round(co_index, 2)
            ozone_index = round(ozone_index, 2)
            pm2_5 = round(pm2_5, 2)
            pm10 = round(pm10, 2)
            gust_mph = round(gust_mph, 2)
            gust_kph = round(gust_kph, 2)
            vis_mi = round(vis_mi, 2)
            vis_km = round(vis_km, 2)

            #Composing embedded message for user
            WeatherInfo = discord.Embed(title="__Weather Report - {0}__".format(condition_text), description="", color=0x97FEEF)
            WeatherInfo.set_thumbnail(url=condition_icon)
            WeatherInfo.add_field(name="Location", value="{0}, {1}, {2}".format(location_city, location_state, location_country), inline=False)
            WeatherInfo.add_field(name="Temperature", value="{0}°F / {1}°C".format(temp_f, temp_c), inline=True)
            WeatherInfo.add_field(name="Feels Like", value="{0}°F / {1}°C".format(feelslike_f, feelslike_c), inline=True)
            WeatherInfo.add_field(name="Humidity", value="{0}%".format(humidity), inline=True)
            WeatherInfo.add_field(name="Wind", value="{0} mph / {1} kph ({2})".format(gust_mph, gust_kph, wind_dir), inline=True)
            WeatherInfo.add_field(name="UV Level", value=uv_level, inline=True)
            WeatherInfo.add_field(name="Visibility", value="{0} mi / {1} km".format(vis_mi, vis_km), inline=True)
            WeatherInfo.add_field(name="Air Quality Index", value="US EPA Index: {0}\nCO Index: {1}\nO3 Index: {2}\nPM2.5 Index: {3}\nPM10 Index: {4}".format(us_epa_index, co_index, ozone_index, pm2_5, pm10), inline=False)
            WeatherInfo.set_footer(text="This information is provided by Weather API")
            
            await ctx.send(embed=WeatherInfo)
            
        else:
            #Print error to console and let the user know that the request is not completed.
            errorMsg = 'There\'s an error with the system. Unable to process request right now. Please try again later.'
            print(errorMsg)
            await ctx.send(errorMsg)


def setup(client):
    client.add_cog(Weather(client))