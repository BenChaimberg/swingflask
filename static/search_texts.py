import producttext,producttitle

class SearchError(Exception):
	def __init__(self):
		pass

def searching(search_string):
	try:
		search_string = search_string.lower()
		search_items = []
		found_index = -1
		product_text = {}
		html_index = 0
		for item in producttext.text:
			non_html = producttext.text[item]
			while not non_html.find('<') == -1:
				non_html = non_html[:non_html.find('<')] + ' ' + non_html[non_html.find('>')+1:]
			product_text[item] = non_html
		while True:
			try_index = found_index+1
			found_index = search_string.find(' ',try_index)
			if not found_index < 0:
				search_items.append(search_string[:found_index])
				search_string = search_string[found_index:]
			else:
				search_items.append(search_string)
				break
		found_titles = []
		found_sites = []
		html = ''
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
		if not found_titles == []:
			sorted_titles = [found_titles.pop()]
		else: raise SearchError
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
					found_index = product_text[search_site].lower().find(search_item,try_index)
					if not found_index < 0:
						space_index = len(product_text[search_site])-found_index
						space_index2 = found_index
						for i in range(0,3):
							space_index = product_text[search_site][::-1].find(' ',space_index+1)
						if space_index < 0:
							space_index = len(product_text[search_site])
						for i in range(0,4):
							if product_text[search_site].find(' ',space_index2+1) > 0:
								space_index2 = product_text[search_site].find(' ',space_index2+1)
						found_sites[-1][1].append(product_text[search_site][len(product_text[search_site])-space_index:found_index]+'<b>'+product_text[search_site][found_index:found_index+len(search_item)]+'</b>'+product_text[search_site][found_index+len(search_item):space_index2])
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
		html += '<ul>'
		for final in found_sorted:
			html += '<li><h2><a href="/product/' + final[0] + '">' + producttitle.title[final[0]] + '</a></h2>'
			for text in final[1]:
				html += text + '&hellip;'
			html += '</li>'
		html += '</ul>'
	except SearchError:
		html = 'There were no pages that matched your search.'
	return html
	