from selenium import webdriver
from selenium.common.exceptions import (
    SessionNotCreatedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.service import Service


def initialise_driver():
    """
    Initialize a Chrome WebDriver instance with specific options.

    Returns:
        WebDriver: An instance of Chrome WebDriver.

    Raises:
        WebDriverException: If a WebDriver-related error occurs.
        PermissionError: If there's a permission error while accessing files.
        FileNotFoundError: If the specified ChromeDriver executable is not found.
        SessionNotCreatedException: If a new WebDriver session cannot be created.
        TimeoutException: If a timeout occurs while initializing the WebDriver.

    """
    try:
        # Set up the WebDriver service using the ChromeDriver executable path
        service = Service(
            "/Users/admin/Documents/Github Repos/EduInsights-Project/EduInsights/Driver/chromedriver-mac-x64/chromedriver"
        )

        # Set up ChromeOptions to configure the Chrome browser instance
        options = webdriver.ChromeOptions()
        options.add_argument(
            "--no-sandbox"
        )  # Disable sandbox mode for headless browsing
        options.add_argument(
            "--disable-dev-shm-usage"
        )  # Disable the /dev/shm usage for headless browsing
        options.add_argument(
            "--headless"
        )  # Run Chrome in headless mode (without GUI)
        options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # Set the binary location of the Brave Browser

        # Launch the Chrome browser with the specified service and options
        driver = webdriver.Chrome(service=service, options=options)

        return driver

    # Handle specific WebDriver-related exceptions
    except (
        WebDriverException,
        PermissionError,
        FileNotFoundError,
        SessionNotCreatedException,
        TimeoutException,
    ) as e:
        print(f"An error occurred: {e}")

    # Handle any other unexpected exceptions
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
