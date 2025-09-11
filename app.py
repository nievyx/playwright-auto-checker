from playwright.sync_api import sync_playwright

PRODUCT_URL = 'https://www.popmart.com/gb/products/1064/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box'

def basic_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(PRODUCT_URL)
        print('Page title:', page.title())
        page.pause() # Pause to allow user interaction
        browser.close()

from scripts.line_through_check import check_stock

products = [
    'https://www.popmart.com/gb/products/1064/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box',
    'https://www.popmart.com/gb/products/1036/Hirono-Echo-Series-Figures',
    'https://www.popmart.com/gb/products/948/SKULLPANDA-Winter-Symphony-Series-Plush'
]

def main():
    for url in products:
        print(f"\nChecking product: {url}")
        check_stock(url)

    

if __name__ == '__main__':
    main()
