import os
import time
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Edge('msedgedriver.exe')

df = pd.read_csv('paperlist.tsv', sep='\t', index_col=0)

ratings = dict()
for paper_id, link in tqdm(list(df.link.items())):

    try:
        driver.get(link)

        xpath = '//div[@id="note_children"]//span[@class="note_content_value"]'
        cond = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, 60).until(cond)

        elems = driver.find_elements_by_xpath(xpath)
        assert len(elems), 'empty ratings'
        elems = [x for x in elems if 'withdrawal' not in x.text]
        ratings[paper_id] = pd.Series([int(x.text.split(':')[0]) for x in elems[::2]], dtype=int)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(paper_id, e)
        ratings[paper_id] = pd.Series(dtype=int)

pd.DataFrame(ratings).T.to_csv('ratings.tsv', sep='\t')
