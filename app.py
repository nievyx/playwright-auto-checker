# Standard library
import datetime
import time
import json #TODO: #For checking products last status, to avoid double notifications

# Third-party
from playwright.sync_api import sync_playwright

# Local imports
from scripts.line_through_check import check_stock
from scripts.send_sms import send_sms


def basic_test():
    PRODUCT_URL = 'https://www.popmart.com/gb/products/1064/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(PRODUCT_URL)
        print('Page title:', page.title())
        page.pause() # Pause to allow user interaction
        browser.close()


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
        'desired_options': []
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


TIME = 300  # 5 minutes

def main():
    
    msg = f"Starting stock check... {'∞' if RUN_MODE else '' }"

    print(BLUE + "┌" + "─" * (len(msg) + 2) + "┐")
    print("│ " + msg + " │")
    print("└" + "─" * (len(msg) + 2) + "┘" + RESET)


    for product in products:
        url = product['url']
        name = product.get('name', get_product_name(url))
        desired_options = product['desired_options']

        print(f"\n{PURPLE}--- {name} ---{RESET}",end='')
        print(f"\nChecking product: {url}")

        #TODO: Step 1: Load previous status # Use JSON file to store last known status to avoid double notifications
        try:
            with open('last_status.json', 'r') as f: #do i need 'r'
                last_status = json.load(f)
        except FileNotFoundError:
            last_status = {}
            print("[DEBUG] No previous status file found. Starting fresh.")


        try:
            stock_info = check_stock(url)

            for option, in_stock in stock_info.items():
                status = ' IN STOCK' if in_stock else ' OUT OF STOCK'
                status_symbol = '✅' if in_stock else '❌'
                print(f'{status_symbol}{option}:{status}')
                # TODO: MORE JSON
                prev_status = last_status.get(url, {}).get(option)
                print(f"[DEBUG] Previous status for '{option}': {prev_status}")

                if option in desired_options and in_stock:
                    print(f'{GREEN}***✔ Desired option "{option}" is available! ***{RESET}')
                    # Later call a function to add to cart / notify user
                    # TODO: JSON logic for checking previous status to go here.
                    if prev_status is None or prev_status != in_stock :  # Only notify if status changed or no previous record
                        #TODO: DEBUG MODE - Comment out send_sms line
                        #send_sms(f'*** {name} - Desired option "{option}" is available! ***\n{url}')
                        print(f"{BLUE}[DEBUG] This would send SMS notification for '{option}'.{RESET}")

            #TODO: # Use JSON file to store last known status to avoid double notifications
            #Step 4
            last_status[url] = stock_info
            print(f"{RED}[DEBUG] Updated last_status: {last_status}{RESET}")

            #TODO: Step 5: Save updated status back to file
            with open('last_status.json', 'w') as f:
                json.dump(last_status, f, indent=4)
                print(f"{GREEN}[DEBUG] Saved last_status to file.{RESET}")

        except Exception as e:
            print(f"{RED}Error checking stock for {name}: {e}{RESET}, continuing to next product.")
        
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Finished checking {name}.")
    
    print(f"\n{BLUE}All products checked. Waiting for next cycle... {'Starting again in '+str(TIME)+ ' seconds' if RUN_MODE else '' } {RESET}\n")


if __name__ == '__main__':
    RUN_MODE = 1 # Set to 1 for continuous running, 0 for single run
    main()
    while RUN_MODE:

        main()
        time.sleep(TIME)  # Wait 5 minutes before next check
