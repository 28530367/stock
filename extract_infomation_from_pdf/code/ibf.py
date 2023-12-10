from tqdm import tqdm
import fitz
from extractPdf import *


class Ibf(ExtractPdf):
    '''Handle 國票(Ibf) pdf

        Args :
            directory_path : (str) pdf path
        
        Return :
            rating : (str) recommend
    '''
    def __init__(self, file_path):
        super().__init__(file_path)
        self.possible_rating = ['買進', '區間操作', '強力買進']

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
            clip_check_version = fitz.Rect(40, 0, page.rect.width, 400)
            text_check_version = page.get_text(
                clip=clip_check_version, sort=True).strip()
            version = self.check_version(text_check_version)
        return advisor, version

    def check_source(self, text_check_source):
        check_source = ['國票投顧所有']
        return True if any(keyword in text_check_source for keyword in check_source) else False

    def check_version(self, text_check_version):
        check_report = ['國票觀點']
        if any(keyword in text_check_version for keyword in check_report):
            return 'old'
        else:
            return 'new'
               
    def get_rating(self, page, version):
        rating_1, rating_2 = 'NULL', 'NULL'
        if version == 'old':
            rating_1 = self.get_rating_old_version_1(page)
            rating_2 = self.get_rating_old_version_2(page)
        else:
            rating_1 = self.get_rating_new_version_1(page)
            rating_2 = self.get_rating_new_version_2(page)
        return rating_1, rating_2
    
    def get_rating_old_version_1(self, page):
        clip_old_version_1 = fitz.Rect(380, 0, page.rect.width, 400)
        text_old_version_1 = page.get_text(clip=clip_old_version_1, sort=True).strip()
        try:
            if '目標價' in text_old_version_1:
                text_old_version_1 = text_old_version_1.split('目標價')[1].strip()
                return text_old_version_1.split('\n')[0].strip()
            elif '區間價位' in text_old_version_1:
                text_old_version_1 = text_old_version_1.split('區間價位')[1].strip()
                return text_old_version_1.split('\n')[0].strip()
            elif '操作區間' in text_old_version_1:
                text_old_version_1 = text_old_version_1.split('操作區間')[1].strip()
                return text_old_version_1.split('\n')[0].strip()
            elif '/買進' in text_old_version_1:
                text_old_version_1 = text_old_version_1.split('/買進')[1].strip()
                return text_old_version_1.split('\n')[0].strip()
        except:
            return 'NULL'

    def get_rating_old_version_2(self, page):
        clip_old_version_2 = fitz.Rect(380, 200, 470, 270)
        text_old_version_2 = page.get_text(clip=clip_old_version_2, sort=True).strip()
        if '買進' in text_old_version_2:
            return '買進'
        elif '區間操作' in text_old_version_2:
            return '區間操作'
        elif '賣出' in text_old_version_2:
            return '賣出'
    
    def get_rating_new_version_1(self, page):
        clip_new_version_1 = fitz.Rect(30, 200, 220, 400)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            if '目標價' in text_new_version_1:
                text_new_version_1 = text_new_version_1.split('目標價')[1].strip()
                rating_1 = text_new_version_1.split('\n')[0].strip()  
            elif '區間價位' in text_new_version_1:
                text_new_version_1 = text_new_version_1.split('區間價位')[1].strip()
                rating_1 = text_new_version_1.split('\n')[0].strip()
            elif '操作區間' in text_new_version_1:
                text_new_version_1 = text_new_version_1.split('操作區間')[1].strip()
                rating_1 = text_new_version_1.split('\n')[0].strip()
            else:
                rating_1 = 'NULL'
            self.rating_1 = rating_1
            return rating_1  
        except:
            return 'NULL'
        
    def get_rating_new_version_2(self, page):
        clip_new_version_2 = fitz.Rect(40, 200, 120, 400)
        text_new_version_2 = page.get_text(clip=clip_new_version_2, sort=True).strip()
        if '強力買進' in text_new_version_2:
            return '強力買進'
        elif '買進' in text_new_version_2:
            return '買進'
        elif '區間操作' in text_new_version_2:
            return '區間操作'
        elif '賣出' in text_new_version_2:
            return '賣出'
        
    # target_price
    def get_tp(self, page, version):
        tp_1, tp_2 = 'NULL', 'NULL'
        if version == 'report':
            tp_1 = self.get_tp_old_version_1(page)
            tp_2 = self.get_tp_old_version_2(page)
        elif version == 'new':
            tp_1 = self.get_tp_new_version_1(page)
            tp_2 = self.get_tp_new_version_2(page)
        return tp_1, tp_2
    
    def get_tp_old_version_1(self, page):
        clip_old_version_1 = fitz.Rect(380, 0, page.rect.width, 400)
        text_old_version_1 = page.get_text(clip=clip_old_version_1).strip()
        try:
            if '目標價' in text_old_version_1:
                text_old_version_1 = text_old_version_1.split('目標價')[1].strip()
                return text_old_version_1.split('\n')[1].strip()
            elif '區間價位' in text_old_version_1:
                text_old_version_1 = text_old_version_1.split('區間價位')[1].strip()
                return text_old_version_1.split('\n')[1].strip()
            elif '操作區間' in text_old_version_1:
                text_old_version_1 = text_old_version_1.split('操作區間')[1].strip()
                return text_old_version_1.split('\n')[1].strip()
            elif '/買進' in text_old_version_1:
                text_old_version_1 = text_old_version_1.split('/買進')[1].strip()
                return text_old_version_1.split('\n')[1].strip()
            else:
                return 'NULL'
        except:
            return 'NULL'
    
    def get_tp_old_version_2(self, page):
        clip_old_version_2 = fitz.Rect(470, 245, 560, 265)
        return page.get_text(clip=clip_old_version_2).strip()
    
    def get_tp_new_version_1(self, page):
        clip_new_version_1 = fitz.Rect(30, 200, 200, 400)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            if '目標價' in text_new_version_1:
                text_new_version_1 = text_new_version_1.split('目標價')[1].strip()
                return text_new_version_1.split('\n')[1].strip()  
            elif '區間價位' in text_new_version_1:
                text_new_version_1 = text_new_version_1.split('區間價位')[1].strip()
                return text_new_version_1.split('\n')[1].strip()  
            elif '操作區間' in text_new_version_1:
                text_new_version_1 = text_new_version_1.split('操作區間')[1].strip()
                return text_new_version_1.split('\n')[1].strip()  
            else:
                return 'NULL'
        except:
            return 'NULL'
    
    def get_tp_new_version_2(self, page):
        clip_new_version_2 = fitz.Rect(30, 200, 200, 400)
        text_new_version_2 = page.get_text(clip=clip_new_version_2, sort=True).strip() 
        try:
            text_new_version_2 = text_new_version_2.split(self.rating_1)[1].strip()
            return text_new_version_2.split('\n')[0].strip()
        except:
            return 'NULL'

    # author
    def get_author(self, page, version):
        author_1, author_2 = 'NULL', 'NULL'
        author_1 = self.get_author_version_1(page)
        author_2 = self.get_author_version_2(page)
        return author_1, author_2
    
    def get_author_version_1(self, page):
        clip_new_version_1 = fitz.Rect(400, 0, page.rect.width, 80)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            text_new_version_1 = text_new_version_1.split('\n')[1].strip()
            return text_new_version_1.split(' ')[0].strip()  
        except:
            return 'NULL'
    
    def get_author_version_2(self, page):
        clip_new_version_2 = fitz.Rect(400, 60, page.rect.width, 80)
        text_new_version_2 = page.get_text(clip=clip_new_version_2, sort=True).strip() 
        return text_new_version_2.split(' ')[0].strip()

    # summary
    def get_summary(self, page, version):
        summary_1, summary_2 = 'NULL', 'NULL'
        summary_1 = self.get_summary_version_1(page)
        summary_2 = self.get_summary_version_2(page)
        return summary_1, summary_2
    
    def get_summary_version_1(self, page):
        clip_new_version_1 = fitz.Rect(0, 80, page.rect.width, 190)
        text_new_version_1 = page.get_text(clip=clip_new_version_1, sort=True).strip()
        try:
            return text_new_version_1.split('\n')[-1].strip()  
        except:
            return 'NULL'

    def get_summary_version_2(self, page):
        clip_new_version_2 = fitz.Rect(0, 125, page.rect.width, 190)
        return page.get_text(clip=clip_new_version_2, sort=True).strip() 