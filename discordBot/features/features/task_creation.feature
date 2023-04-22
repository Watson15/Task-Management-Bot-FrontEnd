Feature: Task Creation

    Scenario: Successful task creation
        Given a user
        When the user inputs "!create_task new task"
        Then the bot outputs "The task "new task" has been created with id <id>!"

    Scenario: Task creation no title
        Given a user
        When the user inputs "!create_task"
        Then the bot responds with "No task name given"