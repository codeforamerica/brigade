# Pivotal Story #24582487

Feature: Anyone can see an app show page
  As a user or visitor
  I want to see an app page
  So that I can learn more about the app

  Scenario: Anyone can see the app page
     Given the following apps have been created
        | Name       |
        | First App  |
        | Second App |
        | Third App  |
        | Fourth App |
      Then I can see the "First App" page after followwing the "Applications" link
      Then I can see the number of deploys that the application has
