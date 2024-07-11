# LJPS-SPM

Github repo link: https://github.com/yyiiinn/LJPS-SPM.git
 
==================
INSTALLATION GUIDE
==================

(1) set up and run a WAMP or MAMP server

(2) execute the contents of 'lms_ljps.sql' under 'sql' folder in phpMyAdmin, i.e. at:

       http://localhost/phpmyadmin  OR
	   http://localhost/phpMyAdmin

(3) find your web server's root directory (e.g. C:\wamp\www) and copy the entire 'LJPS-SPM' folder inside 

(4) if you don't already have Flask installed, do:

	   python -m pip install flask
	   python -m pip install flask_cors
	   python -m pip install Flask-SQLAlchemy
	   python -m pip install mysql-connector-python

(5) in the 'LJPS-SPM' directory, run "python app.py" in a terminal.

(6) go to http://localhost:5000 where the application should be working!

=============
RUNNING TESTS
=============

To run unit and integration tests, go into the 'LJPS-SPM' folder on your
command line and do:

  	python UnitTests.py
  	python IntegrationTests.py

-> If you get an error message, it may be due to missing packages. Resolve
this by doing:

  	python -m pip install flask_testing

for each missing package (in this case, 'flask_testing').

-> If you get an error message - "Your version of Flask doesn't support signals. This requires Flask 0.6+ with the blinker module installed.", resolve this by doing:

  	pip install sentry-sdk[flask]


===============
TROUBLESHOOTING
===============

If running the Flask application gives you an error message along the lines
of "ProgrammingError: (mysql.connector.errors.ProgrammingError) Character set
'255' unsupported", then the following temporary 'fix' will resolve it:

	   python -m pip install mysql-connector-python==0.29

 

