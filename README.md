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

---

### 💡 Why this is better:

* **Targeted:** It only shows jobs that allow you to apply instantly on LinkedIn.
* **Clean Links:** I added a `.split('?')[0]` to the links. This removes all the tracking "junk" from the URL, making the links shorter and cleaner.
* **Interactive:** The "Easy Apply Now" button will open a new tab for each job, so you don't lose your place on your custom dashboard.

**Would you like me to show you how to schedule this script to run automatically every morning at 9:00 AM?**
