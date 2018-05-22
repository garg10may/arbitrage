import requests
from pprint import pprint
import sqlite3
import time
from datetime import datetime
import logging
global database
from sqlQuery import create_table_sql

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


global currency_list
currency_list = [ 'BTC', 'ETH', 'LTC', 
	         'BCH', 'OMG',  'ZRX', 'GNT', 
	         'TRX', 'XLM', 'NEO',
	          'EOS', 'ONT', 'XRP']

database = "cryptos2.db"

koinex_url = 'https://koinex.in/api/ticker'
hitbtc_url = 'https://api.hitbtc.com/api/2/public/ticker/'
bitfinex_url = 'https://api.bitfinex.com/v1/pubticker/'

def prices( exchange):

	'''Return price dict of exchange, supported symbols (BTC, BCH, LTC, XRP, ETH)'''

	if exchange.lower() == 'hitbtc':
		'''
		HitBTC price getting API
		'''

		logger.info("Getting hitbtc prices")
		r = requests.get(hitbtc_url)
		response = r.json()

		prices_dic = {}
		for i in response:
			symbol = i['symbol']
			price = i['last']
			for curr in currency_list:
				if symbol == curr + 'USD':
					prices_dic[curr] = float(price)
				elif symbol == curr + 'USDT':
					prices_dic[curr] = float(price)

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

		logger.info("Getting koinex prices")
		try:
			r = requests.get(koinex_url)
			response =  r.json()
		except Exception as e:
			logger.exception(e)
			logger.info('Most likely limited so try again after 15 minutes')


		prices = response['stats']['inr']
		prices_dic = {}
		for curr in currency_list:
			prices_dic[curr] = float(prices[curr]['last_traded_price'])

		return prices_dic



def arbritrage( exch1, curr1, exch2, curr2):

	'''Find arbitrage oppotunity between exchange 1 and exchange 2
		All exchanges have prices in USD only, only India gives in INR to
		hardcoding for it otherwise not needed
	'''
	prices1 = prices(exch1)
	prices2 = prices(exch2)

	rate = 66.0

	if curr1 == 'INR':
		for k,v in prices1.items():
			prices1[k] = v/rate

	elif curr2 == 'INR':
		for k,v in prices2.items():
			prices2[k] = v/rate

	change = {}
	for i in currency_list:
		change[i] = (  prices1[i] - prices2[i]  )   /   prices2[i]

	price_dic = {}
	for i in currency_list:
		price_dic[i] = [(exch1, round(prices1[i]),2), (exch2, round(prices2[i]),2), round(change[i]*100)]

	return price_dic

def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Exception as e:
		logger.exception(e)
		return None

def create_table():

	global database

	conn = create_connection(database)
	if conn is not None:
		try:
			c = conn.cursor()
			c.execute(create_table_sql)
			logger.info("Created table in databse %s"%database)
		except Exception as e:
			logger.exception(e)
	else:
		logger.info('Error! database connection failed')	

def find_arbitage_opportunity( exch1, exch2):

	global database

	create_table()

	if exch1.lower() == 'koinex':
		curr = 'INR'
	else:
		curr = 'USD'

	while True:
		price_dic = arbritrage(exch1, curr,  exch2, 'USD')
		pprint(price_dic)

		try:
			conn = sqlite3.connect(database)
			c = conn.cursor()
			text = exch1 + ' vs ' + exch2
			c.execute("insert into arbitrage5 values \
				(\
			     ?,?,?,?,?,?,?,?,?,?,\
				 ?,?,?,?,?,?,?,?,?,?,\
				 ?,?,?,?,?,?,?,?,?,?,\
				 ?,?,?,?,?,?,?,?,?,?,\
				 ?\
				 )",

				( 
				price_dic['BTC'][0][1], price_dic['BTC'][1][1], 
				price_dic['ETH'][0][1], price_dic['ETH'][1][1],
				price_dic['XRP'][0][1], price_dic['XRP'][1][1],
				price_dic['LTC'][0][1], price_dic['LTC'][1][1],
				price_dic['BCH'][0][1], price_dic['BCH'][1][1],
				price_dic['OMG'][0][1], price_dic['OMG'][1][1],
				price_dic['ZRX'][0][1], price_dic['ZRX'][0][1],
				price_dic['GNT'][0][1], price_dic['GNT'][0][1],
				price_dic['TRX'][0][1], price_dic['TRX'][0][1],
				price_dic['XLM'][0][1], price_dic['XLM'][0][1],
				price_dic['NEO'][0][1], price_dic['NEO'][0][1],
				price_dic['EOS'][0][1], price_dic['EOS'][0][1],
				price_dic['ONT'][0][1], price_dic['ONT'][0][1],

				price_dic['BTC'][2],
				price_dic['ETH'][2],
				price_dic['XRP'][2],
				price_dic['LTC'][2],
				price_dic['BCH'][2],
				price_dic['OMG'][2],
				price_dic['ZRX'][2],
				price_dic['GNT'][2],
				price_dic['TRX'][2],
				price_dic['XLM'][2],
				price_dic['NEO'][2],
				price_dic['EOS'][2],
				price_dic['ONT'][2],
				datetime.now(),
				text
				)
				
				)

			conn.commit()
			conn.close()
			time.sleep(60*60) #note every hour
		except Exception as e:
			logger.exception(e)
			break


logger.info('running main program')
find_arbitage_opportunity('koinex', 'hitbtc')






