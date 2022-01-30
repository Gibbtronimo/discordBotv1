import discord
import random
import os
from itertools import cycle
from discord.ext import commands
from discord.ext import tasks

client = commands.Bot(command_prefix = '.')     #prefix before a command
status = cycle(['Exam grading', 'Writing emails', 'Talking to Hopkins'])    #cycles through the array, super cool

#Events
@client.event
async def on_ready():               #When the bot is ready - has the info it needs
    change_status.start()           #starts the cycle loop for game status
    print('Bot is ready.')

@client.event
async def on_member_join(member):   #When a new member joins
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member): #When a member leaves
    print(f'{member} has left a server.')

@client.event
async def on_command_error(ctx, error): #Sends an error message - in this case when missing arg requirement
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("You don't know me")

#Task
@tasks.loop(seconds=1800)   #30 minutes
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


#Commands
@client.command()                   #Creates a command - now I understand (checks latency
async def ping(ctx):                #async def is the function header (ctx passes automatically)
    await ctx.send(f'Pong @ {round(client.latency * 1000)}ms')

@client.command()
async def pog(ctx):
    await ctx.send('poggers')

@client.command(aliases=['8ball'])  #all strings in this list can evoke command
async def _8ball(ctx, *, question):         #asterix takes in multiple arguments as one argument
    responses = [
        'Maybe so',
        'Try again later',
        'Brendan is gay',
        'Tri is gay',
        'Prem is gay',
        'Definitely',
        'Absolutely not',
        'Prem asks too many questions'
    ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()                           #just sends SAD quotes
async def sad(ctx):
    quotes = [
        'Hopkins? You there?',
        'conver hex COD3 t o binary',
        'Contro cont con',
        'Tri? Tri? Hello,',
        '192.18.16.1',
        'Pooty',
        'cahpter 3',
        'Tri?',
        'Login lovsl',
        'Les go in poooutyy',
        'They uhhhhh, they say, they they they uhhhh',
        'Ip in',
        'Inter',
        'Interface gig',
        'Tri hold on',
        'Ryan Salinas I can see you'
        ]
    await ctx.send(random.choice(quotes))

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):             #if amount is not specified then automatically 5
    await ctx.channel.purge(limit=amount)   #includes the clear command

@client.command()
async def load(ctx, extension):         #loads a cog to bot
    client.load_extension(f'cogs.{extension}')

@client.command()                       #unloads a cog to bot
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()                       #unloads then reloads a cog - to update a cog
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):   #accesses files inside listdir
    if filename.endswith('.py'):        #checks for .py files
        client.load_extension(f'cogs.{filename[:-3]}')  #removes the .py since we are loading cog.filename

#Error commands
#@clear.error                            #creates an error just for the clear function
#async def clear_error(ctx, error):
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send('Please specify an amount of messages to delete. '
#                       'Keep forgetting that I will mark off exam points.')
#Cannot run this with the other error message



client.run('insert token here')   #Runs the bot using its token
#The real token will not be uploaded to GitHub, this will stay on further revisions posted publicly
