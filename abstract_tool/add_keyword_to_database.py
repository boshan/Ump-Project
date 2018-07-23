from pymongo import MongoClient
from pprint import pprint
import datetime
import csv,sys,os
import xlrd, os
import xlwt
import xlsxwriter
import re
client = MongoClient("localhost",27017)

'''
This script takes some keywords and parses target csv files for documents and checks
 for redundancies in documents.
'''



#database "abstracts"
db = client['abstracts_tool']
#collection "ieee"
posts = db['ieee']
count = 0;
count_errors = 0;
temp_insert = {};
fileLocation =  "C:/Users/bns7/workspace/abstract_tool/dataBetter1/";

#The keyword we are searching for
keywords = ["Life","cycle", "inventory", "Enviromental","impact"]


"""
Setup
"""

#read setup
abstract_location = "C:/Users/bns7/workspace/Split_abstracts/"
# newData = "C:/Users/bns7/Desktop/newestData.xlsx"
# file_location = "C:/Users/bns7/Desktop/smallData.xlsx"
# file_location2 = ("C:/Users/bns7/Downloads/abstract_dataset"
#     "(1)/abstract_dataset/data/ieeexplore_abstracts.csv")

#write setup
# file_location_write = "C:/Users/bns7/Desktop/newData.xlsx"
# writebook = xlsxwriter.Workbook(file_location_write)
# writeExcel = writebook.add_worksheet("Drilling Sheet")



"""
Data Processing
"""


"""
Writes to a file in a csv format.
"""
def processText(text):
    #Process int and floats
    if isinstance(text,int) or isinstance(text,float):
        temp = str(text)
    else:
        #Process others
        temp = text.encode('utf-8')
    return temp

def find_word(text, search):
   result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
   if len(result)>0:
      return True
   else:
      return False

for filename in os.listdir(abstract_location):
    print(filename)
    if(filename.endswith(".xlsx")):
        workbook = xlrd.open_workbook(abstract_location + filename)
        sheet = workbook.sheet_by_index(0)
        #Store the data from spreadsheet in "data" Matrix
        data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
        print("hi");
        #Loops the rows in data
        for row in data:
            abstr = processText(row[11]).lower()
            #Loops through keywords in each row
            for key in keywords:
                keyLow = key.lower()
                #Checks if the word is found in abstract
                if(find_word(abstr,keyLow)):
                #searches db for the document
                    pr = posts.find({"title":row[1]}).count();
                    #insert if document is not redundant
                    if(pr == 0):
                        temp_insert = {};
                        temp_insert['title'] = row[1];
                        temp_insert['authors'] = row[2];
                        temp_insert['author_affiliations'] = row[3];
                        temp_insert['publication_title'] = row[4];
                        temp_insert['date'] = str(row[6]);
                        temp_insert['date'] = temp_insert['date'].split(".")[0];
                        temp_insert['abstract'] = row[11];
                        temp_insert['doi'] = row[14];
                        temp_insert['author_terms'] = row[16];
                        temp_insert['ieee_terms'] = row[17];
                        temp_insert['inspec_controlled_terms'] = row[18];
                        temp_insert['inspec_noncontrolled_terms'] = row[19];
                        temp_insert['mesh_terms'] = row[20];
                        post_id = posts.insert_one(temp_insert)
                    #post_id = posts.insert_one(temp_insert)
                    print(pr);
    else:
        continue
