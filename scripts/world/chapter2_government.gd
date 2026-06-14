extends Node

@onready var player: CharacterBody2D = get_parent().get_node("Player")
@onready var timoci: CharacterBody2D = get_parent().get_node("Vikash")
@onready var receptionist: CharacterBody2D = get_parent().get_node("Receptionist")
@onready var sela: CharacterBody2D = get_parent().get_node("Sela")
@onready var bg: Sprite2D = get_parent().get_node("Background")

const LOBBY_BG  = preload("res://assets/sprites/tilesets/lobby_bg.png")
const FLOOR3_BG = preload("res://assets/sprites/tilesets/government_bg.png")
const FLOOR5_BG = preload("res://assets/sprites/tilesets/landoffice_bg.png")
const STREET_SCENE = "res://scenes/world/suva_street.tscn"
const STREET_SPAWN = Vector2(217, 100)

var _current_floor := 0   # 0=미정, 3=국가계획부, 5=토지청

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)

	# ── 첫 방문: 약속 없음 → 쫓겨남 ──
	if not TrustManager.has_flag("appointment_set"):
		# Vikash/Sela 비활성화 (접수처만 보임)
		_set_npc_active(timoci, false)
		_set_npc_active(sela, false)
		DialogueManager.start("ch2_no_appointment")
		return

	# ── 첫 방문(약속 있음): 입장 내레이션 → 바로 3층 ──
	if not TrustManager.has_flag("ch2_arrived"):
		DialogueManager.start("ch2_enter_building")
		return

	# ── 재방문: 엘리베이터 선택 ──
	_show_elevator()

func _show_elevator() -> void:
	_set_status_location("정부청사 로비")
	# 로비 배경 + 모든 NPC 숨기고 엘리베이터 선택
	bg.texture = LOBBY_BG
	_hide_all_npcs()
	DialogueManager.start("ch2_elevator")

func _set_npc_active(npc: CharacterBody2D, active: bool) -> void:
	npc.visible = active
	npc.set_deferred("process_mode", Node.PROCESS_MODE_INHERIT if active else Node.PROCESS_MODE_DISABLED)
	# 충돌 판정도 토글
	var col = npc.get_node("CollisionShape2D")
	if col:
		col.set_deferred("disabled", not active)

func _hide_all_npcs() -> void:
	_set_npc_active(timoci, false)
	_set_npc_active(receptionist, false)
	_set_npc_active(sela, false)

func _show_floor3() -> void:
	_current_floor = 3
	_set_status_location("정부청사 3층")
	_hide_all_npcs()
	bg.texture = FLOOR3_BG
	_set_npc_active(timoci, true)
	_set_npc_active(receptionist, true)
	_setup_floor3_state()

func _show_floor5() -> void:
	_current_floor = 5
	_set_status_location("토지청 5층")
	_hide_all_npcs()
	bg.texture = FLOOR5_BG
	_set_npc_active(sela, true)
	_setup_floor5_state()

func _set_status_location(value: String) -> void:
	var status_bar = get_parent().get_node_or_null("StatusBar")
	if status_bar and status_bar.has_method("set_location"):
		status_bar.set_location(value)

func _setup_floor3_state() -> void:
	if not TrustManager.has_flag("ch2_timoci_met"):
		timoci.dialogue_id = ""          # 접수처 통과 전 직접 접근 차단
		receptionist.dialogue_id = "ch2_receptionist_2nd"
	elif TrustManager.has_flag("ch4_consent_obtained"):
		# 동의서 획득 후 — 새 상황 반영
		timoci.dialogue_id = "ch2_timoci_after_consent"
		receptionist.dialogue_id = "ch2_receptionist_after"
	else:
		# 면담 완료 후 재방문
		if TrustManager.has_flag("ch2_meeting_frustrated"):
			timoci.dialogue_id = "ch2_timoci_after_frustrated"
		elif TrustManager.has_flag("ch2_meeting_pressure"):
			timoci.dialogue_id = "ch2_timoci_after_pressure"
		else:
			timoci.dialogue_id = "ch2_timoci_after_good"
		receptionist.dialogue_id = "ch2_receptionist_after"

func _setup_floor5_state() -> void:
	if TrustManager.has_flag("ch4_consent_submitted"):
		sela.dialogue_id = "ch2_sela_all_done"
	elif TrustManager.has_flag("ch4_consent_obtained"):
		# Ratu 서명 받아옴 → 제출 가능
		sela.dialogue_id = "ch2_sela_consent_submit"
	elif TrustManager.has_flag("ch3_good_ending") and TrustManager.has_flag("ch4_tltb_contact"):
		# Ratu 동의 완료 + James 소개 있음 → Sela 첫 만남이어도 바로 제출
		TrustManager.set_flag("ch4_sela_contacted")
		TrustManager.set_flag("ch4_consent_obtained")
		sela.dialogue_id = "ch2_sela_consent_direct"
	elif TrustManager.has_flag("ch4_sela_contacted"):
		# 이미 한번 만남 → 대기 대사
		sela.dialogue_id = "ch2_sela_after"
	elif TrustManager.has_flag("ch4_tltb_contact"):
		# James 소개 있음 → 첫 대면
		sela.dialogue_id = "ch2_sela_first"
	else:
		# 소개 없음
		sela.dialogue_id = "ch2_sela_no_referral"

func _exit_to_street(delay: float = 1.5) -> void:
	await get_tree().create_timer(delay).timeout
	if DialogueManager.is_active:
		DialogueManager.end()
	SceneManager.go_to_with_spawn(STREET_SCENE, STREET_SPAWN)

func _on_dialogue_ended(dialogue_id: String) -> void:
	match dialogue_id:
		"ch2_no_appointment":
			_exit_to_street()
		"ch2_enter_building":
			TrustManager.set_flag("ch2_arrived")
			# 첫 방문은 약속대로 바로 3층 → 접수처
			_show_floor3()
		# ── 엘리베이터 ──
		"ch2_elevator_floor3":
			_show_floor3()
		"ch2_elevator_floor5":
			_show_floor5()
		# ── 3층: 접수처 통과 후 Timoci 접근 가능 ──
		"ch2_receptionist_2nd":
			timoci.dialogue_id = "ch2_timoci_first"
		"ch2_timoci_progress_proactive", "ch2_timoci_progress_polite", "ch2_timoci_collaborate_end":
			TrustManager.set_flag("ch2_timoci_met")
			TrustManager.set_flag("appointment_set")
			timoci.dialogue_id = "ch2_timoci_after_good"
			receptionist.dialogue_id = "ch2_receptionist_after"
			TrustManager.save_game()
		"ch2_timoci_pressure":
			TrustManager.set_flag("ch2_timoci_met")
			TrustManager.set_flag("ch2_meeting_pressure")
			timoci.dialogue_id = "ch2_timoci_after_pressure"
			receptionist.dialogue_id = "ch2_receptionist_after"
			TrustManager.save_game()
		"ch2_timoci_frustrated":
			TrustManager.set_flag("ch2_timoci_met")
			TrustManager.set_flag("ch2_meeting_frustrated")
			timoci.dialogue_id = "ch2_timoci_after_frustrated"
			receptionist.dialogue_id = "ch2_receptionist_after"
			TrustManager.save_game()
		# ── 5층: 토지청 Sela ──
		"ch2_sela_first":
			TrustManager.set_flag("ch4_sela_contacted")
			sela.dialogue_id = "ch2_sela_after"
			TrustManager.save_game()
		"ch2_sela_no_referral":
			TrustManager.set_flag("ch4_sela_contacted")
			sela.dialogue_id = "ch2_sela_after"
			TrustManager.save_game()
		"ch2_sela_consent_direct":
			# Sela 첫 만남 + Ratu 동의 한큐 처리
			TrustManager.set_flag("ch4_consent_submitted")
			TrustManager.modify("timoci", 15)
			sela.dialogue_id = "ch2_sela_all_done"
			TrustManager.save_game()
		"ch2_sela_consent_submit":
			TrustManager.set_flag("ch4_consent_submitted")
			TrustManager.modify("timoci", 15)   # Sela→Timoci 연결로 신뢰 보너스
			sela.dialogue_id = "ch2_sela_all_done"
			TrustManager.save_game()
