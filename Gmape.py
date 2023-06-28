import time
import postavke as pst
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# KOD

while True:
    cilj = input("trazim najduzu(d) ili najkracu(k)?")
    if not (cilj == 'd' or cilj == 'k'):
        print('odgovor mora biti d ili k')
    else:
        break

# otvaranje sajta
driver = webdriver.Firefox()
time.sleep(4)
driver.get(pst.sajt_mape)

try:
    # klik na dugme putanja
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, pst.klik_putanja)))
    driver.find_element(By.ID, pst.klik_putanja).click()

    # popunjavanje polja odakle i dokle
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, pst.input_od)))
    od = driver.find_element(By.XPATH, pst.input_od)
    od.send_keys(pst.odakle)

    do = driver.find_element(By.XPATH, pst.input_do)
    do.send_keys(pst.dokle)
    do.send_keys(Keys.RETURN)

    # odredjivanje vida pretrage - najbolje, auto, voz... bira auto
    driver.find_element(By.XPATH, pst.klik_vid).click()

    # u opcijama izaberi da bude bez naplate
    driver.find_element(By.XPATH, pst.klik_opcije).click()

    nrampe = driver.find_element(By.XPATH, pst.klik_nrampe)
    driver.execute_script("arguments[0].click();", nrampe)

    # ocitavanje svih vremena predlozenih putanja u levom panou
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, pst.trajanje)))
    pvoznje = driver.find_elements(By.XPATH, pst.pano_vremena)
    pkilometara = driver.find_elements(By.XPATH, pst.pano_duzine)

    # obrada dobijenih podataka - izdvajanje pojedinacnih vremena
    pano_h = [(n, x.text) for n, x in enumerate(pvoznje)]
    pano_km = [(m, y.text) for m, y in enumerate(pkilometara)]

    # trazi se najduzi/najkraci put
    mins = float(pano_km[0][1][:pano_km[0][1].find(' ')])
    if pano_km[0][1].find(' km') == -1:
        mins /= 1000
    minm = 0

    for m, t in pano_km:
        d = float(t[:t.find(' ')])
        if t.find('km') == -1:
            d /= 1000

        if cilj == 'k':
            if d < mins:
                mins = d
                minm = m
        elif cilj == 'd':
            if d > mins:
                mins = d
                minm = m

    # najduzi/najkraci put je pod rednim brojem minm:
    najb_h = pano_h[minm][1]
    najb_km = pano_km[minm][1]

    # klik na najduzi/najkraci put

    driver.find_elements(By.XPATH, pst.pano)[minm].click()
    if driver.find_element(By.XPATH, pst.detalji).is_displayed():
        driver.find_element(By.XPATH, pst.detalji).click()

    # pokupi vreme i kilometrazu za odabranu deonicu
    time.sleep(2)
    deo_h = driver.find_element(By.XPATH, pst.vr_deo).text
    deo_km = driver.find_element(By.XPATH, pst.km_deo).text.replace('(', '').replace(')', '')

    assert najb_h == deo_h, 'nisu ista vremena'
    assert najb_km == deo_km, 'nije ista duzina'

    driver.quit()

except NoSuchElementException as exception:
    print("Trazeni element " + exception.msg[1 + exception.msg.find(':'):exception.msg.find(
        ';')] + " nema na ovom sajtu. Nesto si se prejebao.")
    driver.quit()

except TimeoutException:
    print('Sajt je predugo ucitava. Probaj ponovo.')
    driver.quit()
