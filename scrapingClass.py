from holderClass import holderClass
import csv, multiprocessing
from time import gmtime, strftime
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup


class scrapingClass:

    startingWebsite = ""
    categoryUrls = []
    holderClassList = []
    pageUrls = []

    def  __init__(self):
        self.startingWebsite = 'http://www.expertonline.it'
        self.holderClassList = multiprocessing.Manager().list()
        self.pageUrls = multiprocessing.Manager().list()

    def startScraping(self):

        self.categorise()
        self.sortPagination()
        self.formFromPageURLS()
        print("Qty of holderClassList: ", len(self.holderClassList))
        seen = set()
        self.holderClassList = [x for x in self.holderClassList if x.article not in seen and not seen.add(x.article)]
        print("Qty of holderClassList: ", len(self.holderClassList))

    def categorise(self):
        website = requests.get(self.startingWebsite)
        content = BeautifulSoup(website.content, "html.parser")
        for ul in content.find_all('ul', {"class": "dropdown-menu"}):
            for div in ul.find_all('div', {"class": "col-sm-12 livello2"}):
                for a in div.find_all('a'):
                    self.categoryUrls.append(self.startingWebsite + a['href'])

    def sortPagination(self):
        print("Starting to proccess pagination ", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        with Pool(multiprocessing.cpu_count()) as p:
            p.map(self.pagination, self.categoryUrls)
        #for url in self.categoryUrls:
        #    self.pagination(url)
        print("Finnished pagination proccess ", strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    def pagination(self, url):
        #print("Paginating: ", url)
        website = requests.get(url)
        if website.status_code != 200:
            print("Something went wrong with: ", website.url, " status code: ", website.status_code)
        else:
            content = BeautifulSoup(website.content, "html.parser")
            if len(content.find_all('div', {"class": "skywalker_scheda"}))>0:
                hc = holderClass(content)
                self.holderClassList.append(hc)
            elif len(content.find_all('ul', {"class": "pagination"})) > 0:
                self.pageUrls.append(url)
                while True:
                    urlList = content.find_all('ul', {"class": "pagination"})[0].find_all('a')
                    urlToAdd = self.startingWebsite + urlList[len(urlList)-1]['href']
                    if '#' in urlToAdd:
                        break
                    else:
                        self.pageUrls.append(urlToAdd)
                        content = BeautifulSoup(requests.get(urlToAdd).content, "html.parser")
            else:
                self.pageUrls.append(url)


    def writeCSV(self):
        print("starting to write CSV file")
        OutputFile = "Out_" + strftime("%Y-%m-%d %H_%M_%S", gmtime()) + ".csv"
        with open(OutputFile, 'w', newline='\n') as csvfile:
            fieldnames = ['product_name', 'article', 'price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for hc in self.holderClassList:
                if hasattr(hc, "name") and hasattr(hc, "article") and hasattr(hc, "price"):
                    writer.writerow({'product_name': hc.name, 'article': hc.article, 'price': hc.price})
        print("CSV file writing finished")

    def formFromPageURLS(self):
        print("Starting to form objects from urls")
        with Pool(multiprocessing.cpu_count()) as p:
            p.map(self.formFromPageURLSWorker, self.pageUrls)
        print("Finnished forming objects")

    def formFromPageURLSWorker(self, url):
        website = requests.get(url)
        if website.status_code != 200:
            print("Something went wrong with: ", website.url, " status code: ", website.status_code)
        else:
            content = BeautifulSoup(website.content, "html.parser")
            productListURLS = [url['href'] for url in content.find_all('a', {"id": "LnkProdotto"})]
            for url in productListURLS:
                website = requests.get(url)
                if website.status_code != 200:
                    print("Something went wrong with: ", website.url, " status code: ", website.status_code)
                else:
                    content = BeautifulSoup(website.content, "html.parser")
                    try:
                        hc = holderClass(content)
                        self.holderClassList.append(hc)
                    except:
                        print("Failure to form", url)
                        continue
                        pass
            #print()
