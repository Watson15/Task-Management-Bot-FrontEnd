Feature: Task Deletion

    Scenario: Delete an existing task
        Given a user
        And an id for a created task
        When the user inputs "!delete_task <id>" with the id of the task
        Then the bot outputs "Task with id <id> deleted"
        And the task with that id is deleted

    Scenario: Delete a non-existant task
        Given a user
        And an id for a task that does not exist
        When the user inputs "!delete_task <id>" with the id of the task
        Then the bot outputs "Task with id <id> does not exist"

    Scenario: User tries to delete a task from another server
        Given a user
        And an id for a task in another server
        When the user inputs "!delete_task <id>" with the id of the task
        Then the bot outputs "Task with id <id> does not exist"