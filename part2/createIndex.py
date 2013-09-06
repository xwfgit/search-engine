import sys
import math
from porter_stemming import PorterStemmer
        
class index_building:

    def __init__(self, arg_collection, arg_stop_words):
        self.stop_words = self.stop_words_set(arg_stop_words)
        self.title_index = dict()
        self.parse_collection(arg_collection)
        
    #filter function
    def obtain_token(self, x):
        if x >= 'a' and x <= 'z' or x >='0' and x <= '9' or x == ' ':
            return x
        else:
            return ' '

    def del_stop_words(self, token):
        return token not in self.stop_words

    #build stop_words set
    def stop_words_set(self, arg_stop_words):
        stop_words_set = set()
        for line in arg_stop_words:
            line = line.rstrip('\n')
            stop_words_set.add(line)
        return stop_words_set

    #parse collections
    def parse_collection(self, arg_collection):
        pageID = -1
        title = ''
        text = ''
        id_page_dict = {}
    #classify tags
        for line in arg_collection:
            split = []
            if line[0] == '<':
                split = line.split('>', 1)
            if len(split) != 0:
                head = split[0][1:]
                if head == 'page':
                    text = ''
                elif head == 'id':
                    id_str = split[1].split('<')
                    id_str = id_str[0]
                    pageID = int(id_str)
                elif head == 'text':
                    if split[1][-8:-1] == '</text>':
                        text += split[1][:-8]
                    else:
                        text += split[1][:-1]
                        for line in arg_collection:
                            if line[-8:-1] == '</text>': 
                                text += (' ' + line[:-8])
                                break
                            else:
                                text += ' ' + line[:-1]
                    title_text = title + '\n' + text
                    id_page_dict[pageID] = title_text
                elif head == 'title':
                    title_list = split[1].split('<')
                    title = title_list[0]
                    self.title_index[pageID] = title
    #lower cases    
        for key, value in id_page_dict.items():
            temp = value.lower()
            value = ''
            flag = False
            for c in temp:
                if c >= 'a' and c <= 'z' or c >='0' and c <= '9':
                    value += c
                    flag = False
                else:
                    if not flag:
                        value += ' '
                        flag = True
            value = value.strip(' ')
            #filter out stop words and porter stemmer 
            p = PorterStemmer()
            value_list = value.split(' ')
            value_list = filter(lambda token: token not in self.stop_words, value_list)
            new_value = []
            for s in value_list:
                new_value.append(p.stem(s, 0, len(s) - 1))
            value = ' '.join(new_value)
            id_page_dict[key] = value
    #build inverted index
        self.doc_no = len(id_page_dict)
        self.inverted_index = self.build_inverted_index(id_page_dict)
        self.compute_tf(id_page_dict)
        
    #build inverted index
    def build_inverted_index(self, id_page_dict):
        inverted_index_dict = {}
        for key, value in id_page_dict.items():
            value_list = value.split()
            pos = 0
            for term in value_list:
                if term in inverted_index_dict:
                    page_pos_dict = inverted_index_dict[term]
                    if key in page_pos_dict:
                        pos_list = page_pos_dict[key]
                        pos_list.append(pos)
                    else:
                        pos_list = [pos]
                    page_pos_dict[key] = pos_list
                else:
                    pos_list = [pos]
                    page_pos_dict = {key : pos_list}
                inverted_index_dict[term] = page_pos_dict   
                pos += 1
        return inverted_index_dict
    
    def compute_tf(self, id_page_dict):
        self.term_pagetf_dict = dict()
        pageID_norm = dict()
        for pageID, text in id_page_dict.items():
            total = 0.0;
            term_list = text.split(' ')
            for term in term_list:
                if term in self.term_pagetf_dict:
                    page_tf_dict = self.term_pagetf_dict[term]
                else:
                    page_tf_dict = dict()
                if pageID not in page_tf_dict:
                    page_pos_dict = self.inverted_index[term]
                    pos_list = page_pos_dict[pageID]
                    tf = len(pos_list)
                    total += tf ** 2
                    page_tf_dict[pageID] = tf
                    self.term_pagetf_dict[term] = page_tf_dict
            pageID_norm[pageID] = math.sqrt(total)
        for term, page_tf_dict in self.term_pagetf_dict.items():
            idf = math.log(self.doc_no * 1.0 / len(self.inverted_index[term]), 10)
            for pageID, tf in page_tf_dict.items():
                page_tf_dict[pageID] = tf *idf / pageID_norm[pageID]
    
if __name__ == '__main__':
    arg_collection = open(sys.argv[2])
    arg_stop_words = open(sys.argv[1])
    arg_myIndex = open(sys.argv[3], 'w')
    arg_myTitle = open(sys.argv[4], 'w')
    arg_posIndex = open('postingIndex.dat', 'w')
    arg_test = open('test.dat', 'w')
    inv_tit_index = index_building(arg_collection, arg_stop_words)
    
    offset = 0
    
    for key in sorted(inv_tit_index.inverted_index.iterkeys()):
        length = 0
        arg_myIndex.write(key + ' ' + str(offset) + ' ')
        page_pos_dict = inv_tit_index.inverted_index[key]
        
        for page_id in sorted(page_pos_dict.iterkeys()):
            arg_posIndex.write(str(page_id) + ' ')
            length += len(str(page_id) + ' ')
        arg_posIndex.write('|')
        length += len('|')
        
        for page_id in sorted(page_pos_dict.iterkeys()):
            pos_list = page_pos_dict[page_id]
            pos_list_str = ' '.join(str(x) for x in pos_list) + ';'
            length += len(pos_list_str)
            arg_posIndex.write(pos_list_str)
        arg_posIndex.write('|')     
        length += len('|')
        page_tf_dict = inv_tit_index.term_pagetf_dict[key]
        for page_id in sorted(page_pos_dict.iterkeys()):
            arg_posIndex.write(str(page_tf_dict[page_id]) + ' ')
            length += len(str(page_tf_dict[page_id]) + ' ')
        
        length += len('\n')
        arg_posIndex.write('\n')
        offset += length
        arg_myIndex.write(str(length) + '\n')
        
        arg_test.write(key + ' ' + str(len(inv_tit_index.inverted_index[key])) + ' ')
        for page_id in sorted(page_pos_dict.iterkeys()):
            arg_test.write(str(inv_tit_index.doc_no) + ' ' + str(page_id) + '$' + str(page_tf_dict[page_id]) + ' ')
        arg_test.write('\n')
    for key in sorted(inv_tit_index.title_index.iterkeys()):
        arg_myTitle.write(str(key) + ' ' + inv_tit_index.title_index[key] + '\n')
