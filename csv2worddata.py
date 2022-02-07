from lib2to3.pytree import convert
from tokenize import Triple
from worddatagenerator import convert2BDSP
import stringLengthCalculator as calculator
import rapidjson

##hardcoding this for now

src = "english.csv"

def splitcsv(filename):
    
    wordDic = {}
    
    with open(filename, "rt", encoding="utf8") as f:
        
        for line in f.read().splitlines():
            
            line = line.split("|")
            
            label = line[0].strip() ##strip removes trailing or leading whitespace
            message = line[1].strip()
            
            wordDic[label] = message
            
    return wordDic, list(wordDic.keys())


def splitjson(filename):
    
    with open(filename, "rt", encoding="utf8") as f:
        wordDic = rapidjson.load(filename)
        
    return wordDic, list(wordDic.keys())


def main():
    
    dic, dicKeys = splitcsv(src)
    
    outfile = 'wordData.json'
    file = open(outfile, "wt", encoding="utf8")
    
    First = True
    
    for key in dicKeys:
        
        message = dic[key]
        label = key
        
        if not First:
            file.write(",\n")
        else:
            First = False
        
        output = convert2BDSP(message, printOutput=False, label=label)
        file.write(output)


if __name__ == "__main__":
    main()