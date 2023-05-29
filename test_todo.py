from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
import os

current_date = datetime.now(tz=None)
cur_time = current_date.strftime('%m-%d-%Y_%H-%M-%S')


def screenshot(page):
    page.screenshot(path=f"Screenshots/screenshot_{cur_time}.png")

def test_add_todo(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://playwright-todomvc.antonzimaiev.repl.co/#/")
    page.get_by_placeholder("What needs to be done?").click()
    page.get_by_placeholder("What needs to be done?").fill("Создать первый сценарий playwright")
    page.get_by_placeholder("What needs to be done?").press("Enter")

    context.close()
    browser.close()


def test_checkbox(page):
    page.goto('https://checks-radios.antonzimaiev.repl.co/')
    page.locator("text=Default checkbox").check()
    page.locator("text=Checked checkbox").check()
    page.locator("text=Default radio").check()
    page.locator("text=Default checked radio").check()
    page.locator("text=Checked switch checkbox input").check()
    screenshot(page)


def test_select(page):
    page.goto('https://select.antonzimaiev.repl.co/')
    page.select_option('#floatingSelect', value="3")
    page.select_option('#floatingSelect', index=1)
    page.select_option('#floatingSelect', label="Нашел и завел bug")
    screenshot(page)


def test_select_multiple(page):
    page.goto('https://select.antonzimaiev.repl.co/')
    page.select_option('#skills', value=["playwright", "python"])
    screenshot(page)


def test_select_multiple_file(page):
    page.goto('https://upload.antonzimaiev.repl.co/')
    page.set_input_files("#formFile", "test.txt")
    screenshot(page)
    page.locator("#file-submit").click()



def test_drag_and_drop(page):
    page.goto('https://draganddrop.antonzimaiev.repl.co/')
    page.drag_and_drop("#drag", "#drop")
    screenshot(page)


def test_dialogs(page):
    page.goto("https://dialog.antonzimaiev.repl.co/")
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_text("Диалог Confirmation").click()
    screenshot(page)


def test_download(page):

    page.goto("https://demoqa.com/upload-download")

    with page.expect_download() as download_info:
        page.locator("a:has-text(\"Download\")").click()

    download = download_info.value
    file_name = download.suggested_filename
    destination_folder_path = "./Download/"
    download.save_as(os.path.join(destination_folder_path, file_name))


def test_inner_text(page):
    page.goto('https://table.antonzimaiev.repl.co/')
    row = page.locator("tr")
    print(row.all_inner_texts())


def test_text_content(page):
    page.goto('https://table.antonzimaiev.repl.co/')
    row = page.locator("tr")
    print(row.all_text_contents())


def test_new_tab(page):
    page.goto("https://tabs.antonzimaiev.repl.co/")
    with page.context.expect_page() as tab:
        page.get_by_text("Переход к Dashboard").click()

    screenshot(page)
    new_tab = tab.value
    page.pause()
    assert new_tab.url == "https://tabs.antonzimaiev.repl.co/dashboard/index.html?"
    sign_out = new_tab.locator('.nav-link', has_text='Sign out')
    screenshot(page)
    assert sign_out.is_visible()

