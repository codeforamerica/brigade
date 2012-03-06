# Story #24719293

Feature: A user deploys an app
  As a user
  I want to be able to deploy an app
  So that it can be used in my community

  Background:
    Given the following apps have been created
      | Name       |
      | First App  |
      | Second App |
      | Third App  |
      | Fourth App |
    And I have registered for an account with "testman@example.com"
    And I choose to deploy "First App"
    And I live in "Norfolk, VA"
    And I belong to the brigade "Test Brigade"

  Scenario: User is able to deploy a new app
    Then I should be presented with a form that lets me deploy "First App"

  Scenario: User successfully deploys an application specifying an existing brigade
    When I successfully deploy the application "First App"
    Then I should be informed that the application "First App" was deployed successfully by "Test Brigade" in "Norfolk, VA"

  Scenario: User unsuccessfully deploys an application specifying an existing brigade
    When I unsuccessfully deploy the application "First App"
    Then I should be informed that the application was not deployed

  Scenario: Only users can deploy an application
    When I logout and visit the application "First App" page
    Then I can not see "Deploy This App"

  @javascript
  Scenario: User successfully deploys an application after specifying a new brigade
    When I specify a new brigade "We Are Titans Brigade"
    Then I should be informed that the application "First App" was deployed successfully by "We Are Titans Brigade" in "Norfolk, VA"
