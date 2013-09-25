# Story #24719377

Feature: A user can issue a challenge
  As a user
  I can issue a challenge to the CfA staff (admin)
  So that they can suggest an app for my needs or issue a request for the app to be developed

  Background:
    Given that the location "Random Location" has been defined

  @javascript
  Scenario: A user submits a form to issue a challenge
    Given I have registered for an account with "testman@example.com"
     When I fill out a challenge form
     Then I am notified that my challenge has been sent to the CfA staff

  Scenario: Only users can submit a challenge form
    Given I am on the homepage
     Then I can not see "Submit a challenge"
