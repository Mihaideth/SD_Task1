from pyactor.context import interval, later
from random import choice
from random import randint


class Peer(object):
	_tell = ['notify', 'afegir_tracker', 'afegir_host', 'init_start', 'stop_interval', 'pushing', 'init_push', 'push', 'make_seed', 'init_pull', 'pulling', 'init_combinado', 'combinado']
	_ask = ['getId', 'getTorrent', 'pull']
	_ref = ['afegir_tracker', 'push', 'afegir_host', 'pull' ]

	def __init__(self):
		self.mida_torrent = 0
		self.data = {}
		self.falten = []

	def init_start(self, idTorrent):
		self.interval = interval(self.host, 3, self.proxy, 'notify', idTorrent)

	def stop_interval(self):
		self.interval.set()

	def make_seed(self):
		pos = 0
		fitxer = open("fitxer.txt", "r")
		line=fitxer.readline()
		for pos in (range(len(line)-1)):
			cont=line[pos]
			self.data[pos] = cont
		fitxer.close()	


	def init_push(self, idTorrent):
		self.interval = interval(self.host, 3, self.proxy, 'notify', idTorrent)
		self.interval_push = interval(self.host, 1, self.proxy, 'pushing', idTorrent)


	def init_pull(self, idTorrent):
		self.mida_torrent = self.tracker.getMidaTorrent(idTorrent)
		for i in range (0, self.mida_torrent):
			self.falten.append(i)
		
		self.interval = interval(self.host, 3, self.proxy, 'notify', idTorrent)
		self.interval_pull = interval(self.host, 1, self.proxy, 'pulling', idTorrent)

	def init_combinado(self, idTorrent):
		self.mida_torrent = self.tracker.getMidaTorrent(idTorrent)
		for i in range (0, self.mida_torrent):
			self.falten.append(i)
		
		self.interval = interval(self.host, 3, self.proxy, 'notify', idTorrent)
		self.interval_combinado = interval(self.host, 1, self.proxy, 'combinado', idTorrent)


	def getId(self):
		return self.id

	def notify(self, nomFitxer):
		self.tracker.announce(nomFitxer, self)

	def afegir_tracker(self, tracker):
		self.tracker = tracker

	def afegir_host(self, host):
		self.host = host

	def getTorrent(self):
		return len(self.data.keys())

	def push(self, chunk_id, chunk_data):
		#print "received", chunk_id, chunk_data
		#print self.data[chunk_id]
		if chunk_id not in self.data.keys():
			#print chunk_data
			self.data[chunk_id] = chunk_data

	def pushing(self, idTorrent):
		# print self.tracker.getPeers(idTorrent)
		for peer in self.tracker.getPeers(idTorrent):
			# print "push ", peer
			try:
				chunk=choice(self.data.items())
			except:
				#print "no tinc res per tant no puc enviar"
				continue
			peer.push(chunk[0], chunk[1])

	def pull(self, chunk_id):
		return self.data[chunk_id]


	def pulling(self, idTorrent):
		if (len(self.data.keys()) < self.mida_torrent):
			for peer in self.tracker.getPeers(idTorrent):
				chunk_id = choice(self.falten)
				try:
					self.data[chunk_id] = peer.pull(chunk_id)
					self.falten.pop(chunk_id)
					break
				except:
					break


	def combinado(self, idTorrent):
		
		for peer in self.tracker.getPeers(idTorrent):
			try:
				chunk=choice(self.data.items())
				peer.push(chunk[0], chunk[1])
			except:
				pass
			if (len(self.data.keys()) < self.mida_torrent):
				chunk_id = choice(self.falten)
				try:
					self.data[chunk_id] = peer.pull(chunk_id)
					self.falten.pop(chunk_id)
					break
				except:
					break
				
				

