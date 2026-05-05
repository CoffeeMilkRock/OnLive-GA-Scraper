from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random

def crawl_chat_github(url, chat_selector, duration_seconds=120):
    print("Initializing GitHub Actions headless browser...")
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    usernames = set()
    
    try:
        print(f"Navigating to {url}...")
        driver.get(url)
        time.sleep(10) 
        
        print(f"\n--- Monitoring Live Chat for {duration_seconds} seconds ---")
        
        end_time = time.time() + duration_seconds
        while time.time() < end_time:
            try:
                chat_elements = driver.find_elements(By.CSS_SELECTOR, chat_selector)
                for el in chat_elements:
                    name = el.get_attribute("textContent").strip()
                    if name and name not in usernames:
                        usernames.add(name)
                        print(f"New participant: {name}")
            except Exception:
                pass 
            time.sleep(1)

        return list(usernames)

    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    finally:
        driver.quit()

if __name__ == "__main__":
    target_url = "https://www.onlive.vn/ducmanh"
    chat_name_css = 'span.channel-text[translate="no"]' 
    
    collected_users = crawl_chat_github(target_url, chat_name_css, duration_seconds=120)
    
    print("\n" + "="*40)
    print("--- FINAL LIST FOR GIVEAWAY ---")
    if collected_users:
        for i, user in enumerate(collected_users, 1):
            print(f"{i}. {user}")
            
        print("\n🥁 Rolling for a random winner...")
        winner = random.choice(collected_users)
        print(f"🎉 THE WINNER IS: {winner} 🎉")
    else:
        print("❌ No participants found.")
    print("="*40 + "\n")
