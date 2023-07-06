import time
import postavke as pst
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


def km_m(duzina):
    d = float(duzina[:duzina.find(' ')])
    if duzina.find(' km') == -1:
        d = d / 1000
    return d


def nadji_putanju(odakle, dokle, kakvu):
    # otvaranje sajta
    driver = webdriver.Firefox()
    # driver = webdriver.Chrome()
    time.sleep(4)
    driver.get(pst.sajt_mape)

    try:
        # klik na dugme putanja
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, pst.klik_putanja)))
        driver.find_element(By.ID, pst.klik_putanja).click()

        # popunjavanje polja odakle i dokle
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, pst.input_od)))
        od = driver.find_element(By.XPATH, pst.input_od)
        od.send_keys(odakle)

        do = driver.find_element(By.XPATH, pst.input_do)
        do.send_keys(dokle)
        do.send_keys(Keys.RETURN)

        # odredjivanje vida pretrage - najbolje, auto, voz... bira auto
        driver.find_element(By.XPATH, pst.klik_vid).click()

        # u opcijama izaberi da bude bez naplate
        driver.find_element(By.XPATH, pst.klik_opcije).click()

        nrampe = driver.find_element(By.XPATH, pst.klik_nrampe)
        driver.execute_script("arguments[0].click();", nrampe)

        # ocitavanje svih vremena predlozenih putanja u levom panou
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, pst.trajanje)))

        putanje = driver.find_elements(By.XPATH, "//*[starts-with(@id,'section-directions-trip')]/div/div/div/div/div")

        zeljenput = km_m(putanje[0].text)
        nput = 0
        for i in range(1, len(putanje)):
            trenutniput = km_m(putanje[i].text)
            if kakvu == 'max':
                if trenutniput > zeljenput:
                    nput = i
            elif kakvu == 'min':
                if trenutniput < zeljenput:
                    nput = i

        najb_km = putanje[nput].text

        if not driver.find_element(By.XPATH, pst.pano).get_attribute('ID') == 'section-directions-trip-details-msg-' \
                + str(nput):
            driver.find_elements(By.XPATH, pst.pano)[nput].click()
        driver.find_element(By.XPATH, pst.detalji).click()

        # pokupi vreme i kilometrazu za odabranu deonicu
        time.sleep(5)
        deo_km = driver.find_element(By.XPATH, pst.km_deo).text.replace('(', '').replace(')', '')

        # assert najb_h == deo_h, 'nisu ista vremena'
        assert najb_km == deo_km, 'nije ista duzina'

        # driver.quit()

    except NoSuchElementException as exception:
        print("Trazeni element " + exception.msg[1 + exception.msg.find(':'):exception.msg.find(
            ';')] + " nema na ovom sajtu. Nesto si se prejebao.")
        driver.quit()

    except TimeoutException:
        print('Sajt je predugo ucitava. Probaj ponovo.')
        driver.quit()
