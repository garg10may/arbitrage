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
	REQ1 integer,
	REQ2 integer,
	ZRX1 integer,
	ZRX2 integer,
	GNT1 integer,
	GNT2 integer,
	BAT1 integer,
	BAT2 integer,
	AE1  integer,
	AE2  integer,
	TRX1 integer,
	TRX2 integer,
	XLM1 integer,
	XLM2 integer,
	NEO1 integer,
	NEO2 integer,
	GAS1 integer,
	GAS2 integer,
	XRB1 integer,
	XRB2 integer,
	NCASH1 integer,
	NCASH2 integer,
	AION1 integer
	AION2 integer,
	EOS1 integer,
	EOS2 integer,
	ONT1 integer,
	ONT2 integer,
	ZIL1 integer,
	ZIL2 integer,
	ZCO1 integer,
	ZCO2 integer,
	IOST1 integer, 
	IOST2 integer,

	BTC integer, 
	ETH integer,
	XRP integer,
	LTC integer,
	BCH integer,
	OMG integer,
	REQ integer,
	ZRX integer,
	GNT integer,
	BAT integer,
	AE  integer,
	TRX integer,
	XLM integer,
	NEO integer,
	GAS integer,
	XRB integer,
	NCASH integer,
	AION integer,
	EOS integer,
	ONT integer,
	ZIL integer,
	ZCO integer,
	IOST integer,

	time date,
	type char
	);
	'''