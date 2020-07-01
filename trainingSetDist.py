import os
import sys

def readFile(trainSetPath,CorpusPath):
    trainSetDict = dict()
    CorpusDict = dict()
    
    # read word-freq in audio train set
    with open(trainSetPath) as fp:
        cnt = 0
        for line in fp:
            cnt += 1
            if cnt > 2:
                fields = line.split()
                trainSetDict[fields[0]]=float (fields[1])
    # read word-freq in text corpus            
    with open(CorpusPath) as fp:
        cnt = 0
        for line in fp:
            cnt += 1
            if cnt > 2:
                fields = line.split()
                word = fields[0]
                freq = float(fields[1])
                CorpusDict[word]= list()
                CorpusDict[word].add(freq)
    # calc the coverage of audio words over text words
    for i in CorpusDict:
        if i in trainSetDict:
            freq0 = CorpusDict[i][0]
            freq1 = trainSetDict[i]
            CorpusDict[i].add(freq1)
            CorpusDict[i].add(freq1/freq0)
        else:
            CorpusDict[i].add(0)
            CorpusDict[i].add(0)
            
    # write statitistics into a file
    outfPath = os.path.splitext(CorpusPath)[0]+'-stats.txt'
    statsFilePtr=open(outfPath, 'w', encoding='utf-8')
    for i in CorpusDict:
        data = CorpusDict[i]
        statsFilePtr.write(i+'\t'+ data[0] + '\t' + data[1]+'\t'+data[2]+'\n')
    statsFilePtr.close()
    

audioSetFile=sys.argv[1]
corpusFile=sys.argv[2]

print("reading files:\t"+audioSetFile + "\t"  + corpusFile)


readFile(audioSetFile, corpusFile)
    

           
                

    
                
                