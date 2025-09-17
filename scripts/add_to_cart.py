from playwright.sync_api import sync_playwright


def add_to_cart(PRODUCT_URL):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--window-size=1920,1080"]) # Make the browser window larger due to button not appearing
        page = browser.new_page()

        page.goto(PRODUCT_URL)
        print('Page title:', page.title())
        

        #Wait for everything to load in 
        
        
        try:
            page.get_by_text("ACCEPT").click()
        except Exception as e:
            print('error:',e)
        
        try:
            page.get_by_text("ADD TO CART").click()
        except Exception as e:
            print('error:',e)
        
        page.pause() # Pause to allow user interaction
        browser.close()

if __name__ == "__main__":
    PRODUCT_URL = 'https://www.popmart.com/gb/products/1036/Hirono-Echo-Series-Figures'
    add_to_cart(PRODUCT_URL)