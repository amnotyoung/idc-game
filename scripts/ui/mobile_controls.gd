extends CanvasLayer

@onready var controls: Control = $Controls
@onready var dpad: Control = $Controls/DPad
@onready var up_btn: Button = $Controls/DPad/UpBtn
@onready var down_btn: Button = $Controls/DPad/DownBtn
@onready var left_btn: Button = $Controls/DPad/LeftBtn
@onready var right_btn: Button = $Controls/DPad/RightBtn
@onready var action_btn: Button = $Controls/ActionBtn
@onready var back_btn: Button = $Controls/BackBtn

var _pressed_dirs: Dictionary = {}

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_connect_direction_button(up_btn, Vector2.UP)
	_connect_direction_button(down_btn, Vector2.DOWN)
	_connect_direction_button(left_btn, Vector2.LEFT)
	_connect_direction_button(right_btn, Vector2.RIGHT)
	action_btn.pressed.connect(MobileInput.press_accept)
	back_btn.pressed.connect(MobileInput.press_back)
	LanguageManager.language_changed.connect(_on_language_changed)
	_refresh_static_texts()
	_sync_visibility()

func _process(_delta: float) -> void:
	_sync_visibility()

func _connect_direction_button(button: Button, direction: Vector2) -> void:
	button.button_down.connect(_set_direction_pressed.bind(direction, true))
	button.button_up.connect(_set_direction_pressed.bind(direction, false))

func _set_direction_pressed(direction: Vector2, pressed: bool) -> void:
	if pressed:
		_pressed_dirs[direction] = true
	else:
		_pressed_dirs.erase(direction)
	_update_move_vector()

func _update_move_vector() -> void:
	var movement := Vector2.ZERO
	for direction: Vector2 in _pressed_dirs.keys():
		movement += direction
	MobileInput.set_move_vector(movement.normalized())

func _sync_visibility() -> void:
	var should_show := _should_show_controls() and not _is_title_screen()
	controls.visible = should_show
	if not should_show:
		_pressed_dirs.clear()
		MobileInput.clear_move_vector()
		return

	var dialogue_active := DialogueManager.is_active
	dpad.visible = not dialogue_active
	if dialogue_active:
		_pressed_dirs.clear()
		MobileInput.clear_move_vector()

	action_btn.position = Vector2(264, 42) if dialogue_active else Vector2(264, 126)
	back_btn.visible = dialogue_active and DialogueManager.can_go_back()

func _should_show_controls() -> bool:
	return DisplayServer.is_touchscreen_available() \
		or OS.has_feature("android") \
		or OS.has_feature("ios") \
		or OS.has_feature("mobile") \
		or OS.has_feature("web_android") \
		or OS.has_feature("web_ios") \
		or OS.has_feature("web_mobile")

func _is_title_screen() -> bool:
	var current_scene := get_tree().current_scene
	if current_scene == null:
		return false
	return current_scene.scene_file_path == "res://scenes/ui/title_screen.tscn"

func _on_language_changed(_locale: String) -> void:
	_refresh_static_texts()

func _refresh_static_texts() -> void:
	back_btn.text = LanguageManager.text("dialogue_back_mobile")
