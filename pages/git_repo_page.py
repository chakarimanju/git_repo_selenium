import time
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.utils import Utils


class RepoPage(BaseDriver):
    log = Utils.custom_logger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    IMPLICIT_WAIT = 2
    REPO_SEARCH_BOX = "//input[contains(@class, 'MuiInputBase-input')]"
    REPO_SEARCH_BUTTON = "//button[starts-with(@class,'MuiButtonBase-root MuiIconButton-root " \
                         "MuiIconButton-sizeMedium')] "
    REPO_ROWS_SELECT_MENULIST = "//div[contains(@class,'MuiSelect-standard MuiInputBase-input')]"
    REPO_TABLE_ROWS = "//table/tbody/tr"
    NEXT_PAGE_FIELD = "//button[starts-with(@title,'Go to next page')]"
    PREVIOUS_PAGE_FIELD = "//button[starts-with(@title,'Go to previous page')]"
    ROW_MENU_LIST_FIELD = "//div/ul/li[contains(@class,'MuiMenuItem-root')]"
    REPO_DETAILS_FIELDS = "//span[@aria-label='Get Details']"
    REPO_DETAILS_HEADING = "//div/h2[@id='customized-dialog-title']"
    REPO_DETAILS_CLOSE_BUTTON = "//button[contains(@class,'MuiButtonBase-root') and @aria-label='close']"
    REPO_DETAILS_INFO_FILEDS = "//div[contains(@class,'MuiDialogContent-root')]/div/p"
    REPO_DETAILS_OK_BUTTON = "//button[contains(@class,'MuiButton-root')]"

    def get_repo_details_fields(self):
        return self.wait_until_elements_present(By.XPATH, self.REPO_DETAILS_FIELDS)

    def get_repo_details_heading(self):
        return self.wait_until_element_present(By.XPATH, self.REPO_DETAILS_HEADING).text

    def get_repo_details_close_button(self):
        return self.wait_until_element_present(By.XPATH, self.REPO_DETAILS_CLOSE_BUTTON)

    def close_repo_details_page(self):
        self.get_repo_details_close_button().click()

    def get_repo_details_info_fields(self):
        return self.wait_until_elements_present(By.XPATH, self.REPO_DETAILS_INFO_FILEDS)

    def get_repo_details_ok_button(self):
        return self.wait_until_element_present(By.XPATH, self.REPO_DETAILS_OK_BUTTON)

    def click_repo_details_ok_button(self):
        self.get_repo_details_ok_button().click()

    TABLE_LINK_ELEMENTS = "//table/tbody/tr/td/a"

    def get_table_link_elements(self):
        return self.wait_until_elements_present(By.XPATH, self.TABLE_LINK_ELEMENTS)

    def get_repo_search_field(self):
        return self.wait_until_element_present(By.XPATH, self.REPO_SEARCH_BOX)

    def enter_repo_search_field(self, repo_search_value):
        self.log.info('Entering ' + repo_search_value + ' to search in Git-Repo')
        self.get_repo_search_field().send_keys(repo_search_value)

    def get_repo_search_button(self):
        return self.wait_until_element_present(By.XPATH, self.REPO_SEARCH_BUTTON)

    def click_repo_search_button(self):
        self.log.info('Clicking search button')
        self.get_repo_search_button().click()

    def wait_for_table_data_to_load(self):
        self.log.info('Wait for table data to load')
        return self.wait_until_elements_present(By.XPATH, self.REPO_TABLE_ROWS)

    def get_next_page_filed(self):
        return self.wait_until_element_present(By.XPATH, self.NEXT_PAGE_FIELD)

    def move_to_next_page(self):
        self.log.info('Moving to next page of the repo search table')
        self.get_next_page_filed().click()
        self.wait_for_table_data_to_load()

    def get_previous_page_filed(self):
        return self.wait_until_element_present(By.XPATH, self.PREVIOUS_PAGE_FIELD)

    def move_to_previous_page(self):
        self.log.info('Moving to next page of the repo search table')
        self.get_previous_page_filed().click()
        self.wait_for_table_data_to_load()

    def get_repo_select_rows_menulist(self):
        return self.wait_until_element_present(By.XPATH, self.REPO_ROWS_SELECT_MENULIST)

    def click_table_row_select_menulist(self):
        self.log.info('Click table row selection dropdown')
        self.get_repo_select_rows_menulist().click()

    def get_table_row_from_menulist_fields(self):
        self.click_table_row_select_menulist()
        return self.wait_until_elements_present(By.XPATH, self.ROW_MENU_LIST_FIELD)

    def set_table_rows_to_display_on_current_page(self, row_count):
        self.log.info('Select number of rows to display')
        table_row_counts = self.get_table_row_from_menulist_fields()
        self.log.info('the row counts are - ' + str(len(table_row_counts)))
        # time.sleep(5)
        for count in table_row_counts:
            self.log.info('dropdown menu list item - ' + str(count.text))
            if str(row_count) in count.text:
                count.click()
                self.log.info('Selected number of rows to display as - ' + str(row_count))
                # time.sleep(5)
                break
        self.wait_for_table_data_to_load()

    def search_repo(self, repo_search_value):
        self.enter_repo_search_field(repo_search_value)
        self.click_repo_search_button()
        self.wait_for_table_data_to_load()

    def get_current_table_data(self, row_count=None):
        if row_count:
            self.set_table_rows_to_display_on_current_page(row_count)
            time.sleep(self.IMPLICIT_WAIT)
        table_data = [['Name', 'Owner', 'Stars', 'Link', 'Details']]
        self.log.info('Find all the table rows')
        table_element = self.wait_for_table_data_to_load()
        time.sleep(self.IMPLICIT_WAIT)
        self.log.info('Found the total number of rows in the current page are - ' + str(len(table_element)))
        for i in range(len(table_element)):
            cells = table_element[i].find_elements(By.XPATH, "//table/tbody/tr[" + str(i + 1) + "]/td")
            row_data = []
            for cell in cells:
                row_data.append(cell.text)
            table_data.append(row_data)

        return table_data

    def verify_search_results(self, str_to_search):
        table_data = self.get_current_table_data()
        self.log.info(str(table_data))
        page_count = 1
        while str_to_search not in str(table_data):
            page_count += 1
            self.move_to_next_page()
            table_data = self.get_current_table_data()
            if str_to_search in str(table_data):
                self.log.info('The search data found in the page - ' + str(page_count))
                break
        else:
            self.log.info('The search data found in the page - ' + str(page_count))

    def verify_links_in_search_results(self):
        link_elements = self.get_table_link_elements()
        parent_handle = self.driver.current_window_handle
        for link in link_elements:
            self.log.info('Open the link - ' + str(link.text))
            link.click()
            all_handles = self.driver.window_handles
            for handle in all_handles:
                if handle != parent_handle:
                    self.driver.switch_to.window(handle)
                    time.sleep(self.IMPLICIT_WAIT)
                    self.log.info('Opened the link and the title of the link page is ' + str(self.driver.current_url))
                    self.log.info('Closing the opened link page')
                    time.sleep(self.IMPLICIT_WAIT)
                    self.driver.close()
                    self.log.info('Moving the focus to parent window')
                    self.driver.switch_to.window(parent_handle)
                    time.sleep(self.IMPLICIT_WAIT)

    def get_current_page_repos_details_info(self):
        repo_details_info = {}
        self.log.info('Find all the table rows')
        details_elements = self.get_repo_details_fields()
        time.sleep(self.IMPLICIT_WAIT)
        self.log.info('The search results has %s repo records in current page'%(len(details_elements)))
        for we in details_elements:
            self.log.info('Open repo details - first click')
            self.driver.execute_script("arguments[0].click()", we)
            time.sleep(self.IMPLICIT_WAIT)
            self.log.info('Wait for repo details title')
            repo_details_heading = self.get_repo_details_heading()
            details_info = self.get_repo_details_info_fields()
            self.log.info('Read repo details - ' + repo_details_heading)
            repo_data = []
            repo_details_info[repo_details_heading] = {}
            for key,value in zip(details_info[::2], details_info[1::2]):
                #repo_data.append(info.text)
                repo_details_info[repo_details_heading][key] = value
            #repo_details_info[repo_details_heading] = repo_data
            self.log.info('Click ok on repo detail window')
            self.click_repo_details_ok_button()

        return repo_details_info
