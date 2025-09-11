from playwright.sync_api import sync_playwright

PRODUCT_URL = 'https://www.popmart.com/gb/products/1064/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(PRODUCT_URL)

    # Wait for at lease one option to be visible
    page.wait_for_selector("div[class*='index_sizeInfoTitle']")#TODO: Try headless with timeout#, timeout=5000)   


    # Locate all product size/option divs
    options = page.locator("div[class*='index_sizeInfoTitle']")
    print(f'Number of options found: {options.count()}')

    for i in range(options.count()):
        print(f'Option {i+1}: {options.nth(i).inner_text()}')

    input("Press Enter to close browser...")
    browser.close()