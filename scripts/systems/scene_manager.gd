extends CanvasLayer
## 씬 전환 (페이드 아웃 → 씬 로드 → 페이드 인)
## 사용: SceneManager.go_to("res://scenes/world/suva_street.tscn")
##        SceneManager.go_to("res://scenes/world/suva_street.tscn", Vector2(80, 120))

signal transition_finished

const FADE_TIME := 0.35

var _spawn_position: Vector2 = Vector2.ZERO
var _has_spawn: bool = false

@onready var _rect: ColorRect = $FadeRect
@onready var _anim: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
	layer = 100
	_rect.color = Color(0, 0, 0, 0)
	_rect.anchor_right = 1.0
	_rect.anchor_bottom = 1.0

func go_to(scene_path: String, spawn_pos: Vector2 = Vector2.ZERO, has_spawn: bool = false) -> void:
	_spawn_position = spawn_pos
	_has_spawn = has_spawn
	_anim.play("fade_out")
	await _anim.animation_finished
	get_tree().change_scene_to_file(scene_path)
	await get_tree().process_frame
	await get_tree().process_frame
	# 스폰 위치 적용
	if _has_spawn:
		var player = get_tree().get_first_node_in_group("player")
		if player:
			player.global_position = _spawn_position
	_anim.play("fade_in")
	await _anim.animation_finished
	transition_finished.emit()

## 편의 함수 — 스폰 위치 지정 버전
func go_to_with_spawn(scene_path: String, spawn_pos: Vector2) -> void:
	go_to(scene_path, spawn_pos, true)
