#encoding:utf8
import requests
import json
class Iwan_baidu(object):
	__headers = {
		"Accept":"application/json, text/javascript, */*; q=0.01",
		"Accept-Encoding":"gzip, deflate, sdch",
		"Accept-Language":"en-US,en;q=0.8,zh;q=0.6",
		"Connection":"keep-alive",
		"Host":"iwan.baidu.com",
		"Referer":"http://iwan.baidu.com/singlegame?psquery=&dlfrom=6652108217_3_1769193129_&yeyouquery=%E7%88%B1%E7%8E%A9%E9%A6%96%E9%A1%B5&mobilebannerquery=%E6%89%8B%E6%9C%BA%E6%B8%B8%E6%88%8F&mobilequery=%E6%89%8B%E6%9C%BA%E6%B8%B8%E6%88%8F&wangyouquery=3d%E7%BD%91%E6%B8%B8&tn=&query=%E7%88%B1%E7%8E%A9%E9%A6%96%E9%A1%B5&pvid=1443667009166799825&qid=1443666167014245985&sid=0&zt=fc&from=fc&fenlei=&hcQuery=&isid=ui%3A2%26as%3A1%26bs%3A0%26ui_sample%3A2&pid=342&f=sug&time=2015-10-01+10%3A36%3A49&oq=%E7%88%B1%E7%8E%A9%E9%A6%96%E9%A1%B5&q=%E7%88%B1%E7%8E%A9%E9%A6%96%E9%A1%B5&psid=0&rqid=1443667009166799825&cookie=347BA07B3BB205AA05787E80EB49E5A3&baiduid=347BA07B3BB205AA05787E80EB49E5A3&fr=fc&fromtab=shouyou",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36",
		"X-Requested-With":"XMLHttpRequest",
	}
	__params = {
		"psquery":None,
		"dlfrom":"6652108217_3_1769193129_",
		"yeyouquery":"爱玩首页",
		"mobilebannerquery":"手机游戏",
		"mobilequery":"手机游戏",
		"wangyouquery":"3d网游",
		"tn":None,
		"query":"爱玩首页",
		"pvid":"1443667014431015671",
		"qid":"1443666167014245985",
		"sid":"0",
		"zt":"fc",
		"from":"fc",
		"fenlei":None,
		"hcQuery":None,
		"isid":"ui:2&as:1&bs:0&ui_sample:2",
		"pid":"342",
		"f":"sug",
		"time":"2015-10-01 10:36:54",
		"oq":"爱玩首页",
		"q":"爱玩首页",
		"psid":"0",
		"rqid":"1443667014431015671",
		"cookie":"347BA07B3BB205AA05787E80EB49E5A3",
		"baiduid":"347BA07B3BB205AA05787E80EB49E5A3",
		"fr":"fc",
		"passid":"1045908596",
		"bdstoken":"c45147dee729311ef5b5c3003946c48f",
		"action_from":"4",
		"gametype":"single",
		"page":"58",
		"type":"0",
	}
	__cookie = {
		"BAIDUID":"347BA07B3BB205AA05787E80EB49E5A3:FG=1",
		"PSTM":"1440946209",
		"BIDUPSID":"6174AF0F5F3A604EAE18C884F2AC0EC1",
		"BDUSS":"UNQVE9rcUxHR0p5ZlN4R2pUd0hEWFJUSGFPblZrNlJhR1F6NEk4eVRPQTRPQTlXQVFBQUFBJCQAAAAAAAAAAAEAAAB0TFc-wePWrrTMx-DWrsn5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADir51U4q-dVV",
		"H_PS_PSSID":"17160_17144_16716_1421_13477_12824_14431_10211_12868_17445_17246_17001_17004_17072_15861_17348_12136_17351_10633_17051",
		"BCLID":"9195523531121888363",
		"BDSFRCVID":"1FDsJeCCYuhF8Ec4B3_LMqCFvRDySYvT8cEd8qqdIz7iZBrtDwUPEG0PJM8g0bC-J3-_ogKK0gOTH65P",
		"H_BDCLCKID_SF":"tRAOoCtKJKvEfnjkq45HMt00qxby26nW2e3eaJ5nJDoAfloS0t-ML6tRbPcD3M5qam0LL66mQpP-HqTJKJbnXRKqbNOu3MrZ5CvtKl0MLP-5DMjxWf8V0TDZ0MnMBMPe52OnaIb8LIF5MI06jjtaePDO-frf54CXtbkX3b7Ef-QSOPO_bfbTWJLJQG74553Gt2ra24jn3tQCs-TbWJjxe-tkba7Db43AMJv0hqo-bpbbSfJHQT3myxrbbN3a3KrZt-jdWb3cWKJJ8UbSj6ome6b0DGuHJTKsbPo3WPT5KRu_Hn7zeU6cLntpbtbmX47aJCtL3KbPt56D8tjJQRD-BpFhbabn0UTG-GOj-Mb6W4blfRvmytbbblLkQN3T-nkO5bRa556SKML5Dn3oyT3JXp0njGoTqjtfJbkt_KDQKJbHjt3phCI5jICShUFsJx5R-2Q-5hOwbRnPbh5njMK5BUAIKtbl-qjRMG7kLf-yKh5fb-jlbMr0jPFlLl5J0nbPLgTxoUJFBCnJhboJqfC5qq4ebPRiJPb9Qg-q_xtLK-oj-D_xDjDa3e",
		"Hm_lvt_75bd2458f44f24f314dc1745f08b258a":"1443666064",
		"Hm_lpvt_75bd2458f44f24f314dc1745f08b258a":"1443667005",
 
}

	__base_url = "http://iwan.baidu.com/SinglegameAjax/getGameLibrary"
	def __init__(self):
		pass
	def get_games(self):
		for pg in range(1,61):
			self.__params['page'] = str(pg)
			r = requests.get(self.__base_url, cookies = self.__cookie, params = self.__params, headers = self.__headers)
			res = json.loads(r.content)
			names = [ ele['name'] for ele in res['game_library']['data']['list']]
			print r.url
			self.save(names)

	def save(self, names):
		with open("iwan_games.txt", "a") as f:
			for n in  names:
				f.write((n + "\n").encode("utf8"))




		pass

if __name__ == "__main__":
	handle = Iwan_baidu()
	handle.get_games()
