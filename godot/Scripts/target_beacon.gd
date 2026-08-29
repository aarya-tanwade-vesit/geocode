extends CSGCombiner3D

var init_pos: Vector3
var movement_mode := ""

func _ready() -> void:
	init_pos = global_position

func _process(delta: float) -> void:

	if Input.is_action_just_pressed("circular"):
		movement_mode = "circular"

	if Input.is_action_just_pressed("linear"):
		movement_mode = "linear"

	if movement_mode == "circular":
		circular_motion()

	elif movement_mode == "linear":
		linear_motion()


func circular_motion() -> void:
	var t = Time.get_ticks_msec() / 1000.0
	
	global_position.x = init_pos.x + sin(t) * 5.0
	global_position.y = init_pos.y + cos(t) * 5.0


func linear_motion() -> void:
	var t = Time.get_ticks_msec() / 1000.0
	
	position.y = sin(t) * 5.0
