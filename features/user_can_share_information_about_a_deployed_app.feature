Feature: A user can share information about a deployed application with a social network
  As a user
  I want to be able to share my deployed application with my friends on my social networks
  So that I can spread the word about the deploy

  Background: 
    Given the following apps have been created
      | Name       |
      | First App  |
      | Second App |
      | Third App  |
      | Fourth App |
    And I choose to deploy "First App"
    And I live in "Norfolk, VA"
    And I belong to the brigade "Test Brigade"
    And I successfully deploy the application "First App"

  Scenario: User able to share to their social networks by clicking a button on the deployed app show page
    When I click the button to share the deployed application
    Then I should be able to share with my facebook and twitter networks

