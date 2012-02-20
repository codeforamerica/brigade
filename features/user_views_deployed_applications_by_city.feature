# Story #24736665

Feature: A user views a list of all deployed apps in their city
  As a user
  I want to view all of the deployed apps related to a city
  So that I can quickly see how I can help more effectively in the place I live

  Background:
    Given the following apps have been deployed:
      | App Name        | City          | Brigade          |
      | First Test App  | Norfolk, VA   | The Test Brigade |
      | Third Test App  | Norfolk, VA   | The Best Brigade |
      | Second Test App | Reston, VA    | The Last Brigade |
      | First Test App  | Richmond, VA  | The Test Brigade |
    And I view all of the apps by "City"


  Scenario: User views all deployed applications before selecting a specific city
    Then I should see the following applications:
      | App Name        | City         | Brigade          |
      | First Test App  | Norfolk, VA  | The Test Brigade |
      | Third Test App  | Norfolk, VA  | The Best Brigade |
      | Second Test App | Reston, VA   | The Last Brigade |
      | First Test App  | Richmond, VA | The Test Brigade |

  Scenario: User filters the deployed apps by a specific city
    When I filter the deployed apps to only those that have been deployed in "Norfolk, VA"
    Then I should see the following applications:
      | App Name        | City        | Brigade          |
      | First Test App  | Norfolk, VA | The Test Brigade |
      | Third Test App  | Norfolk, VA | The Best Brigade |
     But I should not see the following applications:
      | App Name        | City         | Brigade           |
      | Second Test App | Reston, VA   | The Last Brigade  |
      | First Test App  | Richmond, VA | The Test Brigade  |

  Scenario: User filters the deployed apps by a city that has no applications
    When I filter the deployed apps to only those that have been deployed in "Suffolk, VA"
    Then I should be informed that there are no applications deployed in "Suffolk, VA"

   Scenario: User searches through the deployed applications for a specific city
    When I filter the deployed apps to only those that have been deployed in "Norfolk, VA"
     And I search for all applications named "First Test App"
    Then I should see the following applications:
      | App Name        | City         | Brigade          |
      | First Test App  | Norfolk, VA  | The Test Brigade |
