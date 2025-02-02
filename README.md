# 🕵️‍♂️ Policy Scraper - Task at Carbon Crunch

This project is a **web scraper** that dynamically extracts company policy pages and downloads relevant **PDF documents** from a given company's website.

## **🚀 Features**
- ✅ Extracts the **sitemap** from `robots.txt` (if available).
- ✅ Parses the sitemap and filters **policy-related URLs**.
- ✅ Scrapes policy pages to find **PDF downloads**.
- ✅ Records **which policy page** the PDF was found on.
- ✅ **Zips all downloaded PDFs** for easy access.
- ✅ Uses **Selenium with headless browsing** for automation.

---

## **📌 Procedure**
1. **Check for `robots.txt`**  
   - Extracts the **sitemap** if available.
   - If found, parses it to get all URLs.

2. **Identify Policy Pages**  
   - Filters URLs containing **privacy, terms, policy, disclaimer, corporate**.

3. **Extract PDFs**  
   - Visits each policy page and scans for **PDF links**.
   - Downloads the **PDF file** and records the **source policy page**.

4. **Save & Zip Files**  
   - Stores PDFs in `policy_pdfs/` directory.
   - Zips all PDFs into `policies.zip`.
