from talon import Module, actions, Context

from typing import TypedDict, Callable, Optional

Operator = str | Callable[[], None]

class DataStructures(TypedDict, total=False):
	LANGUAGE: str

	LIST_ADD: Operator
	LIST_POP: Operator
	LIST_CHANGE: Operator
	LIST_REMOVE: Operator
	LIST_GET: Operator
	LIST_NEW: Operator

	MAP_ADD: Operator
	MAP_CHANGE: Operator
	MAP_REMOVE: Operator
	MAP_GET: Operator
	MAP_CONTAINS: Operator
	MAP_NEW: Operator

	SET_ADD: Operator
	SET_REMOVE: Operator
	SET_CONTAINS: Operator
	SET_NEW: Operator

	TUPLE_NEW: Operator
	TUPLE_GET: Operator

structures: Optional[DataStructures] = None

module = Module()

module.list('voice_coding_supplement_common_data_structure_name', desc='Active language list of common data structure names')
module.list('voice_coding_supplement_common_data_structure_operation', desc='Active language list of common data structure operation names')

@module.action_class
class Actions:
	def voice_coding_supplement_methods_update():
		'''Updates the current methods object based on the active programming language'''
		pass

	def voice_coding_supplement_methods_should_update(language: str):
		'''Checks if the methods object should be updated based on the active programming language'''
		return not structures or structures['LANGUAGE'] != language

	def voice_coding_supplement_methods_get() -> Optional[DataStructures]:
		'''Returns the current methods object'''
		return structures

	def voice_coding_supplement_common_data_structure_insert(structure_name: str, operation_name: str):
		'''Inserts a method with the specified name'''
		actions.user.voice_coding_supplement_methods_update()
			
		if structures is None:
			raise ValueError("Common Data Structures object is not initialized.")

		combined_name = f"{structure_name}_{operation_name}"
		if combined_name not in structures:
			raise ValueError(f" '{combined_name}' not found in methods object.")
		operation = structures[combined_name]
		if callable(operation):
			operation()
		else:
			try:
				actions.user.code_operator_object_accessor()
			except:
				actions.insert(".")
			actions.insert(operation)
			actions.user.insert_between("(", ")")

javascript_context = Context()
javascript_context.matches = r'''
code.language: javascript
code.language: typescript
'''

def code_generic_subscript():
	actions.user.insert_between("[", "]")

def code_generic_subscript_update():
	actions.user.insert_snippet("[$1] = $0")
	

@javascript_context.action_class("user")
class JavascriptActions:
	def voice_coding_supplement_methods_update():
		if actions.user.voice_coding_supplement_methods_should_update('javascript'):
			global structures
			structures = DataStructures(
				LANGUAGE = 'javascript',
				LIST_ADD = 'push',
				LIST_POP = 'pop',
				LIST_CHANGE = code_generic_subscript_update,
				LIST_REMOVE = lambda: actions.user.insert_between('.splice(', ', 1)'),
				LIST_GET = code_generic_subscript,
				LIST_NEW = lambda: actions.user.insert_between('[', ']'), 

				MAP_ADD = 'set',
				MAP_CHANGE = 'set',
				MAP_REMOVE = 'delete',
				MAP_GET = 'get',
				MAP_CONTAINS = 'has',
				MAP_NEW = lambda: actions.user.insert_between('new Map(', ')'),

				SET_ADD = 'add',
				SET_REMOVE = 'delete',
				SET_CONTAINS = 'has',
				SET_NEW = lambda: actions.user.insert_between('new Set(', ')'),

			)

python_context = Context()
python_context.matches = r'''
code.language: python
'''

@python_context.action_class("user")
class PythonActions:
	def voice_coding_supplement_methods_update():
		if actions.user.voice_coding_supplement_methods_should_update('python'):
			global structures
			structures = DataStructures(
				LANGUAGE = 'python',
				LIST_ADD = 'append',
				LIST_POP = 'pop',
				LIST_CHANGE = code_generic_subscript_update,
				LIST_REMOVE = 'pop',
				LIST_GET = code_generic_subscript,
				LIST_NEW = lambda: actions.user.insert_between('[', ']'),

				MAP_ADD = code_generic_subscript_update,
				MAP_CHANGE = code_generic_subscript_update,
				MAP_REMOVE = 'pop',
				MAP_GET = code_generic_subscript,
				MAP_NEW = lambda: actions.user.insert_between('{', '}'),

				SET_ADD = 'add',
				SET_REMOVE = 'remove',
				SET_NEW = lambda: actions.user.insert_between('set(', ')'),

				TUPLE_NEW = lambda: actions.user.insert_between('(', ')'),
				TUPLE_GET = lambda: actions.user.insert_between('[', ']'),
			)

cpp_context = Context()
cpp_context.matches = r'''
code.language: cpp
code.language: c
'''
@cpp_context.action_class("user")
class CppActions:
	def voice_coding_supplement_methods_update():
		language = 'c++'
		if actions.user.voice_coding_supplement_methods_should_update(language):
			global structures
			structures = DataStructures(
				LANGUAGE = language,
				LIST_ADD = 'emplace_back',
				LIST_POP = 'pop_back',
				LIST_CHANGE = lambda: actions.user.snippet_insert(".at($1) = $0"),
				LIST_REMOVE = 'erase',
				LIST_GET = 'at',

				MAP_ADD = 'emplace',
				MAP_CHANGE = 'emplace',
				MAP_REMOVE = 'erase',
				MAP_GET = 'at',
				MAP_CONTAINS = lambda: actions.user.insert_between('.count(', ') != 0'),

				SET_ADD = 'insert',
				SET_REMOVE = 'erase',
				SET_CONTAINS = lambda: actions.user.insert_between('.count(', ') != 0'),
			)