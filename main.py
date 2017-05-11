from scrapingClass import scrapingClass

if __name__ == '__main__':
    scraping = scrapingClass()
    scraping.startScraping()
    scraping.writeCSV()