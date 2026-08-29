#extends Node3D
#
#@onready var tilt = $pivot/Pan/Tilt
#
#var pan_speed := 1.5
#var tilt_speed := 1.5
#
#func _process(delta):
	#
	## PAN
	#if Input.is_key_pressed(KEY_A):
		#rotate_y(pan_speed * delta)
#
	#if Input.is_key_pressed(KEY_D):
		#rotate_y(-pan_speed * delta)
#
	## TILT
	#if Input.is_key_pressed(KEY_W):
		#tilt.rotate_x(tilt_speed * delta)
#
	#if Input.is_key_pressed(KEY_S):
		#tilt.rotate_x(-tilt_speed * delta)
		
extends Node3D

@onready var pan_node = $pivot/Pan
@onready var tilt_node = $pivot/Pan/Tilt
@onready var camera = $pivot/Pan/Tilt/Camera3D

var udp := PacketPeerUDP.new()

var pan_speed := 1.5
var tilt_speed := 1.5

@onready var target = $"../TargetBeacon"

func _ready() -> void:
	udp.bind(4242)

func _process(delta: float) -> void:

	# Send target screen position
	var screen_pos = camera.unproject_position(target.global_position)

	var message = "%f,%f" % [screen_pos.x, screen_pos.y]

	udp.set_dest_address("127.0.0.1", 5000)
	udp.put_packet(message.to_utf8_buffer())

	# Receive pan/tilt from Python
	if udp.get_available_packet_count() > 0:
		var data = udp.get_packet().get_string_from_utf8()
		var values = data.split(",")

		if values.size() == 2:
			var pan = float(values[0])
			var tilt_amount = float(values[1])

			pan_node.rotate_y(-pan * delta)
			tilt_node.rotate_x(-tilt_amount * delta)
