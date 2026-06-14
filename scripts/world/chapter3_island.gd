extends Node

@onready var ratu: CharacterBody2D = get_parent().get_node("RatuJosefa")
@onready var lani: CharacterBody2D = get_parent().get_node("Lani")
@onready var mere: CharacterBody2D = get_parent().get_node("Mere")
@onready var village_npcs: Node2D = get_parent().get_node("VillageNPCs")
@onready var bg: Sprite2D = get_parent().get_node("Background")
@onready var player: CharacterBody2D = get_parent().get_node("Player")

const ISLAND_BG = preload("res://assets/sprites/tilesets/naitamba_bg.png")
const SEVUSEVU_BG = preload("res://assets/sprites/tilesets/sevusevu_bg.png")

var _in_sevusevu := false
var _ratu_sign_swapped := false

func _ready() -> void:
	await get_tree().process_frame
	_update_village_npcs()
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)
	DialogueManager.dialogue_line_changed.connect(_on_line_check)

	if not TrustManager.has_flag("ch3_arrived"):
		# 첫 방문 — 세부세부 전에는 Ratu 먼저 안내
		lani.dialogue_id = "ch3_lani_not_yet"
		mere.dialogue_id = "ch3_mere_first"
		if TrustManager.has_flag("ch2_timoci_met"):
			DialogueManager.start("ch3_arrive")
		else:
			# 정부청사 안 가고 섬부터 온 경우
			DialogueManager.start("ch3_arrive_early")
	elif TrustManager.has_flag("ch3_visited"):
		# 재방문 — 동의서 or 일반 복원
		if TrustManager.has_flag("ch4_consent_obtained"):
			# 동의서 이미 완료
			ratu.dialogue_id = "ch3_consent_done"
			lani.dialogue_id = "ch3_lani_after"
			mere.dialogue_id = "ch3_mere_consent"
		elif TrustManager.has_flag("ch4_sela_contacted") and TrustManager.has_flag("ch3_good_ending"):
			# Sela 통화 완료 + good ending → 동의서 서명 가능
			ratu.dialogue_id = "ch3_consent_ratu"
			lani.dialogue_id = "ch3_lani_after"
			mere.dialogue_id = "ch3_mere_after_good"
		elif TrustManager.has_flag("ch4_sela_contacted") and not TrustManager.has_flag("ch3_good_ending"):
			# Sela 통화 완료 + neutral ending → Ratu가 서명 거부
			ratu.dialogue_id = "ch3_consent_ratu_neutral"
			lani.dialogue_id = ""
			mere.dialogue_id = "ch3_mere_after_neutral"
		elif TrustManager.has_flag("ch3_good_ending"):
			ratu.dialogue_id = "ch3_ratu_after"
			lani.dialogue_id = "ch3_lani_after"
			mere.dialogue_id = "ch3_mere_after_good"
		else:
			ratu.dialogue_id = "ch3_ratu_after_neutral"
			lani.dialogue_id = ""
			mere.dialogue_id = "ch3_mere_after_neutral"
	else:
		# ch3_arrived는 됐지만 ch3_visited는 아직 — 중간 재진입
		lani.dialogue_id = "ch3_lani_not_yet"
		mere.dialogue_id = "ch3_mere_after_ratu"
		if TrustManager.has_flag("sevusevu_prepared"):
			ratu.dialogue_id = "ch3_ratu_greet_prepared"
		elif TrustManager.has_flag("bought_powder"):
			ratu.dialogue_id = "ch3_ratu_greet_powder"
		elif TrustManager.has_flag("bought_mango"):
			ratu.dialogue_id = "ch3_ratu_greet_mango"
		else:
			ratu.dialogue_id = "ch3_ratu_greet_basic"

func _on_line_check(_line: Dictionary) -> void:
	var did = DialogueManager.current_dialogue_id
	# Sela 이미 만남 + ratu_close_good 도달 → 서명 포함 버전으로 교체 (1회만)
	if did == "ch3_ratu_close_good" and TrustManager.has_flag("ch4_sela_contacted") and not _ratu_sign_swapped:
		_ratu_sign_swapped = true
		DialogueManager.current_dialogue = DialogueManager.dialogues["ch3_ratu_close_good_sign"]
		DialogueManager.current_dialogue_id = "ch3_ratu_close_good_sign"
		DialogueManager.current_line_index = 0
		DialogueManager._show_current_line()
		return
	# 세부세부 시작 → 배경 전환 + NPC/플레이어 숨김 (뿌리/가루/망고/빈손 모두)
	if did in ["ch3_sevusevu_good", "ch3_sevusevu_powder", "ch3_ratu_mango_react", "ch3_sevusevu_miss"] and not _in_sevusevu:
		_in_sevusevu = true
		_set_status_location("세부세부")
		bg.texture = SEVUSEVU_BG
		player.visible = false
		ratu.visible = false
		lani.visible = false
		mere.visible = false
		village_npcs.visible = false

## 섬 NPC 대화 → 관련 이해관계자 소폭 신뢰 상승
const ISLAND_NPC_TRUST = {
	"island_elder_1": {"ratu_josefa": 3},       # 마을 역사 이해
	"island_elder_after": {"ratu_josefa": 2},
	"island_child_1": {"lani": 3},              # 다음 세대 연결
	"island_fisher_1": {"lani": 2, "ratu_josefa": 2},  # 마을 현실
	"island_fisher_after": {"lani": 2},
	"island_woman_1": {"mere": 2, "ratu_josefa": 2},   # 현장 맥락
	"island_woman_after": {"mere": 2},
	"ch3_mere_first_end": {"mere": 3},          # Mere 협력
}

func _on_dialogue_ended(dialogue_id: String) -> void:
	# 섬 NPC 대화 신뢰 보너스
	if dialogue_id in ISLAND_NPC_TRUST:
		for npc_id in ISLAND_NPC_TRUST[dialogue_id]:
			TrustManager.modify(npc_id, ISLAND_NPC_TRUST[dialogue_id][npc_id])
	match dialogue_id:
		"island_elder_1", "island_fisher_1", "island_woman_1":
			# 주민이 직접 관리를 원한다는 현장 정보 → Lani 설득에 공감 선택지 해금
			TrustManager.set_flag("clue_village_maintenance")
		"ch3_arrive", "ch3_arrive_early":
			TrustManager.set_flag("ch3_arrived")
			# Mere와 먼저 대화할 수 있도록 자유 이동 — Ratu는 직접 다가가야 대화
			if TrustManager.has_flag("sevusevu_prepared"):
				ratu.dialogue_id = "ch3_ratu_greet_prepared"
			elif TrustManager.has_flag("bought_powder"):
				ratu.dialogue_id = "ch3_ratu_greet_powder"
			elif TrustManager.has_flag("bought_mango"):
				ratu.dialogue_id = "ch3_ratu_greet_mango"
			else:
				ratu.dialogue_id = "ch3_ratu_greet_basic"
		"ch3_sevusevu_end":
			# 세부세부 끝 → 배경 복원 + Lani에게 직접 말 걸 수 있게
			_restore_island_view()
			lani.dialogue_id = "ch3_village_talk"
			ratu.dialogue_id = ""  # Ratu 대화 완료, Lani가 핵심
		"ch3_lani_deflect":
			_restore_island_view()
			TrustManager.set_flag("ch3_visited")
			ratu.dialogue_id = ""
			lani.dialogue_id = ""
			TrustManager.save_game()
		"ch3_ratu_close_good":
			_restore_island_view()
			TrustManager.set_flag("ch3_visited")
			TrustManager.set_flag("ch3_good_ending")
			lani.dialogue_id = "ch3_lani_after"
			ratu.dialogue_id = "ch3_ratu_after"
			TrustManager.save_game()
		"ch3_ratu_close_good_sign":
			# Sela 만난 후 섬 방문 → 동의 + 서명 한 번에
			_restore_island_view()
			TrustManager.set_flag("ch3_visited")
			TrustManager.set_flag("ch3_good_ending")
			TrustManager.set_flag("ch4_consent_obtained")
			lani.dialogue_id = "ch3_lani_after"
			ratu.dialogue_id = "ch3_consent_done"
			mere.dialogue_id = "ch3_mere_consent"
			TrustManager.save_game()
		"ch3_ratu_close_neutral":
			_restore_island_view()
			TrustManager.set_flag("ch3_visited")
			ratu.dialogue_id = "ch3_ratu_after_neutral"
			lani.dialogue_id = ""
			TrustManager.save_game()
		"ch3_consent_sign", "ch3_consent_sign_quiet":
			TrustManager.set_flag("ch4_consent_obtained")
			ratu.dialogue_id = "ch3_consent_done"
			mere.dialogue_id = "ch3_mere_consent"
			_update_village_npcs()
			TrustManager.save_game()

func _restore_island_view() -> void:
	if _in_sevusevu:
		_in_sevusevu = false
		_set_status_location("나이탬바 섬")
		bg.texture = ISLAND_BG
		player.visible = true
		ratu.visible = true
		lani.visible = true
		mere.visible = true
		village_npcs.visible = true

func _update_village_npcs() -> void:
	if not village_npcs:
		return
	var elder = village_npcs.get_node_or_null("Elder")
	var fisher = village_npcs.get_node_or_null("Fisher")
	var woman = village_npcs.get_node_or_null("Woman")
	if TrustManager.has_flag("ch4_consent_obtained"):
		if elder: elder.dialogue_id = "island_elder_after"
		if fisher: fisher.dialogue_id = "island_fisher_after"
		if woman: woman.dialogue_id = "island_woman_after"
	elif TrustManager.has_flag("ch3_good_ending"):
		if elder: elder.dialogue_id = "island_elder_after"
		if fisher: fisher.dialogue_id = "island_fisher_after"
		if woman: woman.dialogue_id = "island_woman_after"

func _set_status_location(value: String) -> void:
	var status_bar = get_parent().get_node_or_null("StatusBar")
	if status_bar and status_bar.has_method("set_location"):
		status_bar.set_location(value)
