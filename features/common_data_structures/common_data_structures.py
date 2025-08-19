# Adds support for dictating common data structure operations to prevent needing to memorize as many language specific details
# A DataStructures class is provided for organizing operation implementations for a given language
# The vcs_data_structures_update action must be overwritten for each language to provide the appropriate implementations
from talon import Module, actions, Context

from typing import TypedDict, Callable, Optional
from ...shared.described_lambdas import create_described_insert_between, create_described_snippet_insertion

# Defines the type for operator implementations
Operator = str | Callable[[], None]

class DataStructures(TypedDict, total=False):
	"""Organizes common data structure operations for a specific programming language"""

	# The name of the programming language. 
	LANGUAGE: str

	# These operators are for dynamic array data structures like Python's list and Java's ArrayList
	# The operation for adding an element to the end of a list
	LIST_ADD: Operator
	# The operation for removing the last element from a list
	LIST_POP: Operator
	# The operation for changing an element at a specific index in a list
	LIST_CHANGE: Operator
	# The operation for removing an element at a specific index in a list
	LIST_REMOVE: Operator
	# The operation for getting an element at a specific index in a list
	LIST_GET: Operator
	# The operation for creating a new list
	LIST_NEW: Operator

	# These operators are for associative map data structures like Python's dict and JavaScript's Map
	# The operation for adding a key-value pair to a map
	MAP_ADD: Operator
	# The operation for changing the value of associated with a specific key in a map
	MAP_CHANGE: Operator
	# The operation for removing a key-value pair from a map
	MAP_REMOVE: Operator
	# The operation for getting the value associated with a specific key in a map
	MAP_GET: Operator
	# The operation for checking if a key exists in a map
	MAP_CONTAINS: Operator
	# The operation for creating a new map
	MAP_NEW: Operator

	# These operators are for set data structures like Python's set and Java's Set
	# The operation for adding an element to a set
	SET_ADD: Operator
	# The operation for removing an element from a set
	SET_REMOVE: Operator
	# The operation for checking if an element exists in a set
	SET_CONTAINS: Operator
	# The operation for creating a new set
	SET_NEW: Operator

	# These operators are for tuple data structures like Python's tuple
	# The operation for creating a new tuple
	TUPLE_NEW: Operator
	# The operation for getting an element at a specific index in a tuple
	TUPLE_GET: Operator

# Global variable to hold the current DataStructures. This should not be accessed directly outside this file
structures: Optional[DataStructures] = None

module = Module()

module.list('vcs_common_data_structure_name', desc='Active language list of common data structure names')
module.list('vcs_common_data_structure_operation', desc='Active language list of common data structure operation names')
module.tag('vcs_common_data_structure')

@module.action_class
class Actions:
	def vcs_data_structures_update():
		'''Updates the current methods object based on the active programming language. This should be overwritten on a per language basis to update the global structures variable if actions.user.vcs_data_structures_should_update with the name of the language returns true'''
		pass

	def vcs_data_structures_should_update(language: str):
		'''Checks if the methods object should be updated based on the active programming language'''
		return not structures or structures['LANGUAGE'] != language

	def vcs_data_structures_get() -> Optional[DataStructures]:
		'''Returns the current methods object'''
		return structures

	def vcs_common_data_structure_insert(structure_name: str, operation_name: str):
		'''Inserts a method with the specified name'''
		# Update the structures variable if the language has changed or this is the first call
		actions.user.vcs_data_structures_update()
			
		if structures is None:
			raise ValueError("Common Data Structures object is not initialized.")

		combined_name = f"{structure_name}_{operation_name}"
		if combined_name not in structures:
			raise ValueError(f" '{combined_name}' not found in methods object.")
		operation = structures[combined_name]
		# If the action is callable, just call it. Otherwise assume it is a method name
		if callable(operation):
			operation()
		else:
			# If the active language has no implementation of code_operator_object_accessor, insert "."
			try:
				actions.user.code_operator_object_accessor()
			except:
				actions.insert(".")
			actions.insert(operation)
			# If we ever support a language where method calls do not use parentheses, we will need a different grammar for this
			actions.user.insert_between("(", ")")

javascript_context = Context()
javascript_context.matches = r'''
code.language: javascript
code.language: typescript
code.language: javascriptreact
code.language: typescriptreact
'''

# Inserts a subscript
code_generic_subscript = create_described_insert_between("[", "]")

# This use of snippets does not require a defined .snippet file
# $1 is where the cursor will start. The action for moving to the next snippet will next put the cursor at $0.
code_generic_subscript_update = create_described_snippet_insertion("[$1] = $0")


@javascript_context.action_class("user")
class JavascriptActions:
	def vcs_data_structures_update():
		if actions.user.vcs_data_structures_should_update('javascript'):
			global structures
			structures = DataStructures(
				LANGUAGE = 'javascript',
				LIST_ADD = 'push',
				LIST_POP = 'pop',
				LIST_CHANGE = code_generic_subscript_update,
				LIST_REMOVE = create_described_insert_between('.splice(', ', 1)'),
				LIST_GET = code_generic_subscript,
				LIST_NEW = create_described_insert_between('[', ']'), 

				MAP_ADD = 'set',
				MAP_CHANGE = 'set',
				MAP_REMOVE = 'delete',
				MAP_GET = 'get',
				MAP_CONTAINS = 'has',
				MAP_NEW = create_described_insert_between('new Map(', ')'),

				SET_ADD = 'add',
				SET_REMOVE = 'delete',
				SET_CONTAINS = 'has',
				SET_NEW = create_described_insert_between('new Set(', ')'),

			)

python_context = Context()
python_context.matches = r'''
code.language: python
'''

@python_context.action_class("user")
class PythonActions:
	def vcs_data_structures_update():
		if actions.user.vcs_data_structures_should_update('python'):
			global structures
			structures = DataStructures(
				LANGUAGE = 'python',
				LIST_ADD = 'append',
				LIST_POP = 'pop',
				LIST_CHANGE = code_generic_subscript_update,
				LIST_REMOVE = 'pop',
				LIST_GET = code_generic_subscript,
				LIST_NEW = create_described_insert_between('[', ']'),

				MAP_ADD = code_generic_subscript_update,
				MAP_CHANGE = code_generic_subscript_update,
				MAP_REMOVE = 'pop',
				MAP_GET = code_generic_subscript,
				MAP_NEW = create_described_insert_between('{', '}'),

				SET_ADD = 'add',
				SET_REMOVE = 'remove',
				SET_NEW = create_described_insert_between('set(', ')'),

				TUPLE_NEW = create_described_insert_between('(', ')'),
				TUPLE_GET = code_generic_subscript,
			)

cpp_context = Context()
cpp_context.matches = r'''
code.language: cpp
code.language: c
'''
@cpp_context.action_class("user")
class CppActions:
	def vcs_data_structures_update():
		language = 'c++'
		if actions.user.vcs_data_structures_should_update(language):
			global structures
			structures = DataStructures(
				LANGUAGE = language,
				LIST_ADD = 'emplace_back',
				LIST_POP = 'pop_back',
				LIST_CHANGE = create_described_snippet_insertion(".at($1) = $0"),
				LIST_REMOVE = 'erase',
				LIST_GET = 'at',

				MAP_ADD = 'emplace',
				MAP_CHANGE = 'emplace',
				MAP_REMOVE = 'erase',
				MAP_GET = 'at',
				MAP_CONTAINS = create_described_insert_between('.count(', ') != 0'),

				SET_ADD = 'insert',
				SET_REMOVE = 'erase',
				SET_CONTAINS = create_described_insert_between('.count(', ') != 0'),
			)