[![CI status](https://github.com/uvic-seng321/bot8-discordbot/actions/workflows/python-app.yml/badge.svg)](https://github.com/uvic-seng321/bot8-discordbot/actions/workflows/python-app.yml)

A discord bot to help with task management

## General info for bot

This is an MVP for a discord task manager bot. The bot allows for creation of tasks, assigning due dates to tasks, alert times to tasks, users to tasks, deleting tasks, and listing tasks. After a task is created, the bot will say what its id is. The ids of tasks can also be seen by listing the tasks. The id of a task is used to set other properties on the task or delete it.

**Important**: The bot is being hosted and is currently online. There is no need for you to run any files to interact with the bot. Automatic GUI testing is still available and will test the hosted bot. Instructions are below

## Steps for manual testing / demo: 

1. If you do not have a discord account, create one [here](https://discord.com/register)

2. Join the main discord server [here](https://discord.gg/XEB8DKJHCv). This is where you are able to interact with the bot itself to test its functionality

3. Go into the text channel `for-ta` and type in "!help". This will give you a list of commands that you can use to interact with the bot.

## Steps for GUI testing:

1. Clone repo

2. Install requirements
```
pip install -r requirements.txt
```

3. cd into discordBot directory
```
cd discordBot
```

4. Run tests
```
behave
```
**Note**: the first tests which run are very slow since they test the alert functionality which check for alerts which have passed. The next tests will run much faster

After running the behave command the tests will begin to execute. The tests are sending requests to the bot in real time, and reading its responses. You can see this happening in the `bot-testing` channel in the test server which you can join [here](https://discord.gg/XDkcn3AdSb)

## Example usage of the bot

```
!create_task Complete hw 2
```
bot responds: `The task "Complete hw 2" has been created with id 2!`

```
!assign_user 2 @someUser
```
bot responds: `[@someUser] have been assigned to the task!`

```
!list_tasks
```
bot responds: `id: 2, Complete hw 2, [@someUser], None, None`


Put time in Military time ex) 5:30 PM = 17:30 


