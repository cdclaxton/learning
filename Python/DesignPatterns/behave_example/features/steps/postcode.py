from behave import *

from extractor import Extractor


@given("we have a postcode extractor")
def step_impl(context):
    extractor = Extractor()
    context.fn = extractor.postcode


@when('we send "{text}"')
def step_impl(context, text):
    context.result = context.fn(text)


@when("we send {text}")
def step_impl(context, text):
    context.result = context.fn(text)


@then("it won't return anything")
def step_impl(context):
    assert context.result is None


@then('it will return "{text}"')
def step_impl(context, text):
    assert context.result == text


@then("it will return {text}")
def step_impl(context, text):
    assert context.result == text


@then("it will return ")
def step_impl(context):
    assert context.result is None


@given("a table")
def step_impl(context):
    table = []
    for row in context.table:
        table.append({"id": row["ID"], "text": row["Text"]})

    context.extracted_table = table


@when("we extract postcodes in a table")
def step_impl(context):
    extractor = Extractor()
    for row in context.extracted_table:
        row["result"] = extractor.postcode(row["text"])


@then("we get")
def step_impl(context):
    # Walk through each row in the table provided in the feature test
    for idx, row in enumerate(context.table):
        assert row["ID"] == context.extracted_table[idx]["id"]
        assert row["Text"] == context.extracted_table[idx]["text"]

        if len(row["Result"]) == 0:
            assert context.extracted_table[idx]["result"] is None
        else:
            assert (
                row["Result"] == context.extracted_table[idx]["result"]
            ), f"Expected: {row['Result']}, got {context.extracted_table[idx]['result']}"
