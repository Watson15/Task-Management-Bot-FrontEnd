Feature: Task Creation

    Scenario: Successful task creation
        Given a user
        When the user inputs "!create_task new task"
        Then the bot responds with "The task "new task" has been created!"

    Scenario: Task creation no title
        Given a user
        When the user inputs "!create_task"
        Then the bot responds with "No task name given"