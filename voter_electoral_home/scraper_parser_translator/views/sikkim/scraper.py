from selenium import webdriver
import os
import requests
from pathlib import Path
from mimetypes import guess_extension
from ..scraperResponse import ScraperResponse

# driver_path = "/home/samaygandhi/Documents/chromedriver"
# chromedriver_autoinstaller.install()
    
class ScraperClass:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.DRIVER = webdriver.Chrome(options=options)
        self.SCRAPER_RESPONSE = ScraperResponse()
        self.SCRAPER_RESPONSE.captcha_generated = None

    def run(self, district, assemblyConstituency, pollingPart, req_media_dir):
        s = requests.session()
        print(f"ac {assemblyConstituency} pp {pollingPart}")
        assemblyCode = assemblyConstituency.split('-')[-1].strip()

        url = f"https://ceosikkim.nic.in/UploadedFiles/ElectoralRollPolling/S21A{assemblyCode}P{pollingPart}.pdf"

        print(url)
        r = s.get(url)
        print(r.status_code)
        if r.status_code == 200:
            guess = guess_extension(r.headers['content-type'])
            if not guess: guess = ".pdf"
            # pdf_file_path = "/scraper_parser_translator/views/sikkim/electoral_rolls" + guess
            pdf_file_path = req_media_dir + "electoral_rolls" + guess
            # pdf_file_path = (os.path.abspath(os.getcwd()) + pdf_file_path)
            print(pdf_file_path)
            self.SCRAPER_RESPONSE.electoral_roll_PDF = pdf_file_path
            if guess:
                print("Storing pdf...")
                with open(pdf_file_path, "wb") as f:
                    f.write(r.content)
                self.SCRAPER_RESPONSE.status = True
        else:
            self.SCRAPER_RESPONSE.message = "Could not store Electoral PDFs"

        return self.SCRAPER_RESPONSE
         

