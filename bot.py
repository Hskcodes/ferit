from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# JavaScript script file path
SCRIPT_PATH = "modiji.py"

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Use /test to execute the script.")

# Test command
def test(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Testing the script...")

    # Configure Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Target website to test
        target_url = "https://modijiurl.com"  # Replace with your actual testing URL
        driver.get(target_url)
        update.message.reply_text(f"Website loaded: {target_url}")

        # Load JavaScript from modiji.py
        with open(SCRIPT_PATH, "r") as file:
            js_code = file.read()

        # Execute JavaScript code in the browser
        driver.execute_script(js_code)
        update.message.reply_text("Script executed successfully!")

    except Exception as e:
        update.message.reply_text(f"Error during execution: {e}")

    finally:
        driver.quit()
        update.message.reply_text("Test completed.")

# Main function
def main():
    # BotFather se liya gaya token
    TOKEN = "7572985591:AAFQg29Ek-ckECGpwFCJm4m-6i63zXZmrbI"

    # Telegram bot setup
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("test", test))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
