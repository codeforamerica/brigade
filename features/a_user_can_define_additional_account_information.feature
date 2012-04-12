# Story #24719805

Feature: A user can define additional account information
  As a user
  I want to define additional personal info (location, skills)
  So that I can be found by my personal info

  Background:
    Given I have registered for an account with "testman@example.com"

  Scenario: A user can edit his account information
    When I edit my account information
    Then I see the updated information on my account page

  Scenario: No location is used when a user leaves the select location box with add location
    When I edit my account information and leave the select box on Add Location
    Then I am on the show user page with no location

  Scenario: email is shown when user opts in to helping other civic hackers
    When I edit my email preferences
    Then I see a clickable "testman@example.com" on my account page

  @javascript
  Scenario: A user defines a new location via the Add Location option in the selct box
    When I create a new location "Random Location" in the location select box
    Then "Random Location" is available in the select box
