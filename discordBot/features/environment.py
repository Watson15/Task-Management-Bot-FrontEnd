from behave import *
from test_utils.api_connection import APIConnection
from test_utils.test_bot_commands import TestBotCommands
from dotenv import load_dotenv
import os
import time

load_dotenv()
TOKEN = os.environ['TEST_TOKEN']
commands = TestBotCommands(TOKEN)


def before_all(context):
    commands.send_message("-------- **Start of tests** --------")

def before_feature(context, feature):
    time.sleep(0.3)
    commands.send_message(f'**Feature: {feature.name}**')

def before_scenario(context, scenario):
    time.sleep(0.1)
    commands.send_message(f'**Scenario: {scenario.name}**')


def after_all(context):
    APIConnection.delete_all_test_tasks()
    print("Deleted all testing tasks from the database")
    