from vk import VK
import time
import json

if __name__ == '__main__':
	vk = VK()

	params = {'filters'  : 'post' ,
			  'count' : '100' }
	params['end_time'] = int(time.time())
	params['start_time'] = params['end_time'] - 60*60*24*50
	items = []
	tot = 0
	for _ in range(200):
		feed = vk.call_method('newsfeed.get', params)
		items += [ x for x in feed['items'] if len(x['text']) > 0]
		params['start_from'] = feed.get('next_from', None)
		print(feed.keys())
		tot += len(feed['items'])
		print(len(items), tot)
		if not params['start_from']:
			#del params['start_from']
			#params['end_time'] = params['start_time']
			#params['start_time'] = params['end_time'] - 60*60*24*20
			break
	#print(feed)

	liked = [items[x] for x in range(len(items)) if items[x]['likes']['user_likes'] == 1]
	print(len(liked))
	fd = open('data.json', 'w')
	json.dump(items, fd)
	fd.close()
