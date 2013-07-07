from pyquery import PyQuery as pyq
import sys
import urllib2
import urllib

class TaoBaoPricingSpider:
	searchUrl = "http://s.taobao.com/search?commend=all&search_type=item&style=list&q="
	cssPricingClass = ".col .price"
	cssTitleClass = ".summary a"
	cssItemClass = "div.row.item.icon-datalink"
	cssPageCount = "div span.b"

	def __init__(self, obj):
		self.url = self.searchUrl+obj;
		self.data = []
		print "Fetching the Taobao started"

	def get_data(self):
		input_stream = urllib2.urlopen(self.url).read().decode("gbk")
		doc = pyq(input_stream)
		items = doc(self.cssItemClass)

		page_count = doc(self.cssPageCount)
		print page_count

		number = 0
		while len(items) > 0 and number < 4000:
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
			input_stream = urllib2.urlopen(url_with_page).read().decode("gbk")
			doc = pyq(input_stream)
			items = doc(self.cssItemClass)

		print "Geting data done"


	def printResult(self):
		f = open("result.txt","aw+")
		for item in self.data:
			f.writelines(item["title"].encode('utf-8','replace') + "----------------->" + item["price"].encode('utf-8','replace')+"\n")

		f.close()

item = sys.argv[1]
myTaobao = TaoBaoPricingSpider(item)
myTaobao.get_data()
myTaobao.printResult()