#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 23:03:35 2020

@author: qali
"""

import os
import sys
import re
from enum import Enum, unique

@unique
class PubType(Enum):
    Nul=0
    Article = 1
    InProceedings = 2


class IR():
    
    def __init__(self, pubType):
        self.pubType = pubType
        self.title=""
        self.authors=''
        self.journal=''
        self.volume=''
        self.number=''
        self.pages=''
        self.year=''
        self.publisher=''
        
        self.editor=''
        self.booktitle=''
        self.conference=''
        
        self.id=''
   
'''
deal with bibtex format

'''
class Bibtex():
    def __init__(self, bibFile):
        self.irList=[]
        self.bibFile=bibFile
        
    def patternSub(self, matchobj):
        patValue = matchobj.group(0)
        numberStr = re.search(r'[0-9]+', patValue).group()
        
        decValue = int(numberStr, 10)
        codepos = chr(decValue)
        return codepos
        
        
    def removeBrace(self, line):
        line = line.strip();
        if line.startswith('{'):
            line = line[1:]
        if line.endswith(','):
            line = line[:len(line)-1]
        if line.endswith('}'):
            line = line[:len(line)-1]
    
        line= re.sub(r'\\unicode\{[0-9]+\}', self.patternSub, line)
        #dblp_unicode=re.findall(r'\\unicode\{[0-9]+\}', line)
        # remove inside matching {}
        line = line.replace('{','')
        line = line.replace('}','')
        return line
    
    # parse into IR
    def parse2IR(self, infoPiece, pubType):
        ir = IR(pubType)
        
        for line in infoPiece:
            line=line.strip()
            
            # skip first and last curly brace
            if line.startswith('@'):
                ir.id = line
                continue
            elif line.startswith('}'):
                continue
            #elif line.find('unicode') > 0:
               # continue
         
            
            items = line.split('=')
            if len(items) < 2:
                print("error in " + ir.id + ":\t" + line)
                continue
            
           # if len(items) > 1:
            #    print(line)
            key = items[0].strip()
            #print(line)
            value = self.removeBrace(items[1].strip()).strip()
            if key.startswith('author'):
                ir.authors=value
            elif key.startswith('title'):
                ir.title=value
            elif key.startswith('journal'):
                ir.journal=value
            elif key.startswith('volume'):
                ir.volume=value
            elif key.startswith('number'):
                ir.number=value
            elif key.startswith('pages'):
                ir.pages=value.replace('--','-')
            elif key.startswith('year'):
                ir.year = value
            elif key.startswith('publisher'):
                ir.publisher = value
            
            elif key.startswith('editor'):
                ir.editor = value
            elif key.startswith('booktitle'):
                ir.booktitle=value
                ir.conference = value.split(',')[0]
            else:
                pass
            
        return ir
    
        
    def parseInfoPiece(self, infoPiece, flag):
        if flag == PubType.Article or flag == PubType.InProceedings:
                ir = self.parse2IR(infoPiece, flag)
                self.irList.append(ir)
        else:
            print("skip unsupport type:\t"+str(flag) + "\t" + infoPiece[0])
            
    def fetchPubType(self, startLine):
        if startLine.find('article') == 0:
            return PubType.Article
        elif startLine.find('inproceedings') == 0:
            return PubType.InProceedings
        else:
            return PubType.Nul

    def parse(self):
        infoPiece = []
        flag = PubType.Nul
        
        count = 0
        item = ''
        with open(self.bibFile, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('@'):
                    count = count + 1
                    flag = self.fetchPubType(line[1:].lower())
                    infoPiece.clear()
                    infoPiece.append(line.strip())
                # end of an infoPiece, parse it
                elif line.startswith('}'):
                    # finish the previous item
                    if len(item) > 0:
                        infoPiece.append(item)
                        item = ''
                        
                    infoPiece.append(line.strip())
                    self.parseInfoPiece(infoPiece, flag)
                # add a line if with '='; exception: if without '=', contniue the line
                elif line.find('=') >= 0:
                    # finish the previous item
                    if len(item.strip()) > 0:
                        infoPiece.append(item.strip())
                        item = ''
                    item = item + ' ' + line.strip()
                else:
                    
                    item = item + ' ' + line.strip()
                    
        print("Found " + str(count) + ' refs in ' + self.bibFile)
        self.verify()
        return self.irList
    
    def verify(self):
        for ir in self.irList:
          #  print(ir.title)
            pass
 
  
        
class GB():
    def __init__(self, irList, outputFile):
        self.irList = irList
        self.outputFile = outputFile
    
    # 转换作者：
    def getAuthors(self, line):
        # split into multiple authors via 'and'
        authorList = line.split('and')
        authors = ''
        count = 0
        for cell in authorList:
            cell = cell.strip()
            # split first and last names via ','
            if cell.find(',') >= 0:
                names = cell.split(',')
            else:
                names = cell.split(' ')
            names[0] = names[0].strip()
            names[1] = names[1].strip()
            # keep first name and Initial of last name
            authors = authors + names[0] + ' ' + names[1][0] + ', '
            count = count + 1
            # keep at most 3 authors
            if count == 3:
                authors = authors + 'et al. '
                break
        return authors
    
    def dumpArticle(self, ir):
        
        info = self.getAuthors(ir.authors)
        info = info + ir.title;
        
        info = info + '[J]. '
        info = info + ir.journal + ', ';
        info = info + ir.year + ', ';
        info = info + ir.volume;
        
        if(len(ir.number) > 0):
            info = info +'(' + ir.number + ')'
        if(len(ir.pages) > 0 ):
            info = info + ": " + ir.pages
        info = info + "."
        return info
            
            
    def dumpInProceedings(self, ir):
        info = self.getAuthors(ir.authors)
        info = info + ir.title;
        
        info = info + '[C]// '
        info = info + ir.conference + '. '
        info = info + ir.publisher + ', '
        info = info + ir.year + '.'
        return info
    
    def dump(self):
        count = 0
        lines = []
        for ir in self.irList:
            count = count + 1
            if ir.pubType == PubType.Article:
                info = self.dumpArticle(ir)
            elif ir.pubType == PubType.InProceedings:
                info = self.dumpInProceedings(ir)
            else:
                print("skip unsupported pubtype:\t"+ir.id)
                info = ir.id
            lines.append(info)
            #print(info)
            
        print("Transformed " + str(len(lines)) + " refs into " + self.outputFile)
        with open(self.outputFile, 'w') as f:
            for line in lines:
                f.write(line+'\n\n')
       
if __name__ == '__main__':
    #path = '/Users/xxx/sample.bib'
    path = sys.argv[1]
    print(path)
    bibtex = Bibtex(path)
    irList = bibtex.parse()
    
    outputFile = os.path.splitext(path)[0]+'-gb.txt'
    gb = GB(irList, outputFile)
    gb.dump()
    
    
