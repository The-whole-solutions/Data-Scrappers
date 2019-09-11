import pandas as pd
import traceback
from db import Mdb
from utils import sleep_scrapper, get_request_headers, scraper_csv_write
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

class GoogleSearchListingsScraper:
    
    def __init__(self, keyword):
        self.keyword = keyword
        self.mdb = Mdb()
       
        

    def run(self):
        try:

           options = Options()
           options.add_argument("window-size=1400,600")
           ua = UserAgent()
           a = ua.random
           user_agent = ua.random

           options.add_argument(f'user-agent={user_agent}')
           driver = webdriver.Chrome("C:/Users/Dell/Downloads/chromedriver_win32/chromedriver.exe", options=options)
           html = driver.page_source
          
           


           for i in range(00,60,10):
               suffix = '&q=%s' % self.keyword
               url = 'https://www.google.com/search?client=firefox-b-d&biw=1366&bih=654&sa=N&ved=0ahUKEwjfy8ugnZHkAhVLro8KHXq1Ar0Q8tMDCJMC&ei=zslbXd-sHcvcvgT66oroCw&start='+str(i)+suffix
               driver.get(url)
               html = driver.page_source
               
               # scrap_data(website_link,website_title,website_snippet)
               soup = BeautifulSoup(html, 'html.parser')
               print('...........soupppppppppp',soup.encode('utf-8'))
               for div in soup.find_all('div', class_='g'):
                    print('---------------------div', div)
                    self.scrap_result_row(div)
               time.sleep(15)
               sleep_scrapper('GoogleSearchListingsScraper')
        
        except Exception as exp:
            print ('[GoogleSearchListingsScraper] :: run() :: Got exception: %s' % exp)
            print(traceback.format_exc())
    
    def scrape_result_now(self,div):
        try:
            website_link=[]
            website_snippet=[]
            website_title=[]
            results = div.find("div", {"class":""})
            for result in results:
                website_link.append(result.find("div", {"class":"title-bar-left"}).get_text().strip())
                print('[GoogleSearchListingsScraper] :: address . . . . ..:', website_link)
                website_title.append(result.find("span", {"result-adress"}).get_text().strip())
                print('[GoogleSearchListingsScraper] :: title . . . . ..:', website_title)
                website_snippet.append(result.find("div", {"class":"xl-desc"}).get_text().strip())
                print('[GoogleSearchListingsScraper] :: description . . . . ..:', website_snippet)

                self.mdb.google_listings_by_search_scrapper_data(website_link,website_title,website_snippet)

                #header row of csv file defined here 
                df = pd.DataFrame({"Title":website_title,"Address":website_link,"Description":website_snippet})
                df.to_csv("output.csv")
        except Exception as exp:
            print ('[GoogleSearchListingsScraper] :: run() :: Got exception: %s' % exp)
            print(traceback.format_exc())

            

    
       
if __name__ == '__main__':
    google_search_listings = GoogleSearchListingsScraper('android')
    google_search_listings.run()