extends Node

@onready var bg: Sprite2D = get_parent().get_node("Background")
@onready var bgm: AudioStreamPlayer = get_parent().get_node("BGM")
@onready var attendees: Node2D = get_parent().get_node("Attendees")
@onready var water_tank: Sprite2D = get_parent().get_node("WaterTank")
@onready var ending_stage: Node2D = get_parent().get_node("EndingStage")

const OFFICE_BG = preload("res://assets/sprites/tilesets/office_bg.png")
const ISLAND_BG = preload("res://assets/sprites/tilesets/naitamba_bg.png")
const SEVUSEVU_BG = preload("res://assets/sprites/tilesets/sevusevu_bg.png")

var _ending_type: String = ""
var _staged_lines: Dictionary = {}  # 대사 텍스트 → 연출 함수

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)
	DialogueManager.dialogue_line_changed.connect(_on_ending_line)

	TrustManager.set_flag("ch5_started")

	# 회의 시작 (엔딩 판정은 최종 선택 후로 지연)
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
			# 최종 선택의 effects가 적용된 후 판정
			_ending_type = TrustManager.check_ending()
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
	# BGM + 배경 + 캐릭터 모두 페이드아웃
	var tween = get_tree().create_tween()
	tween.set_parallel(true)
	tween.tween_property(bg, "modulate:a", 0.0, 1.2)
	tween.tween_property(attendees, "modulate:a", 0.0, 1.0)
	tween.tween_property(bgm, "volume_db", -40.0, 1.2)
	await tween.finished
	attendees.visible = false

	# 잠깐의 암전
	await get_tree().create_timer(1.5).timeout

	match _ending_type:
		"true":
			_set_status("2025.03", "나이탬바 섬")
			bg.texture = ISLAND_BG
			water_tank.visible = true
			water_tank.modulate.a = 0.0
		"normal":
			_set_status("2025.03", "나이탬바 섬")
			bg.texture = ISLAND_BG
		"bad":
			_set_status("2024.09", "KODA 사무소")
			bg.texture = OFFICE_BG

	# 배경 천천히 페이드인 (BGM은 꺼진 상태 유지 — 고요한 엔딩)
	tween = get_tree().create_tween()
	tween.set_parallel(true)
	tween.tween_property(bg, "modulate:a", 1.0, 1.5)
	if _ending_type == "true":
		tween.tween_property(water_tank, "modulate:a", 1.0, 2.0)
	await tween.finished

	await get_tree().create_timer(1.0).timeout

	match _ending_type:
		"true":
			DialogueManager.start("ch5_ending_true")
		"normal":
			DialogueManager.start("ch5_ending_normal")
		"bad":
			DialogueManager.start("ch5_ending_bad")

## 엔딩 대사 진행 시 시각 연출
func _on_ending_line(line: Dictionary) -> void:
	var text: String = line.get("text", "")
	var did = DialogueManager.current_dialogue_id

	if did == "ch5_ending_true":
		_true_ending_visuals(text)
	elif did == "ch5_ending_normal":
		_normal_ending_visuals(text)
	elif did == "ch5_ending_bad":
		_bad_ending_visuals(text)

func _true_ending_visuals(text: String) -> void:
	if "저수조 앞에 사람들이" in text:
		# 캐릭터들 등장
		ending_stage.visible = true
		ending_stage.modulate.a = 0.0
		var tween = get_tree().create_tween()
		tween.tween_property(ending_stage, "modulate:a", 1.0, 1.0)
	elif "Ratu Josefa가 앞으로" in text:
		# Ratu를 앞으로 이동
		var ratu = ending_stage.get_node("RatuStage")
		var tween = get_tree().create_tween()
		tween.tween_property(ratu, "position", Vector2(158, 110), 0.8)
	elif "양고나를 타노아에" in text:
		# 배경을 세부세부로 전환
		bg.texture = SEVUSEVU_BG
	elif "Lani가 저수조 밸브" in text:
		# 배경을 섬으로 복원, Lani를 저수조 앞으로
		bg.texture = ISLAND_BG
		var lani = ending_stage.get_node("LaniStage")
		var tween = get_tree().create_tween()
		tween.tween_property(lani, "position", Vector2(162, 108), 0.5)
	elif "물이 흘러나왔다" in text:
		# 저수조 밝게 빛남 (물 흐르는 표현)
		var tween = get_tree().create_tween().set_loops(3)
		tween.tween_property(water_tank, "modulate", Color(1.3, 1.3, 1.5), 0.3)
		tween.tween_property(water_tank, "modulate", Color(1, 1, 1), 0.3)
	elif "메케" in text:
		# 캐릭터들 좌우 흔들림 (춤 표현)
		for child in ending_stage.get_children():
			var tween = get_tree().create_tween().set_loops(4)
			var orig_x = child.position.x
			tween.tween_property(child, "position:x", orig_x + 3, 0.2)
			tween.tween_property(child, "position:x", orig_x - 3, 0.2)
			tween.tween_property(child, "position:x", orig_x, 0.2)
	elif "마을 운영위원회 관리" in text:
		# 모든 것이 고요해짐
		for child in ending_stage.get_children():
			var tween = get_tree().create_tween()
			tween.tween_property(child, "position:x", child.position.x, 0.5)

func _normal_ending_visuals(text: String) -> void:
	if "공사가 진행 중" in text:
		# 저수조 반투명 (공사 중)
		water_tank.visible = true
		water_tank.modulate = Color(1, 1, 1, 0.5)
	elif "마을 사람들이 공사 현장" in text:
		# 캐릭터들 등장
		ending_stage.visible = true
		ending_stage.modulate.a = 0.0
		var tween = get_tree().create_tween()
		tween.tween_property(ending_stage, "modulate:a", 1.0, 1.0)
	elif "혼자가 아니다" in text:
		# 저수조가 서서히 밝아짐 (완공 희망)
		var tween = get_tree().create_tween()
		tween.tween_property(water_tank, "modulate:a", 0.8, 1.5)

func _bad_ending_visuals(text: String) -> void:
	if "서랍을 열었다" in text:
		# 화면 약간 어두워짐
		var tween = get_tree().create_tween()
		tween.tween_property(bg, "modulate", Color(0.7, 0.7, 0.75), 1.0)
	elif "새 메모를 쓴다" in text:
		# 화면 더 어두워짐
		var tween = get_tree().create_tween()
		tween.tween_property(bg, "modulate", Color(0.5, 0.5, 0.55), 1.5)
	elif "이 메모가 서랍에" in text:
		# 거의 암전
		var tween = get_tree().create_tween()
		tween.tween_property(bg, "modulate", Color(0.3, 0.3, 0.35), 2.0)

func _trust_bar(value: int) -> String:
	var filled = int(value / 10)
	var empty = 10 - filled
	return "█".repeat(filled) + "░".repeat(empty) + " %d" % value

func _show_report_card() -> void:
	# 런타임에 대화 데이터 주입
	var names = {
		"mere": "Mere",
		"timoci": "Vikash",
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

func _set_status(time_value: String, location_value: String) -> void:
	var status_bar = get_parent().get_node_or_null("StatusBar")
	if not status_bar:
		return
	if status_bar.has_method("set_time"):
		status_bar.set_time(time_value)
	if status_bar.has_method("set_location"):
		status_bar.set_location(location_value)
