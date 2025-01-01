from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot
import time
from selenium.webdriver.chrome.options import Options

# Your Telegram Bot Token
BOT_TOKEN = '6934514903:AAHLVkYqPEwyIZiyqEhJocOrjDYwTk9ue8Y'  # Replace with your Telegram bot token
CHAT_ID = '-1002066437865'   # Replace with your Telegram chat ID

# Initialize ChromeOptions for headless mode and other necessary options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")  # For Linux systems
options.add_argument("--disable-dev-shm-usage")  # For Linux systems
options.add_argument("--remote-debugging-port=9222")  # Fix for DevToolsActivePort error

# Initialize WebDriver with the options
driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is in your PATH
driver.maximize_window()

# Telegram bot setup
bot = Bot(token=BOT_TOKEN)

def send_message(message: str):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Function to bypass ads, timers, and make buttons clickable immediately
def advanced_bypass():
    try:
        remove_elements_script = """
            const adIds = [
                "BR-Footer-Ads", "SoumyaHelp-Ads", "div-gpt-ad-1729274101641-0", 
                "div-gpt-ad-1725903218856-0", "loading-container",
                "znlvejeddvcwhdcgttwvbwrlsewvsctfzdvutkxdeusnorvzdzdxgwy"
            ];
            adIds.forEach(id => {
                const element = document.getElementById(id);
                if (element) element.remove();
            });
            const timerElement = document.getElementById("tp-time");
            if (timerElement) timerElement.innerText = "0";
            const buttons = document.querySelectorAll("button.tp-btn, #verifybtn, #rtg-snp2");
            buttons.forEach(btn => {
                btn.style.display = "block";
                btn.style.visibility = "visible";
            });
        """
        driver.execute_script(remove_elements_script)
        buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'tp-btn') or @id='verifybtn' or @id='rtg-snp2']")
        for button in buttons:
            if button.is_displayed():
                driver.execute_script("arguments[0].click();", button)
                time.sleep(0.1)
    except Exception as e:
        send_message(f"An error occurred during bypass: {e}")

# Main loop to bypass each page's ads and timers
def start():
    send_message("Starting to bypass ads and timers...")
    start_time = time.time()
    for _ in range(4):  
        advanced_bypass()
        time.sleep(0.5)
        try:
            final_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'OPEN - LINK')]"))
            )
            driver.execute_script("arguments[0].click();", final_button)
            final_link = driver.current_url  # Get the final link URL
            send_message(f"Successfully reached the final link: {final_link}")
            break
        except Exception as e:
            send_message("Proceeding to the next page or retrying: " + str(e))

    if (time.time() - start_time) < 5:
        time.sleep(200)
    driver.quit()

# Start the process
start()
