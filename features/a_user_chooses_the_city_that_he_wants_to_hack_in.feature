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

  Scenario: User views all deployed applications before selecting a specific city
    When I decide that I want to start hacking in "Norfolk, VA"
    Then I should see the following applications:
      | App Name        | City         | Brigade          |
      | First Test App  | Norfolk, VA  | The Test Brigade |
      | Third Test App  | Norfolk, VA  | The Best Brigade |

  Scenario: User views applications not deployed in the location he searches for
    When I decide that I want to start hacking in "Norfolk, VA"
    Then I should see the following undeployed applications:
      | App Name         |
      | Second Test App  |

  Scenario: User enters a city that doesn't yet exist in the system
    When I decide that I want to start hacking in "Boston, MA"
    Then I am on the homepage
