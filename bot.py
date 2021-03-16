import discord
import os
from discord.ext import commands

client = discord.Client(command_prefix='!')
bot = commands.Bot(command_prefix='!')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == 'happy birthday':
            await message.channel.send('Happy Birthday 🎈🎉')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity = discord.Game('Among Us'))

@bot.command(name='create channel')
@commands.has_role('Exec')
async def create_channel(ctx, channel_name='Python help'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)



client = MyClient()
client.run('ODA1NTgzODY3NDI2NzY2ODQ5.YBdAcQ.10ietcIA1ApWPAYc3RS5WDuip70')
