import numpy as np
import pandas as pd
import glob
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
from timeit import default_timer as timer
import dask.dataframe as dd

client = MongoClient('localhost',27017)
db = client['abstracts_tool']
#labeled collection
collection = db['ieee_tagged']
#unlabled collection
collection_unlabeled = db['ieee_dump1']

cursor = collection.find({})
cursor_unlabeled = collection_unlabeled.find({})

#path =r'/home/bns7/Downloads/workspace/Split_abstracts/csv_only_first_header' # use your path
#allFiles = glob.glob(path + "/*.csv")
#df = pd.DataFrame()
#list_ = []
#for file_ in allFiles:
#    frame = pd.read_csv(file_,  error_bad_lines=False, header=0)
#    list_.append(frame)
#df = pd.concat(list_)

#Create dataframe
#df = data(db)

df = pd.DataFrame(list(cursor))
print("loaded yay")
df_unlabeled = dd.read_csv('../Split_abstracts/csv/abstract*.csv', names =["","document_title","authors","author_affiliations","publication_title","date_added_to_xplore","year","volume","issue","start_page","end_page","abstract","issn","isbns","doi","pdf_link","author_keywords","ieee_terms","inspec_controlled_terms","inspec_non_controlled_terms","mesh_terms","article_citation_count","patent_citation_count","reference_count","copyright_year","online_date","issue_date","meeting_date","publisher","document_identifier"])

print("loaded 2")

df.loc[df['ump_decision'] == 'yes','ump_decision'] = 1
df.loc[df['ump_decision'] == 'no','ump_decision'] = 0

#df.ump_decision.map(lambda x: 1 if x == 'yes' else 0, 'int 64')

#Actual data

df_x = df['abstract']
df_y = df['ump_decision']


# print(df_y)

#Convert abstract into matrix using TFIDFVectorizer

text_clf = Pipeline([
    ("vect", TfidfVectorizer(min_df=1,stop_words='english')),
    ("clf", SGDClassifier(penalty='elasticnet')),
])
mnb_clf = Pipeline([
    ("vect", TfidfVectorizer(min_df=1,stop_words='english')),
    ("clf", MultinomialNB()),
])
df_y=df_y.astype('int')

#Fit the values of each ML algorithm with the actual results.

# print(df_x.values[:5])

print("df_x")
print(df_x)
print("df_y")
print(df_y)
print("text_clf\n")

text_clf.fit(df_x.values,df_y.values)
print("mnb_clf\n")
mnb_clf.fit(df_x.values,df_y.values)

#Calculate the score of the fit and crossvalidation score.

# pred = text_clf.predict(df_x)

print("scores")
print(text_clf.score(df_x.values,df_y.values))
print(mnb_clf.score(df_x.values,df_y.values))

print("crossvalidation scores")
print(df_unlabeled['abstract'])
ul_test =text_clf.decision_function(df_unlabeled['abstract'])
print(cross_val_score(text_clf,df_x.values,df_y.values, cv=10).mean())
print(cross_val_score(mnb_clf,df_x.values,df_y.values, cv=10).mean())

count = 0;

#only use unique samples
ul_test_u = np.unique(ul_test)

for x in np.nditer(ul_test_u):
    if(x > 0):
         count+=1
print("count: " + str(count))
items = np.argsort(ul_test_u)[-9:]
#item: Argsort returns the index of rating
#then use ul_test_u to get the rating.
print("items[0]: ")
print(items[0])
print("ul_test_u 379684: ")
print(ul_test_u[items[0]])

print("df_unlabeled['title'].iloc[items] ")
print(df_unlabeled['title'].iloc[items])
print(list(df_unlabeled))

from bokeh.plotting import figure, show, output_file, ColumnDataSource, curdoc
from bokeh.models import HoverTool
from bokeh.models import TapTool

output_file("line.html")

TOOLS = 'wheel_zoom,box_zoom,box_select,crosshair,reset'

source = ColumnDataSource(
	data=dict(
	    x = np.argsort(ul_test_u),
	    y = np.sort(ul_test_u),
	    desc=df_unlabeled['title'].iloc[np.argsort(ul_test_u)],
	)
    )
hover = HoverTool(
	tooltips=[
	    ("rating", "@y"),           
	    ("desc", "@desc"),
	    ("index", "@x"),
	]
    )

p = figure(plot_width=400, plot_height=400, tools = [hover,TOOLS,TapTool()])

p.circle('x','y', size=10, color="navy", alpha=0.5, source=source)

show(p)  # open a browser
#
# print(df_unlabeled['title'].iloc[np.argsort(ul_test)[-9:]].values)
# print(df_unlabeled.iloc[243])
