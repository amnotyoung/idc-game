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

## 바다 전환 컷 — 수바↔나이탬바 이동 시 사용
const SEA_CUT_TEX = preload("res://assets/sprites/tilesets/sea_transition.png")

func go_to_with_sea_cut(scene_path: String, spawn_pos: Vector2, caption: String = "") -> void:
	_spawn_position = spawn_pos
	_has_spawn = true

	# 페이드 아웃
	_anim.play("fade_out")
	await _anim.animation_finished

	# 바다 컷을 이 CanvasLayer(layer=100) 안에 표시 — 항상 화면 최상위
	var sea_tex_rect := TextureRect.new()
	sea_tex_rect.texture = SEA_CUT_TEX
	sea_tex_rect.anchor_right = 1.0
	sea_tex_rect.anchor_bottom = 1.0
	sea_tex_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	add_child(sea_tex_rect)

	# 자막 (바다 컷 위에)
	var label: Label = null
	if caption != "":
		label = Label.new()
		label.text = caption
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.anchor_left = 0.0
		label.anchor_right = 1.0
		label.anchor_top = 1.0
		label.anchor_bottom = 1.0
		label.offset_top = -18.0
		label.offset_bottom = -4.0
		label.add_theme_font_size_override("font_size", 7)
		label.modulate = Color(0.95, 0.93, 0.88, 0.9)
		add_child(label)

	# 페이드 인 (바다 보여줌)
	_rect.color = Color(0, 0, 0, 0)
	_anim.play("fade_in")
	await _anim.animation_finished

	# 바다 감상 시간
	await get_tree().create_timer(2.5).timeout

	# 다시 페이드 아웃
	_anim.play("fade_out")
	await _anim.animation_finished

	# 바다 컷 정리
	sea_tex_rect.queue_free()
	if label:
		label.queue_free()

	# 씬 전환
	get_tree().change_scene_to_file(scene_path)
	await get_tree().process_frame
	await get_tree().process_frame
	if _has_spawn:
		var player = get_tree().get_first_node_in_group("player")
		if player:
			player.global_position = _spawn_position
	_anim.play("fade_in")
	await _anim.animation_finished
	transition_finished.emit()
