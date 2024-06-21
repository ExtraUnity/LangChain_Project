# This file is made by Marilouise
Feature: LLM making tool calls when required by the user prompt

Scenario: LLM calls the mathematics() tool from prompt containing simple equation
    Given user prompt "What is 1 + 2 * 3?"
    When agent recieve user prompt 
    Then agent calls on mathmematics tool
    Then LLM output ends with "1 + 2 * 3 is 7"

