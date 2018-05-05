import requests
from pprint import pprint
import sqlite3
import time
from datetime import datetime
import logging
from multiprocessing import Pool
global database

global currency_list
currency_list = [ 'BTC', 'ETH', 'LTC', 'XRP',
	         'BCH', 'OMG',  'ZRX', 'GNT', 
	         'BAT', 'AE', 'TRX', 'XLM', 'NEO',
	         'GAS', 'XRB', 'NCASH', 'AION', 
	         'EOS', 'ONT', 'ZIL', 'IOST']


logger = logging.getLogger(__name__)

database = "cryptos.db"

koinex_url = 'https://koinex.in/api/ticker'
hitbtc_url = 'https://api.hitbtc.com/api/2/public/ticker/'
bitfinex_url = 'https://api.bitfinex.com/v1/pubticker/'

def prices( exchange):

	'''Return price dict of exchange, supported symbols (BTC, BCH, LTC, XRP, ETH)'''

	if exchange.lower() == 'hitbtc':
		'''
		HitBTC price getting API
		'''
		r = requests.get(hitbtc_url)
		response = r.json()

		global curr

		price_dic = {}
		for i in response:
			symbol = i['symbol']
			price = i['last']
			for curr in currency_list:
				if symbol == curr + 'USD':
					price_dic[curr] = float(price)

		prices_dic = {}
		for curr in currency_list:
			prices_dic[curr] = eval(curr + '_hitbtc')

		print (prices_dic)
		return prices_dic

	# elif exchange.lower() == 'bitfinex':
	# 	'''
	# 	BitFinex price getting API
	# 	'''
	# 	response = requests.get(bitfinex_url + 'btcusd').json()
	# 	BTC_bitfinex = float(response['last_price'])

	# 	response = requests.get(bitfinex_url + 'xrpusd').json()
	# 	XRP_bitfinex = float(response['last_price'])

	# 	response = requests.get(bitfinex_url + 'ethusd').json()
	# 	ETH_bitfinex = float(response['last_price'])

	# 	response = requests.get(bitfinex_url + 'bchusd').json()
	# 	BCH_bitfinex = float(response['last_price'])

	# 	response = requests.get(bitfinex_url + 'ltcusd').json()
	# 	LTC_bitfinex = float(response['last_price'])

	# 	return { 'BTC' : BTC_bitfinex, 'ETH' : ETH_bitfinex, 'BCH' : BCH_bitfinex, 'XRP' : XRP_bitfinex, 'LTC' : LTC_bitfinex}

	elif exchange.lower() == 'koinex':
		'''
		Koinex price getting API
		'''
		try:
			r = requests.get(koinex_url)
			response =  r.json()
		except Exception as e:
			print(e)
			print ('Most likely limited so try again after 15 minutes')


		prices = response['stats']['inr']
		prices_dic = {}
		for curr in currency_list:
			key = curr + '_koinex'
			key = float(prices[curr]['last_traded_price'])
			price_dic[curr] = 
		
		prices_dic = {}
		for curr in currency_list:
			prices_dic[curr] = eval(curr + '_koinex')

		return prices_dic



def arbritrage( exch1, curr1, exch2, curr2):

	'''Find arbitrage oppotunity between exchange 1 and exchange 2
		All exchanges have prices in USD only, only India gives in INR to
		hardcoding for it otherwise not needed
	'''

	prices1 = prices(exch1)
	prices2 = prices(exch2)

	if curr1 == 'INR':
		prices1 = prices(exch1)
		rate = 66.0
		for k,v in prices1.items():
			prices1[k] = v/rate

	elif curr2 == 'INR':
		prices2 = prices(exch2)
		rate = 66.0
		for k,v in prices2.items():
			prices2[k] = v/rate

	change = {}
	for i in curr:
		change[i] = (prices1[i] - prices2[i]) / prices2[i]

	price_dic = {}
	for i in curr:
		price_dic[i] = [(exch1, prices1[i]), (exch2, prices2[i]), round(change[i]*100)]

	return price_dic

def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Exception as e:
		print(e)
		return None

def create_table():

	create_table_sql ='''
	create table 
	if not exists arbitrage2 (
	BTC1 integer,
	BTC2 integer,
	ETH1 integer, 
	ETH2 integer,
	XRP1 integer, 
	XRP2 integer, 
	LTC1 integer,
	LTC2 integer,
	BCH1 integer,
	BCH2 integer,
	OMG1 integer,
	OMG2 integer,

	BTC integer, 
	ETH integer,
	XRP integer,
	LTC integer,
	BCH integer,
	OMG integer,

	time date,
	type char
	);
	'''
	global database

	conn = create_connection(database)
	if conn is not None:
		try:
			c = conn.cursor()
			c.execute(create_table_sql)
		except Exception as e:
			print(e)
	else:
		print('Error! database connection failed')	

def find_arbitage_opportunity( exch1, exch2):

	global database

	create_table()

	if exch1.lower() == 'koinex':
		curr = 'INR'
	else:
		curr = 'USD'

	while True:
		price_dic = arbritrage(exch1, curr,  exch2, 'USD')

		try:
			pprint(price_dic)
			conn = sqlite3.connect(database)
			c = conn.cursor()
			text = exch1 + ' vs ' + exch2
			c.execute("insert into arbitrage values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ( 
				price_dic['BTC'][0][1], price_dic['BTC'][1][1], 
				price_dic['ETH'][0][1], price_dic['ETH'][1][1],
				price_dic['XRP'][0][1], price_dic['XRP'][1][1],
				price_dic['LTC'][0][1], price_dic['LTC'][1][1],
				price_dic['BCH'][0][1], price_dic['BCH'][1][1],
				price_dic['OMG'][0][1], price_dic['OMG'][1][1],
				price_dic['BTC'][2], price_dic['ETH'][2], price_dic['XRP'][2], price_dic['LTC'][2], price_dic['BCH'][2], price_dic['OMG'][2],
				datetime.now(),
				text)
				)
			conn.commit()
			conn.close()
			time.sleep(900)
		except Exception as e:
			print (e)
			break

def main():
	print('running main program')
	find_arbitage_opportunity('koinex', 'hitbtc')


if __name__ == '__main__':
	main()





