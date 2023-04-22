import os
from dotenv import load_dotenv
import discord
from test_utils.testable_bot import TestableBot
import requests
import json
from datetime import datetime
import asyncio

alert_times = {} #Dictionary of alert times to be checked by the bot every minute Key=id and Value=alert time
baseurl = 'https://321-hosted-backend.jack-klob.repl.co'
channel_ids = {} #Dictionary of channel ids to be used by the bot to send messages to the correct channel Key=task id and Value=channel id
load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

bot = TestableBot(intents=discord.Intents.all(), command_prefix='!')

def format_date_to_print(date: str):
    date = date.replace("T", " ")
    date = date.replace("Z", "")
    date = date.replace(":00", "")
    return date

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to the server")
    channel = bot.get_channel(1094031740462436446)
    await channel.send("Running")
    url = f'{baseurl}/task'
    response = requests.get(url=url)
    reminders = json.loads(response.text)
    #at start of Discord bot run time, check for any tasks that have a reminder and add them to the alert_times dictionary
    for tasks in reminders:
        DD = tasks["reminder"]
        if DD is not None:
            DD = format_date_to_print(DD)
            ND = datetime.strptime(DD,'%Y-%m-%d %H:%M')
            alert_times[tasks["id"]] = ND
            channel_ids[tasks["id"]] = 1094031740462436446
    bot.loop.create_task(check_alerts())

@bot.event
async def on_message(message):
    print(message.content)
    await bot.process_commands(message)

@bot.command(name = 'create_task', help = 'Creates a task')
async def task_creation(ctx, *args):
    if not args:
        await ctx.send("No task name given")
        return

    title = " ".join(args)
    guild_id = ctx.guild.id

    url =  f'{baseurl}/task'
    response = requests.post(url=url, data={"title": title, 'guild' : guild_id})
    id = json.loads(response.text)['id']
    
    if response.status_code == 201:
        await ctx.send(f"The task \"{title}\" has been created with id {id}!")
    else:
        await ctx.send("An error occured when trying to create the task")

def is_task_available(ctx, id):
    '''
    return true if the task exists and is available to the user
    return false if the tasks does not exist or is from another
    server
    '''
    task = json.loads(requests.get(url=f'{baseurl}/task/{id}').text)
    guild_id = ctx.guild.id

    if 'id' not in task or task['guild'] != guild_id:
        return False
    
    return True


@bot.command(name = 'delete_task', help = 'Deleted a task')
async def task_delete(ctx, id):
    url = f'{baseurl}/task/{id}'
    guild_id = ctx.guild.id

    if not is_task_available(ctx, id):
        await ctx.send(f'Task with id {id} does not exist')
        return
    
    r = requests.delete(url=url)
    print(r)
    
    if r.status_code == 204:
        await ctx.send(f'Task with id {id} deleted')
    else:
        await ctx.send("An error occured when trying to delete task")

'''Command for adding due date alerts for a task'''
@bot.command(name = 'add_alert', help = '!add_alert <task id> <YYYY-MM-DD HH:MM>  Command for adding due date alerts for a task')
async def add_alert(ctx, id=None, alert=None):

    url =  f'{baseurl}/reminder/{id}'
    
    if alert is None: # no alert given
        response = requests.get(url=url)
        if response.status_code == 200:
            await ctx.send(response.text)
        else:
            await ctx.send(f"No task found with that {id}")
    elif id is None:# no idea is given
        await ctx.send("No Task ID Given")
    else:#all is good
        alert_dt = datetime.strptime(alert, '%Y-%m-%d %H:%M')
        alert_times[id]=alert_dt
        data = {"reminder": alert_dt}
        channel_ids[id] = ctx.channel.id
        response = requests.put(url, data=data)

        if response.status_code == 200:
            await ctx.send("Alert has been assigned to the task!")
        else:
            await ctx.send("A problem occurred when trying to add an alert") 
        


@bot.command(name = 'due_date')
async def due_date(ctx, id, *args):
    due_date = " ".join(args)

    if not is_task_available(ctx, id):
        await ctx.send(f'Task with id {id} does not exist')
        return

    url = f'{baseurl}/due-date/{id}'
    data = {"due_date": due_date}
    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        await ctx.send(f'Task {id} due date set to **{due_date}**')
    else:
        await ctx.send("Due date must be in format YYYY-MM-DD HH:MM")


def silence_mention(mention: str):
    if '&' in mention:
        return mention
    else:
        mention = mention[:2] + '&' + mention[2:]
        return mention


@bot.command(name = 'assign_user')
async def assign_user(ctx: discord.abc.Messageable, id = None, *args):
    
    if id is None or not id.isdigit():
        await ctx.send("Must provide id")
        return

    if not args:
        await ctx.send("No assignees given")
        return

    if not is_task_available(ctx, id):
        await ctx.send(f'Task with id {id} does not exist')
        return
   
    url = f'{baseurl}/assignees/{id}'

    assignees = [*args]
    data = {"assignees": assignees}
    response = requests.put(url=url, data=data)

    no_mentions = discord.AllowedMentions.none()

    if response.status_code == 200:
        await ctx.send(f"[{' '.join(assignees)}] have been assigned to the task!", allowed_mentions=no_mentions)
    if response.status_code == 400:
        duplicates = json.loads(response.text)['duplicate_users']
        await ctx.send(f'{" ".join(duplicates)} are already assigned to the task', allowed_mentions=no_mentions)


'''Command for listing all tasks by order of due date'''
@bot.command(name = 'list_tasks', help = '!list_tasks  Command for listing all tasks by order of due date')
async def list_tasks(ctx):
   
    url = f'{baseurl}/task?guild={ctx.guild.id}'
    response = requests.get(url=url)

    if response.status_code != 200:
        await ctx.send("No Tasks found")
    else:
        for t in json.loads(response.text):
            dd= t["due_date"]
            if dd is not None:#formatting the due date
                dd = format_date_to_print(dd)
            ad = t["reminder"]
            if ad is not None:#formatting the alert
                ad = format_date_to_print(ad)
            await ctx.send(f'id: {t["id"]}, {t["title"]}, {t["assignees"]}, {dd}, {ad}')


'''Command for listing all tasks associated with the given user'''
@bot.command(name = 'list_tasks_by_user', help = 'list_tasks_by_user <user id>  Command to list all tasks associated with a given user')
async def list_tasks_by_user(ctx, user=None):

    url = f'{baseurl}/task?user={user}&guild={ctx.guild.id}'
    if user is None:
            await ctx.send("No user given")#if not user is given

    response = requests.get(url=url)

    if response.status_code != 200:
        await ctx.send(f"User {user} not found") #if cant find the user/any tasks associated with the user
    else:
        if json.loads(response.text) == []:
            await ctx.send(f"User {user} has no tasks")
        for t in json.loads(response.text):
            dd= t["due_date"]
            if dd is not None: #formatting the due date
                dd = format_date_to_print(dd)
            ad = t["reminder"]
            if ad is not None:#formatting the alert
                ad = format_date_to_print(ad)
            await ctx.send(f'id: {t["id"]}, {t["title"]}, {t["assignees"]}, {dd}, {ad}')


#Function to check if current time matches any alert time
async def check_alerts():
    
    idsToPop = []
    while True:
        current_time = datetime.now()
        for id, alert_time in alert_times.items():
            print("Alert checking")
            print(f"current time: {current_time}, alert time: {alert_time}")
            if current_time >= alert_time:
                print(f"Alerting id: {id}")
                channel = bot.get_channel(channel_ids[id])
                await channel.send(f"@everyone An alert for a task with id: {id} has occured!")
                idsToPop.append(id)
        for ID in idsToPop: #Remove all the ids that have been alerted so we dont Alert more then once
            alert_times.pop(ID)
            channel_ids.pop(ID)
            print(f"Removed {ID} from alert_times and channel_ids")
        idsToPop = []
        await asyncio.sleep(60) # Check every minute

bot.run(TOKEN)