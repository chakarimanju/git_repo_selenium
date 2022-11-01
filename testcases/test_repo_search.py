#!pytest
import pytest
import time
import softest

from selenium.webdriver.common.by import By
from pages.git_repo_page import RepoPage
from utilities.utils import Utils


@pytest.mark.usefixtures('setup_cleanup')
class TestRepoPage(softest.TestCase):
    log = Utils.custom_logger()

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.repo_page = RepoPage(self.driver)
        self.util = Utils()

    def test_verify_repo_page_title(self):
        page_title = 'Git Repository List'
        self.log.info('Verify the repo page title')
        self.util.compare_and_verify(page_title, self.driver.title)
        self.log.info('Found the expected page title')
        time.sleep(3)

    def test_search_git_repo(self):
        self.repo_page.search_repo('kubernetes')
        self.repo_page.verify_search_results('kubernetes')

    def test_verify_table_rows_displayed_in_current_page(self):
        self.repo_page.search_repo('kubernetes')
        for count in [10, 25, 50]:
            self.log.info('Selecting row count as - ' + str(count))
            results = self.repo_page.get_current_table_data(count)
            displayed_rows = len(results)-1
            self.log.info('The displayed table rows count is - ' + str(displayed_rows))
            assert displayed_rows == count, 'Failed to validate table rows display'
            self.log.info('Found the expected number of rows in the current page')

    def test_verify_links_in_table_displayed_in_current_page(self):
        self.repo_page.search_repo('kubernetes')
        self.repo_page.verify_links_in_search_results()

    def test_verify_current_page_repo_details_info(self):
        self.repo_page.search_repo('kubernetes')
        repo_data = self.repo_page.get_current_page_repos_details_info()
        self.log.info(str(repo_data))
