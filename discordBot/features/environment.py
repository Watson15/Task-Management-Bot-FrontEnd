from behave import *
from test_utils.api_connection import APIConnection

def after_all(context):
    APIConnection.delete_all_test_tasks()
    print("Deleted all testing tasks from the database")
    