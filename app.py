import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random

# --- UI Setup ---
st.set_page_config(page_title="Giveaway Scraper", page_icon="🎁")
st.title("🎁 Live Stream Giveaway Bot by Cafemilkrock")
st.write("Extract usernames from a live chat to pick a random winner!")

# --- Input Form ---
target_url = st.text_input("Enter Stream URL:", "https://www.onlive.vn/")
duration = st.slider("How long to scrape the chat? (Seconds)", min_value=10, max_value=300, value=60)
css_selector = st.text_input("CSS Selector (Advanced):", 'span.channel-text[translate="no"]')

# --- Scraping Logic ---
if st.button("🚀 Start Scraping", type="primary"):
    
    st.info("Initializing background browser... Please wait.")
    
    # Headless Chrome Setup
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=options)
        usernames = set()
        
        st.write(f"🌐 Navigating to {target_url}...")
        driver.get(target_url)
        
        st.write("⏳ Waiting 10 seconds for video and chat to load...")
        time.sleep(10)
        
        # UI Placeholder for live progress updates
        progress_text = st.empty()
        
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                chat_elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
                for el in chat_elements:
                    name = el.get_attribute("textContent").strip()
                    if name and name not in usernames:
                        usernames.add(name)
            except Exception:
                pass
            
            # Update the UI with time remaining
            time_left = int(end_time - time.time())
            progress_text.text(f"📡 Scanning live chat... {time_left}s left. Found {len(usernames)} users so far.")
            time.sleep(1)
            
        driver.quit()
        progress_text.empty() # Clear the progress text
        
        # --- Results & Winner ---
        if usernames:
            user_list = list(usernames)
            st.success(f"✅ Crawl complete! Collected {len(user_list)} unique participants.")
            
            # Display names in a neat dropdown expander
            with st.expander("View Full Participant List"):
                for i, user in enumerate(user_list, 1):
                    st.write(f"{i}. {user}")
            
            st.write("### 🥁 Rolling for a random winner...")
            time.sleep(2)
            
            winner = random.choice(user_list)
            
            # Fire virtual balloons and show winner
            st.balloons()
            st.success(f"## 🎉 THE WINNER IS: {winner} 🎉")
            
        else:
            st.warning("❌ No participants found. Make sure the stream is live and people are chatting!")
            
    except Exception as e:
        st.error(f"A critical error occurred: {e}")
