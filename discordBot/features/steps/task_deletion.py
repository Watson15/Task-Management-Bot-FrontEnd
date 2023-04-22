import os
from behave import *
from dotenv import load_dotenv
from test_utils.test_bot_commands import TestBotCommands
from test_utils.api_connection import APIConnection
from hamcrest import assert_that, equal_to
import json


@given(u'an id for a created task')
def step_impl(context):
    response = json.loads(APIConnection.create_task("Created task from test").text)
    print(response)
    context.id = response['id']

@given(u'an id for a task in another server')
def step_impl(context):
    response = json.loads(APIConnection.create_task("Fake server", APIConnection.FAKE_GUILD).text)
    context.id = response['id']


@given(u'an id for a task that does not exist')
def step_impl(context):
    tasks = json.loads(APIConnection.get_list_all().text)
    if len(tasks) == 0:
        context.id = 100
    else:
        context.id = int(tasks[-1]['id']) + 100



    
@when(u'the user inputs "!delete_task <id>" with the id of the task')
def step_impl(context):
    context.commands.send_message(f'!delete_task {context.id}')
    





@then(u'the bot outputs "Task with id <id> deleted"')
def step_impl(context):
    reply = context.commands.read_reply()['content']
    expected = f'Task with id {context.id} deleted'
    assert_that(reply, equal_to(expected))


@then(u'the task with that id is deleted')
def step_impl(context):
    response = APIConnection.get_task(context.id)
    assert_that(response.status_code, equal_to(404))

@then(u'the bot outputs "Task with id <id> does not exist"')
def step_impl(context):
    reply = context.commands.read_reply()['content']
    expected = f'Task with id {context.id} does not exist'
    assert_that(reply, equal_to(expected))

