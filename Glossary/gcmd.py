#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/4/25 20:46

# gcmd concepts rdf
from pyquery import PyQuery as pq
import urllib.request as rq

url = 'https://gcmdservices.gsfc.nasa.gov/static/kms/concept/'


def rdf_url(baseurl):
	urls = []
	doc = pq(url=baseurl)
	trs = doc("table>tr").items()
	for tr in trs:
		href = tr("td>a[href]").text()
		if str(href).endswith(".rdf"):
			urls.append(href)  # full url
	return urls


def download_rdfs(durls):
	for d_url in durls:
		rq.urlretrieve(url + d_url, "H:\OntoBase\egc-onto\domain\gcmd\concepts\\" + d_url)
		print('download')


import os

if __name__ == '__main__':
	# print(rdf_url(url))
	rdfurls = rdf_url(url)
	if not os.path.exists('list.txt'):
		with open("list.txt", 'w') as f:
			l_durls = [url + durl + '\n' for durl in rdfurls]
			f.write(''.join(l_durls))
	download_rdfs(rdfurls)
# print(pq('https://gcmdservices.gsfc.nasa.gov/static/kms/concept/'))
