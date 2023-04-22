Feature: Assign users to tasks

    Scenario: Assign user to task
        Given a user
        And an id for a created task
        When the user inputs "!assign_user <id> "testUser"" with the id of the task
        Then the bot responds with "[testUser] have been assigned to the task!"

    Scenario: Assign user to task which does not exist
        Given a user
        And an id for a task that does not exist
        When the user inputs "!assign_user <id> "testUser"" with the id of the task
        Then the bot outputs "Task with id <id> does not exist"

    Scenario: Assign user to task in different server
        Given a user
        And an id for a task in another server
        When the user inputs "!assign_user <id> "testUser"" with the id of the task
        Then the bot outputs "Task with id <id> does not exist"