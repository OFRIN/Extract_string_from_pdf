import queue
import pdfplumber

from utility import *

class Helper:
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKNMLOPQRSTUVWXYZ'
        self.alphabet_lower = self.alphabet.lower()

        self.numbers = '0123456789'
        self.special_character = '~!@#$%^&*()_+ '

    def check_korean_sentence(self, sentence):
        en_count, ko_count = 0, 0
        for character in sentence:
            if character in self.alphabet or character in self.alphabet_lower \
                or character in self.numbers or character in self.special_character:
                en_count += 1
            else:
                ko_count += 1

        if en_count > ko_count:
            return False

        return True

    def extract(self, pdf_path):
        #########################################################################################
        # Load pdf file
        #########################################################################################
        reader = pdfplumber.open(pdf_path)

        pages = reader.pages
        
        if check_page(pages[0], 'Manager Chae'):
            del pages[0]

        print('# PDF path is {}.'.format(pdf_path))
        print('# The number of page is {}.'.format(len(pages)))
        
        script_queue = queue.Queue()
        pattern_queue = queue.Queue()

        for page in pages:
            result = check_page(page, '#pattern')
            if result is None:
                continue
            
            if result:
                pattern_queue.put(page)
            else:
                script_queue.put(page)
        
        print('# The number of script is {}.'.format(script_queue.qsize()))
        print('# The number of pattern is {}.'.format(pattern_queue.qsize()))

        #########################################################################################
        # Extract patterns from loaded pdf file
        #########################################################################################
        dataset_from_patterns = []

        for _ in range(pattern_queue.qsize() // 2):
            page1 = pattern_queue.get()
            page2 = pattern_queue.get()

            selected_indices = []
            dataset_written_in_korean = pattern_parsing_using_indices(page1.extract_text(), selected_indices)
            dataset_written_in_english = pattern_parsing_using_indices(page2.extract_text(), selected_indices)

            assert len(dataset_written_in_english) == len(dataset_written_in_korean), "[!] Length of korean pattern is different from length of english pattern."

            for eng, kor in zip(dataset_written_in_english, dataset_written_in_korean):
                dataset_from_patterns.append(tuple([eng, kor]))
        
        #########################################################################################
        # Extract patterns from loaded pdf file
        #########################################################################################
        dataset_from_scripts = []
        dataset_written_in_korean = None

        while not script_queue.empty():
            page = script_queue.get()

            dataset = script_parsing(page.extract_text())
            if len(dataset) < 2:
                continue

            ko_count = 0
            for data in dataset:
                if self.check_korean_sentence(data):
                    ko_count += 1
            
            if ko_count > 0:
                dataset_written_in_korean = dataset
            elif ko_count == 0 and dataset_written_in_korean is not None:
                dataset_written_in_english = dataset

                if len(dataset_written_in_korean) == len(dataset_written_in_english):
                    for eng, kor in zip(dataset_written_in_english, dataset_written_in_korean):
                        eng = remove_frontal_space(eng[4:])
                        kor = remove_frontal_space(kor[4:])
                        
                        if eng != kor:
                            dataset_from_scripts.append(tuple([eng, kor]))
                        else:
                            # TODO: papago
                            # kor = papago.translate(eng)
                            pass
                    
                    dataset_written_in_korean = None
                else:
                    dataset_written_in_korean = dataset_written_in_english
        
        print()
        return tuple(dataset_from_patterns), tuple(dataset_from_scripts)

if __name__ == '__main__':
    import glob
    
    helper = Helper()
    
    # helper.extract('./pdf/200518_conversatin_1_sanghyun_test.pdf')
    # helper.extract('./pdf/200613_conversation_1_sanghyun.pdf')
    # helper.extract('./pdf/200616_conversatin_1_sanghyun.pdf')
    # helper.extract('./pdf/200511_conversation_office_design_share.pdf')
    # helper.extract('./pdf/200331_conversatin_1_sanghyun_article_training.pdf')
    helper.extract('./dataset/yoo/20608_conversation_1_yoo.pdf')

