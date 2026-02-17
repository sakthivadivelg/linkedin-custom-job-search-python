import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
LI_AT_COOKIE = "XXXXXXX"

# Job search keywords
KEYWORDS = "HTML%20CSS%20Javascript"

# Target locations with their LinkedIn location IDs (India cities as first priority)
TARGET_LOCATIONS = {
    "Bangalore, Karnataka": "102713980",      # Bangalore/Bengaluru, India
    "Chennai, Tamil Nadu": "102713981",       # Chennai, India
    "Dubai, UAE": "106057199",
    "Saudi Arabia": "100459407",
    "Singapore": "102454443",
    "Malaysia": "106808692",
    "Australia": "101452733",
    "Netherlands": "102890719",
    "Switzerland": "106693272",
    "Germany": "101282230",
    "United Kingdom": "101165590",
    "France": "105015875",
    "Spain": "105646813",
    "Italy": "103350119",
    "Sweden": "105117694",
    "Norway": "103819153",
    "Denmark": "104514075",
}

# Base search URL template
BASE_SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords={}&location={}&locationId={}&f_AL=true"

def search_jobs_in_location(driver, location_name, location_id):
    """Search for jobs in a specific location"""
    search_url = BASE_SEARCH_URL.format(KEYWORDS, location_name.replace(" ", "%20").replace(",", "%2C"), location_id)
    print(f"🔍 Searching in {location_name}...")
    driver.get(search_url)
    time.sleep(5)  # Wait for jobs to load
    
    job_data = []
    # Find job cards (try multiple selectors for robustness)
    job_cards = (driver.find_elements(By.CSS_SELECTOR, "[data-job-id]") or 
                driver.find_elements(By.CSS_SELECTOR, ".job-card-container") or
                driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item"))
    print(f"📋 Found {len(job_cards)} job cards in {location_name}")

    for i, card in enumerate(job_cards[:10]):  # Get top 10 jobs per location
        try:
            # Try multiple selectors for title
            title_element = None
            for selector in [".job-card-list__title", ".job-card-container__link", "h3 a", "h4 a", "[data-test-job-title]", ".sr-only"]:
                try:
                    title_element = card.find_element(By.CSS_SELECTOR, selector)
                    if title_element.text.strip():
                        break
                except:
                    continue
            
            if not title_element or not title_element.text.strip():
                print(f"  ❌ No title found for job {i+1} in {location_name}")
                continue
                
            title = title_element.text.strip()
            link = title_element.get_attribute("href") or "https://linkedin.com/jobs"
            if link and '?' in link:
                link = link.split('?')[0]  # Clean URL
            
            # Try multiple selectors for company
            company = "Company Not Listed"
            for selector in [".job-card-container__primary-description", ".job-card-container__company-name", "h4", "[data-test-employer-name]"]:
                try:
                    company_element = card.find_element(By.CSS_SELECTOR, selector)
                    if company_element.text.strip():
                        company = company_element.text.strip()
                        break
                except:
                    continue
            
            job_data.append({"title": title, "company": company, "link": link, "location": location_name})
            print(f"  ✓ Job {i+1}: {title} at {company} | {location_name}")
            
        except Exception as e:
            print(f"  ❌ Error parsing job {i+1} in {location_name}: {str(e)[:100]}...")
            continue
    
    return job_data

def run_job_search():
    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    print("🔄 Setting up Chrome driver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("✅ Chrome driver ready")
    
    try:
        # 1. Authorize
        print("🌐 Navigating to LinkedIn...")
        driver.get("https://www.linkedin.com")
        print("🔐 Adding authentication cookie...")
        driver.add_cookie({"name": "li_at", "value": LI_AT_COOKIE, "domain": ".www.linkedin.com"})
        
        all_jobs = []
        
        # 2. Search in each location
        for location_name, location_id in TARGET_LOCATIONS.items():
            location_jobs = search_jobs_in_location(driver, location_name, location_id)
            all_jobs.extend(location_jobs)
            time.sleep(3)  # Be respectful to LinkedIn's servers
        
        # 3. Generate the HTML File
        print(f"📄 Generating HTML file with {len(all_jobs)} total jobs...")
        generate_html(all_jobs)
        
        # Print summary
        location_counts = {}
        for job in all_jobs:
            location = job['location']
            location_counts[location] = location_counts.get(location, 0) + 1
        
        print("\\n📊 Job Summary by Location:")
        for location, count in location_counts.items():
            print(f"  📍 {location}: {count} jobs")
        print(f"\\n🎯 Total jobs found: {len(all_jobs)}")

    finally:
        driver.quit()

def generate_html(jobs):
    # Generate location counts
    location_counts = {}
    for job in jobs:
        location = job['location']
        location_counts[location] = location_counts.get(location, 0) + 1
    
    # Create location filter options
    location_options = ""
    for location, count in sorted(location_counts.items()):
        location_options += f'                    <option value="{location}">{location} ({count})</option>\\n'
    
    # Create job cards HTML
    job_cards_html = ""
    for i, job in enumerate(jobs):
        safe_title = job['title'].replace('"', '&quot;')
        safe_company = job['company'].replace('"', '&quot;')
        safe_location = job['location'].replace('"', '&quot;')
        
        job_cards_html += f'''                <div class="job-card" data-location="{safe_location}">
                    <div class="job-content">
                        <div class="job-number">{i+1}</div>
                        <div class="info">
                            <h3>{safe_title}</h3>
                            <p><strong>Company:</strong> {safe_company}</p>
                            <p class="location">📍 {safe_location}</p>
                        </div>
                    </div>
                    <a href="{job['link']}" class="apply-btn" target="_blank">Easy Apply</a>
                </div>
'''
    
    # Create complete HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Global LinkedIn Job Search Results</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; padding: 40px; }}
        .container {{ max-width: 1200px; margin: auto; }}
        .job-card {{ background: white; padding: 20px; margin-bottom: 15px; border-radius: 10px; 
                   border-left: 5px solid #0073b1; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                   display: flex; justify-content: space-between; align-items: center; }}
        .job-number {{ background: #0073b1; color: white; width: 35px; height: 35px; 
                     border-radius: 50%; display: flex; align-items: center; 
                     justify-content: center; font-weight: bold; margin-right: 15px; }}
        .job-content {{ display: flex; align-items: center; flex-grow: 1; }}
        .info {{ flex-grow: 1; }}
        .info h3 {{ margin: 0 0 5px 0; color: #333; font-size: 18px; }}
        .info p {{ color: #666; margin: 3px 0; }}
        .info .location {{ color: #0073b1; font-weight: 500; }}
        .location-filter {{ margin-bottom: 25px; }}
        .location-filter select {{ padding: 10px 15px; border: 1px solid #ddd; 
                                 border-radius: 5px; font-size: 14px; }}
        .apply-btn {{ background: #0073b1; color: white; padding: 12px 25px; 
                    text-decoration: none; border-radius: 25px; font-weight: bold; 
                    transition: 0.3s; margin-left: 15px; }}
        .apply-btn:hover {{ background: #005582; }}
        .summary {{ background: white; padding: 20px; border-radius: 10px; 
                  margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Global HTML/CSS/JS Job Opportunities</h1>
        
        <div class="summary">
            <h3>📊 Search Summary</h3>
            <p><strong>Total Jobs Found:</strong> {len(jobs)}</p>
            <p><strong>Countries Searched:</strong> {len(location_counts)}</p>
        </div>
        
        <div class="location-filter">
            <label for="location-select"><strong>Filter by Location:</strong> </label>
            <select id="location-select" onchange="filterByLocation()">
                <option value="all">All Locations ({len(jobs)})</option>
{location_options.rstrip()}
            </select>
        </div>
        
        <div id="jobs-container">
{job_cards_html.rstrip()}
        </div>
    </div>
    
    <script>
        function filterByLocation() {{
            const selectedLocation = document.getElementById('location-select').value;
            const jobCards = document.querySelectorAll('.job-card');
            
            jobCards.forEach(card => {{
                if (selectedLocation === 'all' || card.dataset.location === selectedLocation) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>"""
    
    # Write to file
    with open("easy_apply_jobs.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"\\n✅ HTML file created successfully with {len(jobs)} job listings!")

if __name__ == "__main__":
    run_job_search()
