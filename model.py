import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation
from sklearn import linear_model

def flatten(mp):
	rs = {}
	for k in mp.keys():
		if type(mp[k]) != dict:
			rs[k] = mp[k]
		else:
			cur = flatten(mp[k])
			for ck in cur.keys():
				rs[k + '.' + ck] = cur[ck]
	return rs

if __name__ == "__main__":
	data = json.load(open('data.json'))
	data = list(map(flatten, data))
	# id == post_id
	df = pd.DataFrame(data)
	df.loc[np.isnan(df['id']), 'id'] = df['post_id']
	df['likes'] = df['likes.user_likes']
	df = df[['id', 'text', 'likes']]
	vectorizer = CountVectorizer(min_df=1)
	X = df['text']
	Y = df['likes']
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size = 0.4)
	X_train = vectorizer.fit_transform(X_train)
	X_test = vectorizer.transform(X_test)
	mod = linear_model.LogisticRegression(dual=False)
	mod.fit(X_train, y_train)
	print("Train score:", mod.score(X_train, y_train))
	print("Test score:", mod.score(X_test, y_test))

	y_pred = mod.predict(X_test)
	print(list(y_pred).count(1), list(y_test).count(1))
	print("False posives:", len([x for (x,y) in zip(y_test, y_pred) if x!=y and y==1]) )
	print("False negative:", len([x for (x,y) in zip(y_test, y_pred) if x!=y and y==0]) )
