import discord
from discord.ext import commands
from client import client_conn 

TOKEN = 'MTI0NzE5NzI4NTI0MzE1ODUzOQ.G2B-N9.QkeWv2V4VE3nORpnIHjaOsZs0uGi3wHvyf-q4k'

# Créer une instance du bot Discord avec le préfixe de commande
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

# A global variable to keep track of whether an action should be stopped
stop_action = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Command to stop the ongoing action
@bot.command()
async def stop(ctx):
    global stop_action
    stop_action = True
    await ctx.send("Stopping the current action...")

@bot.command(help="Search for a keyword in the last 100 messages and create a thread displaying results.")
async def search_keyword(ctx, *, keyword: str):
    """
    Search for a keyword in the last 100 messages and create a thread displaying results.

    Parameters:
    keyword: The word to search for in the messages(Word).
    """
    thread = await ctx.channel.create_thread(name=f"Results for '{keyword}'", type=discord.ChannelType.public_thread)
    await message.channel.send('Let me do it...')
    async for message in ctx.channel.history(limit=100):
        if stop_action:
            break
        if keyword in message.content:
            await thread.send(f"Found message: {message.content} (Link: {message.jump_url})")
    if stop_action:
        await ctx.send("The search was stopped.")
    else:
        await ctx.send(f"Search for '{keyword}' completed. Check the thread for results.")

# Command to search by theme and create a thread displaying results
@bot.command(help="Search for a theme in the last 100 messages and create a thread displaying results.")
async def search_theme(ctx, *, theme: str):
    """
    Search for a theme in the last 100 messages and create a thread displaying results.

    Parameters:
    theme: The theme to search for in the messages (Word).
    """
    await ctx.send('Let me do it... (This may take a while)')
    
    thread = await ctx.channel.create_thread(name=f"Results for theme '{theme}'", type=discord.ChannelType.public_thread)

    # Skip the last two messages
    messages = []
    async for message in ctx.channel.history(limit=102):
        if stop_action:
            break
        messages.append(message)
    messages = messages[:-2]  # Exclude the last two messages

    for message in messages:
        if stop_action:
            break
        if message.content.startswith(ctx.prefix + ctx.invoked_with):
            continue
        prompt = f"Does this message talk about {theme}?\n\nMessage: {message.content}."
        try:
            response = client_conn.get_chat_response(prompt, temp=0.0, context='search')
            if "yes" in response.lower():
                await thread.send(f"Found message: {message.content} (Link: {message.jump_url})")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            return
    if stop_action:
        await ctx.send("The search was stopped.")
    else:
        await ctx.send(f"Search for theme '{theme}' completed. Check the thread for results.")

@bot.command()
async def hello(ctx):
    await ctx.send('NOOO!')

# Commande pour purger les messages
@bot.command(help="Delete a specified number of messages in the channel.")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int = None):
    """
    Delete a specified number of messages in the channel.

    Parameters:
    limit: The number of messages to delete (Number).
    """
    if limit is None:
        await ctx.send(
            "Syntax Error: You must specify the number of messages to purge. Usage: !purge <number>"
        )
    else:
        deleted = await ctx.channel.purge(limit=limit)
        response = f'Deleted {len(deleted)} messages'
        await ctx.send(
            response, delete_after=5
        )  # Le message de réponse sera supprimé après 5 secondes


@bot.command(help="Get a response from the model for the given prompt.")
async def chat(ctx, *, prompt):
    """
    Get a response from the model for the given prompt.

    Parameters:
    prompt: The prompt to get a response for (Text).
    """
    print(f"Received prompt: {prompt}")  # Debugging line
    await ctx.send('Let me do it...')
    try:
        response = client_conn.get_chat_response(prompt)
        print(f"Received response: {response}")
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}")


# Commande pour résumer un texte
@bot.command(help="Summarize the given text.")
async def summarize(ctx, *, text: str):
    """
    Summarize the given text.

    Parameters:
    text: The text to summarize (Text).
    """
    prompt = f"Summurize : {text}"
    await ctx.channel.send('Let me do it...')
    try:
        response = client_conn.get_chat_response(prompt)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}")


# Commande pour Rephrase un texte
@bot.command(help="Rephrase the given text.")
async def rephrase(ctx, *, text: str):
    prompt = f"Rephrase : {text}"
    await ctx.send('Let me do it...')
    try:
        response = client_conn.get_chat_response(prompt)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Commande pour traduire un texte en français
@bot.command(help="Translate the given text to French.")
async def translate(ctx, *, text: str):
    """
    Translate the given text to French.

    Parameters:
    text: The text to translate (Text).
    """
    prompt = f"Translate in French : {text}"
    await ctx.send('Let me do it...')
    try:
        response = client_conn.get_chat_response(prompt)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Exécuter le bot avec le jeton d'authentification
bot.run(TOKEN)
