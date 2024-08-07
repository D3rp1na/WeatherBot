#
#                  8888888b.   .d8888b.                    d888                     
#                  888  "Y88b d88P  Y88b                  d8888                     
#                  888    888      .d88P                    888                     
#888  888  .d88b.  888    888     8888"  888d888 88888b.    888   88888b.   8888b.  
#`Y8bd8P' d88""88b 888    888      "Y8b. 888P"   888 "88b   888   888 "88b     "88b 
#  X88K   888  888 888    888 888    888 888     888  888   888   888  888 .d888888 
#.d8""8b. Y88..88P 888  .d88P Y88b  d88P 888     888 d88P   888   888  888 888  888 
#888  888  "Y88P"  8888888P"   "Y8888P"  888     88888P"  8888888 888  888 "Y888888 
#                                                888                                
#                                                888                                
#                                                888                                
#

import discord
import os
from discord.ext import commands
import aiohttp

api_key = os.getenv('WTHR_API')
# dont forget to input your weather API from open weather maps, it's free <3

class WeatherCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='weather')
    async def fetch_weather(self, ctx, *, location: str):
        location_query = location.replace(' ', '%20')

        # Check if the location input is a postal code (assumption: postal codes are numeric and typically have a fixed length, here we assume either 5 (US) or 6 digits for simplicity)
        if location.isdigit() and len(location) in [5, 6]:
            url = f'http://api.openweathermap.org/data/2.5/weather?zip={location_query}&appid={api_key}&units=metric'
        elif len(location) == 2 and location.isalpha():  # Check if location is a country code
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location_query}&appid={api_key}&units=metric'
        else:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location_query}&appid={api_key}&units=metric'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if data['cod'] == 200:
                    city_name = data['name']
                    country_code = data['sys']['country']
                    temp_c = data['main']['temp']
                    temp_min_c = data['main']['temp_min']
                    temp_max_c = data['main']['temp_max']
                    temp_f = (temp_c * 9/5) + 32
                    temp_min_f = (temp_min_c * 9/5) + 32
                    temp_max_f = (temp_max_c * 9/5) + 32
                    weather_desc = data['weather'][0]['description']
                    await ctx.send(f"**Location:** {city_name}, {country_code}\n"
                                    f"Current temperature: {temp_c}°C / {temp_f}°F\n"
                                    f"High: {temp_max_c}°C / {temp_max_f}°F\n"
                                    f"Low: {temp_min_c}°C / {temp_min_f}°F\n"
                                    f"Condition: {weather_desc}")
                else:
                    await ctx.send(f"Could not retrieve weather data for {location}. Please check the location name and try again.")

async def setup(bot):
    await bot.add_cog(WeatherCheck(bot))
