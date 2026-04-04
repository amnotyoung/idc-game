extends Node

@onready var mere: CharacterBody2D   = get_parent().get_node("Mere")
@onready var wati: CharacterBody2D   = get_parent().get_node("Wati")
@onready var player: CharacterBody2D = get_parent().get_node("Player")
@onready var phone                   = get_parent().get_node("Phone")

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
			_exit_unlocked = true   # Mere 이야기 중에도 나갈 수 있게
			_setup_wati()
			await get_tree().create_timer(0.8).timeout
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
