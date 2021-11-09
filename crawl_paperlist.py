import os
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Edge('msedgedriver.exe')
driver.get('https://openreview.net/group?id=ICLR.cc/2022/Conference')

cond = EC.presence_of_element_located((By.XPATH, '//*[@id="all-submissions"]/nav/ul/li[13]/a'))
WebDriverWait(driver, 60).until(cond)

with open('paperlist.tsv', 'w', encoding='utf8') as f:
    f.write('\t'.join(['paper_id', 'title', 'link', 'keywords', 'abstract'])+'\n')

for page in tqdm(range(1, 68)):
    text = ''
    elems = driver.find_elements_by_xpath('//*[@id="all-submissions"]/ul/li')
    for i, elem in enumerate(elems):
        try:
            # parse title
            title = elem.find_element_by_xpath('./h4/a[1]')
            link = title.get_attribute('href')
            paper_id = link.split('=')[-1]
            title = title.text.strip().replace('\t', ' ').replace('\n', ' ')
            # show details
            elem.find_element_by_xpath('./a').click()
            time.sleep(0.2)
            # parse keywords & abstract
            items = elem.find_elements_by_xpath('.//li')
            keyword = ''.join([x.text for x in items if 'Keywords' in x.text])
            abstract = ''.join([x.text for x in items if 'Abstract' in x.text])
            keyword = keyword.strip().replace('\t', ' ').replace('\n', ' ').replace('Keywords: ', '')
            abstract = abstract.strip().replace('\t', ' ').replace('\n', ' ').replace('Abstract: ', '')
            text += paper_id+'\t'+title+'\t'+link+'\t'+keyword+'\t'+abstract+'\n'
        except Exception as e:
            print(f'page {page}, # {i}:', e)
            continue

    with open('paperlist.tsv', 'a', encoding='utf8') as f:
        f.write(text)

    # next page
    try:
        driver.find_element_by_xpath('//*[@id="all-submissions"]/nav/ul/li[13]/a').click()
        time.sleep(2) # NOTE: increase sleep time if needed
    except:
        print('no next page, exit.')
        break
