Feature: A user can view details of a brigade on the brigade show page

  Background:
    Given a brigade exists with the name "Norfolk Brigade"
    When I view the brigade "Norfolk Brigade"

  Scenario: I should see details about the brigade
    Then I should see the brigade's name: "Norfolk Brigade"

