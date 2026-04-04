extends Node2D

@onready var player: CharacterBody2D = $Player
@onready var vendor: CharacterBody2D = $StreetNPCs/Vendor
@onready var bula_man: CharacterBody2D = $StreetNPCs/BulaMan
@onready var hindi_man: CharacterBody2D = $StreetNPCs/HindiMan
@onready var police: CharacterBody2D = $StreetNPCs/Police
@onready var bula_woman2: CharacterBody2D = $StreetNPCs/BulaWoman2

# 문 구멍 중심 x, 진입 감지 y, 목적지
const DOORS = [
	{
		"cx": 29.0, "gap": 12.0,        # KODA 구멍 x=17~41
		"enter_y": 76.0,                 # 구멍 통과 시 y
		"scene": "res://scenes/world/chapter1_office.tscn",
		"spawn": Vector2(160, 150)
	},
	{
		"cx": 217.0, "gap": 12.0,        # 정부청사 구멍 x=205~229 (식민지 건물 문)
		"enter_y": 76.0,
		"scene": "res://scenes/world/government_building.tscn",
		"spawn": Vector2(160, 130)
	},
	{
		"cx": 290.0, "gap": 12.0,        # 국제기구 구멍 x=278~302 (우단 건물)
		"enter_y": 76.0,
		"scene": "res://scenes/world/intl_org_office.tscn",
		"spawn": Vector2(160, 130)
	},
]

var _entering := false

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)
	_update_vendor()
	_update_street_npcs()

func _update_street_npcs() -> void:
	# 챕터 진행에 따라 거리 NPC 대사 진화
	# Albert Park 럭비맨 — KODA 알게 된 후 대사 변경
	if TrustManager.has_flag("ch1_intro_done"):
		bula_man.dialogue_id = "bula_man_rugby"
	if TrustManager.has_flag("ch4_james_met"):
		bula_woman2.dialogue_id = "bula_woman_after_ch4"
	if TrustManager.has_flag("ch3_visited"):
		police.dialogue_id = "police_after_island"
	if TrustManager.has_flag("ch2_timoci_met"):
		hindi_man.dialogue_id = "hindi_man_after_timoci"

func _update_vendor() -> void:
	if TrustManager.has_flag("sevusevu_prepared"):
		vendor.dialogue_id = "street_vendor_after"
	elif TrustManager.has_flag("wati_yangona_hint"):
		# Wati가 힌트 준 후 — Damodar City에서 양고나 구매 가능
		vendor.dialogue_id = "street_vendor_yangona"
	else:
		vendor.dialogue_id = "street_vendor_1"

func _on_dialogue_ended(dialogue_id: String) -> void:
	if dialogue_id == "street_vendor_yangona_buy":
		TrustManager.set_flag("sevusevu_prepared")
		vendor.dialogue_id = "street_vendor_after"
		TrustManager.save_game()

# 항구 — 하단 중앙 출구
const HARBOR = {
	"cx": 160.0, "gap": 14.0,
	"exit_y": 158.0,
	"scene": "res://scenes/world/naitamba_island.tscn",
	"spawn": Vector2(160, 130)
}

func _process(_delta: float) -> void:
	if _entering or DialogueManager.is_active:
		return
	var px = player.global_position.x
	var py = player.global_position.y
	for door in DOORS:
		# 구멍 x 범위 안에서 y가 충분히 위로 올라갔을 때
		if py <= door["enter_y"] and abs(px - door["cx"]) <= door["gap"]:
			_entering = true
			SceneManager.go_to_with_spawn(door["scene"], door["spawn"])
			return
	# 항구 출구 (하단)
	if not _entering and not DialogueManager.is_active:
		if py >= HARBOR["exit_y"] and abs(px - HARBOR["cx"]) <= HARBOR["gap"]:
			_entering = true
			SceneManager.go_to_with_spawn(HARBOR["scene"], HARBOR["spawn"])
