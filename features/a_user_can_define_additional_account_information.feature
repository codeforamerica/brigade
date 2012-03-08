# Story #24719805

Feature: A user can define additional account information
  As a user
  I want to define additional personal info (location, skills)
  So that I can be found by my personal info

  Background:
    Given I have registered for an account with "testman@example.com"

  @javascript
  Scenario: A user can edit his account information
    When I edit my account information
    Then I see the updated information on my account page

  Scenario: No location is used when a user leaves the select location box with add location
    When I edit my account information and leave the select box on Add Location
    Then I am on the show user page with no location

  Scenario: email is shown when user opts in to helping other civic hackers
    When I edit my email preferences
    Then I see a clickable "testman@example.com" on my account page
