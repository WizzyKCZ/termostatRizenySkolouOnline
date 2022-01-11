import sys
import csv
import numpy as numpy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import datetime

file = open('file.csv')
type(file)

csvreader = csv.reader(file)

header = []
header = next(csvreader)
header

rows = []
for row in csvreader:
    rows.append(row)
rows

lastRow = rows[len(rows)-1]

username = lastRow[0][lastRow[0].find('input_text.username=')+20:lastRow[0].find(';', lastRow[0].find('input_text.username='))]
password = lastRow[5][lastRow[5].find('input_text.password=')+20:lastRow[5].find(';', lastRow[5].find('input_text.password='))]
tempIdle = (float)(lastRow[10][lastRow[10].find('input_number.tempidle=')+22:lastRow[10].find(';', lastRow[10].find('input_number.tempidle='))])
tempActive = (float)(lastRow[16][lastRow[16].find('input_number.tempactive=')+24:lastRow[16].find(';', lastRow[16].find('input_number.tempidle=')-13)])

file.close()

cas = [400, 450, 500, 555, 620, 670, 720, 770, 780, 870, 920]
now = datetime.datetime.now()


def hledej(lst, s):
    for i in lst:
        if i not in s:
            continue
        yield i, s.index(i)


url = 'https://www.skolaonline.cz/Aktuality.aspx'

driver_location = "/usr/bin/chromedriver"
binary_location = "/usr/bin/google-chrome"

options = webdriver.ChromeOptions()
options.binary_location = binary_location

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path=driver_location, chrome_options=options)

driver.get(url)

driver.find_element(By.ID, 'JmenoUzivatele').send_keys(username)
driver.find_element(By.ID, 'HesloUzivatele').send_keys(password)
button = driver.find_element_by_id("dnn_ctr994_SOLLogin_btnODeslat")
driver.execute_script("arguments[0].click();", button)

soup = BeautifulSoup(driver.page_source, 'lxml')

driver.close()
driver.quit()

cal = soup.find('table', class_="DctTable")

row = soup.find('tr', class_="RowOdd")

final = []

for tds in row.find_all('td', class_="DctCell"):
    if tds.text == "":
        final.append(False)
    else:
        if tds.has_attr('colspan'):
            for x in range(int(tds['colspan'])):
                final.append(True)
        else:
            final.append(True)


cas_nyni = now.hour*60 + now.minute

a = numpy.array(final)
i = a.tolist().index(1)

final.reverse()
ar = numpy.array(final)
ir = ar.tolist().index(1)

if cas[i] < cas_nyni < cas[ir]:
    with open('ofile.csv', 'w') as f:
        f.write("{\"temperature\": " + str(tempActive) + "}")
else:
    with open('ofile.csv', 'w') as f:
        f.write("{\"temperature\": " + str(tempIdle) + "}")
