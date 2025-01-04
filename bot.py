from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to run the Selenium script
def selenium_task():
    # Initialize WebDriver
    driver = webdriver.Chrome()  # Provide ChromeDriver path if not in PATH
    driver.maximize_window()
    driver.get("https://newsonnline.com/safe.php?link={alias}")

    # Function to bypass ads, timers, and make buttons clickable
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

            # Attempt to click all visible "Continue" or "Verify" buttons
            buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'tp-btn') or @id='verifybtn' or @id='rtg-snp2']")
            for button in buttons:
                if button.is_displayed():
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(0.1)

        except Exception as e:
            print(f"An error occurred during bypass: {e}")

    # Main loop for page navigation
    try:
        for _ in range(4):  # Adjust based on flow
            advanced_bypass()
            time.sleep(0.5)

            try:
                final_button = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'OPEN - LINK')]"))
                )
                driver.execute_script("arguments[0].click();", final_button)
                print("Successfully reached the final link!")
                break
            except Exception as e:
                print("Proceeding to the next page or retrying:", e)
    finally:
        driver.quit()

# Telegram command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Starting the Selenium script. Please wait...")
    try:
        selenium_task()
        await update.message.reply_text("Selenium task completed successfully!")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

# Main function to start the bot
if __name__ == "__main__":
    application = ApplicationBuilder().token("6934514903:AAHLVkYqPEwyIZiyqEhJocOrjDYwTk9ue8Y").build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    print("Bot is running...")
    application.run_polling()
