# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Setting up your environment

1. Install pyenv (with python 3.6 or 3.7) and [poetry](https://poetry.eustace.io/). Poetry is a beautiful dependency manager for python.
2. run `poetry install` on the project root (poetry will create a venv for you)
3. run `poetry run pre-commit install` - this will install pre-commit hooks (basically flake8 and black) in order to ensure that the code will meet our standards and
4. run `poetry run pytest` for tests
5. run `poetry shell` for the venv shell
6. run `poetry run <file>` to run the file with the python from the venv poetry created for this project.
7. run `poetry run mkdocs serve` for live development of the docs
8. run `poetry run mkdocs build` to build the docs

if you need to add dependencies: `poetry add x` use `--dev` if you wish to add as a development dependency

## How to make a clean pull request

- Create a personal fork of the project on Github.
- Clone the fork on your local machine. Your remote repo on Github is called `origin`.
- Add the original repository as a remote called `upstream`.
- If you created your fork a while ago be sure to pull upstream changes into your local repository.
- Create a new branch to work on! Branch from `develop`
- Implement/fix your feature, comment your code.
- Follow PEP8.
- Run the tests
- Write or adapt tests as needed.
- Add or change the documentation as needed. (PRs will not be merged without documentation!)
- Squash your commits into a single commit with git's [interactive rebase](https://help.github.com/articles/interactive-rebase). Create a new branch if necessary.
- Push your branch to your fork on Github, the remote `origin`.
- From your fork open a pull request in the correct branch. Target the project's `develop` branch.
- Once the pull request is approved and merged you can pull the changes from `upstream` to your local repo and delete your extra branch(es).

And last but not least: Always write your commit messages in the present tense. Your commit message should describe what the commit, when applied, does to the code – not what you did to the code.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

- The use of sexualized language or imagery and unwelcome sexual attention or
  advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as a physical or electronic
  address, without explicit permission
- Other conduct which could reasonably be considered inappropriate in a
  professional setting
