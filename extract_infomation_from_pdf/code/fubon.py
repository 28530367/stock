from tqdm import tqdm
import fitz
from extractPdf import *


class Fubon(ExtractPdf):
    '''Handle 富邦(Fubon) pdf

        Args :
            directory_path : (str) pdf path
        
        Return :
            rating : (str) recommend
    '''
    def __init__(self, file_path):
        super().__init__(file_path)
        self.possible_rating = ['增加持股', '未評等', '中立', '買進', '降低持股', 'Buy', 'Neutral']

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
        page_check_source = doc.load_page(0)
        text_check_source = page_check_source.get_text()
        if self.check_source(text_check_source):
            advisor = self.__class__.__name__
        return advisor, version

    def check_source(self, text_check_source):
        check_source = ['富邦投顧']
        return True if any(keyword in text_check_source for keyword in check_source) else False

    def check_version(self, text_check_version):
        pass

    def get_rating(self, page, version):
        rating_1, rating_2 = 'NULL', 'NULL'
        rating_1 = self.get_rating_version_1(page)
        rating_2 = self.get_rating_version_2(page)
        return rating_1, rating_2
    
    def get_rating_version_1(self, page):
        clip_version_1 = fitz.Rect(50, 120, 200, 200)
        text_version_1 = page.get_text(clip=clip_version_1, sort=True).strip()
        if text_version_1.split('\n')[0].strip() == '_':
            return text_version_1.split('\n')[1].strip()
        else :
            return text_version_1.split('\n')[0].strip()

    def get_rating_version_2(self, page):
        clip_version_2 = fitz.Rect(50, 140, 210, 165)
        return page.get_text(clip=clip_version_2, sort=True).strip()
        
    # target_price
    def get_tp(self, page, version):
        tp_1, tp_2 = 'NULL', 'NULL'
        tp_1 = self.get_tp_version_1(page)
        tp_2 = self.get_tp_version_2(page)
        return tp_1, tp_2
    
    def get_tp_version_1(self, page):
        clip_version_1 = fitz.Rect(50, 120, 205, 220)
        text_version_1 = page.get_text(clip=clip_version_1, sort=True).strip()
        try:
            text_version_1 = text_version_1.split('$')[2].strip()
            return text_version_1.split('\n')[0].strip()
        except:
            return 'NULL'

    def get_tp_version_2(self, page):
        clip_version_2 = fitz.Rect(140, 150, 205, 177)
        text_version_2 = page.get_text(clip=clip_version_2).strip()
        try:
            return text_version_2.split('$')[1].strip()
        except:
            return 'NULL'

    # author
    def get_author(self, page, version):
        author_1, author_2 = 'NULL', 'NULL'
        author_1 = self.get_author_version_1(page)
        author_2 = self.get_author_version_2(page)
        return author_1, author_2
    
    def get_author_version_1(self, page):
        clip_version_1 = fitz.Rect(0, 760, 200, page.rect.height)
        text_version_1 = page.get_text(clip=clip_version_1, sort=True).strip()
        try:
            text_version_1 = text_version_1.split('-')[0].strip()
            return text_version_1.split('\n')[0].strip()
        except:
            return 'NULL'
    
    def get_author_version_2(self, page):
        clip_version_2 = fitz.Rect(30, 765, 100, 777)
        text_version_2 = page.get_text(clip=clip_version_2).strip()
        return text_version_2.split('\n')[0].strip()

    # summary
    def get_summary(self, page, version):
        summary_1, summary_2 = 'NULL', 'NULL'
        summary_1 = self.get_summary_version_1(page)
        summary_2 = self.get_summary_version_2(page)
        return summary_1, summary_2
    
    def get_summary_version_1(self, page):
        clip_version_1 = fitz.Rect(220, 60, page.rect.width, 140)
        text_version_1 = page.get_text(clip=clip_version_1, sort=True).strip()
        try:
            text_version_1 = text_version_1.split(')')[1].strip()
            return text_version_1.split('\n')[0].strip()
        except:
            return 'NULL'

    def get_summary_version_2(self, page):
        clip_version_2 = fitz.Rect(220, 105, page.rect.width, 140)
        text_version_2 = page.get_text(clip=clip_version_2).strip()
        return text_version_2.split('\n')[0].strip()