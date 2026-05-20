import google.generativeai as genai
import discord
from discord.ext import commands

API_GEMINI = "AIzaSyAT5h1HmXo2auhDyT34IhcviKuGe4mz9O4"
genai.configure(api_key=API_GEMINI)
model = genai.GenerativeModel("gemini-3.5-flash")
def ask_ai(prompt):
    response = model.generate_content(prompt)
    return response.text

TOKEN = "MTUwNjM2MTA4Mjg1MDMxMjIyMg.GgRNGX.uoLuZ7JuuXxgZLYCpr08qapuON97KGSCieLpAk"
intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)
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
        await ctx.send(f'```POMOC\nDostępne komendy:\n!pomoc\n!ping\n!wiek\n!kalkulator\nWpisz !help komenda w celu dokladniejszej pomocy```')

@bot.command()
async def kalkulator(ctx, a='',opcja='', b=''):
    if opcja=='+':
        wynik=int(a)+int(b)
    elif opcja=='-':
        wynik=int(a)-int(b)
    elif opcja=='*':
        wynik=int(a)*int(b)
    elif opcja=='/':
        wynik=int(a)/int(b)
    
    await ctx.send(f"```Wynik:\n {a} {opcja} {b} = {wynik}```")

@bot.command()
async def ai(ctx, *, prompt):
    async with ctx.typing():
        result=ask_ai(f"""Jesteś pomocnym botem Discord.
                            Odpowiadasz:
                            - krótko
                            - konkretnie
                            - bez lania wody
                            - maksymalnie 2000 znaków
                            {prompt}""")
        if len(result)>2000:
            result=result[:1950]
    await ctx.send(f"```{result}```")
bot.run(TOKEN)
