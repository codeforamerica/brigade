# Story #24719989

Feature: A user views all civic hackers
  As a user
  I want to find other users
  So that I can find who I can collaborate with on an app

  Background:
    Given the following civic hackers exist:
      | Email                | Location     | Brigade          | Skills         |
      | testman@example.com  | Norfolk, VA  | The Test Brigade | ruby, html     |
      | testgirl@example.com | Richmond, VA | The Best Brigade | javascript, ui |
     And the following apps have been deployed:
      | App Name        | City          | Brigade          |
      | First Test App  | Norfolk, VA   | The Test Brigade |
      | Third Test App  | Norfolk, VA   | The Best Brigade |
      | First Test App  | Richmond, VA  | The Test Brigade |
     And I view all of the civic hackers

  Scenario: User searches for civic hackers based on Application name
   When PENDING Do we include the deployed apps in the fulltext search?
   When I search for all civic hackers who are working on "First Test App"
   Then I should see a list of civic hackers that includes "testman@example.com"

  Scenario: User searches for civic hackers based on Brigade name
   When I search for all civic hackers who are working with "The Best Brigade"
   Then I should see a list of civic hackers that includes "testgirl@example.com"

  Scenario: User search for civic hackers based on skill set
   When I search for all civic hackers who have the skill "ruby"
   Then I should see a list of civic hackers that includes "testman@example.com"

  Scenario: User search for civic hackers but finds none with his query
   When I search for all civic hackers who are working on "Boston Red Sox"
   Then I should be informed that there are no hackers who fit that criteria
