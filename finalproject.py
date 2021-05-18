#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 13:40:56 2019

@author: saisreya
"""
import math

def clean_text(txt):
        """returns a list containing the words in txt after it has been cleaned"""
        s = ''
        txt = txt.lower()
        for c in txt:
            if c in '.,!&?/][-_;:()/':
                s = s
            else:
                s = s + c
        s_list = []
        s_list = s.split(' ')
        return s_list

def stem(s):
    """return the stem of s"""
    if len(s) != 0:
        if s[-1] == 's':
            if len(s) < 4:
                s = s
            elif s[-2] == s[-1]:
                s = s
            else:
                s = stem(s[:-1])    
        elif s[-3:]== 'ing':
            if len(s) < 6:
                s = s
            elif s[-4] == s[-5]:
                s = s[:-4]
            else:
                s = s[:-3]         
        elif s[-2:] == 'er':
            if len(s) < 7:
                s = s
            elif s[-3] == s[-4]:
                s = s[:-3]
            elif s[-3:] == 'ier':
                s = s[:-3] + 'y'
            else:
                s = s[:-2]
        elif s[-3:] == 'ies':
            if len(s) < 6:
                s = s
            else:
                s = s[:-3] + 'y'
        elif s[-2:] == 'ed':
            if len(s) < 5:
                s = s
            else:
                s = s[:-2]        
        elif s[-4:] == 'ment':
            if len(s) < 9:
                s = s
            else:
                s = s[:-4]       
        elif s[-4:] == 'ness':
            if len(s) < 9:
                s = s
            else:
                s = s[:-4]
        elif s[-3:] == 'ful':
            if len(s) < 8:
                s = s
            else:
                s = s[:-3]       
        elif s[-3:] == 'ion':
            if len(s) < 8:
                s = s
            else:
                s = s[:-3] + 'e'
        else:
            s = s
    return s
         

class TextModel:
    """serves as a blueprint for objects that model a body of text"""
    
    def __init__(self, model_name):
        """constructs a new TextModel object"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.long_word_freq = {}
        
    def  __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of long words:  ' + str(len(self.long_word_freq)) + '\n'
        return s
        
    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
        to all of the dictionaries in this text model.
        """
        sc = s
        sc.replace('?','.').replace('!','.')
        sc = sc.split(".")
        if s[-1] == '.':
            sc = sc[:-1]
        for c in sc:
            length = len(c.split(' '))
            if length in self.sentence_lengths:
                self.sentence_lengths[length] += 1
            else:
                self.sentence_lengths[length] = 1
                
        s = clean_text(s)
        word_list = s
        
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
                
        for w in word_list:
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] = 1
                
        for w in word_list:
            if len(w) > 7:
                if len(w) in self.long_word_freq:
                    self.long_word_freq[len(w)] += 1
                else:
                    self.long_word_freq[len(w)] = 1
                    
        for w in word_list:
            w = stem(w)
            if w in self.stems:
                self.stems[w] += 1
            else:
                self.stems[w] =1
            
                
    def add_file(self, filename):
        """adds all of the text in the file identified by filename to the model"""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        self.add_string(text)
        
    def save_model(self):
        """ saves the TextModel object self by writing its various feature dictionaries to files""" 
        f1 = open((self.name + '_' + 'words'), 'w')  
        f2 = open((self.name + '_' + 'word_lengths'), 'w')
        f3 = open((self.name + '_' + 'stems'), 'w')
        f4 = open((self.name + '_' + 'sentence_lengths'), 'w')
        f5 = open((self.name + '_' + 'long_word_freq'), 'w')
        f1.write(str(self.words))
        f2.write(str(self.word_lengths))
        f3.write(str(self.stems))
        f4.write(str(self.sentence_lengths))
        f5.write(str(self.long_word_freq))
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
        
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from their files and assigns them to the attributes of the called TextModel"""
        f1 = open((self.name + '_' + 'words'), 'r')
        f2 = open((self.name + '_' + 'word_lengths'), 'r')
        f3 = open((self.name + '_' + 'stems'), 'r')
        f4 = open((self.name + '_' + 'sentence_lengths'), 'r')
        f5 = open((self.name + '_' + 'long_word_freq'), 'r')
        f1_str = f1.read()
        f2_str = f2.read()
        f3_str = f3.read()
        f4_str = f4.read()
        f5_str = f5.read()
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
        self.words = dict(eval(f1_str))
        self.word_lengths = dict(eval(f2_str))
        self.stems = eval(f3_str)
        self.sentence_lengths = eval(f4_str)
        self.long_word_freq = eval(f5_str)
        
    def similarity_scores(self, other):
        """ returns a list of log similarity scores measuring the similarity of self and other"""
        word_score = compare_dictionaries(other.words, self.words)
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sentence_length_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        long_word_score = compare_dictionaries(other.long_word_freq, self.long_word_freq)
        return[word_score, word_length_score, stem_score, sentence_length_score, long_word_score]
        
    def  classify(self, source1, source2):
        """compares the called TextModel object (self) to two other “source” TextModel objects (source1 and source2) and 
        determines which of these other TextModels is the more likely source of the called TextModel"""
        s1 = 0
        s2 = 0
        scores1 = self.similarity_scores(source1)
        print("Scores for ", source1.name, ": ", scores1)
        scores2 = self.similarity_scores(source2)
        print("Scores for ", source2.name, ": ", scores2)
        for x in range(5):
            if scores1[x] > scores2[x]:
                s1 += 1
            else:
                s2 += 1
        if s1 > s2:
            print(self.name + " is more likely to have come from " + source1.name)
        else:
            print(self.name + " is more likely to have come from " + source2.name)
    
def compare_dictionaries(d1, d2):
    """ compute and return their log similarity score"""
    score = 0
    total = 0
    for x in d1:
        total += d1[x]
    for w in d2:
        appear = d2[w]
        if w in d1:
            prob = d1[w]/total
            score += appear * (math.log(prob/total))
        else:
            if d1 != {}:
                score += appear * (math.log(0.5/total))
    return score
        

def run_tests():
    """ your docstring goes here """
    source1 = TextModel('rowling')
    source1.add_file('rowling.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare.txt')

    new1 = TextModel('wr120')
    new1.add_file('wr120_source_text.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('rowling_philosophers_stone')
    new2.add_file('jkr_ps.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('friends_script')
    new3.add_file('friends_script.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('one_shakespeare')
    new4.add_file('one_shakespeare.txt')
    new4.classify(source1, source2)
    
    
        
        