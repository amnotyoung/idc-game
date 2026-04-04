extends Node

signal dialogue_started
signal dialogue_line_changed(line: Dictionary)
signal dialogue_choices_presented(choices: Array)
signal dialogue_ended(dialogue_id: String)

var dialogues: Dictionary = {}
var current_dialogue: Dictionary = {}
var current_dialogue_id: String = ""
var current_line_index: int = 0
var is_active: bool = false
var _visible_choices: Array = []

const DIALOGUE_FILES = [
	"res://data/dialogues/chapter1.json",
	"res://data/dialogues/street_npcs.json",
	"res://data/dialogues/chapter2.json",
	"res://data/dialogues/chapter3.json",
	"res://data/dialogues/chapter4.json"
]

func _ready() -> void:
	_load_dialogues()

func _load_dialogues() -> void:
	for path in DIALOGUE_FILES:
		var file = FileAccess.open(path, FileAccess.READ)
		if not file:
			push_error("Dialogue file not found: " + path)
			continue
		var json = JSON.new()
		var err = json.parse(file.get_as_text())
		if err != OK:
			push_error("Failed to parse dialogue: " + path)
			continue
		dialogues.merge(json.get_data())

func start(dialogue_id: String) -> void:
	if not dialogues.has(dialogue_id):
		push_error("Dialogue not found: " + dialogue_id)
		return
	current_dialogue = dialogues[dialogue_id]
	current_dialogue_id = dialogue_id
	current_line_index = 0
	is_active = true
	emit_signal("dialogue_started")
	_show_current_line()

func _show_current_line() -> void:
	var lines: Array = current_dialogue.get("lines", [])
	if current_line_index >= lines.size():
		# 모든 라인 끝 — 선택지 또는 종료
		var choices: Array = current_dialogue.get("choices", [])
		if choices.size() > 0:
			# condition 필드 있는 선택지는 해당 플래그 있을 때만 표시
			_visible_choices = []
			for c in choices:
				var cond: String = c.get("condition", "")
				if cond == "" or TrustManager.has_flag(cond):
					_visible_choices.append(c)
			emit_signal("dialogue_choices_presented", _visible_choices)
		else:
			end()
		return
	emit_signal("dialogue_line_changed", lines[current_line_index])

func advance() -> void:
	if not is_active:
		return
	current_line_index += 1
	_show_current_line()

func choose(choice_index: int) -> void:
	# visible_choices 기준으로 인덱싱 (condition 필터 적용된 배열)
	if choice_index >= _visible_choices.size():
		return
	var choice = _visible_choices[choice_index]
	# 신뢰도 효과 적용
	var effects: Dictionary = choice.get("effects", {})
	for npc_id in effects:
		TrustManager.modify(npc_id, effects[npc_id])
	# 다음 대화로 이동
	var next_id: String = choice.get("next", "")
	end()
	if next_id != "":
		start(next_id)

func end() -> void:
	is_active = false
	var ended_id := current_dialogue_id
	current_dialogue = {}
	current_dialogue_id = ""
	current_line_index = 0
	_visible_choices = []
	emit_signal("dialogue_ended", ended_id)
