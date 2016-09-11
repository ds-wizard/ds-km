# Contributing to DS KM

This projects is fully open to all kinds of contribution:

 - **Improvements** - propose and/or implement improvements, give ideas
 - **Bug report** - let us know about encountered problem/bug
 - **Forking** - use our project for building your own questionnaire knowledge model

## Proposing improvement

If you have any idea about improvement of model, validator, guidelines, documentation or other content of project we encourage you to create new issue with "idea" label. Please check if same or related idea is not already in our issues.

You can of course use fork of this repository, implement your improvement and then request pull to our original repository. Even in this case it may be convenient to create an issue to let others know about your work in order to prevent "work collisions". In case of forking, you might be interested in [LICENSE](LICENSE).

## Reporting bugs

Encountered any bug, typo, inefficiency or other bothersome problem? Please report it by creating new issue with label "bug" and detailed information where and how it occurs. Also please check in advance if your bug is not already reported. It the same as proposing ideas just with diffent label ;-)

## Validation

If your changes affect knowledge model or it's schema you should check validity and eventually repair inconsistencies. Validation will also occur automatically after commit to this repository by Travis CI.
Validator tool is built on widely-used testing framework `pytest` (and some extensions). Please do not use `[ci skip]` if you are changing KM data, schema or validator itself.

## Guidelines

For more information check our project [wiki pages](https://github.com/CCMi-FIT/ds-km-core/wiki). Please pay attention to our repository structure guidelines, coding style, general ideas, goals and methodology.

Helpful guidelines and guides to be followed:

 - [Contributing to Open Source on GitHub](https://guides.github.com/activities/contributing-to-open-source/)
 - [Git Style Guide](https://github.com/agis-/git-style-guide/blob/master/README.md#git-style-guide)
 - [Writing Useful Github Issues](https://upthemes.com/blog/2014/02/writing-useful-github-issues/)
