Feature: A visitor signs up using Github
  As a hacker
  I want to be able to sign up for Code For American with my Github profile
  So that I can participate in Code For America without having to create another account

  Background:
    Given I am on the homepage
      And I follow the "Sign Up" link

  Scenario: Registration page includes a link for signing up using Github
     Then I can sign up using "Github"

  Scenario: User registers with github account that has public email address
    Given I have a github account that has a public email address listed
     When I sign up using "Github"
     Then I am on my profile page

  Scenario: User registers with github account that has no public email address
    Given I have a github account that doesn't have a public email address listed
     When I sign up using "Github"
      And I fill in my email address "testman@example.com" when prompted
     Then I am on my profile page

  Scenario: User registers with github account that hos no public name
