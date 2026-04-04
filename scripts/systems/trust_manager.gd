extends Node

signal trust_changed(npc_id: String, new_value: int)

## 챕터/이벤트 진행 플래그
var _flags: Dictionary = {}

func set_flag(key: String) -> void:
	_flags[key] = true

func has_flag(key: String) -> bool:
	return _flags.get(key, false)

const TRUE_ENDING_THRESHOLD = 70
const NORMAL_ENDING_THRESHOLD = 50

var _trust: Dictionary = {
	"timoci":     0,
	"ratu_josefa": 0,
	"mere":       0,
	"james":      0,
	"lani":       0,
	"wati":       0,
}

func modify(npc_id: String, amount: int) -> void:
	if not _trust.has(npc_id):
		push_error("Unknown NPC id: " + npc_id)
		return
	_trust[npc_id] = clampi(_trust[npc_id] + amount, 0, 100)
	emit_signal("trust_changed", npc_id, _trust[npc_id])

func get_trust(npc_id: String) -> int:
	return _trust.get(npc_id, 0)

func get_all() -> Dictionary:
	return _trust.duplicate()

const SAVE_PATH = "user://save.json"

func save_game() -> void:
	var data = {"flags": _flags, "trust": _trust}
	var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(data))

func load_game() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var file = FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not file:
		return
	var json = JSON.new()
	if json.parse(file.get_as_text()) == OK:
		var data = json.get_data()
		_flags = data.get("flags", {})
		for k in data.get("trust", {}):
			if _trust.has(k):
				_trust[k] = int(data["trust"][k])

func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)

func check_ending() -> String:
	var above_threshold = 0
	for npc_id in _trust:
		if _trust[npc_id] >= TRUE_ENDING_THRESHOLD:
			above_threshold += 1
	if above_threshold == _trust.size():
		return "true"
	elif above_threshold >= 3:
		return "normal"
	else:
		return "bad"
