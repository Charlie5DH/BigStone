#!/usr/bin/env python
"""
Signal
"""

import signal, os, time

class DBASignalHandlers():
	def __init__(self, fn_cbk_app, user_signal):
		#user_signal = signal.SIGUSR1
		self.fn_cbk_app = fn_cbk_app

		signal.signal(user_signal, self.__receive_signal)

	def __receive_signal(self, signum, stack):
		print 'Received signal:', signum
		self.fn_cbk_app("SIGNAL%d" % signum)



if __name__ == '__main__':
	print 'My PID is:', os.getpid()

	while True:
		print 'Waiting...'
		time.sleep(3)
