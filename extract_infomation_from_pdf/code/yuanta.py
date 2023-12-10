from tqdm import tqdm
import fitz
from extractPdf import *


class Yuanta(ExtractPdf):
    '''Handle 元大(Yuanta) pdf

        Args :
            directory_path : (str) pdf path
        
        Return :
            rating : (str) recommend

        Todo :
            fix get tp and author 
    '''
    def __init__(self, file_path):
        super().__init__(file_path)
        self.file_path = file_path
        self.possible_rating = ['持有-超越同業 (維持評等)', '買進 (維持評等)', '持有-落後同業', '持有-落後同業 (維持評等)', 
                 '買進 (調升評等)', '買進 (重新納入研究範圍)',
                 '持有-超越同業 (調降評等)', '買進 (研究員異動)', '買進  (初次報告)', 
                 '買進 (初次報告)', '持有-超越同業', '持有-落後同業(維持評等)', '賣出 (維持評等)', 
                 '持有-超越大盤(維持評等)', '持有-超越大盤 (維持評等)', '買進', '持有-落後大盤']

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
        return advisor, version, stock, date, rating_1, rating_2, rating,\
            tp_1, tp_2, tp, author_1, author_2, author, \
                summary_1, summary_2, summary
        # return advisor, version, stock, date, rating, tp, author, summary
        
    def get_advisor_and_version(self, doc, page):
        advisor, version = 'NULL', 'NULL'
        page_check_source = doc.load_page(-1)
        text_check_source = page_check_source.get_text()
        if self.check_source(text_check_source):
            advisor = self.__class__.__name__
            page_check_report = doc.load_page(0)
            clip_check_report = fitz.Rect(0, 0, page.rect.width, 70)
            text_check_report = page_check_report.get_text(clip=clip_check_report).strip()
            version = self.check_version(text_check_report)
        return advisor, version
        
    def check_source(self, text_check_source):
        check_source = ['元大證券投資顧問']
        return True if any(keyword in text_check_source for keyword in check_source) else False
     
    def check_version(self, text_check_version):
        check_version = ['更新報告', '初次報告']
        if any(keyword in text_check_version for keyword in check_version):
            return 'report'
        else:
            return 'NULL'
        
    # rating
    def get_rating(self, page, version):
        rating_1, rating_2 = 'NULL', 'NULL'
        if version == 'report':
            rating_1 = self.get_rating_report_version_1(page)
            rating_2 = self.get_rating_report_version_2(page)
        return rating_1, rating_2
    
    def get_rating_report_version_1(self, page):
        clip_version_1 = fitz.Rect(0, 0, 210, 230)
        text_version_1 = page.get_text(clip=clip_version_1, sort=True).strip()
        text_version_1 = text_version_1.split('目標價')[0].strip()
        return text_version_1.split('\n')[-1].strip()

    def get_rating_report_version_2(self, page):
        clip_version_2 = fitz.Rect(0, 115, 210, 145)
        text_new_version_1 = page.get_text(clip=clip_version_2).strip()
        return text_new_version_1.split('\n')[0].strip()
    
    # target_price
    def get_tp(self, page, version):
        tp_1, tp_2 = 'NULL', 'NULL'
        if version == 'report':
            tp_1 = self.get_tp_report_version_1(page)
            tp_2 = self.get_tp_report_version_2(page)
        # elif version == 'news':
        #     tp_1 = self.get_tp_news_version_1(page)
        #     tp_2 = self.get_tp_news_version_2(page)
        return tp_1, tp_2
    
    def get_tp_report_version_1(self, page):
        clip_version_1 = fitz.Rect(400, 0, page.rect.width, 200)
        text_version_1 = page.get_text(clip=clip_version_1, sort=True).strip()
        try:
            text_version_1 = text_version_1.split('$')[1].strip()
            return text_version_1.split('\n')[0].strip()
        except:
            return 'NULL'
        
    def get_tp_report_version_2(self, page):
        clip_version_2 = fitz.Rect(30, 135, 120, 170)
        text_version_2 = page.get_text(clip=clip_version_2).strip()
        try:
            text_version_2 = text_version_2.split('NT$')[1].strip()
            return text_version_2.split('\n')[0].strip()
        except:
            return 'NULL'
        
    # author   
    def get_author(self, page, version):
        author_1, author_2 = 'NULL', 'NULL'
        if version == 'report':
            author_1 = self.get_author_report_version_1(page)
            author_2 = self.get_author_report_version_2(page)
        # elif version == 'news':
        #     author_1 = self.get_author_news_version_1(page)
            # author_2 = self.get_author_news_version_2(page)
        return author_1, author_2

    def get_author_report_version_1(self, page):
        clip_version_1 = fitz.Rect(0, 725, 220, page.rect.height)
        text_version_1 = page.get_text(clip=clip_version_1, sort=True).strip()
        try:
            text_version_1 = text_version_1.split('@')[0].strip()
            return text_version_1.split('\n')[0].strip()
        except:
            return 'NULL'
        
    def get_author_report_version_2(self, page):
        clip_version_2 = fitz.Rect(30, 725, 220, 740)
        text_version_2 = page.get_text(clip=clip_version_2).strip()
        return text_version_2.split('\n')[0].strip()
        
    # summary   
    def get_summary(self, page, version):
        summary_1, summary_2 = 'NULL', 'NULL'
        if version == 'report':
            summary_1 = self.get_summary_report_version_1(page)
        #     summary_2 = self.get_summary_report_version_2(page)
        # elif version == 'news':
        #     summary_1 = self.get_summary_news_version_1(page)
        return summary_1, summary_2
    
    def get_summary_report_version_1(self, page):
        clip_version_1 = fitz.Rect(225, 65, page.rect.width, 200)
        text_version_1 = page.get_text(clip=clip_version_1, sort=True).strip()
        try:
            return text_version_1.split('►')[0].strip()
        except:
            return 'NULL'