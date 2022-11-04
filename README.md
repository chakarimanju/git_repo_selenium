# UI Testing with Selenium Python & Pytest - Page Object Model

## Overview
This project a demo project for testing a UI with Selenium WebDriver using Python and pytest and Page Object Model.


## Web Application Under Test
The website that is being tested by this framework is “Repository Search”, that uses Repository APIs to make search when a given keyword is passed into the field

Following functionality has been tested, focusing on the following pages:
* [home/repository-list](http://localhost:3000/) page


### Tech stack
As this is a Python project, build and dependency management is handled by Pipenv, so there is a `Pipfile` (and associated `.lock` file) defining the versions of the dependencies:
* Python v3.9
* Selenium v4.5.0
* Pytest v7.2.0
* Webdriver-Manager v3.8.4
* Pytest-html v3.2.0
* softest 1.2.0.0

Steps to setup this project (Can be developed & run in PyCharm environment too)

* Install pipenv. Example: pip install pipenv
* Install Pipfile, install all the library dependencies and create environment. Example: pipenv install Pipfile
* Activate environment. Example: pipenv shell



### Supported Browsers
The `conftest.py` module uses the Webdriver-Manager dependency to manage the various browser drivers. The `browser` Pytest fixture returns the relevant WebDriver instance for the chosen browser, with support for:
* chrome - the default option
* firefox
* edge


### Running tests
* Run the web application locally by:  
  - npm install && npm start
* Run all tests by running the command: 
  - pytest
* To run a specific test 
  - pytest -k <test_name> (e.g. pytest -k test_verify_repo_page_title)
* To generate the report file for a run
  - pytest --html=reports/report.html (--html is to capture reports in a file  e.g. reports/report.html)
* To change the default browser use --browser as an inline agrument to pytest command
  - pytest --html=report.html --browser=firefox


#### Test Reports
Test reports can be generated locally in the repository by passing the option --html=reports/report.html to pytest utility so that report file will be generated in the project/reports directory.


#### Test Logs
The test INFO messages will be captured in logs/test_logs.log file.


