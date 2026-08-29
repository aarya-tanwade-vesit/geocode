extends Node3D

##part 1
#var udp := PacketPeerUDP.new()
#
#func _ready():
	#udp.bind(9999)
	#print("Waiting for Python...")
#
#func _process(_delta):
	#if udp.get_available_packet_count() > 0:
		#var message = udp.get_packet().get_string_from_utf8()
		#print(message)

##part 2
#var udp := PacketPeerUDP.new()
#
#func _ready():
	#udp.bind(9999)
	#print("Waiting for Python...")
#
#func _process(_delta):
	#if udp.get_available_packet_count() > 0:
		#var message = udp.get_packet().get_string_from_utf8()
		#var number = int(message)
#
		#print("Received:", number)
		
		
##part 3


var udp := PacketPeerUDP.new()

func _ready():
	udp.bind(9999)
	print("Waiting for Python...")


func _process(_delta):
	if udp.get_available_packet_count() > 0:

		var message = udp.get_packet().get_string_from_utf8()

		var values = message.split(",")

		var x = int(values[0])
		var y = int(values[1])

		print("X:", x, " Y:", y)
