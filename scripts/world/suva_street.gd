extends Node2D

@onready var player: CharacterBody2D = $Player
@onready var vendor: CharacterBody2D = $StreetNPCs/Vendor

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
