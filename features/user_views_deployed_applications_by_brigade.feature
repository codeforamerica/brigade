# Story #24737339

Feature: A user views a list of all deployed apps by brigade
  As a user
  I want to view all of the deployed apps related to a brigade
  So that I can quickly see what activities my brigade is undertaking so I'm able to help

  Background:
    Given the following apps have been deployed:
      | App Name        | City          | Brigade          |
      | First Test App  | Norfolk, VA   | The Test Brigade |
      | Third Test App  | Norfolk, VA   | The Best Brigade |
      | Second Test App | Reston, VA    | The Last Brigade |
      | Second Test App | Richmond, VA  | The Test Brigade |
    And I view all of the apps by "Brigade"


  Scenario: User views all deployed applications before selecting a specific city
    Then I should see the following applications:
      | App Name        | City         | Brigade          |
      | First Test App  | Norfolk, VA  | The Test Brigade |
      | Third Test App  | Norfolk, VA  | The Best Brigade |
      | Second Test App | Reston, VA   | The Last Brigade |
      | Second Test App  | Richmond, VA | The Test Brigade |

  Scenario: User filters the deployed apps by a specific city
    When I filter the deployed apps to only those that have been deployed by "The Test Brigade"
    Then I should see the following applications:
      | App Name        | City         | Brigade          |
      | First Test App  | Norfolk, VA  | The Test Brigade |
      | Second Test App | Richmond, VA | The Test Brigade |
     But I should not see the following applications:
      | App Name        | City        | Brigade          |
      | Second Test App | Reston, VA  | The Last Brigade |
      | Third Test App  | Norfolk, VA | The Best Brigade |

  Scenario: User filters the deployed apps by a city that has no applications
    When I filter the deployed apps to only those that have been deployed by "Joe's Brigade"
    Then I should be informed that there are no applications deployed by "Joe's Brigade"

   Scenario: User searches through the deployed applications for a specific city
    When I filter the deployed apps to only those that have been deployed by "The Test Brigade"
     And I search for all applications named "First Test App"
    Then I should see the following applications:
      | App Name        | City         | Brigade          |
      | First Test App  | Norfolk, VA  | The Test Brigade |
