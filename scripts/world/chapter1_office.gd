extends Node

@onready var mere: CharacterBody2D   = get_parent().get_node("Mere")
@onready var wati: CharacterBody2D   = get_parent().get_node("Wati")
@onready var player: CharacterBody2D = get_parent().get_node("Player")
@onready var computer                = get_parent().get_node("Computer")

const STAKEHOLDER_NAMES = {
	"mere": "Mere", "timoci": "Vikash", "ratu_josefa": "Ratu Josefa",
	"lani": "Lani", "james": "James"
}

const EXIT_Y     = 12.0    # 상단 문 통과 — y가 이 값 이하일 때
const EXIT_X_MIN = 135.0
const EXIT_X_MAX = 185.0
const STREET_SCENE = "res://scenes/world/suva_street.tscn"
var _exiting     := false
var _exit_unlocked := false

const BRIEFING_ENDS = [
	"ch1_mere_strategy",   # warm_a/warm_b/cold_a → 최종 도달점
	"ch1_mere_cold_b",     # cold_b는 choices 없이 바로 끝남 (Mere 퇴장)
]

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)
	LanguageManager.language_changed.connect(_on_language_changed)
	_refresh_labels()

	if TrustManager.has_flag("ch1_intro_done"):
		_setup_free_roam()
	else:
		DialogueManager.start("ch1_arrival")

func _process(_delta: float) -> void:
	if _exiting or not _exit_unlocked:
		return
	if DialogueManager.is_active:
		return
	var px = player.global_position.x
	if player.global_position.y <= EXIT_Y and px >= EXIT_X_MIN and px <= EXIT_X_MAX:
		_exiting = true
		SceneManager.go_to_with_spawn(STREET_SCENE, Vector2(29, 115))

func _setup_free_roam() -> void:
	# ── 엔딩 진입 체크 (Sela에게 동의서 제출 완료) ──
	if TrustManager.has_flag("ch4_consent_submitted") \
	   and not TrustManager.has_flag("ch5_started"):
		await get_tree().create_timer(0.5).timeout
		SceneManager.go_to("res://scenes/world/ending_scene.tscn")
		return

	# ── Mere 상태 — 브리핑 후 나이탬바로 떠났으므로 항상 부재 ──
	if TrustManager.has_flag("ch1_mere_left"):
		mere.visible = false

	_setup_wati()
	_exit_unlocked = true

func _setup_wati() -> void:
	if not TrustManager.has_flag("wati_introduced"):
		wati.dialogue_id = "ch1_wati_intro"
	elif not TrustManager.has_flag("appointment_set"):
		wati.dialogue_id = "ch1_wati_appointment_ready"
	elif TrustManager.has_flag("ch3_visited") and not TrustManager.has_flag("ch2_timoci_met"):
		# 정부청사 안 가고 섬부터 갔다 온 경우
		wati.dialogue_id = "ch1_wati_island_first"
	elif TrustManager.has_flag("ch3_visited"):
		# 섬 완료 (Ratu 만남) — 섬 안내 불필요
		wati.dialogue_id = "ch3_wati_island_idle"
	elif not TrustManager.has_flag("sevusevu_prepared") and not TrustManager.has_flag("wati_yangona_hint"):
		# 아직 양고나 안 챙김 → 양고나 + 섬 안내
		wati.dialogue_id = "ch3_wati_island_prep"
	elif TrustManager.has_flag("wati_yangona_hint") or TrustManager.has_flag("sevusevu_prepared"):
		wati.dialogue_id = "ch3_wati_island_idle"
	else:
		wati.dialogue_id = "ch1_wati_idle"

func _on_dialogue_ended(dialogue_id: String) -> void:
	if dialogue_id == "ch1_arrival":
		_mere_walks_in()
	elif dialogue_id in BRIEFING_ENDS:
		_unlock_exit()
		# Mere 퇴장 — 브리핑 후 나이탬바로 떠남 (cold_b는 화나서 퇴장)
		TrustManager.set_flag("ch1_mere_left")
		mere.dialogue_id = ""
		var tween = get_tree().create_tween()
		tween.tween_property(mere, "modulate:a", 0.0, 0.8)
		tween.tween_callback(mere.queue_free)
		TrustManager.save_game()
	elif dialogue_id == "ch1_wati_intro":
		TrustManager.set_flag("wati_introduced")
		wati.dialogue_id = "ch1_wati_waiting"
	elif dialogue_id == "ch1_wati_appointment_ready":
		TrustManager.set_flag("appointment_set")
		wati.dialogue_id = "ch1_wati_idle"
	elif dialogue_id == "ch3_wati_island_prep":
		TrustManager.set_flag("wati_yangona_hint")
		wati.dialogue_id = "ch3_wati_island_idle"
	# ch4_sela_call 제거됨 — Sela는 정부청사에서 대면
	elif dialogue_id == "ch1_computer_send":
		_send_progress_email()

## 만난 적 있는 이해관계자만 메일 대상
const MET_FLAGS = {
	"mere":       "ch1_intro_done",     # Mere는 인트로에서 만남
	"timoci":     "ch2_timoci_met",
	"ratu_josefa":"ch3_visited",
	"lani":       "ch3_visited",
	"james":      "ch4_james_met",
}

func _send_progress_email() -> void:
	var eligible: Array = []
	for npc_id in TrustManager.ENDING_NPCS:
		var flag = MET_FLAGS.get(npc_id, "")
		if flag != "" and TrustManager.has_flag(flag) and TrustManager.get_trust(npc_id) < 100:
			eligible.append(npc_id)

	if eligible.size() == 0:
		DialogueManager.dialogues["ch1_email_result"] = {
			"lines": [{"speaker": "", "text": LanguageManager.text("email_no_recipient")}]
		}
		await get_tree().create_timer(0.3).timeout
		DialogueManager.start("ch1_email_result")
		return

	var picked: String = eligible[randi() % eligible.size()]
	TrustManager.modify(picked, 3)
	var npc_name = STAKEHOLDER_NAMES.get(picked, picked)
	var trust = TrustManager.get_trust(picked)

	# 신뢰도 구간별 답장 톤
	var reply_text = _get_email_reply(picked, npc_name, trust)

	DialogueManager.dialogues["ch1_email_result"] = {
		"lines": [{"speaker": "", "text": reply_text}]
	}
	await get_tree().create_timer(0.3).timeout
	DialogueManager.start("ch1_email_result")

## 신뢰도 구간: 0~25 냉담 / 26~50 사무적 / 51~70 호의적 / 71+ 협력적
func _get_email_reply(npc_id: String, npc_name: String, trust: int) -> String:
	var tier = "cold"
	if trust >= 71:
		tier = "ally"
	elif trust >= 51:
		tier = "warm"
	elif trust >= 26:
		tier = "formal"

	return npc_name + LanguageManager.email_reply(npc_id, tier)

func _mere_walks_in() -> void:
	# Mere가 플레이어 바로 옆으로 와서 대화 (카메라에 둘 다 잡히게)
	var target = Vector2(player.position.x + 18, player.position.y - 8)
	var tween = get_tree().create_tween()
	tween.tween_property(mere, "position", target, 1.8)\
		 .set_trans(Tween.TRANS_LINEAR)
	tween.tween_callback(_start_mere_dialogue)

func _start_mere_dialogue() -> void:
	player.face("right")   # Mere 쪽을 바라봄
	mere.face("left")      # 플레이어 쪽을 바라봄
	DialogueManager.start("ch1_mere_entrance")

func _unlock_exit() -> void:
	TrustManager.set_flag("ch1_intro_done")
	TrustManager.save_game()
	_exit_unlocked = true
	# Mere 대사 교체 — 이미 얘기 끝난 상태
	mere.dialogue_id = "ch1_mere_after_talk"
	# "▲ 나가기" 힌트 페이드인
	var hint: Label = get_parent().get_node("ExitDoor/ExitHint")
	var tween = get_tree().create_tween()
	tween.tween_property(hint, "modulate:a", 1.0, 0.8)

func _on_language_changed(_locale: String) -> void:
	_refresh_labels()

func _refresh_labels() -> void:
	var root := get_parent()
	var exit_hint: Label = root.get_node_or_null("ExitDoor/ExitHint")
	if exit_hint:
		exit_hint.text = LanguageManager.text("hint_exit_up")
	var project_file_label: Label = root.get_node_or_null("ProjectFile/Label")
	if project_file_label:
		project_file_label.text = LanguageManager.text("hint_project_file")
	var computer_label: Label = root.get_node_or_null("Computer/Label")
	if computer_label:
		computer_label.text = LanguageManager.text("hint_computer")
