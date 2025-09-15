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

GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
PURPLE = "\033[95m"
RESET = "\033[0m"


products = [
    {
        "name" : "Labubu - Big into Energy",
        "url": "https://www.popmart.com/gb/products/1064/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box",
        'desired_options': ['Single Box', 'Whole Set']
    },
    {
        "url": "https://www.popmart.com/gb/products/1036/Hirono-Echo-Series-Figures",
        'desired_options': ['Whole Set']
    },
    {
        "url": "https://www.popmart.com/gb/products/948/SKULLPANDA-Winter-Symphony-Series-Plush",
        'desired_options': ['Single Box']
    },
    {
        "url": "https://www.popmart.com/gb/products/641/THE-MONSTERS---Exciting-Macaron-Vinyl-Face-Blind-Box",
        'desired_options': ['Single Box', 'Whole Set']
    },
]

def get_product_name(url: str) -> str:
    """Return the product name from the URL if no name is given."""
    raw_name = url.rstrip("/").split("/")[-1]
    return raw_name.replace("-", " ")

def main():
    
    msg = "Starting stock check..."

    print(BLUE + "┌" + "─" * (len(msg) + 2) + "┐")
    print("│ " + msg + " │")
    print("└" + "─" * (len(msg) + 2) + "┘" + RESET)

    
    for product in products:
        url = product['url']
        name = product.get('name', get_product_name(url))
        desired_options = product['desired_options']

        print(f"\n{PURPLE}--- {name} ---{RESET}",end='')
        print(f"\nChecking product: {url}")
        stock_info = check_stock(url)

        for option, in_stock in stock_info.items():
            status = ' IN STOCK' if in_stock else ' OUT OF STOCK'
            status_symbol = '✅' if in_stock else '❌'
            print(f'{status_symbol}{option}:{status}')

            if option in desired_options and in_stock:
                print(f'{GREEN}***✔ Desired option "{option}" is available! ***{RESET}')
                # Later call a funvtion to add to cart / notify user



if __name__ == '__main__':
    main()
