import os
import time

import pytest
from selenium import webdriver

from utilities.utils import Utils

url = "http://localhost:3000/"
driver = None


@pytest.fixture(autouse=True)
def setup_cleanup(request):
    log = Utils.custom_logger()
    global driver
    log.info("Creating web browser driver")
    driver = webdriver.Chrome()
    request.cls.driver = driver
    log.info("Launching web browser and opening the url")
    driver.get(url)
    log.info("Maximising browser window")
    driver.maximize_window()
    log.info("The page is launched and ready for testing")
    yield
    log.info("Closing the browser")
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        # always add url to report
        extra.append(pytest_html.extras.url(url))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            report_directory = os.path.dirname(item.config.option.htmlpath)
            file_name = report.nodeid.replace("::", "_") + ".png"
            destination_file = os.path.join(report_directory, file_name)
            driver.save_screenshot(destination_file)
            # only add additional html on failure
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:300px;hight"200px onclick="window.open(' \
                       'this.src)" align="right"/><div>' % file_name
            extra.append(pytest_html.extras.html(html))
        report.extra = extra


def pytest_html_report_title(report):
    report.title = "GIT-Repo Test Execution Report"
