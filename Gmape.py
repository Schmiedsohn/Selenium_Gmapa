# postavke pretrage
sajt_mape = "https://www.google.com/maps/"

klik_putanja = "hArJGc"

input_od = "//*[@id='sb_ifc50']/*[@class='tactile-searchbox-input']"

input_do = "//*[@id='sb_ifc51']/*[@class='tactile-searchbox-input']"

odakle = "Budapest"
dokle = "Beograd"

klik_vid = "//*[@class='FkdJRd vRIAEd dS8AEf']/div[2]" #autom



import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#otvaranje sajta
driver = webdriver.Firefox()
time.sleep(4)
driver.get(sajt_mape)

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


# ocitavanje svih vremena predlozenih putanja
put = "//*[contains(@class,'Fk3sm')]"
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, put)))
putevi = driver.find_elements(By.XPATH, put)

# obrada dobijenih podataka - izdvajanje pojedinacnih vremena
v = [ vr.text for vr in putevi ]
vreme =[]
for x in v:
    sati = int(x[:x.find(' сат')])
    minu = x[x.find(' сат'):]
    minuta = int( ''.join(c for c in minu if c.isdigit()) )
    vreme.append(sati*60+minuta)

# odredjivanje najbrzeg puta i klik na njega
najbrzi = vreme.index(min(vreme))    

driver.find_element(By.ID,'section-directions-trip-' + str(najbrzi)).click()

