import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from selene import browser, support
import os
from dotenv import load_dotenv
from appium import webdriver

@pytest.fixture(scope='function', autouse=True)
def load_env():
    load_dotenv()

def attach_bstack_video(session_id):
    import requests
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(os.getenv("BS_USERNAME"), os.getenv("BS_KEY")),
    ).json()
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='Видео теста',
        attachment_type=allure.attachment_type.HTML,
    )

@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    options = UiAutomator2Options().load_capabilities({
        "platformName": "android",
        "platformVersion": os.getenv("ANDROID_PLATFORM_VERSION"),
        "deviceName": "Samsung Galaxy S23 Ultra",
        "app": os.getenv("APP_ANDROID"),
        'bstack:options': {
            "projectName": "Browserstack Android Tests",
            "buildName": "Browserstack-build-1",
            "sessionName": "Search Test",
            "userName": os.getenv("BS_USERNAME"),
            "accessKey": os.getenv("BS_KEY")
        }
    })

    # browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    # browser.config.driver_options = options

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            'http://hub.browserstack.com/wd/hub',
            options=options
        )

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='Screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='XML screen structure',
        attachment_type=allure.attachment_type.XML,
    )

    session_id = browser.driver.session_id
    browser.quit()
    attach_bstack_video(session_id)


