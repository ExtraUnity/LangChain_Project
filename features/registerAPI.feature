# This file is made by Marilouise
Feature: API key registration

Scenario: Valid API key accepted
    Given a model executor has been initalized
    And "4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk" is a valid Api key
    When register API key
    Then API key accepted 

Scenario: Invalid API key denied
    Given a model executor has been initalized
    And "invalid1234" is an invalid Api key
    When register API key
    Then API key denied