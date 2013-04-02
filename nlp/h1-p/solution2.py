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


def q(y1,y2,y3) :
    return float(three_gram[(y1,y2,y3)]) / float(two_gram[(y1,y2)])


def tagger(sentence) :
    sentence_length = len(sentence)
    f = {}
    backpointers = {}    
    res_tag = []
    tag_list = []    
    f[(0,'*','*')] = 1.0
    max_val = 0.0
    max_tag = None    

    for tag in one_gram :
        tag_list.append(tag)
    
    for k in range(1,sentence_length+1) :
        if k <= 2 : w_tag_list = ['*']
        else : w_tag_list = tag_list
        if k <= 1 : u_tag_list = ['*']
        else : u_tag_list = tag_list     
        for u in u_tag_list :
            for v in tag_list :
                max_val = 0.0
                for w in w_tag_list :
                    tmp = q(w,u,v) * f[(k-1,w,u)]
                    if word_set.get(sentence[k-1]) == None :
                        tmp *= e[('_RARE_',v)]
                    else :
                        tmp *= e.get((sentence[k-1],v),0.0)
                    if tmp >= max_val :
                        max_val = tmp
                        max_tag = w
                f[(k,u,v)] = max_val
                backpointers[(k,u,v)] = max_tag
    
    max_val = 0.0
    tag_u, tag_v, tag_w = '', '', ''
    for u in tag_list :
        for v in tag_list :
            tmp = f[(sentence_length,u,v)] * q(u,v,'STOP')
            if max_val <= tmp :
                max_val = tmp
                tag_u, tag_v = u, v
    tag_w = backpointers[(sentence_length,tag_u,tag_v)]

    res_tag.append(tag_v)
    res_tag.append(tag_u)
    res_tag.append(tag_w)
    k = sentence_length
    while k>3 :
        tag_v = tag_u
        tag_u = tag_w
        tag_w = backpointers[(k-1,tag_u,tag_v)]
        res_tag.append(tag_w)
        k -= 1
    res_tag.reverse()
    return res_tag
                
def work(FILE_NAME='gene.test', OUTPUT='gene_test.p2.out') :
    outputf = open(OUTPUT,'w')
    args = []
    with file(FILE_NAME,'r') as f :
        for item in f:
            word = item.split()
            if len(word) > 0:
                args.append(word[0])
            else :
                res_tag = tagger(args)
                for w,t in zip(args,res_tag) :
                    outputf.write('%s %s\n' % (w,t))
                outputf.write('\n')
                args = []
    outputf.close()

if __name__ == '__main__' :
    computeEmissionParameters()
    work() 
