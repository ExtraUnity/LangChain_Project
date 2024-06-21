# This file is made by Marilouise
import os
from behave import *
from LLM.ModelExecutor import ModelExecutor
from langchain_fireworks import ChatFireworks

@given('a model executor has been initalized')   
def step_init_model_executor(context):
    context.executor = ModelExecutor() 

@given('{api_key} is a valid Api key')
def step_api_key_is_valid(context, api_key):
    context.new_key = api_key
    try: 
        os.environ["FIREWORKS_API_KEY"] = api_key
        llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)   
        llm.invoke("test")
        assert True
    except:
        assert False
    
@given('{api_key} is an invalid Api key')
def step_api_key_is_invalid(context, api_key):
    context.new_key = api_key
    try:
        os.environ["FIREWORKS_API_KEY"] = api_key
        llm = ChatFireworks(model="accounts/fireworks/models/firefunction-v1", temperature=0)   
        llm.invoke("test")
        assert False
    except:
        assert True

@when('register API key')
def step_register_new_api_key(context):
    context.api_result = context.executor.updateAPIKey(context.new_key)

@then('API key accepted')
def step_accept_new_api_key(context):
    assert (context.api_result)

@then('API key denied')
def step_accept_new_api_key(context):
    assert (context.api_result==False)