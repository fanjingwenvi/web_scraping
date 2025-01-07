import os
import logging
import time
import undetected_chromedriver as uc 
from selenium import webdriver
import random

# Set the log file path with the timestamp inside the default log folder
log_folder = 'log'
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = os.path.join(log_folder, f"upwork_log_{timestamp}.log")

def configure_logging():
    """
    Configure logging to output log messages to both a file and the terminal screen.
    """
    # Create a logger
    logger = logging.getLogger('')
    # Check if handlers are already added to the logger
    if not logger.handlers:
        # Display INFO and higher level messages on the terminal
        logger.setLevel(logging.INFO)  
        # Create a file handler to save log messages to the specified log file
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)  
        # Create a stream handler to display log messages on the terminal
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)  
        # Create a formatter for the handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

# Call configure_logging() to configure logging when the module is imported
configure_logging()
# Add a default logging.info message when the module is imported
logging.info("Logging is successfully configured. Log file: %s" % log_file_path)

def configure_driver():
    """
        Config undetected chrome driver
        Set --user-data-dir to as Chrome default user profile to keep the website account login 
        Check chrome version is matcheted to the chrome driver version chrome://version/  
        Set implicitly wait time: implicitly_wait: defualt 0, set timeout to implicitly wait for findElement, or a command to complete
        Clean the Google/Chrome/Default/Default folder to avoid cache error 
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=/Users/violet/Library/Application Support/Google/Chrome/Default')
    # options.add_argument('proxy-server=106.122.8.54:3128')
    driver = uc.Chrome(options=options)    
    driver.implicitly_wait(20)
    return driver 

def get_to_page(driver, url): 
    
    """
        Get to the page and wait random time 
    """
    driver.get(url)
    time.sleep(random.randint(10, 20))
    # time.sleep(random.randint(5, 10)) for api

# Usage example:
if __name__ == "__main__":
    # Log some messages
    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")
                     
                     