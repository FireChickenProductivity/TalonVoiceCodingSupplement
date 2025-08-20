# Provides support for defining lambda functions that contain an associated documentation string. This is useful for documentation and help system support.

from talon import actions

def describe_function(lambda_function, documentation: str):
	"""Returns the lambda function with the specified documentation string."""
	lambda_function.__doc__ = documentation
	return lambda_function

def create_described_insert_between(left: str, right: str):
	documentation = f"user.insert_between('{left}', '{right}')"
	insert_between = describe_function(lambda: actions.user.insert_between(left, right), documentation)
	return insert_between

def create_described_snippet_insertion(snippet_body: str):
	snippet_insertion = describe_function(lambda: actions.user.insert_snippet(snippet_body), f"Inserts the snippet: {snippet_body}")
	return snippet_insertion
