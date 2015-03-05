from static import producttext,producttitle
search_items = ['furniture','stripper']
found_titles = []
found_sites = []
for search_site in producttitle.title:
	found_index = -1
	found_site = [search_site,[]]
	found_titles.append(found_site)
	for search_item in search_items:
		while True:
			try_index = found_index+1
			found_index = producttitle.title[search_site].lower().find(search_item,try_index)
			if not found_index < 0:
				found_titles[-1][1].append(found_index)
			else:
				break
	found_titles[-1][1].sort()
	if found_titles[-1][1] == []:
		found_titles.pop()
sorted_titles = [found_titles.pop()]
for titled in found_titles:
	for sorted in sorted_titles:
		if len(sorted[1]) < len(titled[1]):
			sorted_titles.insert(sorted_titles.index(sorted),titled)
			break
		if sorted_titles.index(sorted) == len(sorted_titles) - 1:
			sorted_titles.append(titled)
			break
for search_site in producttext.text:
	found_index = -1
	found_site = [search_site,[]]
	found_sites.append(found_site)
	for search_item in search_items:
		while True:
			try_index = found_index+1
			found_index = producttext.text[search_site].lower().find(search_item,try_index)
			if not found_index < 0:
				found_sites[-1][1].append(found_index)
			else:
				break
	found_sites[-1][1].sort()
	if found_sites[-1][1] == []:
		found_sites.pop()
found_sorted = [found_sites.pop()]
for found_site in found_sites:
	for sorted in found_sorted:
		site_title_len = 0
		sort_title_len = 0
		for sorted_title in sorted_titles:
			if found_site[0] == sorted_title[0]:
				site_title_len = len(sorted_title[1])
			if sorted[0] == sorted_title[0]:
				sort_title_len = len(sorted_title[1])
		if (len(sorted[1]) < len(found_site[1]) and sort_title_len <= site_title_len) or sort_title_len < site_title_len:
			found_sorted.insert(found_sorted.index(sorted),found_site)
			break
		if found_sorted.index(sorted) == len(found_sorted) - 1:
			found_sorted.append(found_site)
			break
html = ''
for final in found_sorted:
	mini_html = producttext.text[final[0]]
	times = 0
	for index in final[1]:
		index += times * 7
		index2 = mini_html.find(' ',index)
		print final,index,index2
		mini_html = mini_html[:index] + '<b>' + mini_html[index:index2] + '</b>' + mini_html[index2:]
		times += 1
	html += mini_html
	html += '\n'
print html