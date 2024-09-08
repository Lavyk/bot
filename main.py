
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from ultil import renew_connection, navigate_and_click
from threading import Thread
import time

def start_chrome():
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = '/usr/bin/chromium-browser'
        options.add_argument('--no-sandbox')
        options.add_argument('--disabled-dev-shm-usage')
        options.add_argument('--proxy-server=socks5://localhost:9050')
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)        
        return driver
    except Exception as e:
        print(f'Failed to start Chrome browser: {repr(e)}')

def start():
    driver = start_chrome()
    navigate_and_click(driver)
    driver.quit()        

def main():
    for count in range(50):
        try:
            threads = []
           
            renew_connection()
            print("Conectou")
            print(f"{count + 1} tentativas.")
            thread1 = Thread(target=start)           
            thread1.start()

            thread2 = Thread(target=start)
            thread2.start()

            thread1.join()
            thread2.join()

            time.sleep(10)
        except:
            print('Não foi possivel concluir.')
            driver.quit()

if __name__ == "__main__":
    main()
