from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH
driver.maximize_window()

# Start from the first URL
driver.get("https://newsonnline.com/safe.php?link=tMtMFl")

# Function to bypass ads, timers, and make buttons clickable immediately
def advanced_bypass():
    try:
        # JavaScript to remove all identified ads, timers, and other blocking elements
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
            
            // Force countdown to zero if exists
            const timerElement = document.getElementById("tp-time");
            if (timerElement) timerElement.innerText = "0";
            
            // Show hidden buttons and enable them
            const buttons = document.querySelectorAll("button.tp-btn, #verifybtn, #rtg-snp2");
            buttons.forEach(btn => {
                btn.style.display = "block";
                btn.style.visibility = "visible";
            });
        """
        driver.execute_script(remove_elements_script)

        # Attempt to click all visible "Continue" or "Verify" buttons immediately
        buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'tp-btn') or @id='verifybtn' or @id='rtg-snp2']")
        for button in buttons:
            if button.is_displayed():
                driver.execute_script("arguments[0].click();", button)
                time.sleep(0.1)  # Short delay to allow page transition

    except Exception as e:
        print(f"An error occurred during bypass: {e}")

# Main loop to bypass each page's ads and timers
start_time = time.time()
for _ in range(4):  # Adjust based on the number of pages in the flow
    advanced_bypass()
    time.sleep(0.5)  # Minimal pause to load the next page

    # Check for the "OPEN - LINK" button on the final page
    try:
        final_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'OPEN - LINK')]"))
        )
        driver.execute_script("arguments[0].click();", final_button)
        print("Successfully reached the final link!")
        break
    except Exception as e:
        print("Proceeding to the next page or retrying:", e)

# Close the browser after completion or after a set timeout (for safety)
if (time.time() - start_time) < 5:
    time.sleep(200)
driver.quit()
