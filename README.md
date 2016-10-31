# Hip Flask

Hip Flask forks the [Google App Engine Flask Skeleton](https://github.com/GoogleCloudPlatform/appengine-flask-skeleton) and adds a little more meat to its bone so that you can get a [Flask](http://flask.pocoo.org) project up and running on the App Engine platform even more quickly.

It is behind small projects like https://github.com/klenwell/decruiter and larger projects like http://forekarma.com.

- Demo Site: https://hip-flask-on.appspot.com/
- Trello Board: https://trello.com/b/3w3mlaUf/hip-flask
- App Engine Dashboard: https://console.cloud.google.com/appengine


## Installation

1. Install the [App Engine Python SDK](https://developers.google.com/appengine/downloads).

    See the README file for directions. You'll need python 2.7 and [pip 1.4 or later](http://www.pip-installer.org/en/latest/installing.html) installed too.

2. Set up new project directory and clone this repo.

    ```
    mkdir my-new-project
    cd my-new-project
    git clone https://github.com/klenwell/hip-flask.git app-engine
    ```

3. Install dependencies in project's lib directory.

    I recommend using a [pyenv](https://github.com/yyuu/pyenv) [virtualenv](https://github.com/yyuu/pyenv-virtualenv).

    ```
    cd app-engine
    pyenv virtualenv 2.7.7 flask-hip
    pyenv local flask-hip
    ```

    Install dependencies:

    ```
    pip install -r requirements.txt -t lib
    ```

4. Update config files.

    First copy the dist secrets file:

    ```
    cp -v config/secrets.py{-dist,}
    ```

    Then update `config/__init__.py` and `config/secrets.py`.

5. Run local development server.

    ```
    cd my-new-project
    dev_appserver.py --port=8080 --admin_port=8081 --api_port=8082 ./app-engine
    ```

    Visit the application [http://localhost:8080](http://localhost:8080)

    See [the development server documentation](https://developers.google.com/appengine/docs/python/tools/devserver) for options when running dev_appserver.


## Tests

First, install testing libraries:

    cd my-new-project/app-engine
    pip install -r requirements-test.txt

To run tests:

    cd my-new-project/app-engine
    nosetests -c nose.cfg

With coverage:

    nosetests -c nose.cfg --with-coverage --cover-erase \
      --cover-package=config,models

To run a single test:

    nosetests -c nose.cfg tests/controllers/test_pages_controller.py


## Deployment

1. Use the [Admin Console](https://appengine.google.com) to create a project/app id. (App id and project id are identical).

2. [Deploy the application](https://developers.google.com/appengine/docs/python/tools/uploadinganapp):

   ```
   appcfg.py update -A <your-app-id> -e <your-user-name> ./app-engine
   ```

3. Congratulations!  Your application is now live at your-app-id.appspot.com
