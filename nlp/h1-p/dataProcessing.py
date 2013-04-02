#!usr/bin/python

word_tag = {}
word_set = {}
infrequent_words_map = {}

def tag_rare(word) :
    for c in word :
        if c.isdigit() == True : return 'Numeric'
    if word.isupper() == True : return 'All Capitals'
    if word[-1:].isupper() == True : return 'Last Capital'
    return 'Rare'

def replace() :
    FILE_NAME = 'gene.counts'
    with file(FILE_NAME, 'r') as f :
        for item in f:
            info = item.split()
            if info[1] == 'WORDTAG' :
                word_set[info[3]] = word_set.get(info[3],0) + int(info[0]);
    infrequent_words_map = dict([(word,1) for word in word_set if word_set[word] < 5])
 
    out = file('gene.train.changed2','w')
    with file('gene.train','r') as f :
        for item in f :
            info = item.split()
            if len(info) > 0 and infrequent_words_map.get(info[0]) != None:
                out.write('%s %s\n' % (tag_rare(info[0]),info[1]))
            else:
                out.write('%s'%(item))
    out.close()

if __name__ == '__main__' :
    replace()
