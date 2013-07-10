from pyquery import PyQuery as pyq
import sys
import urllib2
import json

class TaoBaoPricingSpider:
	searchUrl = "http://s.taobao.com/search?commend=all&search_type=item&style=list&q="
	cssPricingClass = ".col .price"
	cssTitleClass = ".summary a"
	cssItemClass = "div.row.item.icon-datalink"
	MAX_PAGES = 4000;

	def __init__(self, obj):
		self.url = self.searchUrl+obj;
		self.url = self.url.decode('utf-8').encode('utf-8')
		self.url = urllib2.unquote(self.url)
		self.data = []
		print "Fetching the Taobao started"

	def get_data(self):
		input_stream = urllib2.urlopen(self.url).read().decode("gbk","ignore")
		doc = pyq(input_stream)
		items = doc(self.cssItemClass)

		number = 0
		while len(items) > 0 and number < self.MAX_PAGES:
			print len(items)
			print "getting the page %d" %(number / 40 + 1)

			for item in items:
				taobaoTuple = {}
				taobaoTuple["price"] = pyq(item).find(self.cssPricingClass).text()
				taobaoTuple["title"] = pyq(item).find(self.cssTitleClass).attr('title')
				taobaoTuple["href"]  = pyq(item).find(self.cssTitleClass).attr('href')
				self.data.append(taobaoTuple)

			number += 40
			url_with_page = self.url+"&s="+str(number)
			input_stream = urllib2.urlopen(url_with_page).read().decode("gbk","ignore")
			doc = pyq(input_stream)
			items = doc(self.cssItemClass)

		print "Geting data done"


	def save_result_with_json(self):
		f = open("result.txt","aw")
		item_json = json.dumps(self.data,sort_keys=False, indent=4)
		f.write(item_json)
		f.close()

	def save_result_in_text(self):
		f= open("show.txt", "aw")
		for item in self.data:
			f.writelines(item["title"].encode("utf-8") + "=====>" + item["price"].encode("utf-8")+"\n")
		f.close;


item = sys.argv[1]
myTaobao = TaoBaoPricingSpider(item)
myTaobao.get_data()
myTaobao.save_result_in_text()