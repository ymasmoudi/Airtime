#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

class AirTime:
    """ Main class managing the air time calculation in usec
    """
    def __init__(self, pd_len, sf):
        """ class constructor
        Args:
            pd_len : the payload length
            sf :  the spreading factor
        Returns: None
        Raise: None
        """
        self._len     	= int(pd_len)
        self._sf      	= int(sf)
        self._bw      	= 125000
        self._power   	= 0
        self._cr      	= 1     # coding rate from 1 to 4
        self._preamble  = 8     # lorawan preambule (8 symbols by default)
        self._fixlen 	= 0
        self._de     	= 0     # de = 1 if low data rate optimization is enabled 
        self._crcOn  	= 1

    def airtime(self):
		if self._sf < 7 or self._sf > 12:
			print("Wrong spanning factor")
			return 0.0

		self._de = (self._sf >= 11)
		symbol_duration = math.pow(2, self._sf) / self._bw

		a = float(8*self._len - 4*self._sf + 28 + 16*self._crcOn - 20*self._fixlen)
		b = float(4*(self._sf - 2*self._de))

		nbr_symbols = math.ceil(a/b) * (self._cr + 4)
		if nbr_symbols < 0:
			nbr_symbols = 0

		nbr_symbols += 8 											# Add preambule 
		preambule_duration = (self._preamble + 4.25) * symbol_duration
		payload_duration = nbr_symbols * symbol_duration 			# mutliply by symbol duration
		packet_duration = preambule_duration + payload_duration  	# add prem duration
		return packet_duration


if __name__ == "__main__":
	""" Main function
	"""
	import argparse
	import sys

	parser = argparse.ArgumentParser(
        prog="AirTime",
        description="LoRaWAN AirTime Calculator",
        epilog="(c) Youssef 2018"
	)

	parser.add_argument("-p", "--pd-len", help="Frame payload length", required=True)
	parser.add_argument("-s", "--sf", help="Frame spanning factor", required=True)

	try:
		options = parser.parse_args(sys.argv[1:])
		air = AirTime(options.pd_len, options.sf)
		print ('Payload Length={} SF={} AirTime={}'.format(options.pd_len, options.sf, air.airtime()))

	except Exception as e:
		print('Execution failed.  Exit')
		print(repr(e))
        sys.exit(1)

	sys.exit(0)

