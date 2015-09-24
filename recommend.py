import json
import pandas as pd
from vk import VK
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import os
from consts import TEXT_LENTH

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

def get_recommendations(vk, max_count):
	params = { 'filters' : 'post',
			'count' : '100' }
	items = []
	for _ in range(200):
		feed = vk.call_method('newsfeed.getRecommended', params)
		items += [ x for x in feed['items'] if x['type'] == 'post' and len(x['text']) > TEXT_LENTH]
		params['start_from'] = feed.get('next_from', None)
		print('Geting newsfeed', len(items), '/', max_count)
		if not params['start_from'] or len(items) >= max_count:
			break
	# no need to predict allready liked
	items = [ x for x in items if x['likes']['user_likes'] == 0 ]
	return items

def send_news(vk, news):
	params = { 'user_id' : vk.uid }
	attach = 'wall' + str(news['source_id']) + '_' + str(news['post_id'])
	params['attachment'] = attach
	vk.call_method('messages.send', params)

send_best = False

if __name__ == "__main__":
	vk = VK()
	if os.path.isfile('recs_cache.json'):
		print("Using cache")
		recs = json.load(open('recs_cache.json'))
	else:
		recs = get_recommendations(vk, 300)
		json.dump(recs, open('recs_cache.json', 'w'))
	recs = list(map(flatten, recs))

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
	X = vectorizer.fit_transform(X)
	recs_X = vectorizer.transform([ x['text'] for x in recs ])

	mod = RandomForestClassifier(n_estimators=10)
	mod.fit(X, Y)
	print("Train score:", mod.score(X, Y))

	recs_pred = mod.predict_proba(recs_X)
	print('classes', mod.classes_)
	lst = [(recs_pred[i][1], i) for i in range(len(recs_pred))]
	if (send_best):
		ind = max(lst)
		send_news(vk, recs[ind[1]])
	else:
		lst.sort()
		for i in lst:
			print(i[0])
			print(recs[i[1]]['text'])
