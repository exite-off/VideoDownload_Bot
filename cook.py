from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# initialize a browser driver
options = Options()
options.add_argument('--headless')
driver: WebDriver = webdriver.Firefox(options=options)

# navigate to a webpage
driver.get("!!!well known domain here...!!!")

# get cookies
all_cookies: list[dict] = driver.get_cookies()

# turn cookies into Netscape format
def generate_netscape_cookie_line(domain, flag, path, secure, expiration, name, value):
    return f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}"

# write cookies to a file
with open("cookies.txt", "w") as f:
    for cookie in all_cookies:

        line = generate_netscape_cookie_line(
            cookie["domain"],
            cookie["httpOnly"],
            cookie["path"],
            cookie["secure"],
            cookie.get("expiry") or 0,
            cookie["name"],
            cookie["value"]
        )
        f.write(line + "\n")

# close the browser
driver.quit()