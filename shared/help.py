# This module implements a basic help system

from talon import Module, Context, actions, imgui


help_title: str
help_text: list[str]

@imgui.open(y=0)
def help_gui(gui):
	gui.text(help_title)
	gui.line()
	for line in help_text:
		gui.text(line)
	gui.line()
	if gui.button("Close"):
		actions.user.vcs_help_clear()

module = Module()
context = Context()

module.tag("vcs_help_showing")

@module.action_class
class Actions:
	def vcs_help_clear():
		"""Clears the vcs help system state and hides the active interface"""
		global help_title, help_text
		help_title = ""
		help_text = []
		help_gui.hide()
		context.tags = []

	def vcs_help_get_text() -> list[str]:
		"""Returns the current vcs help text"""
		return help_text

	def vcs_help_set(title: str, text: list[str]):
		"""Sets the vcs help text and title"""
		actions.user.vcs_help_clear()
		global help_title, help_text
		help_title = title
		help_text = text
		help_gui.show()
		context.tags = ["user.vcs_help_showing"]
