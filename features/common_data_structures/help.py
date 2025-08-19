# This module defines support for displaying help information for the common data structure operations

from talon import Module, actions
from typing import TypedDict, Callable, Optional

module = Module()

@module.action_class
class Actions:
	def vcs_help_data_structures():
		"""Shows the current vcs help interface for the common data structure support"""
		title = "Common Data Structures"
		note = "note: this list does not update automatically when the context changes"
		try:
			actions.user.vcs_data_structures_update()
		# Not implemented means the active context does not have a common data structures implementation
		except NotImplementedError:
			pass
		structures: Optional[TypedDict] = actions.user.vcs_data_structures_get()
		if structures is None:
			actions.user.vcs_help_set(title, [note, "No operations are available for the current context."])
		else:
			help_text = []
			for name, operation in structures.items():
				if callable(operation):
					operation_text = operation.__doc__ or 'No documentation available.'
				else:
					operation_text = operation
				help_text.append(f"{name}: {operation_text}")
			help_text.sort()
			help_text.insert(0, note)
			actions.user.vcs_help_set(title, help_text)
