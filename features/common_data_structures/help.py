# This module defines support for displaying help information for the common data structure operations

from talon import Module, actions
from typing import TypedDict, Callable, Optional

module = Module()

@module.action_class
class Actions:
	def vcs_help_data_structures():
		"""Shows the current vcs help interface for the common data structure support"""
		title = "Common Data Structures"
		actions.user.vcs_data_structures_update()
		structures: Optional[TypedDict] = actions.user.vcs_data_structures_get()
		if structures is None:
			actions.user.vcs_help_set(title, ["No operations are available for the current context."])
		else:
			help_text = []
			for name, operation in structures.items():
				if callable(operation):
					help_text.append(f"{name}(): {operation.__doc__ or 'No documentation available.'}")
				else:
					help_text.append(f"{name}: {operation}")
			help_text.sort()
			actions.user.vcs_help_set(title, help_text)
