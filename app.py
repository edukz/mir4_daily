from playwright.sync_api import Playwright, sync_playwright, expect
import json

def login(page, account):
    try:
        print(f"Fazendo login em {account['server_name']}..")
        page.get_by_placeholder("Username").click()
        page.get_by_placeholder("Username").fill(account["username"])
        page.get_by_placeholder("Username").press("Tab")
        page.get_by_placeholder("Password").fill(account["password"])
        page.get_by_placeholder("Password").press("Enter")
        
        # Verifica se o login foi bem-sucedido (você pode ajustar isso com base na página real)        
        page.get_by_role("menuitem", name="Special").click()
        page.locator("#shop").get_by_text("Daily Gift").click()
        page.get_by_role("dialog", name="【Daily Gift 2.0】 Information").get_by_role("button", name="Buy").click()
        page.get_by_placeholder("Select").click()
        page.get_by_text(account["server_name"]).click()  #e camente
        page.get_by_role("button", name="OK").click()
        page.get_by_role("link", name=" Logout").click()
        page.wait_for_timeout(500)  # Espera um tempo antes de iniciar o próximo login
    
    except Exception as e:
        print(f"Erro ao fazer login: {str(e)}")

def run(playwright: Playwright) -> None:
    with open('config.json', encoding='utf-8') as config_file:
        config = json.load(config_file)

    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context(viewport={"width": 800, "height": 600})
    page = context.new_page()
    page.goto("https://console.playmir4.com/login")

    for account in config["accounts"]:
        login(page, account)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)