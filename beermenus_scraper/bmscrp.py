#! /bin/env python
# script to scrape Boston beers using selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os

def get_sumpage(driver):
    driver.get('http://beermenus.com/places')
    driver.find_element_by_class_name('close').click()
    addr=driver.find_element_by_name('location[address]')
    addr.send_keys(len("Long Beach, CA, 90808, US")*Keys.BACKSPACE)
    addr.send_keys('Boston, MA, United States')
    time.sleep(1)
    sug_id=driver.page_source.split('id="option-')[1].split('"')[0]
    driver.find_element_by_id('option-'+sug_id).click()
    driver.find_element_by_name("commit").click()
    with open('/tmp/p1.html','w') as f: f.write(driver.page_source)
    driver.find_element_by_partial_link_text("Next").click()
    with open('/tmp/p2.html','w') as f: f.write(driver.page_source)

def get_htmls(driver,outdir="data_html",inf='/tmp/p1.html'):
    os.system('mkdir -p '+outdir)
    with open(inf) as f:
        for url in [i.split('>')[0].split('"')[0] for i in f.read().split('<a href="/places/')[1:]]:
            with open('{0}/{1}.html'.format(outdir,url),'w') as outf:
                driver.get('https://www.beermenus.com/places/'+url)
                if 'class="close"' in driver.page_source: driver.find_element_by_class_name('close').click()
                if "View All Bottles" in driver.page_source: driver.find_element_by_partial_link_text("View All Bottles" ).click()
                if "View All Cans" in driver.page_source: driver.find_element_by_partial_link_text("View All Cans" ).click()
                outf.write(driver.page_source)
            

if __name__=='__main__':
    drv=webdriver.Firefox()
    get_sumpage(drv)
    get_htmls(drv,'data_html','/tmp/p1.html')
    get_htmls(drv,'data_html','/tmp/p2.html')
    drv.quit()

