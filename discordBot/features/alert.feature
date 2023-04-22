Feature: Alert Functionality

    Scenario: User creates an alert
        Given a user 
        And an id for a created task
        When the user inputs <!add_alert <id>  "2077-04-09 11:55"> with the id of a task
        Then the bot outputs "Alert has been assigned to the task!"
        
    @slow
    Scenario: Alert message is sent
        Given a user
        And an id for a created task
        And the task with id <id> has an alert time of "2023-04-09 11:55" added (a time in the past)
        When the user waits '90' seconds
        Then the bot outputs "@everyone An alert for a task with id: <id> has occured!"