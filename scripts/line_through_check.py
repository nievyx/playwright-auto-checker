from playwright.sync_api import sync_playwright


# PRODUCT_URL = "https://www.popmart.com/gb/products/1064/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box"
# PRODUCT_URL = "https://www.popmart.com/gb/products/1036/Hirono-Echo-Series-Figures"
# PRODUCT_URL = 'https://www.popmart.com/gb/products/948/SKULLPANDA-Winter-Symphony-Series-Plush'

def check_stock(product_url,headless_mode=False):
    """Check stock status of Single Box / Whole Set. 
    Returns dict with option name as key and boolean as value."""
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless_mode)  # Set True in production
        page = browser.new_page()
        page.goto(product_url)

        page.wait_for_selector("div[class*='index_sizeInfoTitle']", timeout=5000)  # 5 seconds


        # Find all options
        options = page.locator("div[class*='index_sizeInfoTitle']")
        print(f"Number of options found: {options.count()}")

        for i in range(options.count()):
            option = options.nth(i)
            text = option.inner_text().strip()
            
            # Get element class and parent class
            option_classes = option.get_attribute("class") or ""
            parent_classes = option.locator("xpath=..").get_attribute("class") or ""
            
            # Determine stock status
            if "index_disabledSizeTitle__" in option_classes:
                print(f"X '{text}' is OUT of stock (disabled title)")
                results[text] = False
            elif "index_disabled__" in parent_classes:
                print(f"X '{text}' is OUT of stock (crossed out / parent)")
                results[text] = False
            else:
                print(f"'{text}' is IN stock")
                results[text] = True

        browser.close()
    
    return results

if __name__ == "__main__":
    PRODUCT_URL = 'https://www.popmart.com/gb/products/1036/Hirono-Echo-Series-Figures' 
    stock = check_stock(PRODUCT_URL)
    #print(stock) # Removed to avoid double logging

