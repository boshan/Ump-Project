from pymongo import MongoClient
from pprint import pprint
import datetime
import csv,sys,os
client = MongoClient("localhost",27017)
#database "abstracts"
db = client['abstracts_tool']
#collection "ieee"
posts = db['ieee_dump2']
count = 0;
count_errors = 0;
temp_insert = {};
fileLocation =  "C:/Users/bns7/workspace/abstract_tool/dataBetter/";
#reset the database for testings
#db.ieee.drop();
for filename in os.listdir(fileLocation):
    if filename.endswith(".csv"):
        #open each file
        with open(fileLocation+filename,'rU') as f:
            reader = csv.reader(f, dialect='excel')
            #loop through each row.
            for row in reader:
                pr = posts.find({"title":row[1]}).count();
                #insert if document is not redundant
                if(pr == 0):
                    try:
                        print(count);
                        count+=1;
                        #sets each dict to coorespnding column in the csv.
                        temp_insert.clear()
                        for value, column in enumerate(row):
                            column = column.lower();
                            if value == 1:
                                temp_insert['title'] = column;
                            elif value == 2:
                                temp_insert['authors'] = column;
                            elif value == 3:
                                temp_insert['author_affiliations'] = column;
                            elif value == 4:
                                temp_insert['publication_title'] = column;
                            elif value == 6:
                                temp_insert['date'] = str(column);
                                temp_insert['date'] = temp_insert['date'].split(".")[0];
                            elif value == 11:
                                temp_insert['abstract'] = column;
                            elif value == 14:
                                temp_insert['doi'] = column;
                            elif value == 16:
                                temp_insert['author_terms'] = column;
                            elif value == 17:
                                temp_insert['ieee_terms'] = column;
                            elif value == 18:
                                temp_insert['inspec_controlled_terms'] = column;
                            elif value == 19:
                                temp_insert['inspec_noncontrolled_terms'] = column;
                            elif value == 20:
                                temp_insert['mesh_terms'] = column;
                        #insert the json file format into mongo
                        post_id = posts.insert_one(temp_insert)
                    # for doc in posts.find_one({"date":"2006.0"}):
                    #     pprint(doc);
                    except e:
                        count_errors+=1;
                        continue;
        print(count_errors)
