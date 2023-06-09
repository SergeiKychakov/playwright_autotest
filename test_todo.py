from playwright.sync_api import Playwright, Page, Route, sync_playwright, expect
from datetime import datetime
import os

current_date = datetime.now(tz=None)
cur_time = current_date.strftime('%m-%d-%Y_%H-%M-%S')


def screenshot(page: Page):
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


def test_checkbox(page: Page):
    page.goto('https://checks-radios.antonzimaiev.repl.co/')
    page.locator("text=Default checkbox").check()
    page.locator("text=Checked checkbox").check()
    page.locator("text=Default radio").check()
    page.locator("text=Default checked radio").check()
    page.locator("text=Checked switch checkbox input").check()
    screenshot(page)


def test_select(page: Page):
    page.goto('https://select.antonzimaiev.repl.co/')
    page.select_option('#floatingSelect', value="3")
    page.select_option('#floatingSelect', index=1)
    page.select_option('#floatingSelect', label="Нашел и завел bug")
    screenshot(page)


def test_select_multiple(page: Page):
    page.goto('https://select.antonzimaiev.repl.co/')
    page.select_option('#skills', value=["playwright", "python"])
    screenshot(page)


def test_select_multiple_file(page: Page):
    page.goto('https://upload.antonzimaiev.repl.co/')
    page.set_input_files("#formFile", "test.txt")
    screenshot(page)
    page.locator("#file-submit").click()


def test_drag_and_drop(page: Page):
    page.goto('https://draganddrop.antonzimaiev.repl.co/')
    page.drag_and_drop("#drag", "#drop")
    screenshot(page)


def test_dialogs(page: Page):
    page.goto("https://dialog.antonzimaiev.repl.co/")
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_text("Диалог Confirmation").click()
    screenshot(page)


def test_download(page: Page):

    page.goto("https://demoqa.com/upload-download")

    with page.expect_download() as download_info:
        page.locator("a:has-text(\"Download\")").click()

    download = download_info.value
    file_name = download.suggested_filename
    destination_folder_path = "./Download/"
    download.save_as(os.path.join(destination_folder_path, file_name))


def test_inner_text(page: Page):
    page.goto('https://table.antonzimaiev.repl.co/')
    row = page.locator("tr")
    print(row.all_inner_texts())


def test_text_content(page: Page):
    page.goto('https://table.antonzimaiev.repl.co/')
    row = page.locator("tr")
    print(row.all_text_contents())


def test_new_tab(page: Page):
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


def test_todo(page: Page):
    page.goto('https://demo.playwright.dev/todomvc/#/')
    expect(page).to_have_url("https://demo.playwright.dev/todomvc/#/")
    input_field = page.get_by_placeholder('What needs to be done?')
    expect(input_field).to_be_empty()
    input_field.fill("Закончить курс по playwright")
    input_field.press('Enter')
    input_field.fill("Добавить в резюме, что умею автоматизировать")
    input_field.press('Enter')
    todo_item = page.get_by_test_id('todo-item')
    expect(todo_item).to_have_count(2)
    todo_item.get_by_role('checkbox').nth(0).click()
    expect(todo_item.nth(0)).to_have_class('completed')


def test_listen_network(page: Page):
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    page.goto('https://osinit.ru/')


def test_network(page: Page):
    page.route("**/register", lambda route: route.continue_(post_data='{"email": "user","password": "secret"}'))
    page.goto('https://reqres.in/')
    page.get_by_text(' Register - successful ').click()


def test_mock_tags(page: Page):
    page.route("**/api/tags", lambda route: route.fulfill(path="data.json"))
    page.goto('https://demo.realworld.io/')


def test_intercepted(page: Page):
    def handle_route(route: Route):
        response = route.fetch()
        json = response.json()
        json["tags"] = ["open", "solutions"]
        route.fulfill(json=json)

    page.route("**/api/tags", handle_route)

    page.goto("https://demo.realworld.io/")
    sidebar = page.locator('css=div.sidebar')
    expect(sidebar.get_by_role('link')).to_contain_text(["open", "solutions"])


def test_inventory(page):
    response = page.request.get('https://petstore.swagger.io/v2/store/inventory')
    print(response.status)
    print(response.json())


def test_add_user(page):
    data = [
              {
                "id": 9743,
                "username": "fsd",
                "firstName": "fff",
                "lastName": "ggg",
                "email": "bbb",
                "password": "tt",
                "phone": "333",
                "userStatus": 0
              }
            ]
    header = {
        'accept': 'application/json',
        'content-Type': 'application/json'
    }
    response = page.request.post('https://petstore.swagger.io/v2/user/createWithArray', data=data, headers=header)
    print(response.status)
    print(response.json())

