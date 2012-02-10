Feature: A visitor signs up using Github
  As a hacker
  I want to be able to sign up for Code For American with my Github profile
  So that I can participate in Code For America without having to create another account

  Scenario: Registration page includes a link for signing up using Github
    Given I am on the homepage
      And I follow the "Sign Up" link
     Then I can sign up using "Github"
