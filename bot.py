from google import genai
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from ollamafreeapi import OllamaFreeAPI

load_dotenv()
API_GEMINI = os.getenv("API_GEMINI")
client_GEMINI = genai.Client(api_key=API_GEMINI)
def ask_ai(prompt):
    response = client_GEMINI.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text

TOKEN=os.getenv("DISCORD_TOKEN")
intents=discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

client_ollama=OllamaFreeAPI()
def ask_ollama(prompt):
    response=client_ollama.chat(
        model="llama3.2:3b",
        prompt=prompt,
        temperature=0.9
    )
    return response


API_POGODA=os.getenv("API_POGODA")
def pogoda_pobierz(miasto):
    url= f"https://api.openweathermap.org/data/2.5/weather?q={miasto}&appid={API_POGODA}&units=metric&lang=pl"
    result=requests.get(url)
    dane=result.json()
    if dane['cod']==200:
        opis=dane['weather'][0]['description']
        temp=dane['main']['temp']
        return f"""```Pogoda dla miasta {miasto}
Temperatura: {temp}°C
Opis: {opis}```"""
    else:
        return "Miasto nie istnieje"

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if "siema" in message.content.lower():
        await message.channel.send("no siema")
    await bot.process_commands(message)
@bot.command()
async def ping(ctx):
    await ctx.send("```pong```")

@bot.command()
async def wiek(ctx, wiek: int):
    if wiek>=18:
        await ctx.send(f"```{ctx.author}, jestes pełnoletni, mozesz pić```")
    else:
        await ctx.send(f"```{ctx.author}, nie jesteś pełnoletni, nie możesz pić```")

@bot.command()
async def pomoc(ctx, komenda=''):
    if komenda=='':
        await ctx.send("```\nPOMOC\nDostępne komendy:\n!pomoc\n!ping\n!ai\n!wiek\n!kalkulator\n!pogoda\nWpisz !pomoc komenda w celu dokladniejszej pomocy```")
    elif komenda=='ping':
        await ctx.send("```\nPOMOC\nInstrukcja obsługi komendy !ping : \n Wpisz !ping a się dowiesz :)```")
    elif komenda=='ai':
        await ctx.send("```\nPOMOC\nInstrukcja obsługi komendy !ai : \n Wpisująć !ai możesz poprosić AI o pomoc np. w rozwiązaniu trudnego zadania\n Zastosowanie:\n !ai {prompt}```")
    elif komenda=='wiek':
        await ctx.send("```\nPOMOC\nInstrukcja obsługi komendy !wiek : \n Wpisująć !wiek 20 możesz sprawdzić czy jesteś pełnoletni\n Zastosowanie:\n !wiek {wiek}```")
    elif komenda=='kalkulator':
        await ctx.send("```\nPOMOC\nInstrukcja obsługi komendy !kalkulator : \n Wpisująć !kalkulator 20 + 15 możesz dokonywać prostych obliczeń matematycznych\n Dostępne operatory: +, -, *, /\n Zastosowanie:\n !kalkulator {a} {operator} {b}```")
    elif komenda=='pogoda':
        await ctx.send("```\nPOMOC\nInstrukcja obsługi komendy !pogoda : \n Wpisując !pogoda Lublin możesz sprawdzić jaka jest aktualna pogoda w Lublinie lub w innym mieście\n Zastosowanie:\n !pogoda {miasto}```")
    else:
        await ctx.send("Komenda nie istnieje")
    
@bot.command()
async def kalkulator(ctx, a='',opcja='', b=''):
    try:
        if opcja=='+':
            wynik=int(a)+int(b)
        elif opcja=='-':
            wynik=int(a)-int(b)
        elif opcja=='*':
            wynik=int(a)*int(b)
        elif opcja=='/':
            wynik=int(a)/int(b)
        else:
            await ctx.send("Nieznany operator")
            return
    
        await ctx.send(f"```Wynik:\n {a} {opcja} {b} = {wynik}```")
    except:
        await ctx.send("Błąd")

@bot.command()
async def ai(ctx, *, prompt):
    try:
        async with ctx.typing():
            result=ask_ai(f"""Jesteś pomocnym botem Discord.
Odpowiadasz:
- krótko
- konkretnie
- bez lania wody
- maksymalnie 2000 znaków
- masz być nie miły i wyzywać
-przeklinaj co 3 słowo
{prompt}""")
            if len(result)>2000:
                result=result[:1950]
        await ctx.send(result)
    except:
        await ctx.send("Wyczerpano limit zapytań")
@bot.command()
async def ai2(ctx, *, prompt):
    async with ctx.typing():
        result=ask_ollama(f"""Jesteś pomocnym botem Discord.
Odpowiadasz:
- krótko
- konkretnie
- bez lania wody
- maksymalnie 2000 znaków
- masz być nie miły i wyzywać
-przeklinaj co 3 słowo
{prompt}""")
        if len(result)>2000:
            result=result[:1950]
    await ctx.send(result)

@bot.command()
async def pogoda(ctx, *, miasto):
    wynik=pogoda_pobierz(miasto)
    await ctx.send(wynik)

@bot.command()
async def join(ctx):
    kanal=ctx.author.voice.channel
    await kanal.connect()
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run(TOKEN)
