#
# Script for scrapping
#


import requests
import traceback
from db import Mdb
from bs4 import BeautifulSoup
from utils import sleep_scrapper, get_request_headers, scraper_csv_write


class YellowPagesScraper:

    def __init__(self):
        self.mdb = Mdb()

    def run(self):
        base_url = 'https://www.yellowpages.com/search?search_terms=software+company&geo_location_terms=New+York%2C+NY&page='

        for j in range(27, 100, 1):
            try:
                url = base_url + str(j)
                print ('[YellowPagesScraper] :: fetching data from url: ', url)

                r = requests.get(url, headers=get_request_headers())
                if not r.status_code == 200:
                    print ('[YellowPagesScraper] :: Failed to get the content ' \
                          'of url: %s' % url)
                    return
                html_doc = r.content

                soup = BeautifulSoup(html_doc, 'html.parser')
                for div in soup.find_all('div', class_='info'):
                    self.scrap_result_row(div)
                sleep_scrapper('YellowPagesScraper')
            except Exception as exp:
                print ('[YellowPagesScraper] :: run() :: Got exception: %s' % exp)
                print(traceback.format_exc())

    def scrap_result_row(self, div):

        try:
 #get title of company
            h2 = div.find('h2', class_='n')
            title = h2.find('a', class_='business-name').text.strip()
            print ("[YellowPagesScraper] :: title: %s" % title)
 #get rating_count of company       
            rating_count = 0
            span = div.find('span', class_='count')
            if span:
                span = span.text.strip()
                rating_count = span
                print ("[YellowPagesScraper] :: rating_count: %s" % rating_count)
#get the address of the company
            
            p = div.find('p', class_='adr')
            street_address = p.find('div',class_='street-address')
            if street_address:
                str_adrs = street_address.text.strip()
                locality = p.find('div',class_='locality').text.strip()
                address = str_adrs + locality
                print ("[YellowPagesScraper] :: address: %s" % address)
            
                address=''
            
              else:  
#get the contact Number of Company
            phone = ''
            li = div.find('div', class_='phones phone primary')
            if li:
                phone = li.text.strip()
                print ("[YellowPagesScraper] :: phone: %s" % phone)
            else:
                print ("[YellowPagesScraper] :: phone: %s" % li)
#get the categories of company
            categories = ''
            cat_div = div.find('div', class_='categories')
            category = cat_div.find('a')
            if category:
                categories = cat_div.text.strip()
                print ("[YellowPagesScraper] :: categories: %s" % categories)
            else:
                print ("[YellowPagesScraper] :: categories: %s" % cat_div)
#get the website of the company
            
            div22=div.find('div',class_='info-section info-primary')
            webpage_link  = div22.find('a', {'class': 'track-visit-website'})
            if webpage_link:
                website_link = (webpage_link)['href']
                print('[YellowPagesScraper] :: webpage_link: %s' % website_link)
            else:
                website_link=''
                 

           
            self.mdb.yellowpages_scrapper_data(title, rating_count, address, phone, categories,website_link)

            fname = 'data_yellow_pages.csv'
            msg = "%s, %s, %s, %s, %s, %s" % (title, rating_count, address, phone, categories, website_link)
            #print ("[YellowPagesScraper] :: scrap_result_row() :: msg:", msg)
            scraper_csv_write(fname, msg)

         
        # except:
        #     pass
        except Exception as exp:
            
                
            print ('[YellowPagesScraper] :: scrap_result_row() :: ' \
             'Got exception: %s' % exp)
            print(traceback.format_exc())
            


if __name__ == '__main__':
    yellowpages = YellowPagesScraper()
    yellowpages.run()

