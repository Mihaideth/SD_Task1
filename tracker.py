from datetime import datetime
from sets import Set
from pyactor.context import interval
from pyactor.context import set_context, create_host, sleep, shutdown
from peer import *
from random import sample




class Tracker(object):
	_tell = ['announce', 'comprovarPeers', 'init_start', 'infopeer', 'afegir_host']
	_ask = ['getPeers', 'getMidaTorrent']
	_ref = ['announce', 'getPeers', 'getTorrent', 'afegir_host']

	def __init__(self):
		self.tDictionary = {}

	def init_start(self):
		self.interval_check = interval(self.host, 1, self.proxy, 'comprovarPeers')

	def getMidaTorrent(self, idTorrent):
		mida = 0
		fitxer = open("fitxer.txt", "r")	#Aqui s'obriria el fitxer del torrent
		line=fitxer.readline()
		fitxer.close()
		mida = (len(line)-1)
		return mida

	def announce(self, idTorrent, refPeer):
		try:
			# printself.tracker.getPeers(idTorrent) "announce "+refPeer.getId()
			self.tDictionary[idTorrent][refPeer] = datetime.now()
		except:
			self.tDictionary[idTorrent] = {refPeer:datetime.now()}

	def getPeers(self, idTorrent):
		try:
			keys = self.tDictionary[idTorrent].keys()
			return sample(keys, 3)
		except Exception as e:
            		return []

	def comprovarPeers(self):
		tactual = datetime.now()
		for key, peerList in self.tDictionary.items():
			aux = {}
			for peer, t_peer in peerList.items():
				result=tactual-t_peer

				if result.total_seconds() <= 10:
					aux[peer] = t_peer
				else:
					print "eliminar "+peer

			self.tDictionary[key]=aux

	def infopeer(self):
		print "//////////////////////////////////"
		for x in self.tDictionary:
			print(x)
			for y in self.tDictionary[x]:
				#refPeer= self.host.lookup(y)
				print " -"+y.getId()+": "
				print y.getTorrent()
			print "//////////////////////////////////"
	
	def afegir_host(self, host):
		self.host = host

if __name__ == "__main__":
	set_context()
	h = create_host()
	p1 = h.spawn('peer1', Peer)
	p2 = h.spawn('peer2', Peer)
	p3 = h.spawn('peer3', Peer)
	p4 = h.spawn('peer4', Peer)
	p5 = h.spawn('peer5', Peer)
	seed = h.spawn('seed', Peer)
	t = h.spawn('tracker', Tracker)
	t.init_start()

	p1.afegir_host(h)
	p2.afegir_host(h)
	p3.afegir_host(h)
	p4.afegir_host(h)
	p5.afegir_host(h)
	seed.afegir_host(h)
	t.afegir_host(h)

	p1.afegir_tracker(t)
	p2.afegir_tracker(t)
	p3.afegir_tracker(t)
	p4.afegir_tracker(t)
	p5.afegir_tracker(t)
	seed.afegir_tracker(t)

	
	seed.make_seed()
	sleep(2)	
	
	p1.init_combinado("GOT")
	p2.init_combinado("GOT")
	p3.init_combinado("GOT")
	p4.init_combinado("GOT")
	p5.init_combinado("GOT")
	
	seed.init_combinado('GOT')
	



	for x in range(100):
		sleep(1)
		t.infopeer()
		

sleep(2)
shutdown()
