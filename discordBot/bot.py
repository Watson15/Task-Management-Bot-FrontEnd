import os
from dotenv import load_dotenv
import discord
from test_utils.testable_bot import TestableBot
import requests
import json
from datetime import datetime
import asyncio

alert_times = {} #Dictionary of alert times to be checked by the bot every minute Key=id and Value=alert time
# backend currently must be hosted locally
baseurl = 'https://321-hosted-backend.jack-klob.repl.co'

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

bot = TestableBot(intents=discord.Intents.all(), command_prefix='!')
channel_id = 1094137655568105522 # Replace with your channel ID

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to the server")
    channel = bot.get_channel(1094137655568105522)
    await channel.send("Running")
    url = f'{baseurl}/task'
    response = requests.get(url=url)
    reminders = json.loads(response.text)
    #at start of Discord bot run time, check for any tasks that have a reminder and add them to the alert_times dictionary
    for tasks in reminders:
        DD = tasks["reminder"]
        if DD is not None:
            DD = DD.replace("T", " ")
            DD = DD.replace("Z", "")
            DD = DD.replace(":00", "")
            ND = datetime.strptime(DD,'%Y-%m-%d %H:%M')
            alert_times[tasks["id"]] = ND
    bot.loop.create_task(check_alerts())

@bot.command(name = 'create_task', help = 'Creates a task')
async def task_creation(ctx, *args):
    if not args:
        await ctx.send("No task name given")
        return

    title = " ".join(args)
    guild_id = ctx.guild.id

    url =  f'{baseurl}/task'
    response = requests.post(url=url, data={"title": title, 'guild' : guild_id})
    
    if response.status_code == 201:
        await ctx.send(f"The task \"{title}\" has been created!")
    else:
        await ctx.send("An error occured when trying to create the task")

@bot.command(name = 'delete_task', help = 'Deleted a task')
async def task_delete(ctx, id):
    url = f'{baseurl}/task/{id}'
    guild_id = ctx.guild.id

    task = json.loads(requests.get(url=url).text)

    if 'id' not in task or task['guild'] != guild_id:
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
        response = requests.put(url, data=data)

        if response.status_code == 200:
            await ctx.send("Alert has been assigned to the task!")
        else:
            await ctx.send("A problem occurred when trying to add an alert") 
        


@bot.command(name = 'due_date')
async def due_date(ctx, id, *args):
    url = f'{baseurl}/task/{id}'
    due_date = " ".join(args)
    guild_id = ctx.guild.id
    task = json.loads(requests.get(url=url).text)

    if 'id' not in task or task['guild'] != guild_id:
        await ctx.send(f'Task with id {id} does not exist')
        return

    url = f'{baseurl}/due-date/{id}'
    data = {"due_date": due_date}
    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        await ctx.send(f'Task {id} due date set to **{due_date}**')
    else:
        await ctx.send("Due date must be in format YYYY-MM-DD HH:MM")
    

'''Command for assigning users to a task'''
@bot.command(name = 'assign_user')
async def assign_user(ctx: discord.abc.Messageable, id, args):

    url = f'{baseurl}/assignees/{id}'

    if args is None:
        await ctx.send("No assignees given")
        return

    assignees = [args]
    #user_ids = [username[2:-1] for username in assignees]
    #print(user_ids)
    print(assignees)

    data = {"assignees": assignees}
    print(f"data: {data}")
    response = requests.put(url=url, data=data)

    no_mentions = discord.AllowedMentions.none()

    print(response)
    print(response.text)

    if response.status_code == 200:
        await ctx.send(f"assignees: {assignees} have been assigned to the task!", allowed_mentions=no_mentions)
    else:
        await ctx.send("A problem occurred when trying to add a assignees")


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
                dd = dd.replace("T", " ")
                dd = dd.replace("Z", "")
                dd = dd.replace(":00", "")
            ad = t["reminder"]
            if ad is not None:#formatting the alert
                ad = ad.replace("T", " ")
                ad = ad.replace("Z", "")
                ad = ad.replace(":00", "")
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
                dd = dd.replace("T", " ")
                dd = dd.replace("Z", "")
                dd = dd.replace(":00", "")
            ad = t["reminder"]
            if ad is not None:#formatting the alert
                ad = ad.replace("T", " ")
                ad = ad.replace("Z", "")
                ad = ad.replace(":00", "")
            await ctx.send(f'id: {t["id"]}, {t["title"]}, {t["assignees"]}, {dd}, {ad}')


#Function to check if current time matches any alert time
async def check_alerts():
    channel = bot.get_channel(channel_id)
    idsToPop = []
    while True:
        current_time = datetime.now()
        for id, alert_time in alert_times.items():
            print("Alert checking")
            print(f"current time: {current_time}, alert time: {alert_time}")
            if current_time >= alert_time:
                print(f"Alerting id: {id}")
                await channel.send(f"@everyone An alert for a task with id: {id} has occured!")
                idsToPop.append(id)
        for ID in idsToPop: #Remove all the ids that have been alerted so we dont Alert more then once
            alert_times.pop(ID)
            print(f"Removed {ID} from alert_times")
        idsToPop = []
        await asyncio.sleep(60) # Check every minute

bot.run(TOKEN)