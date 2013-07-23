from pyquery import PyQuery as pyq
import urllib2
import json
import time

class SpirderParser:
	def __init__(self):
		pass

	#config the Rule for the json file
	def get_task_data(self, filename):
		files = open(filename)
		task_data = {}
		task_data = json.load(files)

		assert task_data, "The task_data is empty"

		self.task_data = dict(task_data)

	def run(self):
		self.__run()

	def __run(self):

		#get the Rules
		self.url = self.task_data['url']
		self.itemRule = self.task_data['item']
		self.priceRule = self.task_data['price']
		self.titleRule = self.task_data['title']
		self.linkRule = self.task_data['link']
		self.outfile = self.task_data['outfile']

		#get the Data from the url
		webStream = urllib2.urlopen(self.url).read()
		domDocument = pyq(webStream.decode('gbk',"ignore"))
		items = domDocument(str(self.itemRule))

		self.data = []

		number = 0
		for item in items:
			itemDic = {}
			itemDic['price'] = pyq(item).find(self.priceRule).text()
			itemDic['title'] = pyq(item).find(self.titleRule).text()
			itemDic['link']  = pyq(item).find(self.linkRule).attr('href')
			self.data.append(itemDic)

	def save_result_in_text(self):
		f= open(self.outfile+".txt", "w")
		for item in self.data:
			f.writelines(item["title"].encode("utf-8") + "=====>" + item["price"].encode("utf-8")+"\n")
		f.close;