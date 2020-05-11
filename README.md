# Fotogalleri - FAFA

<p align="center" style="max-width: 200px">
    <img
        src="https://raw.githubusercontent.com/Teknologforeningen/fotogalleri/master/.github/logo_black.svg?sanitize=true"
        alt="Fotogalleri Logo"
        width="200"
    />
</p>

Photo Gallery for [Teknologföreningen](https://tf.fi)

See live version of the latest release at: [https://foto.tf.fi](https://foto.tf.fi)

------------------------------------------------------------------------------------------------------------------------

## Development

The development tool heavily used is [Make](https://www.gnu.org/software/make/manual/make.html).
You may find all the commands and variables specified here in the `Makefile`.

### Environmental variables

There are _two_ ways to change environmental variables:
1. Copy the file `fotogalleri/.env.example` as `fotogalleri/.env` and change values as needed in the newly copied `fotogalleri/.env` file.
2. Change the default values for environmental variables in `fotogalleri/fotogalleri/settings.py`
    - E.g. to enable thumbnail generation in production do the following change
    ```
    ENABLE_THUMB_QUEUE = env('ENABLE_THUMB_QUEUE', True) -> ENABLE_THUMB_QUEUE = env('ENABLE_THUMB_QUEUE', False)
    ```

##### Enable thumbnail generation

If one wishes to run thumbnail generation when in development one has to set the `ENABLE_THUMB_QUEUE` environmental variable to true.
The variable is false by default to avoid accidental thumbnail generations during production.


### Make Rules

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

------------------------------------------------------------------------------------------------------------------------

## Production

*Note: these production configurations have had the production environment of TF in mind, note that your environment might be setup differently (e.g. deployment).*

###### Note about the ENABLE_THUMB_QUEUE environmental variable

The `ENABLE_THUMB_QUEUE` variable cannot be set dynamically.
To change the variable (and thus enabling thumbnail generation) one has to temporarily turn off the production application while changing the variable.


### First time setup

First and foremost you have to deploy the repository to your server.
There are multiple ways to do this, one way would be to have a production Git remote on your server, to which you can push every release and automate deployment through a `post-receive` hook.

The deployment strategy below assumes you have deployed the application to `/var/www/fotogalleri` and that you've setup a Python virtual environment in the root the of the application directory.


#### Running Fotogalleri

Before starting the production application, check whether your desired and required options are set in `fotogaller/.env`.
An example configuration can be found under `fotogaller/.env.example`.

Anything that spins up a Django application should work, however, only `WSGI` through [Gunicorn](https://gunicorn.org/) has been tested.


#### WSGI

The application is pre-configured to run with `WSGI`, the accompanying file can be found under `fotogalleri/fotogalleri/fotogalleri/wsgi.py`.
To run the `WSGI` application use a `WSGI HTTP server`, in this deployment strategy we use [Gunicorn](https://gunicorn.org/).
You can spin up a Gunicorn instance with, e.g., a `SystemD` service and socket file, and then configure a proxy to this instance from your webserver.

##### Example SystemD service file:

```
[Unit]
Description=gunicorn3 daemon for fotogalleri
Requires=fotogalleri.socket
After=network.target

[Service]
PermissionsStartOnly=True
RuntimeDirectory=fotogalleri
PIDFile=/run/fotogalleri/pid
User=www-data
Group=www-data
WorkingDirectory=/var/www/fotogalleri/fotogalleri
Environment=PYTHONPATH=/var/www/fotogalleri/lib/python3.5/site-packages
ExecStart=/usr/bin/gunicorn3 --pid /run/fotogalleri/pid --timeout 90 fotogalleri.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

##### Example SystemD socket file:

```
[Unit]
Description=gunicorn3 socket for fotogalleri

[Socket]
ListenStream=/run/fotogalleri/socket
ListenStream=0.0.0.0:8888

[Install]
WantedBy=sockets.target
```

*Note the port you set for* `ListenStream`.

#### Static files and serving images

In production mode Django does not serve static files nor images.
The distinction this project uses is that static files are files for the interface itself (e.g. CSS and icons) while images are the images that the gallery actually serves.
This makes the whole project less cluttered and enables you have separation of concerns regarding static images and served images.

##### Static files

The root of all static files are assumed to be under `fotogalleri/gallery/static/`.
Thus move all static files there if you have additional ones, or you have, e.g., a new app with static files that you want served as well.

*Note: this could be circumvented if one configured the* `STATICFILES_DIRS` *variable in the project settings.*
*Currently, however, we only have one app, so this is not used.*

##### Images

As this project is a interface for a flat-file directory of images (the Django models are only concerned with metadata) you have to setup a server for serving images.
The project is agnostic to how this is done, the only thing assumed is that the images can be found under the endpoint `/images` as a directory structure.

###### Apache2 with symlinking of images

One solution for serving images could be symlinking the images directory to the root of the application (i.e. `/images`) and serving this directory with [Apache2](https://httpd.apache.org/).
This would allow you to use the images directory itself for other tasks (e.g. having an `ftp` server).

###### Example:

For symlinking you could do this (replacing `<IMAGE_DIRECTORY_PATH>` with the path to your image directory):

```
ln --symbolic --relative <IMAGE_DIRECTORY_PATH> /var/www/fotogalleri/images
```

And then append this to you Apache site configuration:

```
Alias /images/ /var/www/fotogalleri/images/
<Directory /var/www/fotogalleri/images>
  Require all granted
  Options -Indexes
</Directory>

ProxyPass "/images" !
ProxyPassReverse "/images" !
```
