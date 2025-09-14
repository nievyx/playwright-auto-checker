# Labubu Checker  

A small Python application that uses [Playwright](https://playwright.dev/python/) to check stock availability of products on the [Pop Mart](https://www.popmart.com/gb) website.  

The script detects whether **Single Box** or **Whole Set** options are in stock by checking if product options are styled with a line-through (disabled).  

---

## Features  
- ✅ Check multiple product URLs automatically  
- ✅ Detect whether options are **in stock** or **out of stock**  
- ✅ Clean boolean output for easy automation later  
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
   git clone https://github.com/nievyx/labubu-checker.git
   cd labubu-checker
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
Checking product: https://www.popmart.com/gb/products/1036/Hirono-Echo-Series-Figures
Single Box: IN STOCK
Whole Set: OUT OF STOCK
```

---

## Roadmap  

- [ ] Send SMS/email alerts when desired items are in stock  
- [ ] Auto-add items to cart (experimental)  
- [ ] Deploy on Raspberry Pi for 24/7 monitoring  

---

## License  

MIT License – feel free to use and modify.  
