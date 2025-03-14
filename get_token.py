import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from preset import getPreset

chrome_options = Options()
user_agent=f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
chrome_options.add_argument("user-agent="+user_agent)
chrome_options.add_experimental_option("detach", True)
os = platform.system()
if os == 'Windows':
    chrome_options.add_argument('user-data-dir=C:\\user_data\\user')
elif os == 'Darwin': # Mac
    pass
elif os == 'Linux':
    pass
driver = webdriver.Edge(options=chrome_options)

def main():
    presetData = getPreset()

    if presetData['page'] == '':
        driver.get("https://beyondlive.com")
        input('시청 페이지 접속 후 아무 키를 누르고 엔터: ')
    else:
        driver.get(presetData['page'])



def wait_element(t, element, clickable=False):
    target = WebDriverWait(driver, t).until(EC.visibility_of_element_located(element))
    if clickable:
        target.click()
    return target


if __name__ == "__main__":
    main()