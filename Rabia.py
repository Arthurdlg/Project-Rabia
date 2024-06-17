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
        await message.channel.send('Let me think about it...')
        print(f"Received prompt: {prompt}")  # Debugging line
        try:
            response = client_conn.get_chat_response(prompt)
            print(f"Received response: {response}")  # Debugging line
            
            await message.channel.send(response)
        except Exception as e:
            await message.channel.send(f"Error: {e}")

    if message.content.startswith('$history'):
        await message.channel.send('po!')

    await bot.process_commands(message)  # Process commands


@bot.command()
async def get_message_id(ctx, *, search_text: str):
    try:
        # Fetch messages in the channel history
        async for message in ctx.channel.history(limit=100): # To get  history of 100 messages
            if search_text in message.content:
                await ctx.send(f"Message ID for '{search_text}': {message.id}")
                return
        await ctx.send(f"No message found containing: {search_text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")



@bot.command()
async def hello(ctx):
    await ctx.send('NOOO!')

# Commande pour purger les messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int = None):
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


@bot.command()
async def chat(ctx, *, prompt):
    print(f"Received prompt: {prompt}")  # Debugging line
    try:
        response = client_conn.get_chat_response(prompt)
        print(f"Received response: {response}")
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}")


import random

@bot.command()
async def tictactoe(ctx, player2: discord.Member):
    board = [' '] * 9
    turn = 'X'
    game_over = False

    def print_board():
        return f"{board[0]}|{board[1]}|{board[2]}\n{board[3]}|{board[4]}|{board[5]}\n{board[6]}|{board[7]}|{board[8]}"

    await ctx.send(f"Tic-Tac-Toe game started between {ctx.author.mention} and {player2.mention}.\n{print_board()}")

    while not game_over:
        def check_winner():
            wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
            for win in wins:
                if board[win[0]] == board[win[1]] == board[win[2]] and board[win[0]] != ' ':
                    return board[win[0]]
            if ' ' not in board:
                return 'Draw'
            return None

        def check_input(msg):
            return msg.author in [ctx.author, player2] and msg.content.isdigit() and int(msg.content) in range(9) and board[int(msg.content)] == ' '

        await ctx.send(f"{turn}'s turn. Enter a number (0-8):")
        try:
            move = await bot.wait_for('message', check=check_input, timeout=60.0)
            board[int(move.content)] = turn
            winner = check_winner()
            if winner:
                game_over = True
                if winner == 'Draw':
                    await ctx.send("It's a draw!\n" + print_board())
                else:
                    await ctx.send(f"{winner} wins!\n" + print_board())
            else:
                turn = 'O' if turn == 'X' else 'X'
                await ctx.send(print_board())
        except TimeoutError:
            await ctx.send("Game over due to inactivity.")
            game_over = True

# Exécuter le bot avec le jeton d'authentification
bot.run(TOKEN)
