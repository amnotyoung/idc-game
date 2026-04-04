extends Node

@onready var mere: CharacterBody2D   = get_parent().get_node("Mere")
@onready var wati: CharacterBody2D   = get_parent().get_node("Wati")
@onready var player: CharacterBody2D = get_parent().get_node("Player")

const EXIT_Y     = 12.0    # 상단 문 통과 — y가 이 값 이하일 때
const EXIT_X_MIN = 135.0
const EXIT_X_MAX = 185.0
const STREET_SCENE = "res://scenes/world/suva_street.tscn"
var _exiting     := false
var _exit_unlocked := false

const BRIEFING_ENDS = [
	"ch1_mere_warm_a",
	"ch1_mere_warm_b",
	"ch1_mere_cold_a",
	"ch1_mere_cold_b",
]

func _ready() -> void:
	await get_tree().process_frame

	if TrustManager.has_flag("ch1_intro_done"):
		_setup_free_roam()
	else:
		DialogueManager.dialogue_ended.connect(_on_dialogue_ended)
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
	mere.position = Vector2(210, 85)
	mere.face("down")
	mere.dialogue_id = "ch1_mere_revisit"
	if not TrustManager.has_flag("wati_introduced"):
		wati.dialogue_id = "ch1_wati_intro"
	elif not TrustManager.has_flag("appointment_set"):
		# 밖에 나갔다 돌아왔으면 Wati가 약속을 잡아놓은 상태
		wati.dialogue_id = "ch1_wati_appointment_ready"
	elif TrustManager.has_flag("ch2_timoci_met") and not TrustManager.has_flag("sevusevu_prepared"):
		wati.dialogue_id = "ch3_wati_island_prep"
	else:
		wati.dialogue_id = "ch3_wati_island_idle" if TrustManager.has_flag("sevusevu_prepared") else "ch1_wati_idle"
	_exit_unlocked = true

func _on_dialogue_ended(dialogue_id: String) -> void:
	if dialogue_id == "ch1_arrival":
		_mere_walks_in()
	elif dialogue_id in BRIEFING_ENDS:
		_unlock_exit()
		if dialogue_id == "ch1_mere_cold_b":
			# Mere가 나가버린 상황 — 씬에서 퇴장
			mere.dialogue_id = ""
			var tween = get_tree().create_tween()
			tween.tween_property(mere, "modulate:a", 0.0, 0.6)
			tween.tween_callback(mere.queue_free)
	elif dialogue_id == "ch1_wati_intro":
		TrustManager.set_flag("wati_introduced")
		wati.dialogue_id = "ch1_wati_idle"
	elif dialogue_id == "ch1_wati_appointment_ready":
		TrustManager.set_flag("appointment_set")
		wati.dialogue_id = "ch1_wati_idle"
	elif dialogue_id == "ch3_wati_island_prep":
		TrustManager.set_flag("sevusevu_prepared")
		wati.dialogue_id = "ch3_wati_island_idle"
	elif dialogue_id == "ch1_mere_revisit":
		pass  # Mere는 자기 갈 길 가는 것

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
	_exit_unlocked = true
	# Mere 대사 교체 — 이미 얘기 끝난 상태
	mere.dialogue_id = "ch1_mere_after_talk"
	# "▲ 나가기" 힌트 페이드인
	var hint: Label = get_parent().get_node("ExitDoor/ExitHint")
	var tween = get_tree().create_tween()
	tween.tween_property(hint, "modulate:a", 1.0, 0.8)
