import re
from behave import *

use_step_matcher("re")

from standardiser import standardise_sortcode


@given("a sort code standardiser")
def step_impl(context):
    context.fn = standardise_sortcode


# One approach to handling optional double quotes around the text without
# using use_step_matcher("re"):
#
# @when("I standardise {text}")
# @when('I standardise "{text}"')


@when('I standardise "?(?P<text>.*?)"?')
def step_impl(context, text):
    context.input = text
    context.result = context.fn(text)


@then("it returns (?P<expected>.*)")
def step_impl(context, expected):
    assert (
        context.result == expected
    ), f"Expected: {expected}, actual: {context.result}, for input: {context.input}"
