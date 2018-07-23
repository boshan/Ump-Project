import xlrd, os
import xlwt
import xlsxwriter
import re
"""
Fields
"""
#The keyword we are searching for
keywords = ["Life","cycle", "inventory", "Enviromental","impact"]



"""
Setup
"""
folder = 'dataBetter'
if not os.path.exists(folder):
    os.makedirs(folder)
#Count the number of times our keywords show up
count = {}
writeTo = {}
for key in keywords:
    #Opens a text file for each keyword
    writeTo[key] = open(folder+"/" + key + ".csv", "w")
    count[key] = 0

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
        #Loops the rows in data
        for row in data:
            abstr = processText(row[11]).lower()
            #Loops through keywords in each row
            for key in keywords:
                keyLow = key.lower()
                #references the correct writeFile
                writeFile = writeTo[key]
                #Checks if the word is found in abstract
                if(find_word(abstr,keyLow)):
                    #Writes to respective keyword file
                    for column in range(sheet.ncols):
                        text = processText(row[column])
                        #Writes to file
                        writeFile.write("\""+text + "\"")
                        #Adds the commas
                        writeFile.write("" if (column == sheet.ncols-1) else ",")
                    writeFile.write("\n")
                    #increments count near the end
                    count[key]+=1
    else:
        continue

#prints counts for each keyword
for k in keywords:
    print(k + ": " + str(count[k]))

#Saves to output file
#writebook.save(file_location_write);
