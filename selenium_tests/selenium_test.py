from http import HTTPStatus
from flask import Flask
import pytest

from selenium_tests.fixture_test import driver, app_with_temp_board, trello_service_fix
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from todo_app.data.item import ItemType

from todo_app.data.trello_service import TrelloService

itemName = 'MyNewToDo'

def __get_item_row(driver: WebDriver, itemName: str = itemName) -> WebElement:
    return (driver
                .find_element(By.XPATH, f"//div[text()='{itemName}']")
                .find_element(By.XPATH, '..'))

def __get_item_status(row: WebElement) -> WebElement:
    return row.find_element(By.CLASS_NAME, 'itemStatus')

def __progress_item(row: WebElement) -> None:
    row.find_element(By.TAG_NAME, 'button').click()

@pytest.fixture(autouse=True)
def create_item(driver: WebDriver, app_with_temp_board: Flask, trello_service_fix):
    driver.get('http://localhost:5000')
    form = driver.find_element(By.ID, 'create-todo')
    form.find_element(By.TAG_NAME, 'input').send_keys(itemName)
    form.find_element(By.TAG_NAME, 'button').click()

@pytest.fixture(autouse=True)
def delete_item(trello_service_fix: TrelloService):
    yield
    resp = trello_service_fix.delete_item(itemName)
    assert resp.status_code == HTTPStatus.OK

def test_task_journey(driver: WebDriver, app_with_temp_board: Flask):
    driver.get('http://localhost:5000')
    assert driver.title == 'To-Do App'

def test_create_item(driver: WebDriver):
    driver.find_element(By.XPATH, f"//div[text()='{itemName}']")

def test_progress_item(driver: WebDriver):
    row = __get_item_row(driver)
    status = __get_item_status(row)
    assert status.text == ItemType.ToDo

    __progress_item(row)
    row = __get_item_row(driver)
    status = __get_item_status(row)
    assert status.text == ItemType.Doing

    __progress_item(row)
    row = __get_item_row(driver)
    status = __get_item_status(row)
    assert status.text == ItemType.Done