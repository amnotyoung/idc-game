extends Node

@onready var bg: Sprite2D = get_parent().get_node("Background")
@onready var bgm: AudioStreamPlayer = get_parent().get_node("BGM")
@onready var attendees: Node2D = get_parent().get_node("Attendees")

const OFFICE_BG = preload("res://assets/sprites/tilesets/office_bg.png")
const ISLAND_BG = preload("res://assets/sprites/tilesets/naitamba_bg.png")

var _ending_type: String = ""

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)

	_ending_type = TrustManager.check_ending()
	TrustManager.set_flag("ch5_started")

	# 회의 시작
	DialogueManager.start("ch5_meeting_start")

func _on_dialogue_ended(dialogue_id: String) -> void:
	match dialogue_id:
		"ch5_meeting_start":
			DialogueManager.start("ch5_mere_report")
		"ch5_mere_report":
			await get_tree().create_timer(0.6).timeout
			_start_timoci()
		"ch5_timoci_response_good", "ch5_timoci_response_neutral", "ch5_timoci_response_bad":
			await get_tree().create_timer(0.6).timeout
			_start_james()
		"ch5_james_response_good", "ch5_james_response_neutral", "ch5_james_response_bad":
			await get_tree().create_timer(0.6).timeout
			_start_sela()
		"ch5_sela_response", "ch5_sela_response_no_sign":
			DialogueManager.start("ch5_final_choice")
		"ch5_resolve":
			_show_ending()
		"ch5_ending_true", "ch5_ending_normal", "ch5_ending_bad":
			await get_tree().create_timer(2.5).timeout
			_show_report_card()
		"ch5_report":
			await get_tree().create_timer(1.0).timeout
			DialogueManager.start("ch5_credits")
		"ch5_credits":
			TrustManager.set_flag("game_complete")
			TrustManager.save_game()
			await get_tree().create_timer(2.0).timeout
			SceneManager.go_to("res://scenes/ui/title_screen.tscn")

func _start_timoci() -> void:
	var trust = TrustManager.get_trust("timoci")
	if trust >= TrustManager.TRUE_ENDING_THRESHOLD:
		DialogueManager.start("ch5_timoci_response_good")
	elif trust >= TrustManager.NORMAL_ENDING_THRESHOLD:
		DialogueManager.start("ch5_timoci_response_neutral")
	else:
		DialogueManager.start("ch5_timoci_response_bad")

func _start_james() -> void:
	var trust = TrustManager.get_trust("james")
	if trust >= TrustManager.TRUE_ENDING_THRESHOLD:
		DialogueManager.start("ch5_james_response_good")
	elif trust >= TrustManager.NORMAL_ENDING_THRESHOLD:
		DialogueManager.start("ch5_james_response_neutral")
	else:
		DialogueManager.start("ch5_james_response_bad")

func _start_sela() -> void:
	if TrustManager.has_flag("ch3_good_ending"):
		DialogueManager.start("ch5_sela_response")
	else:
		DialogueManager.start("ch5_sela_response_no_sign")

func _show_ending() -> void:
	# BGM 페이드아웃 + 배경 페이드아웃 동시
	var tween = get_tree().create_tween()
	tween.set_parallel(true)
	tween.tween_property(bg, "modulate:a", 0.0, 1.2)
	tween.tween_property(bgm, "volume_db", -40.0, 1.2)
	await tween.finished

	# 잠깐의 암전
	await get_tree().create_timer(1.5).timeout

	match _ending_type:
		"true":
			bg.texture = ISLAND_BG
		"normal":
			bg.texture = ISLAND_BG
		"bad":
			bg.texture = OFFICE_BG

	# 배경 천천히 페이드인 (BGM은 꺼진 상태 유지 — 고요한 엔딩)
	tween = get_tree().create_tween()
	tween.tween_property(bg, "modulate:a", 1.0, 1.5)
	await tween.finished

	await get_tree().create_timer(1.0).timeout

	match _ending_type:
		"true":
			DialogueManager.start("ch5_ending_true")
		"normal":
			DialogueManager.start("ch5_ending_normal")
		"bad":
			DialogueManager.start("ch5_ending_bad")

func _trust_bar(value: int) -> String:
	var filled = int(value / 10)
	var empty = 10 - filled
	return "█".repeat(filled) + "░".repeat(empty) + " %d" % value

func _show_report_card() -> void:
	# 런타임에 대화 데이터 주입
	var names = {
		"mere": "Mere",
		"timoci": "Timoci",
		"ratu_josefa": "Ratu Josefa",
		"lani": "Lani",
		"james": "James"
	}
	var lines: Array = [
		{"speaker": "", "text": "— 관계 성적표 —"}
	]
	for npc_id in TrustManager.ENDING_NPCS:
		var trust = TrustManager.get_trust(npc_id)
		var bar = _trust_bar(trust)
		lines.append({"speaker": names[npc_id], "text": bar})

	var label = ""
	match _ending_type:
		"true":
			label = "True Ending — 마을이 주인이 되다"
		"normal":
			label = "Normal Ending — 아직 갈 길이 남다"
		"bad":
			label = "Bad Ending — 10년 전의 반복"
	lines.append({"speaker": "", "text": label})

	DialogueManager.dialogues["ch5_report"] = {"lines": lines}
	DialogueManager.start("ch5_report")
