from tqdm import tqdm
import fitz
from extractPdf import *


class Masterlink(ExtractPdf):
    '''Handle 元富(Masterlink) pdf

        Args :
            directory_path : (str) pdf path
        
        Return :
            rating : (str) recommend
    '''
    def __init__(self, file_path):
        super().__init__(file_path)
        self.possible_rating = ['維持買進', 'BUY', '評等中立', '維持中立', 'HOLD', '中立轉買進', 
                 'Upgrade to BUY', '買進轉中立', 'Downgrade to HOLD', '評等買進', 
                 'UPGRADE TO BUY', 'Upgrade To BUY', '買進轉強力買進', '維持強力買進', 
                 'STRONG BUY', 'Upgarde to BUY']

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
            clip_check_version= fitz.Rect(page.rect.width/2, 0, page.rect.width, 150)
            text_check_version = page.get_text(clip=clip_check_version, sort=True).strip()
            version = self.check_version(text_check_version)
        return advisor, version
        
    def check_source(self, text_check_source):
        check_source = ['本刊載之報告為元富投顧於特定日期之分析']
        return True if any(keyword in text_check_source for keyword in check_source) else False
     
    def check_version(self, text_check_version):
        check_report = ['公司訪談報告', 'Company Report', '評等調升報告', '個股報告', '公司拜訪報告']
        if any(keyword in text_check_version for keyword in check_report):
            return 'report' 
        elif '公司拜訪快報' in text_check_version :
            return 'news' 
        else: 
            return 'NULL'

    # stock
    # def get_stock(self, page, version):
    #     if version == 'report':
    #         return self.get_stock_report_version(page)
    #     elif version == 'news':
    #         return self.get_stock_news_version(page)
    #     else:
    #         return 'NULL'

    # def get_stock_report_version(self, page):
    #     clip_report_version_1 = fitz.Rect(220, 85, page.rect.width, 125)
    #     text_report_version_1 = page.get_text(clip=clip_report_version_1, sort=True).strip()
    #     try:
    #         if '（' in text_report_version_1:
    #             text_report_version_1 = text_report_version_1.split('（')[1].strip()
    #         elif '(' in text_report_version_1:
    #             text_report_version_1 = text_report_version_1.split('(')[1].strip()
    #         if '）' in text_report_version_1:
    #             text_report_version_1 = text_report_version_1.split('）')[0].strip()
    #         elif ')' in text_report_version_1:
    #             text_report_version_1 = text_report_version_1.split(')')[0].strip()
    #         return text_report_version_1.split('\n')[0].strip()
    #     except:
    #         return 'NULL'
        
    # def get_stock_news_version(self, page):
    #     clip_news_version_1 = fitz.Rect(45, 70, 230, 140)
    #     try:
    #         text_news_version_1 = page.get_text(clip=clip_news_version_1, sort=True)
    #         if '（' in text_news_version_1:
    #             text_news_version_1 = text_news_version_1.split('（')[1].strip()
    #         elif '(' in text_news_version_1:
    #             text_news_version_1 = text_news_version_1.split('(')[1].strip()
    #         if '（' in text_news_version_1:
    #             text_news_version_1 = text_news_version_1.split('）')[0].strip()
    #         elif ')' in text_news_version_1:
    #             text_news_version_1 = text_news_version_1.split(')')[0].strip()
    #         return text_news_version_1.split('\n')[0].strip()
    #     except:
    #         return 'NULL'
    
    # # date
    # def get_date(self, page, version):
    #     if version == 'report':
    #         return self.get_date_report_version(page)
    #     elif version == 'news':
    #         return 'NULL'
    #     else:
    #         return 'NULL'
    
    # def get_date_report_version(self, page):
    #     clip_report_version_1 = fitz.Rect(0, 0, page.rect.width, 100)
    #     text_report_version_1 = page.get_text(clip=clip_report_version_1, sort=True).strip()
    #     try:
    #         text_report_version_1 = text_report_version_1.split('個股報告')[1].strip()
    #         Date_1 = text_report_version_1.split('\n')[0].strip()
    #         return datetime.datetime.strptime(Date_1, '%B %d, %Y').date()
    #     except:
    #         return 'NULL'

    # rating
    def get_rating(self, page, version):
        rating_1, rating_2 = 'NULL', 'NULL'
        if version == 'report':
            rating_1 = self.get_rating_report_version_1(page)
            rating_2 = self.get_rating_report_version_2(page)
        elif version == 'news':
            rating_1 = self.get_rating_news_version_1(page)
            rating_2 = self.get_rating_news_version_2(page)
        return rating_1, rating_2
    
    def get_rating_report_version_1(self, page):
        clip_report_version_1= fitz.Rect(0, 0, page.rect.width, 100)
        text_report_version_1 = page.get_text(clip=clip_report_version_1, sort=True).strip()
        try:
            text_report_version_1 = text_report_version_1.split(')')[-1].strip()
            return text_report_version_1.split('\n')[0].strip()
        except:
            return 'NULL'

    def get_rating_report_version_2(self, page):
        clip_report_version_2 = fitz.Rect(310, 60, page.rect.width, 110)
        return page.get_text(clip=clip_report_version_2, sort=True).strip()
    
    def get_rating_news_version_1(self, page):
        clip_news_version_1 = fitz.Rect(0, 0, page.rect.width, 150)
        text_news_version_1 = page.get_text(clip=clip_news_version_1, sort=True).strip()
        try:
            text_news_version_1 = text_news_version_1.split('建議：')[1].strip()
            return text_news_version_1.split('\n')[0].strip()
        except:
            return 'NULL'

    def get_rating_news_version_2(self, page):
        clip_news_version_2 = fitz.Rect(80, 105, page.rect.width, 140)
        return page.get_text(clip=clip_news_version_2).strip()

    # target_price
    def get_tp(self, page, version):
        tp_1, tp_2 = 'NULL', 'NULL'
        if version == 'report':
            tp_1 = self.get_tp_report_version_1(page)
            # tp_2 = self.get_tp_report_version_2(page)
        # elif version == 'news':
        #     tp_1 = self.get_tp_news_version_1(page)
        #     tp_2 = self.get_tp_news_version_2(page)
        return tp_1, tp_2
    
    def get_tp_report_version_1(self, page):
        clip_report_version_1 = fitz.Rect(40, 100, 220, 320)
        text_report_version_1 = page.get_text(clip=clip_report_version_1, sort=True).strip()
        try:
            text_report_version_1 = text_report_version_1.split('目標價')[1].strip()
            return text_report_version_1.split('\n')[1].strip()
        except:
            return 'NULL'
    
    # def get_tp_report_version_2(self, page):
    #     clip_report_version_2 = fitz.Rect(510, 260, 555, 270)
    #     return page.get_text(clip=clip_report_version_2).strip()
        
    # def get_tp_news_version_1(self, page):
    #     clip_news_version_1 = fitz.Rect(40, 140, 290, 180)
    #     text_news_version_1 = page.get_text(clip=clip_news_version_1, sort=True).strip()
    #     try:
    #         text_news_version_1 = text_news_version_1.split('目標價')[1].strip()
    #         return text_news_version_1.split('\n')[6].strip()
    #     except:
    #         return 'NULL'
    
    # def get_tp_news_version_2(self, page):
    #     clip_news_version_2 = fitz.Rect(210, 167, 250, 175)
    #     return page.get_text(clip=clip_news_version_2).strip()

    # author   
    def get_author(self, page, version):
        author_1, author_2 = 'NULL', 'NULL'
        if version == 'report':
            author_1 = self.get_author_report_version_1(page)
            # author_2 = self.get_author_report_version_2(page)
        # elif version == 'news':
            # author_1 = self.get_author_news_version_1(page)
            # author_2 = self.get_author_news_version_2(page)
        return author_1, author_2

    def get_author_report_version_1(self, page):
        clip_report_version_1 = fitz.Rect(40, 100, 220, 320)
        text_report_version_1 = page.get_text(clip=clip_report_version_1, sort=True).strip()
        try:
            text_report_version_1 = text_report_version_1.split('研究員')[1].strip()
            return text_report_version_1.split(' ')[0].strip()
        except:
            return 'NULL'
        
    def get_author_report_version_2(self, page):
        clip_report_version_2 = fitz.Rect(30, 70, 75, 100)
        return page.get_text(clip=clip_report_version_2).strip()
    
    # def get_author_news_version_1(self, page):
    #     clip_news_version_1 = fitz.Rect(0, 700, 260, 770)
    #     text_news_version_1 = page.get_text(clip=clip_news_version_1, sort=True).strip()
    #     try:
    #         text_news_version_1 = text_news_version_1.split('/')[1].strip()
    #         return text_news_version_1.split(' ')[0].strip()
    #     except:
    #         return 'NULL'
        
    # summary   
    def get_summary(self, page, version):
        summary_1, summary_2 = 'NULL', 'NULL'
        if version == 'report':
            summary_1 = self.get_summary_report_version_1(page)
            # summary_2 = self.get_summary_report_version_2(page)
        # elif version == 'news':
            # summary_1 = self.get_summary_news_version_1(page)
        return summary_1, summary_2
    
    def get_summary_report_version_1(self, page):
        clip_report_version_1 = fitz.Rect(220, 100, 550, 150)
        return page.get_text(clip=clip_report_version_1, sort=True).strip()
        
    # def get_summary_report_version_2(self, page):
    #     clip_report_version_2 = fitz.Rect(30, 170, 375, 195)
    #     try:
    #         return page.get_text(clip=clip_report_version_2, sort=True).strip()
    #     except:
    #         return 'NULL'
    
    # def get_summary_news_version_1(self, page):
    #     clip_news_version_1 = fitz.Rect(260, 60, page.rect.width, 125)
    #     text_news_version_1 = page.get_text(clip=clip_news_version_1, sort=True).strip()
    #     try:
    #         if '）' in text_news_version_1:
    #             return text_news_version_1.split('）')[1].strip()
    #         elif ')' in text_news_version_1:
    #             return text_news_version_1.split(')')[1].strip()
    #     except:
    #         return 'NULL'
    
    # def get_summary_news_version_2(self, page):
    #     clip_news_version_2 = fitz.Rect(265, 105, page.rect.width, 123)
    #     try:
    #         return page.get_text(clip=clip_news_version_2, sort=True).strip()
    #     except:
    #         return 'NULL'
