import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import requests
from stem import Signal
from stem.control import Controller
import time
import random

gecko_driver_path = "/usr/local/bin/geckodriver"  # Caminho para o geckodriver no Linux

os.environ['PATH'] += os.pathsep + gecko_driver_path

def start_tor_browser(profile):
    try:
        tor_options = Options()
        tor_options.binary_location = "/usr/bin/tor-browser"  # Altere para o caminho correto do Tor Browser no Linux
        tor_options.set_preference("network.proxy.type", 1)
        tor_options.set_preference("network.proxy.socks", "127.0.0.1")
        tor_options.set_preference("network.proxy.socks_port", 9150)
        tor_options.add_argument("-profile")
        tor_options.add_argument(profile)
        driver = webdriver.Firefox(options=tor_options)
        return driver
    except Exception as e:
        print(f'Failed to start Tor browser: {repr(e)}')

def get_ip(driver):
    driver.get("https://check.torproject.org/")
    try:
        ip_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.content p strong'))
        )
        ip = ip_element.text
        print(f"Current IP: {ip}")
    except Exception as e:
        print(f"Failed to retrieve IP: {e}")
    time.sleep(2)

def click_elemento_aleatorio(elements):
    elemento = random.choice(elements)
    elemento.click()

def navigate_and_click(driver):
    try:
        driver.get("https://Fodaralho.Com")
        time.sleep(3)
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Aceitar"]'))
        )
        accept_button.click()
        time.sleep(1)
        abas = driver.window_handles
        
        if len(abas) > 1:
            driver.switch_to.window(abas[0])
            time.sleep(5)
            driver.close()
            abas = driver.window_handles
            driver.switch_to.window(abas[0])
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Aceitar"]'))
            )
            accept_button.click()
            
        time.sleep(2)
        elementos_sponsored = driver.find_elements(By.CSS_SELECTOR, ".ad-desktop div div")
        if elementos_sponsored:
            click_elemento_aleatorio(elementos_sponsored)

        abas = driver.window_handles
        
        if len(abas) > 1:
            driver.switch_to.window(abas[1])
            time.sleep(10)
            driver.close()
            abas = driver.window_handles
            driver.switch_to.window(abas[0])
            
        div_categorias = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "list-categorias"))
        )
        
        links = div_categorias.find_elements(By.TAG_NAME, "a")
        elem = random.choice(links)
        driver.get(elem.get_attribute('href'))
        
        time.sleep(2)
        elementos_sponsored = driver.find_elements(By.CSS_SELECTOR, ".ad-desktop div div")
        if elementos_sponsored:
            click_elemento_aleatorio(elementos_sponsored)
            time.sleep(8)
        
    except Exception as e:
        print(f"Failed to navigate and click: {e}")
    time.sleep(5)

def get_current_ip():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
    }

    try:
        r = session.get('http://httpbin.org/ip')
        return r.text
    except Exception as e:
        print(e)

def renew_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="YOUR_TOR_PASSWORD")  # Autenticar com o controlador do Tor
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())
        print(f"Novo IP: {get_current_ip()}")

def main():
    for count in range(50):
        drivers = []
        drivers.append(start_tor_browser("/path/to/your/firefox/profile"))  # Altere para o caminho do perfil do Firefox

        text_found = False
        time.sleep(5)
        while not text_found:
            try:
                drivers[0].find_element(By.ID, "cancelButton")
            except:
                text_found = True
                pass
    
        print("Conectou")
        
        for driver in drivers:
            try:
                navigate_and_click(driver)
            except Exception as e:
                print(f"Erro: {e}")
        for driver in drivers:
            driver.quit()
        
        print(f"{count} tentativas.")
        renew_ip()

if __name__ == "__main__":
    main()
