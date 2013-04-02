#!usr/bin/python

word_tag = {}
one_gram = {}
two_gram = {}
three_gram = {}
word_set = {}
e = {}

def computeEmissionParameters(FILE_NAME = 'gene.counts.changed') :
    with file(FILE_NAME, 'r') as f :
        for item in f:
            info = item.split()
            if info[1] == 'WORDTAG' :
                word_set[info[3]] = word_set.get(info[3],0) + int(info[0]);
                word_tag[(info[3],info[2])] = int(info[0])
            elif info[1] == '1-GRAM' :
                one_gram[info[2]] = int(info[0])
            elif info[1] == '2-GRAM' :
                two_gram[(info[2],info[3])] = int(info[0])
            elif info[1] == '3-GRAM' :
                three_gram[(info[2],info[3],info[4])] = int(info[0])
    for (word,tag) in word_tag :
        e[(word,tag)] = (float(word_tag[(word,tag)]) / one_gram[tag])

def tagger(word) :
    if word_set.get(word) == None :
        word = '_RARE_'
    max_val = [0.0,None]
    for tag in one_gram:
        if max_val[0] < e.get((word,tag),0):
            max_val[0] = e[(word,tag)]
            max_val[1] = tag;
    return max_val[1]

def work(FILE_NAME='gene.test', OUTPUT='gene_test.p1.out') :
    outputf = open(OUTPUT,'w')
    with file(FILE_NAME,'r') as f :
        for item in f:
            word = item.split()
            if len(word) > 0:
                outputf.write('%s %s\n' % (word[0], tagger(word[0])))
            else :
                outputf.write('\n')
    outputf.close()

if __name__ == '__main__' :
    computeEmissionParameters()
    work() 
    print tagger('off')
