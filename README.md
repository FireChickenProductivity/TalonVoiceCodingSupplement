# TalonVoiceCodingSupplement
Under construction talonvoice programming supplemental configuration for useful ideas deemed unsuitable for community. 

# Structure
Unlike the community structure that has functionality separated on a per language basis, the directories under features contain self contained functionality. See the readme for each feature directory for documentation. Every feature requires a tag activation so that you opt into features as you want them (see tags.talon). 

Functionality intended to be used by multiple features is in the `shared` directory. Note that `shared` does not provide any commands. 

# Contributing
If you want to contribute, please submit an issue before submitting any code so you can get feedback on if your proposed changes are suitable for this project. Anything that makes it easier to code by voice that is not too optimized for a single user's workflow may belong here.

Please separate proposed changes into small pull requests to make review easier. A gigantic pull request that would take serious time to review may be ignored.

Each python file should have a comment at the top explaining its purpose.

Each feature directory should have a README.md file explaining the feature's purpose, how to use it, what languages are currently supported (if applicable), any dependencies on external actions or other talon constructs including dependencies on community and cursorless. A stability section for modules that may undergo breaking changes is desired explaining which parts might get changed. 

Please try to avoid unnecessarily complex code and document anything not straightforward. Keep in mind that reviewers need to make sure that your code is not malware and excessively difficult code to understand may be assumed malicious. 

Prefix everything in the talon global namespace with `vcs_` to avoid conflicts.

When a command needs a prefix to avoid potential conflicts, use `sup`, which is short for "supplemental".