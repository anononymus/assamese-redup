# assamese-redup
Automatic Identification of Assamese reduplication

This repository contains python implementation of automatic reduplication identification along with cllasification into different types.

We used python-3 along with IndicNLP library-

1) Install indic nlp : pip3 install indicnlp 
2) Copy the file under kept in 'indicnlp' directory to the location 'indicnlp/tokenize' where IndicNLP is installed.

For details of IndicNLP package visit github link- https://github.com/anoopkunchukuttan/indic_nlp_resources#indic-nlp-resources

To run the programme, please run the 'find_redup.py' file. This will take 'social_media_post.txt' as input. After procesing, the programm will generate a text file named 'redup_word.txt' in the same directory which contain all the reduplicated word along with its classification.
