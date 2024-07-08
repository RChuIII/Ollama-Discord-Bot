import discord
import os
from dotenv import load_dotenv, dotenv_values
import responses
import time

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

async def send_ai_message(message, user_message, is_private, segment_length=2000,model='dolphin-llama3'):
    try:
        response = responses.get_ollama_response(model, 'user', user_message)
        if len(response) > 2000:
            response_list = [response[i:i+segment_length] for i in range(0, len(response), segment_length)]
            if is_private:
                for r in response_list:
                    await message.author.send(r)
            else:
                for r in response_list:
                    await message.channel.send(r)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_API_TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        log_message(username, user_message, channel)
        
        if message.author == client.user:
            return

        if user_message[0:4] == '&*?!':
            user_message = user_message[4:]
            await send_message(message, user_message,is_private=True)
        elif user_message[0] == "!":
            user_message = user_message[1:]
            await send_ai_message(message, user_message, is_private=False)
        else:
            return
            await send_message(message, user_message, is_private=False)
    
    client.run(TOKEN)

def log_message(author: str, message: str, channel: str) -> None:
    with open('log.txt', 'a') as f:
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        f.write('TIMESTAMP: ' + now  + '\n' + f'{author} said: {message} ({channel})' + '\n\n')