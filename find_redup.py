from __future__ import division
import re
import csv
import os, glob
import fileinput
import Levenshtein
import nltk

from indicnlp.morph import unsupervised_morph

# loader.load()
from indicnlp.tokenize import indic_tokenize
from indicnlp.tokenize import sentence_tokenize
d=0

def prepare_input(filepath):
    words = ['?', '।', '৷' ]
    with open('input.txt', 'w') as file1:
        with open(filepath, 'r') as f:
            for line in f:
                for t in sentence_tokenize.sentence_split(line, 'hi'):
                    # if word in t:
                    # for word in words:
                    #   if word in t:
                    file1.write("%s\n" % t)
        f.close()
    file1.close()


def generate_gram(word_list, n):
    token = [token for token in word_list.split(" ") if token != ""]
    ngrams = zip(*[token[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


# return grams


def get_bigram_echo(word_token):
    word_token=word_token.strip()
    if (len(word_token) < 4 or ' ' not in word_token):
        return 'NA'
    org_word = word_token
    word_token = word_token.split()
    print("-----------------------------------------%s----------------------------------%s" % (word_token,org_word))
    if(len(word_token[0])>0 and len(word_token[1]) > 0 ):
	    if (word_token[0] == word_token[1]):  ## Rule ONO-R1
        	print("%s---" % org_word)
        	return 1
    #Return 1 means Full duplication
    return 'NA'


def prepare_sentence(sent):
    # word_token=word_token.replace('"',"") # eliminate " from the word

    # if word_token.endswith(',') or word_token.startswith(','):
    #   word_token = word_token.replace(',', "")
    # if word_token.endswith(':') or word_token.startswith(':'):
    #   word_token = word_token.replace(':', "")
    # if word_token.endswith('।') or  word_token.startswith('।'):
    #   word_token = word_token.replace('।', "")
    # if word_token.endswith('।') or word_token.startswith('।'):
    #       word_token = word_token.replace('।', "")

    # if word_token.endswith('.') or word_token.startswith('.'):
    #   word_token = word_token.replace('.', "")
    # if word_token.endswith('-') or word_token.startswith('-'):
    #   word_token = word_token.replace('-', "")
    # if word_token.endswith(';') or  word_token.startswith(';'):
    #   word_token = word_token.replace(';', "")
    # if word_token.endswith('?') or  word_token.startswith('?'):
    #   word_token = word_token.replace("?", "")
    line = sent
    line = line.replace('_', ' _ ')
    line = line.replace('_', ' _ ')
    line = line.replace('।', ' । ')
    line = line.replace('।', ' । ')
    line = line.replace('৷', ' ৷ ')
    line = line.replace('|', ' | ')
    line = line.replace('!', ' ! ')
    line = line.replace('?', ' ? ')
    line = line.replace('#', ' # ')
    line = line.replace('=', ' = ')
    line = line.replace(',', ' , ')
    line = line.replace(':', ' : ')
    line = line.replace('*', ' * ')
    line = line.replace(', ', ' , ')
    line = line.replace('"', ' " ')
    line = line.replace('"', ' " ')
    line = line.replace(')', ' ) ')
    line = line.replace('(', ' ( ')
    line = line.replace('{', ' { ')
    line = line.replace('}', ' } ')
    line = line.replace('[', ' [ ')
    line = line.replace(']', ' ] ')
    line = line.replace('- ', ' - ')
    line = line.replace('--', ' - ')
    line = line.replace('``', ' ` ')
    line = line.replace('/', ' / ')
    # line = line.replace('\', ' \ ')
    line = line.replace('\n', '')
    # line = line.replace("  " , "")
    return line

def vowelCount(word_token):
    v_count=0;
    for element in range(0, len(word_token)):
        if word_token[element] in ['ে', 'ি', 'ী', 'ো', 'ৌ', 'ৗ', 'ৈ', 'া', 'ু', 'ূ']:
            v_count = v_count + 1
    return v_count
        #if word_token[element] == 'ে':

def even_vowel(word_token):
    v_count=0
    counter_a = word_token.count('ে')
    counter_i = word_token.count('ি')
    counter_ee = word_token.count('ী')
    counter_o = word_token.count('ো')
    counter_ou = word_token.count('ৌ')
    counter_oi = word_token.count('ৗ')
    counter_ei = word_token.count('ৈ')
    counter_aa = word_token.count('া')
    counter_oo = word_token.count('ু')
    counter_uu= word_token.count('ূ')

    v_count=counter_a%2 + counter_i%2 + counter_ee%2 +  counter_o%2 +  counter_ou%2 +  counter_oi%2 +  counter_ei%2 +  counter_aa%2 +  counter_oo%2 +  counter_uu%2
    #print ("Even vowel count %s " % v_count)
    return v_count





def get_echo(word_token):
    e_vowel = even_vowel(word_token)
    if (word_token.endswith('লৈ') or word_token.endswith('কৈ'))  and '-' not in word_token:
        word_token=word_token[0:len(word_token)-2]
    org_word = word_token



    digits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯']
    for word in digits:
        if word in word_token:
            return 'NA'

    vowel_count=vowelCount(word_token)

    # অনুȂপ/Anurup/ (ECHO word)word formin

    word_token = org_word
    if '-' in word_token:
        word_token = word_token.split('-')
        word_token1 = word_token[0]
        word_token2 = word_token[1]
        d = Levenshtein.distance(word_token1, word_token2)

        l1 = len(word_token1)
        l2 = len(word_token2)
        if (l2 == 0 or l1 == 0):
            return 'NA'
        # keeping the minimum length of the two segment
        if (l1 < l2):
            sm = l1
        else:
            sm = l2
        print("%s-------------------length---%s, Distance %s" % (word_token1, sm,d))
        if (d == 1 and word_token1[0] != 'চ' and word_token2[0] == 'চ'):
            return 2
        if (d == 1 and (word_token1[0] == 'চ' or word_token1[0] == 'ছ') and word_token2[0] == 'ত'):
            return 2
        if (d == 1 and (word_token1.endswith('চ') or word_token1.endswith('ছ')) and (
                word_token2[0] == 'ত' or word_token2[0] == 'ছ' or word_token2[0] == 'চ')):
            return 2
        # ECH-R5
        if (d < sm and e_vowel == 0 and (
                word_token1[0] == word_token2[0] or word_token1[l1 - 1] == word_token2[l2 - 1])):
            return 2

        # ECH-R8
        if (d < sm and e_vowel < 2 and (word_token1[0] == word_token2[0] and word_token1.startswith('আ') or
                word_token1[l1 - 1] == word_token2[l2 - 1])):
            return 2

        # ECH-R9
        if (word_token1[0] not in ['আ', 'উ', 'এ', 'ও'] and l1 > 1):
            if ((word_token1[0] == word_token2[0] and word_token1[1] == 'া' and l1 == 2)):
                return 2
        if (word_token1[0] == 'আ' and word_token2[0] == 'অ' and l1 == 1):
            return 2
        #ECH-R10
        if (word_token1[0] == word_token2[0] and l1 == 2 and word_token1[1] == 'য়'):
            return 2

    #vowel_count = 0;
    #for element in range(0, len(word_token)):
     #   if word_token[element] in ['ে', 'ি', 'ী', 'ো', 'ৌ', 'ৗ', 'ৈ', 'া', 'ু', 'ূ']:
      #      vowel_count = vowel_count + 1

    word_token = org_word

    if '-' not in word_token:
        if(word_token.endswith('িৰ') or word_token.endswith('াৰ') or word_token.endswith('াই') or word_token.endswith('ৱৰ') or word_token.endswith('ীৰ') or word_token.endswith('্যত') or word_token.endswith('তা') or word_token.endswith('ীয়া') or word_token.endswith('িয়া')):
            return 'NA'

#**************For Levenshtein Distance*******

    new_length = int(len(word_token) / 2)
    #if ((len(word_token) % 2 != 0 and word_token[0] !='আ' ) or (len(word_token) % 2 != 0 and word_token[0] != 'উ') or (len(word_token) % 2 != 0 and word_token[0] != 'এ' ) or (len(word_token) % 2 != 0 and  word_token[0] != 'ও'  )):
    if (len(word_token) % 2 != 0 and word_token[0] not in ['আ','উ','এ','ও']):
        new_length = new_length + 1
    if '-' not in word_token:
        word_token1 = word_token[0:new_length]
        word_token2 = word_token[-new_length:]
    else:
        word_token = word_token.split('-')
        word_token1 = word_token[0]
        word_token2 = word_token[1]
    d= Levenshtein.distance(word_token1,word_token2)
    print("Levenstein Distance ******************** %s---%s : %s" % (d,word_token1,word_token2))
    vowel_count_word_token1=vowelCount(word_token1)
    vowel_count_word_token2=vowelCount(word_token2)
    #for element in range(0, len(word_token1)):
     #   if word_token1[element] in ['ে', 'ি', 'ী', 'ো', 'ৌ', 'ৗ', 'ৈ', 'া', 'ু', 'ূ']:
      #      vowel_count_word_token1 = vowel_count_word_token1 + 1
    #for element in range(0, len(word_token2)):
     #   if word_token2[element] in ['ে', 'ি', 'ী', 'ো', 'ৌ', 'ৗ', 'ৈ', 'া', 'ু', 'ূ']:
      #      vowel_count_word_token2 = vowel_count_word_token2 + 1
    vowel_diff = abs(vowel_count_word_token1 - vowel_count_word_token2)

    #if vowel_count_word_token1==1 and vowelCount(word_token2[1:len(word_token2)])==0 :
     #   return 'NA'
    #if 1 < vowel_diff:
    #print("Vowel diff -------------------------------------%s %s %s" % (vowel_diff,vowel_count_word_token1,vowel_count_word_token2))
    #    return 'NA'


    word_token=org_word
#************************levenshtein end***********

    if (len(word_token) < 3):
        return 'NA'

    if (len(word_token) < 6 and word_token.endswith('ৰ') and '-' not in word_token):
        return 'NA'

    word_token = word_token.replace('্যা', '')
    word_token = word_token.replace('ে', '')
    word_token = word_token.replace('ি', '')
    word_token = word_token.replace('ী', '')
    word_token = word_token.replace('ো', '')
    word_token = word_token.replace('ৌ', '')
    word_token = word_token.replace('ৗ', '')
    word_token = word_token.replace('ৈ', '')
    word_token = word_token.replace('া', '')
    word_token = word_token.replace('ু', '')
    word_token = word_token.replace('ূ', '')
    word_token = word_token.replace('া্', '')
    word_token = word_token.replace('্', '')

    print("word token %s" % word_token)
    if (len(word_token) < 3):
        return 'NA'

    v_less_word_token = word_token
    # word_token=word_token.replace('\u09C1','')
    #print("************************ %s" % word_token)
    new_length = int(len(word_token) / 2)
    if(len(word_token)%2 !=0 ):
        new_length=new_length+1
    if '-' not in word_token:
        word_token1 = word_token[0:new_length]
        word_token2 = word_token[-new_length:]
    else:
        word_token = word_token.split('-')
        word_token1 = word_token[0]
        word_token2 = word_token[1]
    if(len(word_token2)==0):
        return 'NA'
    diff=0
    diff = Levenshtein.distance(word_token1, word_token2)
    # If vowel differ than 1  in both the segment


    if e_vowel >= 1:
        print("Even vowel count %s, Diff %s " % (e_vowel,diff))
        #if diff >= 1 and  (word_token1[0] != 'আ' or word_token[0] != 'উ' or word_token[0] != 'এ' or word_token[0] != 'ও'  ):
        if diff >=1 and ((len(word_token) % 2 != 0 and word_token[0] != 'আ') or (
                    len(word_token) % 2 != 0 and word_token[0] != 'উ') or (
                    len(word_token) % 2 != 0 and word_token[0] != 'এ') or (
                    len(word_token) % 2 != 0 and word_token[0] != 'ও')):
        #if diff >=1 and  word_token1[0] not in ['আ', 'উ', 'এ', 'ও']:

            print("Vowel Distance %s " % diff)
            return 'NA'
    #     print("Even vowel count %s " % e_vowel)
    #    if diff > 1:
     #       print("Vowel Distance %s " %  diff )
      #      return 'NA'
    if( len(word_token1) <= 2 or len(word_token2) <= 2 ) and d>1 :
        return 'NA'

    # if (new_length % 2) == 0 and new_length>0:
    if (len(word_token) % 2) == 0 and new_length > 0 and d<3:
        # print("New length ==== %s ", new_length)
        # word_token1 = word_token[0:new_length]
        # print("word_token 1----%s, word_token 2---%s" % (word_token1,word_token2))
        # word_token2 = word_token[-new_length:]

        # it covers ONO-R2,ONO-R3

        if word_token1 == word_token2 and d<3:
            return 3
        if len(org_word) > 4:
            # word_token1 = word_token[0:new_length]
            # word_token2 = word_token[-new_length:]
            # if (((word_token1.startswith('চ') and word_token2.startswith('প')) or (word_token1.startswith('জ') and word_token2.startswith('প')) or (word_token1.startswith('ল') and word_token2.startswith('প')) or  (word_token1.startswith('ধ') and word_token2.startswith('প')) or             (word_token1.startswith('ঢ') and word_token2.startswith('প')) or (word_token1.startswith('হ') and word_token2.startswith('প'))) and (word_token1[len(word_token1)-1]==word_token2[len(word_token2)-1])):
            # print("Word Token1 %s---%s" % (len(word_token1), word_token1[1:len(word_token1)-1]))
            # print("Word Token2 %s----%s" % (len(word_token2), word_token2[1:len(word_token2) - 1]))
            # print("Word Token1 %s---%s" % (len(word_token1), word_token1[-len(word_token1)-2:]))
            # print("Word Token2 %s----%s" % (len(word_token2), word_token2[-len(word_token2)-2:]))
            # All but first character are same and all 2nd segment starts with specific letter ধৰ্ফৰ্,  হেৰফেৰ
            # if((word_token1[1:len(word_token1)-1]== word_token2[1:len(word_token2) - 1])  or (word_token1[-len(word_token1)-3:]==word_token2[-len(word_token2)-3:]):
            if ((word_token1[1:len(word_token1) - 1] == word_token2[1:len(word_token2) - 1]) and word_token2[0] in ['প',
                                                                                                                    'ফ',
                                                                                                                    'ভ',
                                                                                                                    'ম',
                                                                                                                    'ঢ',
                                                                                                                    'জ',
                                                                                                                    'দ'] and d<3):
                return 3
            # Last character is same and vowel count is even চেলেংপেটেং
            if (word_token1[len(word_token1) - 1] == word_token2[
                len(word_token2) - 1]) and vowel_count != 0 and vowel_count % 2 == 0 and d<3:
                return 3
            # ONO-R4 আবোলতাবোল, আমনজিমন
            if ((word_token1[1:len(word_token1) - 1] == word_token2[1:len(word_token2) - 1]) and word_token1[0] in ['অ',
                                                                                                                    'আ',
                                                                                                                    'ই',
                                                                                                                    'ঈ',
                                                                                                                    'এ',
                                                                                                                    'এ',
                                                                                                                    'ও',
                                                                                                                    'ঔ'] and
                    word_token2[0] in ['জ', 'ত'] and d<3):
                return 3
            # ONO-R5
            if word_token1[0] == word_token2[0] and vowel_count != 0 and vowel_count % 2 == 0 and d<3:
                return 3
            # ONO-R7
            word_token_new = v_less_word_token[1:len(v_less_word_token)]
            # print("*****ONO-R7************** %s" % word_token)
            if '-' not in word_token_new:
                word_token_new1 = word_token_new[0:new_length]
                word_token_new2 = word_token_new[-new_length:]
            else:
                word_token_new = word_token_new.split('-')
                word_token_new1 = word_token_new[0]
                word_token_new2 = word_token_new[1]
            if word_token_new1 == word_token_new2:
                return 3
            # ONO-R8
            if word_token1[0] == word_token2[0] and word_token1[len(word_token1) - 1] == word_token2[
                len(word_token2) - 1] and d<3:
                return 3


    return 'NA'

#d=Levenshtein.distance("abcc", "abc")

#print("Levenshtein distance----------------------------%s" % (d))


#print("Levenshtein distance---------------------------- %s" % Levenshtein.distance('চেলেংপ', 'েেংপ'))
#print("Levenshtein distance-----------------------------%s" % nltk.edit_distance('চেলেংপ', 'েলেংপ'))
count = 1
word_matrix = []
file1 = open("redup_word.txt", "w")

#prepare_input('input_file.txt')
prepare_input('social_media_post.txt')
#prepare_input('agriculture_corpus1.txt')

with open('input.txt', 'r') as f:
    for line in f:
        # if  t!='\n':
        line = prepare_sentence(line)
        bi_gram = generate_gram(line, 2)  # bigram check

        # print(line)
        print(bi_gram)
        # print(len(bi_gram))
        j = 0

        # file1.write("<Word id=%s>\n" % count)
        # count = count + 1;
        t = line.strip().split()
        k = 0
        # print(t)
        # print(len(t))
        for i in range(len(t)):
            pos = 'NA';
            if (k < len(t)):
                if j < len(bi_gram):
		    #print("Bigram**********************************************%s " % bi_gram)
                    pos = 'NA';
                    pos = get_bigram_echo(bi_gram[j])
                    if (pos != 'NA'):
                        file1.write("Bigram Word id=%s --- %s \\\ \n " % (count, bi_gram[j]))
                        count = count + 1
                        word_token = bi_gram[j]
                        j = j + 2
                        k = k + 2
                    else:
                        if (k < len(t)):
                            # print(t[k])
                            pos = 'NA';
                            pos = get_echo(t[k])
                            # if (pos != 0):
                            if (pos != 'NA'):
                                if(pos == 2):
                                    file1.write("Unigram Echo Word id=%s ---%s \\\ \n " % (count, t[k]))
                                if(pos == 3):
                                    file1.write("Unigram Onomatopoeic Word id=%s ---%s \\\ \n " % (count, t[k]))
                                count = count + 1
                            word_token = t[k]
                            # file2 = open("unavailable_word_in_xobdo.csv", "w+")
                            f = 0
                            k = k + 1
                            j = j + 1
                else:
                    # print(t[k])
                    pos = 'NA';
                    pos = get_echo(t[k])
                    if (pos != 'NA'):
                        if(pos == 3 ):
                            file1.write("Unigram Echo Word id=%s --- %s \\\ \n" % (count, t[k]))
                        if(pos == 2 ):
                            file1.write("Unigram Onomatopoeic Word id=%s ---%s \\\ \n " % (count, t[k]))
                        count = count + 1
                    word_token = t[k]
                    f = 0
                    k = k + 1
                    j = j + 1

    # file1.write("\n</word>\n")
file1.close()
