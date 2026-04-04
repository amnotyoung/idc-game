extends Node2D
## 건물 내부 씬 공통 출구 스크립트
## 하단으로 걸어 나가면 수바 거리로 복귀

@export var street_scene: String = "res://scenes/world/suva_street.tscn"
@export var spawn_x: float = 160.0
@export var spawn_y: float = 100.0
@export var exit_y: float  = 162.0   # 이 y를 넘으면 나가기

var _exiting := false

func _process(_delta: float) -> void:
	if _exiting:
		return
	if DialogueManager.is_active:
		return
	var player = get_tree().get_first_node_in_group("player")
	if player and player.global_position.y >= exit_y:
		_exiting = true
		SceneManager.go_to_with_spawn(street_scene, Vector2(spawn_x, spawn_y + 32.0))
