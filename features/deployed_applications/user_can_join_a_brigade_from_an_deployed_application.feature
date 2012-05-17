Feature: A user can join a brigade from the deployed application page

  Background:
    Given I have previously registered for an account
    And I want to access my account
    And I correctly fill in my email "testman@example.com" and password "password"
    And the following apps have been deployed:
      | App Name | City        | Brigade      |
      | Cool App | Norfolk, VA | Cool Brigade |
    When I view the last deployed app page

  Scenario: I should be able to join and leave the associated brigade
    Then I click the button to join the brigade
    And I should see a message that I am a member of the brigade associated with this deploy

