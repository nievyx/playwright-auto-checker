# Standard library
from datetime import datetime, timedelta
import time
import random
import json #For checking products last status, to avoid double notifications

# Third-party
from playwright.sync_api import sync_playwright

# Local imports
from scripts.line_through_check import check_stock
from scripts.send_sms import send_sms
from scripts.add_to_cart import add_to_cart


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


products = [ #Put in order of priority
    {
        "url": "https://www.popmart.com/gb/products/641/THE-MONSTERS---Exciting-Macaron-Vinyl-Face-Blind-Box",
        'desired_options': ['Single Box', 'Whole Set']
    },
    {
        "name" : "Labubu - Big into Energy",
        "url": "https://www.popmart.com/gb/products/1064/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box",
        'desired_options': ['Single Box', 'Whole Set']
    },
    {
        "url": "https://www.popmart.com/gb/products/1036/Hirono-Echo-Series-Figures",
        'desired_options': ['Single Box']
    },
    # {
    #     "url": "https://www.popmart.com/gb/products/948/SKULLPANDA-Winter-Symphony-Series-Plush",
    #     'desired_options': ['Single Box']
    # },
]

def get_product_name(url: str) -> str:
    """Return the product name from the URL if no name is given."""
    raw_name = url.rstrip("/").split("/")[-1]
    return raw_name.replace("-", " ")


TIME = 300  # 5 minutes
DEBUG = False  # Set to 1 to enable debug prints, 0 to disable
SMS_MODE = 0  # Set to 1 to enable SMS notifications, 0 to disable
CART_MODE: 1  # Set to 1 to enable add to cart function, 0 to disable

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

        # JSON Step 1: Load previous status
        try:
            with open('last_status.json', 'r') as f: 
                last_status = json.load(f)
        except FileNotFoundError:
            last_status = {}
            if DEBUG:
                print("[DEBUG] No previous status file found. Starting fresh.")


        try:
            stock_info = check_stock(url)

            for option, in_stock in stock_info.items():
                status = ' IN STOCK' if in_stock else ' OUT OF STOCK'
                status_symbol = '✅' if in_stock else '❌'
                print(f'{status_symbol}{option}:{status}')
                # JSON Step 2: Check if option is in desired_options
                prev_status = last_status.get(url, {}).get(option)
                if DEBUG:
                    print(f"[DEBUG] Previous status for '{option}': {prev_status}")

                if option in desired_options and in_stock:
                    print(f'{GREEN}***✔ Desired option "{option}" is available! ***{RESET}')
                    # Later call a function to add to cart / notify user
                    
                    if prev_status is None or prev_status != in_stock :  # Only notify if status changed or no previous record
                        if SMS_MODE:
                            send_sms(f'*** {name} - Desired option "{option}" is available! ***\n{url}')
                        else:
                            print(f"{RED}SMS_MODE is off, not sending SMS.{RESET}")
                        if DEBUG:
                            print(f"{BLUE}[DEBUG] This would send SMS notification for '{option}'.{RESET}")
                        
                    #TODO:
                    # Add to cart function can be called here
                    if CART_MODE:
                        add_to_cart(url)


            # JSON Step 4: Use JSON file to store last known status to avoid double notifications
            last_status[url] = stock_info
            if DEBUG:
                print(f"{RED}[DEBUG] Updated last_status: {last_status}{RESET}")

            # JSON Step 5: Save updated status back to file
            with open('last_status.json', 'w') as f:
                json.dump(last_status, f, indent=4)
                if DEBUG:
                    print(f"{GREEN}[DEBUG] Saved last_status to file.{RESET}")

        except Exception as e:
            print(f"{RED}Error checking stock for {name}: {e}{RESET}, continuing to next product.")
        
       
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Finished checking {name}.")


    # Random delay between -30 and +30 seconds
    random_delay = random.randint(-30, 30)

    print(f"\n{BLUE}All products checked. Waiting for next cycle... {'Starting again in '+str(TIME)+ ' seconds ' if RUN_MODE else '' } {RESET}\n")
    print(f"[DEBUG] Waiting an additional {random_delay} seconds before next product check.")

    next_run = datetime.now() + timedelta(seconds=TIME) + timedelta(seconds=random_delay)
    print(f"[DEBUG] Next run scheduled at Approx {next_run.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    RUN_MODE = 1 # Set to 1 for continuous running, 0 for single run
    main()
    
    while RUN_MODE:

        main()

        

        time.sleep(TIME)  