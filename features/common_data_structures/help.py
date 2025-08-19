# This module defines support for displaying help information for the common data structure operations

from talon import Module, actions, registry
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
			structure_names = registry.lists["user.vcs_common_data_structure_name"][-1]
			operator_names = registry.lists["user.vcs_common_data_structure_operation"][-1]
			help_text = []
			for name in structure_names:
				internal_structure_name = structure_names.get(name)
				for operator in operator_names:
					combined_text = f"{internal_structure_name}_{operator_names.get(operator)}"
					if combined_text in structures:
						operation = structures[combined_text]
						if callable(operation):
							operation_text = operation.__doc__ or 'No documentation available.'
						else:
							operation_text = operation
						help_text.append(f"{name} {operator}: {operation_text}")

			help_text.sort()
			help_text.insert(0, note)
			actions.user.vcs_help_set(title, help_text)
