# linkedin-custom-job-search-python
A Python-based automation tool using Selenium that scrapes LinkedIn for HTML, CSS, and JavaScript 'Easy Apply' jobs and generates a custom HTML dashboard for quick applications
Files to Add (Post-Creation)
Once you click Create repository, you should upload three main files to make the project complete:

scraper.py: The actual Python code we discussed (using the li_at cookie).

requirements.txt: A list of the libraries needed to run your code. It should contain:

<pre>Plaintext
selenium
webdriver-manager
</pre>
README.md: A guide on how to use it. You should include:

How to find the li_at cookie.

How to install the requirements.

How to run the script.

**Visibility & License**
Visibility: Keep it Public if you want to show this off in your portfolio.

Add .gitignore: Select the Python template. This prevents "junk" files (like __pycache__) from being uploaded to GitHub.

Add license: I recommend the MIT License. It’s a standard, simple license that allows others to use your code while protecting you from liability.


I have noted your `li_at` cookie. **A quick word of caution:** Treat that code like a password. Anyone who has it can access your LinkedIn account without needing your email or 2FA. Never share it in public forums!

To answer your question: **Yes, we can filter specifically for "Easy Apply" jobs.** This makes your generated HTML page much more powerful because you know every link will lead to a quick 1-2 minute application.

### 🔍 Filtering for "Easy Apply"

On LinkedIn, "Easy Apply" is a specific search filter. When you toggle it, LinkedIn adds `f_AL=true` to the URL.

Here is your updated configuration and the final logic to build that HTML page:

---

### 🛠️ The Final Python Script

```python
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
LI_AT_COOKIE = "XXXXXXXXX"
# This URL includes the "f_AL=true" filter for Easy Apply
SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords=HTML%20CSS%20Javascript&f_AL=true"

def run_job_search():
    options = Options()
    # options.add_argument("--headless") # Run in background
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 1. Authorize
        driver.get("https://www.linkedin.com")
        driver.add_cookie({"name": "li_at", "value": LI_AT_COOKIE, "domain": ".www.linkedin.com"})
        
        # 2. Search
        driver.get(SEARCH_URL)
        time.sleep(5) # Wait for jobs to load

        job_data = []
        # 3. Find job cards
        job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")

        for card in job_cards[:15]: # Get the top 15 jobs
            try:
                title_element = card.find_element(By.CLASS_NAME, "job-card-list__title")
                title = title_element.text
                link = title_element.get_attribute("href").split('?')[0] # Clean URL
                company = card.find_element(By.CLASS_NAME, "job-card-container__primary-description").text
                
                job_data.append({"title": title, "company": company, "link": link})
            except:
                continue

        # 4. Generate the HTML File
        generate_html(job_data)

    finally:
        driver.quit()

def generate_html(jobs):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Easy Apply Dashboard</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 40px; }}
            .container {{ max-width: 800px; margin: auto; }}
            .job-card {{ background: white; padding: 20px; margin-bottom: 15px; border-radius: 10px; border-left: 5px solid #0073b1; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }}
            .info h3 {{ margin: 0; color: #333; }}
            .info p {{ color: #666; margin: 5px 0; }}
            .apply-btn {{ background: #0073b1; color: white; padding: 12px 25px; text-decoration: none; border-radius: 25px; font-weight: bold; transition: 0.3s; }}
            .apply-btn:hover {{ background: #005582; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 HTML/CSS/JS Easy Apply Leads</h1>
            <p>Found {len(jobs)} jobs for you today.</p>
            {"".join([f'''
            <div class="job-card">
                <div class="info">
                    <h3>{j['title']}</h3>
                    <p>{j['company']}</p>
                </div>
                <a href="{j['link']}" class="apply-btn" target="_blank">Easy Apply Now</a>
            </div>
            ''' for j in jobs])}
        </div>
    </body>
    </html>
    """
    with open("easy_apply_jobs.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("\n✅ Done! Open 'easy_apply_jobs.html' to start applying.")

if __name__ == "__main__":
    run_job_search()

```

-----------------------------------------------------------------------------------------------------------------------------------------------------

### 💡 Why this is better:

* **Targeted:** It only shows jobs that allow you to apply instantly on LinkedIn.
* **Clean Links:** I added a `.split('?')[0]` to the links. This removes all the tracking "junk" from the URL, making the links shorter and cleaner.
* **Interactive:** The "Easy Apply Now" button will open a new tab for each job, so you don't lose your place on your custom dashboard.


Using the **`li_at`** cookie is much safer and more reliable than typing your password into a script. This cookie is a "session token" that tells LinkedIn you are already logged in, allowing your script to bypass the login screen and the pesky 2FA (Two-Factor Authentication) codes.

### 🔍 How to find your `li_at` cookie

1. Open Chrome and log in to [LinkedIn.com](https://www.google.com/url?sa=E&source=gmail&q=https://www.linkedin.com).
2. Right-click anywhere on the page and select **Inspect** (or press `F12`).
3. Go to the **Application** tab at the top (you might need to click the `>>` arrows to see it).
4. In the left sidebar, under **Storage**, click on **Cookies** and then select `https://www.linkedin.com`.
5. In the list that appears, search for the name **`li_at`**.
6. Copy the long string of text in the **Value** column. **Keep this secret!** It acts like a temporary password.

---

### 🛠️ Updated Python Script (Cookie Version)

Now, we modify the script to inject that cookie into the browser session. This is much faster and less likely to get your account flagged.

```python
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
LI_AT_COOKIE = "PASTE_YOUR_COOKIE_HERE"  # Replace with your actual li_at value
SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords=HTML%20CSS%20Javascript"

def get_jobs_with_cookie():
    options = Options()
    # options.add_argument("--headless") # Optional: runs without opening a window
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 1. Visit LinkedIn first (required to set cookies for the domain)
    driver.get("https://www.linkedin.com")
    
    # 2. Add the session cookie
    driver.add_cookie({
        "name": "li_at",
        "value": LI_AT_COOKIE,
        "domain": ".www.linkedin.com"
    })
    
    # 3. Refresh or navigate to the jobs page
    driver.get(SEARCH_URL)
    time.sleep(5) # Give the page time to load the jobs

    # ... (Insert the same scraping logic from the previous script here) ...
    
    print("Successfully bypassed login using cookies!")
    # driver.quit()

get_jobs_with_cookie()

```

### 💡 Pro-Tips for Your Job Board HTML

Since you want a custom HTML page to browse these jobs, here are two ways to make it better:

* **Filter for "Easy Apply":** You can modify the `SEARCH_URL` to include the Easy Apply filter. On LinkedIn, click the "Easy Apply" button manually once, then copy that new URL into your script.
* **Auto-Date:** Add a timestamp to your HTML file name (e.g., `jobs_Feb_16.html`) so you can track your search history over time.

-------------------------------------------------------------------------------------------------------------------------------

To build a working automation for LinkedIn, we need to use **Selenium** because LinkedIn's job listings are loaded dynamically with JavaScript.

### 🛠️ Prerequisites

You will need to install the following libraries:
`pip install selenium webdriver-manager`

---

## 🚀 The Python Automation Script

This script will log in to LinkedIn, search for the keywords, scrape the job links, and generate your HTML file.

```python
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
EMAIL = "your_email@example.com"
PASSWORD = "your_password"
SEARCH_QUERY = "https://www.linkedin.com/jobs/search/?keywords=HTML%20CSS%20Javascript"

def get_linkedin_jobs():
    # Setup Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Uncomment to run without opening browser
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    job_results = []

    try:
        # 1. Login
        driver.get("https://www.linkedin.com/login")
        driver.find_element(By.ID, "username").send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5) # Wait for login to complete

        # 2. Search Jobs
        driver.get(SEARCH_QUERY)
        time.sleep(5)

        # 3. Scrape Job Cards
        # We look for the job cards and extract Title, Company, and Link
        cards = driver.find_elements(By.CLASS_NAME, "job-card-container")
        
        for card in cards[:10]: # Limit to first 10 for safety
            try:
                title_el = card.find_element(By.CLASS_NAME, "job-card-list__title")
                title = title_el.text
                link = title_el.get_attribute("href")
                company = card.find_element(By.CLASS_NAME, "job-card-container__primary-description").text
                
                job_results.append({"title": title, "company": company, "link": link})
            except Exception as e:
                continue

    finally:
        driver.quit()
    
    return job_results

def save_to_html(jobs):
    html_template = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; padding: 50px; background: #f4f4f9; }}
            .job-card {{ background: white; padding: 20px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .apply-btn {{ display: inline-block; background: #0073b1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Latest Frontend Jobs</h1>
        {''.join([f'<div class="job-card"><h3>{j["title"]}</h3><p>{j["company"]}</p><a class="apply-btn" href="{j["link"]}" target="_blank">Apply on LinkedIn</a></div>' for j in jobs])}
    </body>
    </html>
    """
    with open("my_job_board.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Success! Open 'my_job_board.html' to see your links.")

# Run the process
scraped_jobs = get_linkedin_jobs()
if scraped_jobs:
    save_to_html(scraped_jobs)
else:
    print("No jobs found or login failed.")

```

---

## ⚠️ Vital Precautions

LinkedIn's security is world-class. If you use this script, follow these rules to avoid getting your account banned:

1. **Use a "Human" Delay:** LinkedIn detects rapid clicking. Notice the `time.sleep(5)` commands; these are necessary to let the page load and look like a human is browsing.
2. **Two-Factor Authentication (2FA):** If your account has 2FA, the script will pause at the login screen. You will need to manually enter the code in the browser window before the script continues.
3. **The "li_at" Method:** Professional scrapers often use the `li_at` cookie instead of email/password to bypass the login screen entirely. This is more stable but slightly more advanced to set up.

---

### How this works for you:

Once you run this, a file named `my_job_board.html` will appear in your folder. When you open it, you’ll have a clean list of jobs with buttons that take you directly to the application page.

