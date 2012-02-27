
Feature: User deploys an application after searching for deployed apps

  Background:
    Given the following apps have been deployed:
      | App Name        | City          | Brigade          |
      | First Test App  | Norfolk, VA   | The Test Brigade |
      | Third Test App  | Norfolk, VA   | The Best Brigade |
      | Second Test App | Reston, VA    | The Last Brigade |
      | Second Test App | Richmond, VA  | The Test Brigade |

  Scenario: User can deploy an different appilication after searching for deployed apps by location
    When I view all of the apps by "Location"
     And I filter the deployed apps to only those that have been deployed in "Norfolk, VA"
    Then I should be able to deploy another application if I choose

  Scenario: User can deploy an different appilication after searching for deployed apps by location
    When I view all of the apps by "Brigade"
     And I filter the deployed apps to only those that have been deployed by "The Test Brigade"
    Then I should be able to deploy another application if I choose
