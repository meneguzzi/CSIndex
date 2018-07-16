# CSIndexbr: Exploring Brazilian Scientific Production in Computer Science

# @author: Marco Tulio Valente - ASERG/DCC/UFMG

# http://aserg.labsoft.dcc.ufmg.br

import xmltodict
import re
import gzip
import time
    
## constants

FIRST_YEAR= 2013
LAST_YEAR= 2018
min_paper_size = 10

count = 0
papers = {}

def paperSize(dblp_pages):
  page= re.split(r"-|:", dblp_pages)
  if len(page) == 2:
     p1= page[0]
     p2= page[1]
     return int(p2) - int(p1) + 1
  elif (len(page) == 4):
     p1= page[1]
     p2= page[3]
     return int(p2) - int(p1) + 1
  else:
     return 0


def parse_dblp_xml(_, dblp_xml):
    global count, papers, journals
        
    count += 1
    if count % 20000 == 0:
       print str(count)
              
    if 'year' in dblp_xml:
       syear= dblp_xml['year']
       year = int(syear)
       
       if ((year >= FIRST_YEAR) and (year <= LAST_YEAR)):
          if 'journal' in dblp_xml:
              journal = dblp_xml['journal']
              if journal in journals:
                 if 'pages' in dblp_xml:
                    dblp_pages = dblp_xml['pages']
                    size = paperSize(dblp_pages)
                    if (size >= min_paper_size):
                       print syear + ":" + journal
                       papers[journal][year - 2013] += 1  
    return True
           
 
# main program

start_time = time.time()

journals= {}
with open("journals.txt") as file:
   journals = file.read().splitlines()
for journal in journals:
    papers[journal] = [0, 0, 0, 0, 0, 0]   

xmltodict.parse(gzip.GzipFile('dblp-fixed.xml.gz'), item_depth=2, item_callback=parse_dblp_xml)

f = open("out.csv",'w')
for journal in journals:
    f.write(journal)
    f.write(',')
    
    f.write(str(papers[journal][0]))
    f.write(',')
    f.write(str(papers[journal][1]))
    f.write(',')
    f.write(str(papers[journal][2]))
    f.write(',')
    f.write(str(papers[journal][3]))
    f.write(',')
    f.write(str(papers[journal][4]))
    f.write(',')
    f.write(str(papers[journal][5])) 
    f.write('\n')    
f.close()

print("Runtime (minutes): " % (time.time() - start_time) / 60)
