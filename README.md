# Automatic Identification of Assamese reduplication

This repository contains python implementation of automatic reduplication identification along with classification into different types.

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Please see to instructions to run the project.


### Library requirement

It is encouraged to work in virtual virtual environments.

We used Python 3 along with IndicNLP library. IndicNLP a python library is required for processing Indian languages. 

1) Install indic nlp: 

```
pip3 install indicnlp 

```
2) Copy the file under kept in 'indicnlp' directory to the installation directory location 'indicnlp/tokenize' where IndicNLP is installed.

For more details of IndicNLP package visit github link- https://github.com/anoopkunchukuttan/indic_nlp_resources#indic-nlp-resources

### Dataset

We have used three dataset for our experiment. Except the third one, the other two are own collection. 

1) Social Media dataset (sample file included in the repo, named as 'social_media_post.txt' )

2) Agricultural dataset ( sample file inculded in repo, named as 'agicultural_dataset.txt' )

3) TDIL dataset:  Acquired dataset named 'Assamese Monolingual Text Corpus ILCI-II' from TDIL, Indian Languages Corpora Initiative phase –II (ILCI Phase-II) project, initiated by the MeitY, Govt. of India, Jawaharlal Nehru University. Not allowed for open publishing.

TDIL Link: https://tdil-dc.in/index.php?option=com_download&task=showresourceDetails&toolid=1877&lang=en

### How to run the project

To run the programme, please run the 'find_redup.py' file-
```
python find_redup.py 
```
1) This will take 'social_media_post.txt' as input.

2) After procesing, the programm will generate a text file named  ***redup_word.txt*** in the same directory which contain all the reduplicated word along with its classification.

##If you use the our code or dataset, please cite this paper [https://dl.acm.org/doi/10.1145/3510419]: 

```

    @article{10.1145/3510419,
    author = {Pathak, Dhrubajyoti and Nandi, Sukumar and Sarmah, Priyankoo},
    title = {Reduplication in Assamese: Identification and Modeling},
    year = {2022},
    issue_date = {September 2022},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    volume = {21},
    number = {5},
    issn = {2375-4699},
    url = {https://doi.org/10.1145/3510419},
    doi = {10.1145/3510419},
    journal = {ACM Trans. Asian Low-Resour. Lang. Inf. Process.},
    month = {may},
    articleno = {90},
    numpages = {18},
    }

      



```

