import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Path to ChromeDriver
chromedriver_path = r"C:\Users\Shajin\Devops\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Local HTML files
urls = [
    r"C:\Users\Shajin\Devops\index.html",
    r"C:\Users\Shajin\Devops\about.html",
    r"C:\Users\Shajin\Devops\Aswin.html",
    r"C:\Users\Shajin\Devops\Berin.html",
    r"C:\Users\Shajin\Devops\Gershan.html",
    r"C:\Users\Shajin\Devops\Shajin.html"
]

# Pages with extra sections
portfolio_files = ["Aswin.html", "Berin.html", "Gershan.html", "Shajin.html"]

# Folder for screenshots
output_folder = r"C:\Users\Shajin\Devops\Test_output"
os.makedirs(output_folder, exist_ok=True)

# -- Headless driver for testing --
headless_options = Options()
headless_options.add_argument("--headless")
headless_options.add_argument("--window-size=1920,1080")

service = Service(chromedriver_path)
test_driver = webdriver.Chrome(service=service, options=headless_options)

# Run tests
for url in urls:
    try:
        print(f"\n🔎 Testing: {url}")
        test_driver.get(f"file:///{url}")
        time.sleep(1)

        filename = os.path.basename(url)

        # Profile picture
        try:
            test_driver.find_element(By.CLASS_NAME, "profile-pic")
            print("[✓] Profile Picture found.")
        except:
            print("[✗] Profile Picture not found.")

        # About section
        try:
            test_driver.find_element(By.XPATH, "//h2[contains(translate(text(),'ABOUT','about'), 'about')]")
            print("[✓] About Section found.")
        except:
            print("[✗] About Section not found.")

        # Other sections for portfolios
        if filename in portfolio_files:
            for section in ["SKILLS", "PROJECTS", "CONTACT", "FIND ME ONLINE"]:
                try:
                    test_driver.find_element(By.XPATH, f"//h2[contains(translate(text(),'{section}','{section.lower()}'), '{section.lower()}')]")
                    print(f"[✓] {section} Section found.")
                except:
                    print(f"[✗] {section} Section not found.")

        # Screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = filename.replace(".html", f"_{timestamp}.png")
        screenshot_path = os.path.join(output_folder, screenshot_name)
        test_driver.save_screenshot(screenshot_path)
        print(f"[✓] Screenshot saved: {screenshot_path}")

    except Exception as e:
        print(f"[!] Error while testing {url}: {e}")

test_driver.quit()
print("\n✅ All tests completed.")

# -- Open ONLY index.html and let user explore manually --
visible_options = Options()
visible_options.add_experimental_option("detach", True)  # Keeps the browser open
visible_driver = webdriver.Chrome(service=service, options=visible_options)

# Open homepage only
visible_driver.get(f"file:///{urls[0]}")
visible_driver.maximize_window()
print(f"🌐 Opened homepage: {urls[0]}")
print("🟢 User can now manually explore the portfolio.")

# Wait for user
input("🔵 Press ENTER to close the browser...")

visible_driver.quit()
