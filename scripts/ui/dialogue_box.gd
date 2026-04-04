extends CanvasLayer

# 뷰포트 320x180 기준 — 하단 50px 영역을 대화창으로 사용
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
	# 패널 클릭으로도 대화 진행 가능
	panel.gui_input.connect(_on_panel_input)

func _on_panel_input(event: InputEvent) -> void:
	if not DialogueManager.is_active:
		return
	if choices_container.visible:
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		DialogueManager.advance()
		get_viewport().set_input_as_handled()

func _unhandled_input(event: InputEvent) -> void:
	if not DialogueManager.is_active:
		return
	# Q키 — 뒤로 가기
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_Q:
			if DialogueManager.can_go_back():
				DialogueManager.go_back()
				get_viewport().set_input_as_handled()
			return
	# 선택지 표시 중에는 스페이스/엔터 입력 차단
	if choices_container.visible:
		return
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
	# 어떤 UI 요소도 포커스 갖지 않게 — 엔터키가 _unhandled_input에 도달하도록
	get_viewport().gui_release_focus()

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
	# 선택 즉시 모든 버튼을 scene tree에서 분리 (입력 가로채기 완전 차단)
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

func _clear_choices() -> void:
	for child in choices_container.get_children():
		choices_container.remove_child(child)
		child.queue_free()
