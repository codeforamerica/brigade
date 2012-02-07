# Story #24579051

Feature: User logs into account
  As a user
  I want to be able to log into the system
  So that I can use the features that it offers

  Scenario: User successfully logs into account
    Given I have previously registered for an account
      And I want to access my account
     When I correctly fill in my email "testman@example.com" and password "password"
     Then I am on my profile page

  Scenario: User unsuccessfully logs into account
    Given I have previously registered for an account
      And I want to access my account
     When I incorrectly fill in my log in credentials
     Then I should be informed that my log in was unsucessfull and I need to try again
