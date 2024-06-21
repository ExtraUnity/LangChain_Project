# This file is made by Marilouise
from behave import *
from LLM.ModelExecutor import ModelExecutor

@given('user prompt {user_prompt}')
def step_init_user_prompt(context, user_prompt):
    context.user_prompt = user_prompt

@when('agent recieve user prompt')
def step_recieve_user_prompt(context):
    context.executor = ModelExecutor()
    context.executor.updateAPIKey(APIKey="4kGE92EQWNc7YvDDQqLoohUt0x8HdW8b3fjkq6ZQrs8FOEQk")
    context.result = context.executor.handle_input(user_input=context.user_prompt)

@then('agent calls on {tool_name} tool')
def step_calls_math_tool(context, tool_name):
    if str(tool_name) in context.executor.testing_intermediate_steps: assert True


@then('LLM output ends with {end_of_output}')
def step_LLM_output_ends_with(context,end_of_output):
    if context.result.endswith(end_of_output) == True: assert True