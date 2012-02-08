# Story #24580365

Feature: Anyone can see the app directory
  As a user or visitor
  I want to see the app directory
  So that I can decide which app I can deploy for my purposes

  Scenario: Anyone can see the app directory
    Given I have previously registered for an account
      And the following apps have been created
        | Name       |
        | First App  |
        | Second App |
        | Third App  |
        | Fourth App |
     When I follow the "Applications" link
     Then I see a directory of the following apps
        | Name       |
        | First App  |
        | Second App |
        | Third App  |
        | Fourth App |
