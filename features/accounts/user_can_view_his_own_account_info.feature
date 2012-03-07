Feature: A user can view his profile

  Background:
    Given I have registered for an account with "thomas@mail.com"
    And "thomas@mail.com" is part of the "Awesome" brigade
    When I go to my profile as "thomas@mail.com"

  Scenario: I should see my profile data
    Then I should see the "Awesome" brigade
