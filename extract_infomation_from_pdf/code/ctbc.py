import tqdm
import fitz
from extractPdf import *


class Ctbc(ExtractPdf):
    '''Handle 中信託(CTBC) pdf

        Args :
            directory_path : (str) pdf path
        
        Return :
            rating : (str) recommend
    '''
    def __init__(self, file_path):
        super().__init__(file_path)
        self.possible_rating = ['中立', '買進', '增加持股(Overweight)', '中立(Neutral)', 
                              '買進(Buy)', '增加持股', '-', '降低持股(Underweight)', '未評等', '增加持股(OW)', '未評等(Not Rated)', '增加持股(OＷ)']

    def get_all(self):
        doc, page = self.open()
        advisor, version = self.get_advisor_and_version(doc, page)
        # stock = self.get_stock(page, version)
        # date = self.get_date(page, version)
        stock = 'NULL'
        date = 'NULL'
        rating_1, rating_2 = self.get_rating(page, version)
        rating = self.check_rating(rating_1, rating_2, self.possible_rating)
        tp_1, tp_2 = self.get_tp(page)
        tp = self.check_targrt_price(tp_1, tp_2)
        author_1, author_2 = self.get_author(page)
        author = self.check_author(author_1, author_2)
        summary_1, summary_2 = self.get_summary(page, version)
        summary = self.check_summary(summary_1, summary_2)
        self.close(doc)
        return advisor, version, stock, date, rating_1, rating_2, rating, tp_1, tp_2, \
            tp, author_1, author_2, author, summary_1, summary_2, summary
        # return advisor, version, stock, date, rating, tp, author, summary

    def get_advisor_and_version(self, doc, page):
        advisor, version = 'NULL', 'NULL'
        page_check_source = doc.load_page(-1)
        text_check_source = page_check_source.get_text()
        if self.check_source(text_check_source):
            advisor = self.__class__.__name__
            text_check_report = text_check_source
            if self.check_report(text_check_report):
                clip_check_version= fitz.Rect(370, 80, 450, 200)
                text_check_version = page.get_text(clip=clip_check_version, sort=True).strip()
                version = self.check_version(text_check_version)
        return advisor, version
        
    def check_source(self, text_check_source):
        check_source = ['中國信託金融控股', '中信投顧投資分析報告']
        return True if any(keyword in text_check_source for keyword in check_source) else False
    
    def check_report(self, text_check_report):
        check_report = ['個股報告']
        return True if any(keyword in text_check_report for keyword in check_report) else False
    
    def check_version(self, text_check_version):
        check_version = ['投資評等', '首次評等']
        return 'old' if any(keyword in text_check_version for keyword in check_version) else 'new'

    # rating
    def get_rating(self, page, version):
        rating_1, rating_2 = 'NULL', 'NULL'
        if version == 'old':
            rating_1 = self.get_rating_old_version_1(page)
            rating_2 = self.get_rating_old_version_2(page)
        elif version == 'new':
            rating_1 = self.get_rating_new_version_1(page)
            rating_2 = self.get_rating_new_version_2(page)
        return rating_1, rating_2
    
    def get_rating_new_version_1(self, page):
        clip_new_version_1 = fitz.Rect(200, 0, page.rect.width, 200)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            if '評 等' in text_new_version_1:
                text_new_version_1 = text_new_version_1.split('評 等')[1]
                return text_new_version_1.split('\n')[1].strip()
            elif '重 新 覆 蓋' in text_new_version_1:
                text_new_version_1 = text_new_version_1.split('重 新 覆 蓋')[1]
                return text_new_version_1.split('\n')[1].strip()
        except:
            return 'NULL'
        
    def get_rating_new_version_2(self, page):
        clip_new_version_2 = fitz.Rect(350, 115, 570, 200)
        text_new_version_1 = page.get_text(clip=clip_new_version_2, sort=True).strip()
        return text_new_version_1.split('\n')[0].strip()
    
    def get_rating_old_version_1(self, page):
        clip_old_version_1= fitz.Rect(370, 80, 450, 200)
        text_old_version_1 = page.get_text(clip=clip_old_version_1, sort=True).strip()
        try:
            text_old_version_1 = text_old_version_1.split('投資評等')[1].strip()
            return text_old_version_1.split('\n')[0].strip()
        except:
            return 'NULL'

    def get_rating_old_version_2(self, page):
        clip_old_version_2 = fitz.Rect(380, 125, 500, 145)
        return page.get_text(clip=clip_old_version_2, sort=True).strip()
    
    # target_price
    def get_tp(self, page):
        tp_1, tp_2 = 'NULL', 'NULL'
        tp_1 = self.get_tp_new_version_1(page)
        tp_2 = self.get_tp_new_version_2(page)
        return tp_1, tp_2
    
    def get_tp_new_version_1(self, page):
        clip_new_version_1 = fitz.Rect(0, 100, 200, 200)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            text_new_version_1 = text_new_version_1.split('目 標 價')[1].strip()
            return text_new_version_1.split('元')[0].strip()
        except:
            return 'NULL'
    
    def get_tp_new_version_2(self, page):
        clip_new_version_2 = fitz.Rect(0, 165, 200, 175)
        text_new_version_2 = page.get_text(clip=clip_new_version_2).strip()
        try:
            text_new_version_2 = text_new_version_2.split('目 標 價')[1].strip()
            return text_new_version_2.split('元')[0].strip()
        except:
            return 'NULL'

    # author   
    def get_author(self, page):
        author_1, author_2 = 'NULL', 'NULL'
        author_1 = self.get_author_old_version_1(page)
        author_2 = self.get_author_old_version_2(page)
        return author_1, author_2

    def get_author_old_version_1(self, page):
        clip_old_version_1 = fitz.Rect(0, 555, 200, 620)
        text_old_version_1 = page.get_text(clip=clip_old_version_1, sort=True).strip()
        try:
            text_old_version_1 = text_old_version_1.split('@')[0].strip()
            text_old_version_1 = text_old_version_1.split('\n')[0].strip()
            return text_old_version_1.split('(')[0].strip()
        except:
            return 'NULL'
    
    def get_author_old_version_2(self, page):
        clip_old_version_2 = fitz.Rect(0, 0, 200, page.rect.height)
        text_old_version_2 = page.get_text(clip=clip_old_version_2).strip()
        try:
            text_old_version_2 = text_old_version_2.split('個股與大盤走勢')[1].strip()
            text_old_version_2 = text_old_version_2.split('@')[0].strip()
            text_old_version_2 = text_old_version_2.split('\n')[-2].strip()
            return text_old_version_2.split('(')[0].strip()
        except:
            return 'NULL'
        
    # summary   
    def get_summary(self, page, version):
        summary_1 = 'NULL'
        if version == 'old':
            summary_1 = self.get_summary_old_version_1(page)
        elif version == 'new':
            summary_1 = self.get_summary_new_version_1(page)
        return summary_1, 'NULL'
    
    def get_summary_old_version_1(self, page):
        clip_old_version_1 = fitz.Rect(210, 145, page.rect.width, 300)
        text_old_version_1 = page.get_text(clip=clip_old_version_1, sort=True).strip()
        try:
            text_old_version_1 = text_old_version_1.split('結論與建議')[1].strip()
            text_old_version_1 = text_old_version_1.split('：')[0].strip()
            return ''.join(text_old_version_1.split('\n')[:-1]).strip()
        except:
            return 'NULL'

    def get_summary_new_version_1(self, page):
        clip_new_version_1 = fitz.Rect(210, 145, page.rect.width, 300)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            return text_new_version_1.split('\uf06c')[0].strip()
        except:
            return 'NULL'