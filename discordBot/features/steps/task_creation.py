import os
from behave import *
from dotenv import load_dotenv
from test_utils.test_bot_commands import TestBotCommands
from hamcrest import assert_that, equal_to

@given(u'a user')
def step_impl(context):
    load_dotenv()
    TOKEN = os.environ['TEST_TOKEN']
    context.commands = TestBotCommands(TOKEN)


@when(u'the user inputs "{command}"')
def step_impl(context, command):
    context.commands.send_message(command)


@then(u'the bot responds with "{reply}"')
def step_impl(context, reply):
    message = context.commands.read_reply()['content']
    assert_that(message, equal_to(reply))






