# Purpose

This offers support for dictating common data structure operations in various languages with a common grammar to prevent needing to memorize these details.

# Stability
This is a draft, so the grammar and implementation are not stable and may be revised in response to user feedback.

# Dependencies
The following community actions:
- user.code_operator_object_accessor
- user.insert_between
- user.insert_snippet

# Usage
Dictate the name of a data structure followed by the operation you want to perform to use a data structure operation. For instance, saying `ray add` in python inserts `.append()` and in javascript inserts `.push()`.

See the vcs_common_data_structure_name.talon-list file for the list of data structures and the vcs_common_data_structure_operation.talon-list file for the list of operations.

`help common data structures` shows the supported operators. 

# Supported Languages
The following languages have full support:
- Python
- Java

The following languages have partial support:
- JavaScript
- C++