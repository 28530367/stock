from tqdm import tqdm
import fitz
from extractPdf import *


class Sinopac(ExtractPdf):
    '''Handle 永豐(Sinopac) pdf

        Args :
            directory_path : (str) pdf path
        
        Return :
            rating : (str) recommend
    '''
    def __init__(self, file_path):
        super().__init__(file_path)
        self.file_path = file_path
        self.possible_rating = ['買進', '中立']

    def get_all(self):
        doc, page = self.open()
        advisor, version = self.get_advisor_and_version(doc, page)
        # stock = self.get_stock(page, version)
        # date = self.get_date(page, version)
        stock = 'NULL'
        date = 'NULL'
        rating_1, rating_2 = self.get_rating(page, version)
        rating = self.check_rating(rating_1, rating_2, self.possible_rating)
        tp_1, tp_2 = self.get_tp(page, version)
        tp = self.check_targrt_price(tp_1, tp_2)
        author_1, author_2 = self.get_author(page, version)
        author = self.check_author(author_1, author_2)
        summary_1, summary_2 = self.get_summary(page, version)
        summary = self.check_summary(summary_1, summary_2)
        self.close(doc)
        return advisor, version, stock, date, rating_1, rating_2, rating, \
            tp_1, tp_2, tp, author_1, author_2, author, \
            summary_1, summary_2, summary
        # return advisor, version, stock, date, rating, tp, author, summary
        
    def get_advisor_and_version(self, doc, page):
        advisor, version = 'NULL', 'NULL'
        page_check_source = doc.load_page(-1)
        text_check_source = page_check_source.get_text()
        if self.check_source(text_check_source):
            advisor = self.__class__.__name__
            version = self.check_version(text_check_source)
        return advisor, version

    def check_source(self, text_check_source):
        check_source = ['永豐證券投資顧問股份有限公司', 'SinoPac Securities']
        return True if any(keyword in text_check_source for keyword in check_source) else False

    def check_version(self, text_check_version):
        check_report = ['SinoPac Securities']
        if any(keyword in text_check_version for keyword in check_report):
            return 'new'
        else:
            return 'old'
    
    def get_rating(self, page, version):
        rating_1, rating_2 = 'NULL', 'NULL'
        if version == 'old':
            rating_1 = self.get_rating_old_version_1(page)
            rating_2 = self.get_rating_old_version_2(page)
        elif version == 'new':
            rating_1 = self.get_rating_new_version_1(page)
            rating_2 = self.get_rating_new_version_2(page)
        return rating_1, rating_2

    def get_rating_old_version_1(self, page):
        clip_old_version_1 = fitz.Rect(220, 80, 560, 140)
        text_old_version_1 = page.get_text(clip=clip_old_version_1, sort=True).strip()
        try:
            text_old_version_1 = text_old_version_1.split('）')[1].strip()
            return text_old_version_1.split('\n')[1].strip()
        except:
            return 'NULL'

    def get_rating_old_version_2(self, page):
        clip_old_version_2 = fitz.Rect(425, 90, 560, 130)
        return page.get_text(clip=clip_old_version_2, sort=True).strip()
    
    def get_rating_new_version_1(self, page):
        clip_new_version_1 = fitz.Rect(0, 0, 200, 400)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            text_new_version_1 = text_new_version_1.split('投資建議')[1]
            return text_new_version_1.split('\n')[0].strip()
        except:
            return 'NULL'
    
    def get_rating_new_version_2(self, page):
        clip_new_version_2 = fitz.Rect(75, 200, 120, 235)
        text_new_version_2 = page.get_text(clip=clip_new_version_2, sort=True).strip()
        return text_new_version_2  

    def get_tp(self, page, version):
        tp_1, tp_2 = 'NULL', 'NULL'
        if version == 'old':
            tp_1 = self.get_tp_old_version_1(page)
            tp_2 = self.get_tp_old_version_2(page)
        elif version == 'new':
            tp_1 = self.get_tp_new_version_1(page)
            tp_2 = self.get_tp_new_version_2(page)
        return tp_1, tp_2
    
    def get_tp_old_version_1(self, page):
        clip_old_version_1 = fitz.Rect(130, 100, 200, 160)
        text_old_version_1 = page.get_text(clip=clip_old_version_1, sort=True).strip()
        try:
            text_old_version_1 = text_old_version_1.split('NT$')[1].strip()
            return text_old_version_1.split('\n')[0].strip()
        except:
            return 'NULL'
    
    def get_tp_old_version_2(self, page):
        clip_old_version_2 = fitz.Rect(130, 140, 200, 160)
        text_old_version_2 = page.get_text(clip=clip_old_version_2).strip()
        try:
            text_old_version_2 = text_old_version_2.split('NT$')[1].strip()
            return text_old_version_2.split('\n')[0].strip()
        except:
            return 'NULL'
    
    def get_tp_new_version_1(self, page):
        clip_new_version_1 = fitz.Rect(115, 0, 200, 300)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            text_new_version_1 = text_new_version_1.split('NT$')[1].strip()
            return text_new_version_1.split('\n')[0].strip()
        except:
            return 'NULL'
    
    def get_tp_new_version_2(self, page):
        clip_new_version_2 = fitz.Rect(115, 235, 200, 270)
        text_new_version_2 = page.get_text(clip=clip_new_version_2, sort=True).strip()
        try:
            text_new_version_2 = text_new_version_2.split('NT$')[1].strip()
            return text_new_version_2.split('\n')[0].strip()
        except:
            return 'NULL'

    def get_author(self, page, version):
        author_1, author_2 = 'NULL', 'NULL'
        if version == 'old':
            author_1 = self.get_author_old_version_1(page)
            author_2 = self.get_author_old_version_2(page)
        elif version == 'new':
            author_1 = self.get_author_new_version_1(page)
            author_2 = self.get_author_new_version_2(page)
        return author_1, author_2
    
    def get_author_old_version_1(self, page):
        clip_old_version_1 = fitz.Rect(0, 700, 200, page.rect.height)
        text_old_version_1 = page.get_text(clip=clip_old_version_1, sort=True).strip()
        try:
            text_old_version_1 = text_old_version_1.split('詳見最後頁聲明')[0].strip()
            return text_old_version_1.split(' ')[0].strip()
        except:
            return 'NULL'
    
    def get_author_old_version_2(self, page):
        clip_old_version_2 = fitz.Rect(0, 700, 200, 780)
        text_old_version_2 = page.get_text(clip=clip_old_version_2).strip()
        try:
            return text_old_version_2.split(' ')[0].strip()
        except:
            return 'NULL'

    def get_author_new_version_1(self, page):
        clip_new_version_1 = fitz.Rect(0, 700, 200, page.rect.height)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            text_new_version_1 = text_new_version_1.split('永豐證券投資顧問股份有限公司')[0].strip()
            return text_new_version_1.split(' ')[0].strip()
        except:
            return None
    
    def get_author_new_version_2(self, page):
        clip_new_version_2 = fitz.Rect(0, 700, 200, 780)
        text_new_version_2 = page.get_text(clip=clip_new_version_2).strip()
        try:
            return text_new_version_2.split(' ')[0].strip()
        except:
            return None

    def get_summary(self, page, version):
        summary_1, summary_2 = 'NULL', 'NULL'
        if version == 'old':
            summary_1 = self.get_summary_old_version_1(page)
            summary_2 = self.get_summary_old_version_2(page)
        elif version == 'new':
            summary_1 = self.get_summary_new_version_1(page)
            summary_2 = self.get_summary_new_version_2(page)
        return summary_1, summary_2
    
    def get_summary_old_version_1(self, page):
        clip_old_version_1 = fitz.Rect(0, 0, page.rect.width, 170)
        text_old_version_1 = page.get_text(clip=clip_old_version_1, sort=True).strip()
        try:
            text_old_version_1 = text_old_version_1.split('目標價')[1].strip()
            return text_old_version_1.split('\n')[0].strip()
        except:
            return 'NULL'

    def get_summary_old_version_2(self, page):
        clip_old_version_2 = fitz.Rect(220, 125, 550, 155)
        text_old_version_2 = page.get_text(clip=clip_old_version_2).strip()
        try:
            return text_old_version_2.split('\n')[0].strip()
        except:
            return 'NULL'

    def get_summary_new_version_1(self, page):
        clip_new_version_1 = fitz.Rect(200, 170, page.rect.width, 250)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            text_new_version_1 = text_new_version_1.split(')')[1].strip()
            return text_new_version_1.split('\n')[0].strip()
        except:
            return None

    def get_summary_new_version_2(self, page):
        clip_new_version_2 = fitz.Rect(200, 200, 560, 250)
        text_new_version_2 = page.get_text(clip=clip_new_version_2).strip()
        try:
            return text_new_version_2.split('\n')[0].strip()
        except:
            return None
