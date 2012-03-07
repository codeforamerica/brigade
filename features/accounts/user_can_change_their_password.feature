Feature: A user can change their password

  Background:
    Given I have registered for an account with "thomas@mail.com"
    When I go to edit my profile as "thomas@mail.com"

  Scenario: I can change my password
    Then I can change my password
    And I am still on my edit profile page for "thomas@mail.com"


