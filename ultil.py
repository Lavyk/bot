import random
import time

from stem import Signal
from stem.control import Controller

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="bot")
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())
        
def click_elemento_aleatorio(driver):
    elementos_sponsored = driver.find_elements(By.CSS_SELECTOR, ".ad-desktop div div")
    if elementos_sponsored:
        elemento = random.choice(elementos_sponsored)
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        
        actions = ActionChains(driver)

        x_offset = 10
        y_offset = 15

        actions.move_to_element_with_offset(elemento, x_offset, y_offset).click().perform()
        #elemento.click()
        
        abas = driver.window_handles
        if len(abas) > 1:
            driver.switch_to.window(abas[1])
            time.sleep(15)
            driver.close()
            abas = driver.window_handles
            driver.switch_to.window(abas[0])
        
def navigate_and_click(driver):
    try:
        driver.get("https://fodaralho.com")
        time.sleep(3)
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Aceitar"]'))
        )
        accept_button.click()
        time.sleep(1)
        
        # Ir para pagina do anuncio home
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
            
        time.sleep(4)
        
        # Clicar em um anuncio na pagina principal
        click_elemento_aleatorio(driver)
            
        # Entrar em uma categoria aleatoria
        div_categorias = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "list-categorias"))
        )
        
        links = div_categorias.find_elements(By.TAG_NAME, "a")
        elem = random.choice(links)
        driver.get(elem.get_attribute('href'))
        time.sleep(4)
        
        # Clicar anuncio dentro da categoria
        click_elemento_aleatorio(driver)
            
        
        # Entrar em um video aleatorio        
        links = driver.find_elements(By.CLASS_NAME, "card")
        elem = random.choice(links)
        driver.get(elem.get_attribute('href'))
        time.sleep(4)
        
        # Clicar anuncio dentro do video
        click_elemento_aleatorio(driver)
        
    except Exception as e:
        print(f"Failed to navigate and click: {e}")
        
