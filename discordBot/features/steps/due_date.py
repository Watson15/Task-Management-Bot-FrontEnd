import os
from behave import *
from dotenv import load_dotenv
from test_utils.test_bot_commands import TestBotCommands
from hamcrest import assert_that, equal_to


@when(u'the user inputs <!due_date <id> "{date}"> with the id of a task')
def step_impl(context, date):
    context.commands.send_message(f'!due_date {context.id} {date}')

@then(u'the bot outputs "Task <id> due date set to **2023-04-06 12:15**"')
def step_impl(context):
    reply = context.commands.read_reply()['content']
    expected = f'Task {context.id} due date set to **2023-04-06 12:15**'
    assert_that(reply, equal_to(expected))
