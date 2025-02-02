from selenium import webdriver
from selenium.webdriver.common.by import By
import xml.etree.ElementTree as ET
import requests, os, random, time, zipfile

options = webdriver.ChromeOptions()
options.add_argument("--headless")  
driver = webdriver.Chrome(options=options)

# Function to extract sitemap from robots.txt
def get_sitemap_url(website):
    robots_url = website.rstrip("/") + "/robots.txt"
    try:
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            for line in response.text.split("\n"):
                if "Sitemap:" in line:
                    return line.split("Sitemap:")[1].strip()
    except requests.RequestException:
        pass
    return None

# Function to parse sitemap and get all URLs
def parse_sitemap(sitemap_url):
    urls = []
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for elem in root.iter():
                if "loc" in elem.tag:
                    urls.append(elem.text)
    except Exception as e:
        print("Error parsing sitemap:", e)
    return urls

# Function to identify policy pages from a list of URLs
def filter_policy_urls(urls):
    keywords = ["privacy", "policy", "terms", "corporate", "disclaimer"]
    return [url for url in urls if any(keyword in url.lower() for keyword in keywords)]

# Function to download PDFs and record the source policy URL
def download_pdfs(driver, policy_urls):
    pdf_dir = "policy_pdfs"
    os.makedirs(pdf_dir, exist_ok=True)

    pdf_links = []  
    pdf_sources = {}  

    for url in policy_urls[45:55]:  # Limiting range for controlled testing
        driver.get(url)
        time.sleep(random.uniform(2, 4))  

        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and href.endswith(".pdf"):
                pdf_links.append((url, href))  
                pdf_sources[href] = url  
                
                pdf_name = href.split("/")[-1]
                pdf_path = os.path.join(pdf_dir, pdf_name)
                try:
                    response = requests.get(href, timeout=10)
                    if response.status_code == 200:
                        with open(pdf_path, "wb") as f:
                            f.write(response.content)
                except requests.RequestException:
                    pass

    return pdf_links, pdf_sources

# Function to zip downloaded PDFs
def zip_pdfs():
    pdf_dir = "policy_pdfs"
    zip_file = "policies.zip"
    with zipfile.ZipFile(zip_file, "w") as zipf:
        for root, _, files in os.walk(pdf_dir):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    return zip_file


company_url = "https://www.goldmansachs.com/"  # Example usage
sitemap_url = get_sitemap_url(company_url)
if sitemap_url:
    print("Using Sitemap-Based Crawling...")
    urls = parse_sitemap(sitemap_url)
    policy_urls = filter_policy_urls(urls)
else:
    print("Sitemap not found.")

if not policy_urls:
    print("No policy pages found.")
else:
    print("Extracted Policy URLs:", policy_urls)
    pdf_links, pdf_sources = download_pdfs(driver, policy_urls)
    if pdf_links:
        print("Downloaded PDFs:")
        for policy_page, pdf in pdf_links:
            print(f"PDF: {pdf} (Found on: {policy_page})")

        zip_file = zip_pdfs()
        print("All PDFs zipped:", zip_file)

print("Finished.")
print(f'Number of policy urls extracted:{len(policy_urls)}, Number of pdfs extracted from 10 links used: {len(pdf_links)}')
driver.quit()
