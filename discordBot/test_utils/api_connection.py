import requests
import json

class APIConnection():
    '''
    a small API wrapper to mimic commands from the
    testing bot server. needed to aquire id's of tasks
    created through the BDD tests
    '''

    FAKE_GUILD = -10

    # the server id of the testing server
    _guild_id = 1094137227484856360

    # url where backend is hosted
    _baseurl =  'https://321-hosted-backend.jack-klob.repl.co'

    @classmethod
    def create_task(cls, title, guild=_guild_id):
        url = cls._baseurl + "/task"
        return requests.post(url=url, data={"title": title, 'guild' : guild})
    
    @classmethod
    def get_list_guild(cls, guild=_guild_id):
        url = f'{cls._baseurl}/task?guild={guild}'
        return requests.get(url=url) 
    
    @classmethod
    def get_list_all(cls):
        url = f'{cls._baseurl}/task'
        return requests.get(url=url) 
    
    @classmethod
    def get_task(cls, id):
        url = f'{cls._baseurl}/task/{id}'
        return requests.get(url=url)
    
    @classmethod
    def delete_all_test_tasks(cls):
        tasks = json.loads(cls.get_list_guild().text)
        tasks += json.loads(cls.get_list_guild(guild=cls.FAKE_GUILD).text)
        ids = [task['id'] for task in tasks]
        for id in ids:
            requests.delete(url=f'{cls._baseurl}/task/{id}')
        