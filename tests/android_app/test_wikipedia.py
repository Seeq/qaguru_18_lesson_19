from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


def test_search_wikipedia():
    with step('Skip onboarding'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")).click()

    with step('doubletap on search to activate searchfield'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/nav_tab_search")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/nav_tab_search")).click()

    with step('Type search request'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Appium')

    with step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


def test_search_wikipedia_skateboarding():
    with step('Skip onboarding'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")).click()

    with step('doubletap on search to activate searchfield'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/nav_tab_search")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/nav_tab_search")).click()

    with step('Type search request'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Skateboarding')

    with step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Skateboarding'))
