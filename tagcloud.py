from collections import Counter
import csv
import json
import codecs
import sys, os

FP_WORKDIR = '/var/www/twitter_trends'
ATT_WORD = 'key'
ATT_COUNT = 'value'


def wordCount_json_new(myData):
        """
            1- count word frequencies
            2- build a json file that contains bios tag cloud [{"value": 23, "key": "food"}, {"value": 25, "key": "world"}]
           
        """

        for key, value in myData.items():
                #now build word frequncies for tag cloud
                #print(value)
                text = value.split(' ');
                #print(text)
                wordcount = Counter(text)   
                targetFile = '';
                try:
                        TARGET_FILENAME=FP_WORKDIR+'/output/countries/'+key+'.json';
                        print(TARGET_FILENAME)
                        FP = codecs.open(TARGET_FILENAME, 'w',encoding='utf-8');
                        str_list=[]
                        for w in sorted(wordcount, key=wordcount.get, reverse=True):
                                word= w;
                                count=wordcount[w];                
                
                                str_list.append({ ATT_WORD : word, ATT_COUNT : count });                                

                        json.dump(str_list, FP, ensure_ascii=False);
                        FP.close();
                except IOError as e:
                                print >> sys.stderr,'ERROR: failed to open file  ',filename, str(e)
                                FP.close();
                FP.close()

stopWords=['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your']
def remove_stop_words(text):
        #remove stop words from trends
        wordlistIn = text.split()
        try:
                filtered_words = [w for w in wordlistIn if w.strip().lower() not in stopWords]
                

        except Exception as e:
                print >> sys.stderr, '----------Error in removing my stopword',str(e)
                pass
        return filtered_words


myDict={}
FP_SOURCE_CSV = FP_WORKDIR+'/output/trends.csv'
#FP_SOURCE_CSV = FP_WORKDIR+'/output/test.csv'
sourceFile = codecs.open(FP_SOURCE_CSV, 'r', 'utf-8')
nextline = sourceFile.readline().strip()#read headers
nextline = sourceFile.readline().strip()#read first line
count = 0
while (len(nextline) > 0):
        #print(nextline)
        try:
                cells = nextline.split(',');
                location = cells[1]
                #print(location)
                trends = cells[2]
                #trends = cells[2].replace('#',' ')
                trends = trends.replace(' ', '!')
                trends = trends.replace('!', '')
                trends = trends.replace('|', '  ')
                trend_list = remove_stop_words(trends)
                text = ''
                for w in trend_list:
                        #print(w)
                        text= text+w+' ' ;
                trends=text
                #print('new..;', trends)
                if location in myDict:
                        trends+=myDict[location];
                        del myDict[location];
                myDict[location]=trends;
                nextline = sourceFile.readline();
                #nextline = sourceFile.readline().strip();


        except Exception as e:
                #print(sys.stderr,str(e))
                nextline = sourceFile.readline().strip();
wordCount_json_new(myDict);
print("done...")


'''
#Stop Words - Not Required
#

'''




