# Fotogalleri - FAFA

<p align="center">
    <img
        src="https://raw.githubusercontent.com/Teknologforeningen/fotogalleri/master/.github/logo_black.svg"
        alt="Fotogalleri Logo"
        style="max-width: 100%;"
    />
</p>

Photo Gallery for [Teknologföreningen](https://tf.fi)

See live version at: [https://foto.tf.fi](https://foto.tf.fi)

## Development

The development tool heavily used is [Make](https://www.gnu.org/software/make/manual/make.html).
You may find all the commands and variables specified here in the `Makefile`.

### Rules

To run the development server:

    make serve

To run tests:

    make test

To run the linter:
    
    make lint

To make Django migrations run:

    make migrations

To migrate the database:

    make migrate

To clean the project:

    make clean

To clean *everything* in the project (includes the virtualenvironment):

    make clean-all

### Creating a Python virtual environment

To create a virtualenvironment for the project:

    make bin/python

This will also install all requirements from the requirements file specified by the `REQUIREMENTS_FILE` variable (defaults to `requirements.txt`).
    
*This is set as a [prerequisite](https://raw.githubusercontent.com/c00k133/neergaard.fi/master/.title.png) to other [rules](https://raw.githubusercontent.com/c00k133/neergaard.fi/master/.title.png), so you do not need to explicitly run it, it is always checked before any other command.*

**Note:** the rule uses a variable named `PYTHON_EXECUTABLE` to determine which Python version to use (defaults to `/usr/bin/python3`).
If you want to change this (e.g. your `/usr/bin/python3` points to another version than in the requirements) you may specify it as follows:

    make PYTHON_EXECTUABLE=<path/to/python/executable> bin/python

### Example workflow

#### Setup

Let's say you just cloned this repository and want to start hacking.
What you want to do first is to create the virtual environment:

    make bin/python

Then you want to apply all migrations

    make migrate

And finally you can serve the project locally:

    make serve

Now you're ready to start hacking!

*For completeness sake* here is a quick copy-paste for the setup:

    # Create virtual environment
    make bin/python

    # Apply migrations
    make migrate

    # Serve locally
    make serve

#### Pre-PR

Before a PR it is good to check that your local code will pass our reviews.
To do that with your local setup you have to run our tests and then check the linting.
Run the following snippet and your code will be tested and checked for linting errors, run them separately in case something fails:

    # Run tests
    make test

    # Run lint-check
    make lint
