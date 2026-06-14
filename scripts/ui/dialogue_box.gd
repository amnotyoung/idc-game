extends CanvasLayer

const BOX_HEIGHT = 50

@onready var panel: Panel               = $Panel
@onready var speaker_label: Label       = $Panel/VBox/SpeakerLabel
@onready var text_label: Label          = $Panel/VBox/TextLabel
@onready var choices_container: VBoxContainer = $Panel/VBox/ChoicesContainer
@onready var back_btn: Button           = $Panel/BackBtn

func _ready() -> void:
	DialogueManager.dialogue_started.connect(_on_dialogue_started)
	DialogueManager.dialogue_line_changed.connect(_on_line_changed)
	DialogueManager.dialogue_choices_presented.connect(_on_choices_presented)
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)
	panel.visible = false
	back_btn.pressed.connect(_on_back_pressed)
	MobileInput.accept_pressed.connect(_on_mobile_accept_pressed)
	MobileInput.back_pressed.connect(_on_mobile_back_pressed)

## _input — GUI보다 먼저 키 입력을 잡음 (엔터키 누락 방지)
func _input(event: InputEvent) -> void:
	if not DialogueManager.is_active:
		return
	if not panel.visible:
		return

	# Q키 — 뒤로 가기
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_Q:
			if DialogueManager.can_go_back():
				DialogueManager.go_back()
			get_viewport().set_input_as_handled()
			return

	# 선택지 표시 중
	if choices_container.visible and choices_container.get_child_count() > 0:
		# 엔터/스페이스 → 포커스된 버튼 직접 클릭
		if event.is_action_pressed("ui_accept"):
			var focused = get_viewport().gui_get_focus_owner()
			if focused is Button and focused.get_parent() == choices_container:
				focused.emit_signal("pressed")
				get_viewport().set_input_as_handled()
		# 방향키 → 포커스 이동 (Godot 기본 동작에 맡김)
		return

	# 엔터/스페이스 — 대화 진행
	if event.is_action_pressed("ui_accept"):
		DialogueManager.advance()
		get_viewport().set_input_as_handled()

func _on_dialogue_started() -> void:
	panel.visible = true
	choices_container.visible = false
	_clear_choices()
	back_btn.visible = false

func _on_line_changed(line: Dictionary) -> void:
	choices_container.visible = false
	_clear_choices()
	speaker_label.text = line.get("speaker", "")
	text_label.text    = line.get("text", "")
	back_btn.visible   = DialogueManager.can_go_back()

func _on_choices_presented(choices: Array) -> void:
	_clear_choices()
	for i in choices.size():
		var btn := Button.new()
		btn.text = choices[i].get("text", "")
		btn.add_theme_font_size_override("font_size", 7)
		btn.custom_minimum_size = Vector2(0, 14)
		btn.focus_mode = Control.FOCUS_ALL
		btn.pressed.connect(_on_choice_selected.bind(i))
		choices_container.add_child(btn)
	choices_container.visible = true
	back_btn.visible = DialogueManager.can_go_back()
	await get_tree().process_frame
	if choices_container.get_child_count() > 0:
		choices_container.get_child(0).grab_focus()

func _on_choice_selected(index: int) -> void:
	_clear_choices()
	choices_container.visible = false
	DialogueManager.choose(index)

func _on_dialogue_ended(_dialogue_id: String) -> void:
	panel.visible = false
	_clear_choices()
	back_btn.visible = false

func _on_back_pressed() -> void:
	if DialogueManager.can_go_back():
		DialogueManager.go_back()

func _on_mobile_accept_pressed() -> void:
	if not DialogueManager.is_active:
		return
	if not panel.visible:
		return
	if choices_container.visible and choices_container.get_child_count() > 0:
		return
	DialogueManager.advance()

func _on_mobile_back_pressed() -> void:
	if DialogueManager.is_active and DialogueManager.can_go_back():
		DialogueManager.go_back()

## 마우스/터치 클릭으로 대화 진행 — _unhandled_input 이라 '이전' 같은 버튼이
## 먼저 클릭을 소비하면 여기엔 오지 않음 (버튼 클릭이 advance 로 새는 것 방지)
func _unhandled_input(event: InputEvent) -> void:
	if not DialogueManager.is_active or not panel.visible:
		return
	# 선택지 표시 중엔 선택지 버튼이 처리 (여기서 진행 안 함)
	if choices_container.visible and choices_container.get_child_count() > 0:
		return
	if (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT) \
			or (event is InputEventScreenTouch and event.pressed):
		DialogueManager.advance()
		get_viewport().set_input_as_handled()

func _clear_choices() -> void:
	for child in choices_container.get_children():
		choices_container.remove_child(child)
		child.queue_free()
