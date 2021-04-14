# Created by : Hitansh Bhatt
#Perms to give to the bot : Administrator (pereferable)
#Import Disocrd package
import discord
from discord.ext import commands

#Client (the Bot)
client = commands.Bot(command_prefix = '!')
reaction_title = "" # global variable
reactions = {}      # creating a blank dicitionary
reaction_message_id = ""

#get server id by doing context.guild.id OR user.guild.id

@client.event
async def on_ready():
    print('The bot is online!')

@client.command(name = 'info')
async def info(context):
    myEmbed = discord.Embed(title='Server Owner', description='Hitansh Bhatt#7760', color=0x00ff00)
    myEmbed.add_field(name = 'Date Released:', value = 'March 5th, 2021', inline = False)
    myEmbed.set_footer(text = 'Thank you for trying out my server!')
    myEmbed.set_author(name = "Hitansh Bhatt")
    await context.message.channel.send(embed = myEmbed)

#Basic commands
@client.event
async def on_message(self, message):
    if message.author == self.user:
        return

    if message.content == 'ping':
        await message.channel.send('pong')

    if message.content == 'happy birthday':
        await message.channel.send('Happy Birthday 🎈🎉')

#Embedded messages
@client.event
async def on_message(message):
    if message.content == 'info':
        myEmbed = discord.Embed(title='Onwer', description='Hitansh Bhatt#7760', color=0x00ff00)
        myEmbed.add_field(name = 'Date Released:', value = 'March 5th, 2021', inline = False)
        myEmbed.set_footer(text = 'Thank you for trying out my server!')
        myEmbed.set_author(name = "Py_Bot")
        await message.channel.send(embed = myEmbed)

    await client.process_commands(message)

    #send DM to user
    if message.content == 'send me a DM':
        await message.author.send('Hello, you requested a DM. How can I help you?')

    await client.process.commands(message)

# command to kick a member, Command syntax: !kick @User_Name
@client.command(name ='kick', pass_context = True)
@commands.has_permissions(kick_members = True)
async def kick(context, member: discord.Member):
    await member.kick()
    await context.send('User `'+ member.display_name + '` has been kicked.')

# command to ban a member, Command syntax: !ban @User_Name "abusive language"
@client.command(name = 'ban', pass_context = True)
@commands.has_permissions(ban_members = True)
async def ban(context, member : discord.Member, * , reason = 'inappropriate/abusive language'):
    await member.ban(reason = reason)
    await context.send('User ' + member.display_name + ' has been banned.')

@client.command(name = 'create_reaction_post')
async def create_reaction_post(context):
    embed = discord.Embed(title = 'Create a reaction post', color = 0x00ff00)
    embed.set_author(name = 'Py_Bot')
    embed.add_field(name = "Set Title", value = "!set_reaction_title \"New Title\"")  # , inline = False
    embed.add_field(name = "Add Role", value = "!add_reaction_role @Role EMOJI_HERE") # , inline = False
    embed.add_field(name = "Remove Role", value = "!remove_reaction_role @Role")      # , inline = False
    embed.add_field(name = "Send Creation Post Role", value = "!send_reaction_post")      # , inline = False

    await context.send(embed=embed)
    await context.message.delete()

#!set_reaction_title "This is a new title"
@client.command(name = 'set_reaction_title')
async def set_reaction_title(context, new_title):
    global reaction_title               # to access the global vairable
    reaction_title = new_title
    await context.send("The title for the message is now `" + reaction_title + "`!")
    await context.message.delete()

# Example : !add_reaction_role @Moderator EMOJI_HERE
@client.command(name = 'add_reaction_role')
async def add_reaction_role(context, role: discord.Role, reaction):
    if role != None:            # error handling
        reactions[role.name] = reaction # reaction is the emoji, don't need to use the 'global' keyword because Python automatically assumes that the dictionary was created elsewhere because of the []
        await context.send("Role `" + role.name + "` has been added with the emoji " + reaction)
        await context.message.delete();
        #print(reactions)
    else:
        await context.send('No role was entered! Please try again.')

@client.command(name = 'remove_reaction_role')
async def remove_reaction_role(context, role: discord.Role):
    if role.name in reactions:
        del reactions[role.name]        #'del' for delete
        await context.send("Role `" + role.name + "` has been deleted ")
        await context.message.delete();
        #print(reactions)
    else:
        await context.send('That role was not added, please try again.')

    #print(reactions)

@client.command(name = 'send_reaction_post')
async def send_reaction_post(context):
    description = "React to add new roles!\n"

    for role in reactions:
        description += "`" + role + "` - " + reactions[role] + "\n"

    embed = discord.Embed(title = reaction_title, description = description, color = 0x00ff00)
    embed.set_author(name = "Py_Bot")

    message = await context.send(embed = embed)     # stores the message that it sent to the discord channel in the vairable 'message', we need to access this 'message' to add reactions to it

    global reaction_message_id
    reaction_message_id = str(message.id)

    # to add the emojis (reactions) to the message
    for role in reactions:
        await message.add_reaction(reactions[role])

    await context.message.delete()

@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        message = reaction.message

        global reaction_message_id
        if str(message.id) == reaction_message_id:
            # Add roles ot our user
            role_to_give = ""

            for role in reactions:
                if reactions[role] == reaction.emoji:
                    role_to_give = role

            role_for_reaction = discord.utils.get(user.guild.roles, name = role_to_give)
            await user.add_roles(role_for_reaction)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity = discord.Game('Among Us'))

client.run('ENTER_TOKEN_HERE')
