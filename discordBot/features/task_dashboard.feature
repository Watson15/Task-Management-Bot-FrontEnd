Feature: Task Dashboard

     Scenario: User lists all tasks by due date
        Given a user 
        And an id for a created task
        When the user inputs "!list_tasks" 
        Then the bot outputs "id: <id>, Created task from test, [], None, None"

    Scenario: User lists all tasks by assignee
        Given a user 
        And an id for a created task
        And a user testUser has been assigned to the task with id <id>
        When the user inputs "!list_tasks_by_user testUser" 
        Then the bot outputs "id: <id>, Created task from test, ['testUser'], None, None"