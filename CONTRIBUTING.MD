# Contributing

## Language

Default language for naming variables and programming: english
Default language for interface and templates : french
Default language for wiki : english

## Commit Message

The default template for commit message is :
```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```
The header is mandatory and the scope optional.
If a commit is revertig another one, it must begin with revert: and the body must be "This commit reverts <hash>"

### Type
Must be one of the following
* docs : Documentation only changes
* feat : a new feature
* fix : a bug fix
* perf : a code change that improves performance
* refactor: A code change that neither fixes a bug nor adds a feature
* style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)

### Scope
Must be one the following :
* gestion : if the changes are in the 'gestion' app
* documents : if the changes are in the 'documents' app
* aloes : if the changes are in the 'aloes' app
* acl : if the changes are ACL only

### Subject
The subject contains a small summary of the commit :
* use the imperative
* don't capitalize the first letter
* don't use the point (.)

### Body
Longer description of the commit. Use the imperative.

### Footer
The footer should contain any information about Breaking Changes and is also the place to reference GitHub issues that this commit closes.

## Changelog
The chanlog is changed when a new tag is created, to indicate the breaking changes with the previous tag (version).

## Some simple rules
* test your code
* use branches
* write documentation
* in case of fire : git commit; git push; exit
