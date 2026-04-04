extends CanvasLayer

# 뷰포트 320x180 기준 — 하단 50px 영역을 대화창으로 사용
const BOX_HEIGHT = 50

@onready var panel: Panel           = $Panel
@onready var speaker_label: Label   = $Panel/VBox/SpeakerLabel
@onready var text_label: Label      = $Panel/VBox/TextLabel
@onready var choices_container: VBoxContainer = $Panel/VBox/ChoicesContainer

func _ready() -> void:
	DialogueManager.dialogue_started.connect(_on_dialogue_started)
	DialogueManager.dialogue_line_changed.connect(_on_line_changed)
	DialogueManager.dialogue_choices_presented.connect(_on_choices_presented)
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)
	panel.visible = false

func _unhandled_input(event: InputEvent) -> void:
	if not DialogueManager.is_active:
		return
	if choices_container.visible:
		return
	if event.is_action_pressed("ui_accept"):
		DialogueManager.advance()
		get_viewport().set_input_as_handled()

func _on_dialogue_started() -> void:
	panel.visible = true
	choices_container.visible = false
	_clear_choices()

func _on_line_changed(line: Dictionary) -> void:
	choices_container.visible = false
	_clear_choices()
	speaker_label.text = line.get("speaker", "")
	text_label.text    = line.get("text", "")

func _on_choices_presented(choices: Array) -> void:
	_clear_choices()
	for i in choices.size():
		var btn := Button.new()
		btn.text = choices[i].get("text", "")
		btn.add_theme_font_size_override("font_size", 7)
		btn.custom_minimum_size = Vector2(0, 14)
		btn.focus_mode = Control.FOCUS_ALL   # 키보드 포커스 허용
		btn.pressed.connect(func(): DialogueManager.choose(i))
		choices_container.add_child(btn)
	choices_container.visible = true
	# 첫 번째 버튼에 포커스 — 방향키/엔터로 선택 가능
	await get_tree().process_frame
	if choices_container.get_child_count() > 0:
		choices_container.get_child(0).grab_focus()

func _on_dialogue_ended(_dialogue_id: String) -> void:
	panel.visible = false
	_clear_choices()

func _clear_choices() -> void:
	for child in choices_container.get_children():
		child.queue_free()
