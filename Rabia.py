import discord
from discord.ext import commands
from client import client_conn 

TOKEN = 'MTI0NzE5NzI4NTI0MzE1ODUzOQ.G2B-N9.QkeWv2V4VE3nORpnIHjaOsZs0uGi3wHvyf-q4k'

# Créer une instance du bot Discord avec le préfixe de commande
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)


# Définir le message de confirmation lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('NOOO!')

    if message.content.startswith('$chat_'):
        await message.channel.send('po!')

    if message.content.startswith('$chat-rabia'):
        prompt = message.content[len('$chat-rabia '):]
        print(f"Received prompt: {prompt}")  # Debugging line
        try:
            response = client_conn.get_chat_response(prompt)
            print(f"Received response: {response}")  # Debugging line
            await message.channel.send(response)
        except Exception as e:
            print(f"Error: {e}")  # Debugging line
            await message.channel.send(f"Error: {e}")
    if 

    await bot.process_commands(message)  # Process commands


@bot.command()
async def hello(ctx):
    await ctx.send('NOOO!')


@bot.command()
async def chat(ctx, *, prompt):
    print(f"Received prompt: {prompt}")  # Debugging line
    try:
        response = client_conn.get_chat_response(prompt)
        print(f"Received response: {response}")
        await ctx.send(response)
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send(f"Error: {e}")

# Exécuter le bot avec le jeton d'authentification
bot.run(TOKEN)