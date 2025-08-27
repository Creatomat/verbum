import nltk  
from nltk.corpus import words, wordnet 

nltk.download('words')
nltk.download('wordnet')

L=[]
for w in words.words():
    if len(w)==6:
        L.append(w.lower())


added=set()

D={}
f=open('Word_Database.txt', 'w')
for i in L:
    s=wordnet.synsets(i)
    for syn in s:
        for lemma in syn.lemma_names():
            if len(lemma)==6 and lemma.lower() not in added:  
                f.write(lemma.lower()+':'+ syn.definition()+'\n')
                added.add(lemma.lower())
f.close()
        

