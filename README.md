# fgh-web
Frogs' Greatest HITs web prototype

## Setting up for development

Note: if you don't have Python installed, you can install it on Mac using Homebrew:

    brew install python
Or you can install it on Windows using the instructions at http://docs.python-guide.org/en/latest/starting/install/win/.

You may also need to install sqlite and/or sqlite3-devel depending on your operating system.

To run the app, you need to install Django and dependencies:

    git clone https://github.gatech.edu/cdchealthyweight/fgh-web.git fgh
    cd fgh
    pip install -r requirements.txt

After this, you can set up the app locally:

    (may not work) python manage.py syncdb
    (try) python manage.py migrate

And run it using:

    python manage.py runserver
    
The application should now be accessible at http://127.0.0.1:8000/questionnaire.

Note: if for some reason you wish to run the development server on a machine other than your development box, you can do that as follows:

    python manage.py runserver 0.0.0.0:8000&
(see http://stackoverflow.com/questions/13522228/running-django-development-server-on-a-remote-machine-using-putty-how-to-run-th)

However, if you find yourself doing this on a regular basis you should really just bite the bullet and set up Apache+WSGI.

## Windows 10 Troubleshooting

* First things first - make sure you are using Python 2.7 and that `python27` and `python27/scripts` directories are in the environmental variable path using the python instructions guide above.
* Error - need `Microsoft Visual C++ Compiler for Python 2.7`
   * download and install from [https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266]
* Error - can't find `sqlite.h` file
   * download `pysqlite-2.8.2-cp27-cp27m-win_amd64.whl` from [http://www.lfd.uci.edu/~gohlke/pythonlibs/#pysqlite]
   * save it in the `python27/scripts` directory and browse to this directory
   * open a cmd prompt (`File->Open Cmd Prompt`) and install with
   * `pip install pysqlite-2.8.2-cp27-cp27m-win_amd64.whl`

