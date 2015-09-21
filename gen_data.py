from vk import VK
import time
import json

def get_newsfeed(vk, max_count):
	params = {'filters'  : 'post' ,
			  'count' : '100' }
	params['start_time'] = 1
	items = []
	for _ in range(200):
		feed = vk.call_method('newsfeed.get', params)
		items += [ x for x in feed['items'] if len(x['text']) > 0]
		params['start_from'] = feed.get('next_from', None)
		print('Geting newsfeed', len(items), '/', max_count)
		if not params['start_from'] or len(items) >= max_count:
			break
	items = [ x for x in items if x['likes']['user_likes'] == 0 ]
	return items

def get_favs(vk, max_count):
	cnt, off, got = 100, 0, 1
	items = []
	params = { 'count' : str(cnt) }
	while got > 0 and len(items) < max_count:
		favs = vk.call_method('fave.getPosts', params)
		items += [ x for x in favs['items'] if len(x['text']) > 0 ]
		got = len(favs['items'])
		off += cnt
		params['offset'] = off
		print('Getting favorites', len(items), '/', max_count)
	return items

if __name__ == '__main__':
	vk = VK()
	
	recent = get_newsfeed(vk, 1000)
	favs = get_favs(vk, 100)

	data = recent + favs
	fd = open('data.json', 'w')
	json.dump(data, fd)
	fd.close()
