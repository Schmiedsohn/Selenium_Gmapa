# postavke pretrage
sajt_mape = "https://www.google.com/maps/"

klik_putanja = "hArJGc"

input_od = "//*[@id='sb_ifc50']/*[@class='tactile-searchbox-input']"

input_do = "//*[@id='sb_ifc51']/*[@class='tactile-searchbox-input']"

odakle = "Budapest"
dokle = "Beograd"

klik_opcije = "//*[contains(@class,'OcYctc ')]"
klik_autoput = "//*[@id='pane.directions-options-avoid-highways']"
klik_nrampe = "//*[@id='pane.directions-options-avoid-tolls']"

klik_vid = "//*[@class='FkdJRd vRIAEd dS8AEf']/div[2]" 


trajanje = "//*[contains(@class,'Fk3sm')]"
duzina = "//*[contains(@class,'ivN21e tUEI8e fontBodyMedium')]/div"

vr_deonica = "//*[@class='directions-mode-distance-time fontBodySmall']"
km_deonica = "//*[@class='directions-mode-distance-time fontBodySmall']/span"

#KOD
import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

#otvaranje sajta
driver = webdriver.Firefox()
time.sleep(4)
driver.get(sajt_mape)
#driver.set_window_size(400,300)

try:
    # klik na dugme putanja
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, klik_putanja)) )
    driver.find_element(By.ID, klik_putanja).click()

    # popunjavanje polja odakle i dokle
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, input_od)))
    od = driver.find_element(By.XPATH, input_od)
    od.send_keys(odakle)

    do = driver.find_element(By.XPATH, input_do)
    do.send_keys(dokle)
    do.send_keys(Keys.RETURN)

    # odredjivanje vida pretrage - najbolje, auto, voz...
    driver.find_element(By.XPATH, klik_vid).click()

    # u opcijama izaberi da ne ide auto-putevima i da bude bez naplate
    driver.find_element(By.XPATH, klik_opcije).click()

##    autoput = driver.find_element(By.XPATH, klik_autoput)
##    driver.execute_script("arguments[0].click();", autoput)
    nrampe = driver.find_element(By.XPATH, klik_nrampe   )
    driver.execute_script("arguments[0].click();", nrampe )

    # ocitavanje svih vremena predlozenih putanja

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, trajanje)))
    hvoznje = driver.find_elements(By.XPATH, trajanje)
    kilometri = driver.find_elements(By.XPATH, duzina)
    
    # obrada dobijenih podataka - izdvajanje pojedinacnih vremena
    v = [ vr.text for vr in hvoznje ]
    
    vreme =[]
    for x in v:
        sati = int(x[:x.find(' сат')])
        minu = x[x.find(' сат'):]
        minuta = int( ''.join(c for c in minu if c.isdigit()) )
        vreme.append(sati*60+minuta)

    # odredjivanje najbrzeg puta i klik na njega
    najbrzi = vreme.index(min(vreme))    

    km = [ int(k.text[:k.text.find(' km')]) for k in kilometri ]

    
    driver.find_element(By.ID,'section-directions-trip-' + str(najbrzi)).click()



    UkVrDeonica = driver.find_elements(By.XPATH, vr_deonica)
    UkKmDeonica = driver.find_elements(By.XPATH, km_deonica)

    v = [ vr.text for vr in UkVrDeonica ]
    km_d = [ k.text for k in UkKmDeonica ]

    km2 = 0
    for x in km_d:
        if x.find('km') == -1:
            km2 += int(x[1:x.find(' m')])/1000
        else:
            km2 += float(x[1:x.find(' km')].replace(',','.'))

    km2 = math.ceil(km2)
                       
    vreme2 =[]
    for x in v:
        sati = int(x[:x.find(' сат')]) if x.find(' сат')>0 else 0
        minu = x[x.find(' сат'):x.find(' (')] if x.find(' сат')>0 else x[:x.find(' (')]
        minuta = int( ''.join(c for c in minu if c.isdigit()) )
        vreme2.append(sati*60+minuta)

        
    print ('Provera vremena: ' + ('OK' if sum(vreme2) == vreme[najbrzi] else ('Nije dobro. Po deonicama: ' + str(sum(vreme2))    + ' min, a cela ruta: ' + str(vreme[najbrzi])    )))
    print ('Provera duzine: '  + ('OK' if km2 == km[najbrzi]       else ('Nije dobro. Po deonicama: ' + str(km2)       + ' km, a cela ruta: ' + str(km[najbrzi])   )))

    driver.quit()
    
except NoSuchElementException as exception:
    print("Trazeni element nema na ovom sajtu. Nesto si se prejebao.")
    driver.quit()
    
except TimeoutException:
    print('Sajt je predugo ucitava. Probaj ponovo.')
    driver.quit()
