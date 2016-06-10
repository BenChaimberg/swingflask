from sqlalchemy import or_
from models import Products
import re


def products_search(search_string):
    search_string = search_string.lower()
    search_items = []
    found_index = -1
    html = ''
    found_sites = []
    multiple_products = []
    while True:
        try_index = found_index+1
        found_index = search_string.find(' ', try_index)
        if not found_index < 0:
            search_items.append(search_string[:found_index])
            search_string = search_string[found_index:]
        else:
            search_items.append(search_string)
            break
    for search_item in search_items:
        multiple_products += Products.query.filter(or_(
            Products.text.like('%'+search_item+'%'),
            Products.title.like('%'+search_item+'%'),
            Products.directions.like('%'+search_item+'%')
        )).all()
    products = set(multiple_products)
    for product in products:
        print product.id
    for product in products:
        product.text = re.sub(r'<[^>]*>', r'', product.text)
        product.directions = re.sub(r'<[^>]*>', r'', product.directions)
    for product in products:
        found_site = [product, []]
        found_sites.append(found_site)
        for search_item in search_items:
            found_index = -1
            while True:
                try_index = found_index+1
                found_index = product.text.lower().find(
                    search_item,
                    try_index
                )
                if not found_index < 0:
                    space_index = len(product.text)-found_index
                    space_index2 = found_index
                    for i in range(0, 3):
                        space_index = product.text[::-1].find(
                            ' ',
                            space_index+1
                        )
                    if space_index < 0:
                        space_index = len(product.text)
                    for i in range(0, 4):
                        if product.text.find(' ', space_index2+1) > 0:
                            space_index2 = product.text.find(
                                ' ',
                                space_index2+1
                            )
                    found_sites[-1][1].append(
                        product.text[
                            len(product.text)-space_index:
                            found_index
                        ]+'<b>'+product.text[
                            found_index:
                            found_index+len(search_item)
                        ]+'</b>'+product.text[
                            found_index+len(search_item):
                            space_index2
                        ]
                    )
                else:
                    break
            found_index = -1
            while True:
                try_index = found_index+1
                found_index = product.directions.lower().find(
                    search_item,
                    try_index
                )
                if not found_index < 0:
                    space_index = len(product.directions)-found_index
                    space_index2 = found_index
                    for i in range(0, 3):
                        space_index = product.directions[::-1].find(
                            ' ',
                            space_index+1
                        )
                        if space_index < 0:
                            space_index = len(product.directions)
                            break
                    for i in range(0, 4):
                        if product.directions.find(
                            ' ',
                            space_index2+1
                        ) > 0:
                            space_index2 = product.directions.find(
                                ' ',
                                space_index2+1
                            )
                    found_sites[-1][1].append(
                        product.directions[
                            len(product.directions)-space_index:
                            found_index
                        ]+'<b>'+product.directions[
                            found_index:
                            found_index+len(search_item)
                        ]+'</b>'+product.directions[
                            found_index+len(search_item):
                            space_index2
                        ]
                    )
                else:
                    break
        found_sites[-1][1].sort()
        if found_sites[-1][1] == []:
            found_sites.pop()
    try:
        found_sorted = [found_sites.pop()]
    except IndexError:
        return 'There were no pages that matched your search.'
    else:
        for found_site in found_sites:
            for sorted in found_sorted:
                if len(sorted[1]) < len(found_site[1]):
                    found_sorted.insert(found_sorted.index(sorted), found_site)
                    break
                if found_sorted.index(sorted) == len(found_sorted) - 1:
                    found_sorted.append(found_site)
                    break
        html += '<ul>'
        for final in found_sorted:
            final_title = re.sub(r'<[^>]*>', r' ', final[0].title)
            html += '<li><h2><a href="/product/' + \
                str(final[0].id) + \
                '">' + \
                final_title + \
                '</a></h2>'
            for text in final[1]:
                html += text + '&hellip;'
            html += '</li>'
        html += '</ul>'
        return html
