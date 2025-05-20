import requests
import json
from behave import given, when, then

@given ('the api endpoint is "{url}"')
def step_set_endpoint(context, url):
    context.url = url

@when('I send a POST request with body')
def step_send_post_request_with_body(context):
    body = json.loads(context.text)
    context.response = request.post