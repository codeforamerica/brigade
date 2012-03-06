Feature: A user can view details of a deployed application

  Background:
    Given the following apps have been deployed: 
      | App Name | City        | Brigade      |
      | Cool App | Norfolk, VA | Cool Brigade |
    When I view the last deployed app page

  Scenario: I should see details about the brigade
    Then I should see the last deployed application's name

