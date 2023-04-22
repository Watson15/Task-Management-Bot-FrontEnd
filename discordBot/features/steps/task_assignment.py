from behave import *

@when(u'the user inputs "!assign_user <id> "testUser"" with the id of the task')
def step_impl(context):
    context.commands.send_message(f'!assign_user {context.id} testUser')