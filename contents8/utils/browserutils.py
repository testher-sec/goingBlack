import time

def wait_for_browser(browser):
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)
    return
