import xlrd, os
import xlwt
import xlsxwriter
import csv, sys
"""
Fields
"""

"""
Parses .csv files in "data" to refine the dataset based on "keywords".

USAGE: refine_abstract.py arg1 [arg2]
eg. refine_abstract.py filename key,words,I,want,to,refine
"""

#The keyword we are searching for
if(len(sys.argv) == 3):
    folder = sys.argv[1]
    keywords = []
    keywordArr = sys.argv[2].split(',')
    for key in keywordArr:
        print(key)
        keywords.append(key)

    print(keywords)
    """
    Setup
    """
    #Count the number of times our keywords show up
    abstract_location = "C:/Users/bns7/workspace/abstract_tool/data/"
    write_location = "C:/Users/bns7/workspace/abstract_tool/" + folder + "/"
    if not os.path.exists(write_location):
        os.makedirs(write_location)

        count = {}
        writeTo = {}
        #Loops through files
        for filename in os.listdir(abstract_location):
            fileLocation = abstract_location + filename;

            with open(fileLocation,'rb') as f:
                writeFile = open(write_location + filename, "w")
                print(filename)
                reader = csv.reader(f)
                try:
                    #loop through each row.
                    for row in reader:
                        #Checks if any keyword is in abstract
                        for key in keywords:
                            if(row[1].find(key)!=-1):
                                for value, column in enumerate(row):
                                    writeFile.write("\""+column + "\"")
                                    writeFile.write("" if (value == len(row)-1) else ",")
                                writeFile.write("\n")
                                break

                except csv.Error, e:
                    sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
    else:
        print("File already exists")

    def processText(text):
        #Process int and floats
        if isinstance(text,int) or isinstance(text,float):
            temp = str(text)
        else:
            #Process others
            temp = text.encode('utf-8')
        return temp

else:
    print("Number of args incorrect")
    print("USAGE: refine_abstract.py arg1 [arg2]")

#read setup
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
"""def processText(text):
    #Process int and floats
    if isinstance(text,int) or isinstance(text,float):
        temp = str(text)
    else:
        #Process others
        temp = text.encode('utf-8')
    return temp

for filename in os.listdir(abstract_location):
    print(filename)
    if(filename.endswith(".csv")):
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
                if(abstr.find(keyLow) != -1):
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
#writebook.save(file_location_write);"""
