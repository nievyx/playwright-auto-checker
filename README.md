# Playwright Auto Checker

A Python automation tool that monitors product stock on e-commerce sites using Playwright
. When selected product options are available, it sends real-time SMS notifications. Designed as a personal automation project, it’s also a practical way to explore web scraping, browser automation, and notification systems.


This application is currently tailored for Pop Mart
, where it checks the availability of Single Box and Whole Set options. Stock status is determined by detecting whether product options are styled with a line-through (indicating they’re disabled/out of stock) 

---

## Features  

- ✅ Automatically check multiple product URLs  
- ✅ Detect whether product options are **in stock** or **out of stock**  
- ✅ Return clean boolean output for easy automation  
- ✅ Send SMS alerts when desired items are available  
- ✅ Store and track stock status using JSON to avoid duplicate notifications  
- ✅ Designed to run on a local machine or Raspberry Pi


---

## Project Structure  

```
.

├── .gitignore                  # Ignore virtual env, .env, etc.
├── .env                        # Local environment variables (Twilio keys, phone number)
├── config.py                   # Imports env variables for scripts
├── app.py                       # Main entry point to run product checks
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── scripts/                     # All individual scripts
    ├── line_through_check.py    # Core stock checker script
    ├── detect_stock.py          # Optional/legacy stock checking
    └── send_sms.py              # Sends SMS notifications for in-stock items

```

## Demo

Here’s a screenshot of the app in action:

![Screenshot of app](assets/Screenshot.PNG)


---

## Scripts Overview  

- **`app.py`**  
  Main entry point. Iterates through a list of product URLs and prints stock availability for each.  

- **`scripts/line_through_check.py`**  
  Core stock checker. Contains the `check_stock()` function that returns a dictionary of `{option: bool}` (e.g., `{"Single Box": True, "Whole Set": False}`).  

- **Other experimental scripts** *(optional)*  
  You may still have older scripts like `detect_stock.py` or `check_options.py` in the repo. These were early tests and can be cleaned up later. The main production-ready script is `line_through_check.py`.  

---

## Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/nievyx/playwright-auto-checker.git
   cd project-name
   ```

2. Set up a virtual environment (optional but recommended):  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

---

## Usage  

Run a stock check on a single product:  
```bash
python scripts/line_through_check.py
```

Or run checks on multiple products with:  
```bash
python app.py
```

Example output:  
```
Checking product: https://www.<example>.com/gb/products/1036/<example>-Echo-Series-Figures
Single Box: IN STOCK
Whole Set: OUT OF STOCK
```
## for SMS usage:
Create a .env file (local only)
```
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
MY_PHONE_NUMBER=+0987654321
```
---

## Roadmap  

- [ ] Auto-add items to cart (experimental)  
- [ ] Deploy on Raspberry Pi for 24/7 monitoring  

---

## License  

MIT License – feel free to use and modify.  
