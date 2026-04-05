extends Node

@onready var mere: CharacterBody2D   = get_parent().get_node("Mere")
@onready var wati: CharacterBody2D   = get_parent().get_node("Wati")
@onready var player: CharacterBody2D = get_parent().get_node("Player")
@onready var phone                   = get_parent().get_node("Phone")
@onready var computer                = get_parent().get_node("Computer")

const STAKEHOLDER_NAMES = {
	"mere": "Mere", "timoci": "Timoci", "ratu_josefa": "Ratu Josefa",
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

	# ── 전화기 (현재 미사용 — Sela는 정부청사에서 대면) ──
	phone.dialogue_id = ""

	# ── Mere 상태 ──
	if TrustManager.has_flag("ch1_mere_left"):
		# 이미 퇴장 — 화면에서 완전히 제거
		mere.visible = false
	elif TrustManager.has_flag("ch2_timoci_met"):
		# 정부청사 면담 완료 후 첫 복귀 — 작별 대사 자동 시작
		mere.dialogue_id = ""
		if not TrustManager.has_flag("ch1_mere_farewell_seen"):
			TrustManager.set_flag("ch1_mere_farewell_seen")
			mere.position = Vector2(170, 60)
			mere.face("down")
			_exit_unlocked = true
			_setup_wati()
			await get_tree().create_timer(0.8).timeout
			# 타이머 중 다른 대화가 시작됐으면 farewell 취소
			if not DialogueManager.is_active:
				DialogueManager.start("ch1_mere_farewell")
			return
		else:
			# farewell은 봤지만 아직 free-walking 상태(버그 방어)
			mere.visible = false
	else:
		# 아직 Timoci 못 만남 — 사무실에 있음
		mere.position = Vector2(170, 60)
		mere.face("down")
		mere.dialogue_id = "ch1_mere_revisit"

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
	elif TrustManager.has_flag("ch2_timoci_met") and not TrustManager.has_flag("wati_yangona_hint"):
		wati.dialogue_id = "ch3_wati_island_prep"
	elif TrustManager.has_flag("wati_yangona_hint"):
		wati.dialogue_id = "ch3_wati_island_idle"
	else:
		wati.dialogue_id = "ch1_wati_idle"

func _on_dialogue_ended(dialogue_id: String) -> void:
	if dialogue_id == "ch1_arrival":
		_mere_walks_in()
	elif dialogue_id in BRIEFING_ENDS:
		_unlock_exit()
		if dialogue_id == "ch1_mere_cold_b":
			# Mere가 화난 상태로 퇴장 — 씬에서 즉시 제거
			mere.dialogue_id = ""
			TrustManager.set_flag("ch1_mere_left")
			var tween = get_tree().create_tween()
			tween.tween_property(mere, "modulate:a", 0.0, 0.6)
			tween.tween_callback(mere.queue_free)
	elif dialogue_id == "ch1_mere_farewell":
		# 현장 나가는 Mere — 자연스럽게 퇴장
		TrustManager.set_flag("ch1_mere_left")
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
			"lines": [{"speaker": "", "text": "아직 보낼 사람이 없다. 먼저 이해관계자들을 만나야 한다."}]
		}
		await get_tree().create_timer(0.3).timeout
		DialogueManager.start("ch1_email_result")
		return

	var picked: String = eligible[randi() % eligible.size()]
	TrustManager.modify(picked, 3)
	var npc_name = STAKEHOLDER_NAMES.get(picked, picked)

	# 누구에게 보냈는지 + 맥락 있는 답장
	var replies = {
		"mere": "에게서 답장이 왔다. \"현장 조사 결과 정리되면 공유할게요.\"",
		"timoci": "에게서 답장이 왔다. \"서류 확인했습니다. 감사합니다.\"",
		"ratu_josefa": "에게서 Lani를 통해 전달이 왔다. \"알겠소.\"",
		"lani": "에게서 답장이 왔다. \"마을 사람들한테 전할게요.\"",
		"james": "에게서 답장이 왔다. \"APAT 쪽도 업데이트할게요.\"",
	}
	var reply_text = npc_name + replies.get(picked, "에게서 답장이 왔다.")

	DialogueManager.dialogues["ch1_email_result"] = {
		"lines": [{"speaker": "", "text": reply_text}]
	}
	await get_tree().create_timer(0.3).timeout
	DialogueManager.start("ch1_email_result")

func _mere_walks_in() -> void:
	var target = Vector2(player.position.x + 22, player.position.y - 18)
	var tween = get_tree().create_tween()
	tween.tween_property(mere, "position", target, 1.8)\
		 .set_trans(Tween.TRANS_LINEAR)
	tween.tween_callback(_start_mere_dialogue)

func _start_mere_dialogue() -> void:
	player.face("up")
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
