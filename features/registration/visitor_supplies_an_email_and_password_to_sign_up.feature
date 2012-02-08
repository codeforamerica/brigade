Feature: A visitor can supply an email address and password to sign up traditionally
  As a visitor
  So that I can access my account
  I want to be able to register using my email address and a specified password

  Background:
    Given I am on the homepage
      And I follow the "Sign Up" link

  Scenario: User successfully registers for code for america
    Given I successfully register with my email "testman@example.com"
     Then I am on my profile page

  Scenario: User unsuccessfully registers for code for america
    Given I unsuccessfully register by not filling in my email
     Then I am notified that the email field can't be blank
