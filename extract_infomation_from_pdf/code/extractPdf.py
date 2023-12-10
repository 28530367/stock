import fitz

class ExtractPdf(object):
    '''Extracts pdf's informations'''
    def __init__(self, file_path:str):
        '''
        Args :
            file_path : (str) target file's full path
        '''
        self.file_path = file_path

    def open(self):
        doc = fitz.open(self.file_path)
        page = doc.load_page(0)
        return doc, page
    
    def close(self, doc):
        return doc.close()
    
    def check_rating(self, rating_1, rating_2, possible_rating):
        '''Check that the extracted ratings are correct

            Return :
                rating : (str) recommend rating
        '''
        if rating_1 == rating_2:
            return rating_1
        for rating in possible_rating:
            if rating == rating_1:
                return rating
            elif rating == rating_2:
                return rating
        return 'NULL'
    
    def check_targrt_price(self, tp_1, tp_2):
        '''Check that the extracted target_price are correct

            Return :
                tp : (str) recommend target price
        '''
        tp = 'NULL'
        if tp_1 == tp_2:
            tp = tp_1
        elif tp_1 != 'NULL' and tp_2 == 'NULL':
            tp = tp_1
        elif tp_2 != 'NULL' and tp_1 == 'NULL':
            tp = tp_2
        else:
            tp = 'NULL'
        try: 
            tp = float(tp)
            return tp
        except:
            return 'NULL'

    def check_author(self, author_1, author_2):
        '''Check that the extracted target_price are correct

            Return :
                tp : (str) recommend target price
        '''
        if author_1 == author_2:
            return author_1
        elif author_1 != 'NULL' and author_2 == 'NULL':
            return author_1
        elif author_2 != 'NULL' and author_1 == 'NULL':
            return author_2
        else:
            return 'NULL'

    def check_summary(self, summary_1, summary_2):
        '''Check that the extracted target_price are correct

            Return :
                tp : (str) recommend target price
        '''
        summary = 'NULL'
        if summary_1 == summary_2:
            summary = summary_1
        elif summary_1 != 'NULL' and summary_2 == 'NULL':
            summary = summary_1
        elif summary_2 != 'NULL' and summary_1 == 'NULL':
            summary = summary_2
        else:
            summary = 'NULL'
        if len(summary)>20: # pdf命名長度限制取決於作業系統及MYSQL 一般為255
            return summary[:20]
        else:
            return summary


