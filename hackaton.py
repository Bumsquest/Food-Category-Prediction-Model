# -*- coding: utf-8 -*-
"""hackaton.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18S-BwBLsvQBwJYD8JunY8FgVolULgEeP
"""

import pandas as pd
import numpy as np
import io
import re
from google.colab import files
import matplotlib.pyplot as plt

uploaded = files.upload()

dataSet = pd.read_csv('train (1).csv')
dataSet.head()

dataSet['text'] = dataSet['text'].str.replace('"', '').str.replace(r"\(.*\)","").str.replace('\n', '').str.replace('\r', '')

dataSet.index

from io import StringIO
col = ['category', 'text']
df = dataSet[col]
df = df[pd.notnull(df['text'])]
df.columns = ['category', 'text']
df['category_id'] = df['category'].factorize()[0]
category_id_df = df[['category', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'category']].values)
df.head()

fig = plt.figure(figsize=(8,6))
df.groupby('category').text.count().plot.bar(ylim=0)
plt.show()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(df.text).toarray()
labels = df.category_id
features.shape

from sklearn.feature_selection import chi2
import numpy as np
N = 3
for Product, category_id in sorted(category_to_id.items()):
  features_chi2 = chi2(features, labels == category_id)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
  print("# '{}':".format(Product))
  print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
  print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['category'],test_size=0.20, random_state = 0)
#count_vect = CountVectorizer()
#X_train_counts = count_vect.fit_transform(X_train)
#tfidf_transformer = TfidfTransformer()
#X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
X_train_tfidf = tfidf.fit_transform(X_train)

clf = MultinomialNB().fit(X_train_tfidf, y_train)
print(X_train_tfidf)

uploaded3 = files.upload()
pred_df = pd.read_excel("Test_Validate.xlsx")

pred_df['text'] = pred_df['text'].str.replace('"', '').str.replace(r"\(.*\)","").str.replace('\n', '').str.replace('\r', '')
submit = pd.DataFrame(columns=['Id'])
l1=[]
l2=[]
z=""
for recipe in pred_df['text'].index:
  input = [pred_df['text'][recipe]]
  l1.append(pred_df['Id'][recipe])
  z=clf.predict(tfidf.transform(input))
  l1.append(z[0])
  #print(l1)
  l2.append(l1.copy())
  
  l1.clear()
  #print(l2)

print(l2)
  #print("h")
  #input = [pred_df['text'][recipe]]
  #submit.append({"Id":pred_df['Id'][recipe],"category":clf.predict(count_vect.transform(input))}, ignore_index=True)
#,"category":clf.predict(count_vect.transform(input))

#submit.to_csv('df.csv')
#files.download('df.csv')
submit = pd.DataFrame(l2, columns=['Id','category'])
submit.to_csv('submission.csv')
files.download('submission.csv')
submit.head(100)

uploaded4 = files.upload()

df_sub = pd.read_csv("submission.csv")

from sklearn.metrics import accuracy_score
y_pred = pred_df['category']
y_true = df_sub['category']
accuracy_score(y_true, y_pred)