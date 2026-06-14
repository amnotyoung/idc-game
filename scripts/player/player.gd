extends CharacterBody2D

const WALK_SPEED = 70.0
const RUN_SPEED = 130.0

@onready var interact_ray: RayCast2D = $InteractRay
@onready var sprite: Sprite2D = $Sprite

# 스프라이트시트 열 순서: 0=하, 1=좌, 2=우, 3=상
const DIR_FRAME = {"down": 0, "left": 1, "right": 2, "up": 3}

var _facing: Vector2 = Vector2.DOWN

# 탭/클릭 이동 목표 (모바일 탭 이동 + 데스크톱 마우스 클릭 이동)
var _has_target: bool = false
var _move_target: Vector2 = Vector2.ZERO
var _target_interactable: Node = null

func _ready() -> void:
	add_to_group("player")

func _physics_process(_delta: float) -> void:
	if DialogueManager.is_active:
		velocity = Vector2.ZERO
		_has_target = false
		_target_interactable = null
		return

	# 키보드 입력이 있으면 방향 이동이 우선 (탭 목표 취소)
	var kbd := Vector2(
		Input.get_axis("ui_left", "ui_right"),
		Input.get_axis("ui_up", "ui_down")
	).normalized()

	if kbd != Vector2.ZERO:
		_has_target = false
		_target_interactable = null
		_facing = kbd
		interact_ray.target_position = _facing * 14.0
		_update_sprite()
		var speed := WALK_SPEED if Input.is_key_pressed(KEY_SHIFT) else RUN_SPEED
		velocity = kbd * speed
		move_and_slide()
	elif _has_target:
		_move_toward_target()
	else:
		velocity = Vector2.ZERO
		move_and_slide()

## 탭/클릭으로 지정한 목표를 향해 이동. 상호작용 대상이면 도착 후 말 걸기.
func _move_toward_target() -> void:
	var to := _move_target - global_position
	var dist := to.length()
	# 대상(NPC/사물)이면 조금 떨어진 곳에서 멈춰 말 걸고, 빈 땅이면 거의 도착까지
	var stop_dist := 14.0 if _target_interactable != null else 3.0
	if dist <= stop_dist:
		velocity = Vector2.ZERO
		move_and_slide()
		var target := _target_interactable
		_has_target = false
		_target_interactable = null
		if target != null and is_instance_valid(target) and target.has_method("interact"):
			_face_toward(target.global_position)
			target.interact()
		return

	var dir := to.normalized()
	_facing = dir
	interact_ray.target_position = _facing * 14.0
	_update_sprite()
	velocity = dir * RUN_SPEED
	move_and_slide()
	# 벽에 막혀 더 나아가지 못하면 목표 포기 (무한정 벽에 비비기 방지)
	if get_real_velocity().length() < 3.0:
		_has_target = false
		_target_interactable = null

func _unhandled_input(event: InputEvent) -> void:
	# 대화 중 입력(진행/뒤로/선택)은 dialogue_box 가 처리
	if DialogueManager.is_active:
		return
	# 화면 탭(모바일 터치) / 마우스 좌클릭(데스크톱) → 이동 또는 대상에게 다가가 말 걸기
	# 웹 모바일에서 터치가 마우스로 에뮬되지 않을 수 있어 InputEventScreenTouch 도 직접 처리
	var tap_pos := Vector2.INF
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		tap_pos = event.position
	elif event is InputEventScreenTouch and event.pressed:
		tap_pos = event.position
	if tap_pos != Vector2.INF:
		# 스크린 좌표 → 월드 좌표 (카메라 반영)
		_on_world_tap(get_viewport().get_canvas_transform().affine_inverse() * tap_pos)
		return
	# 키보드 상호작용 (스페이스/엔터) — 바라보는 방향의 대상
	if event.is_action_pressed("ui_accept"):
		_try_interact()

## 탭한 월드 좌표 근처에 상호작용 대상이 있으면 그쪽으로, 없으면 그 지점으로 이동.
func _on_world_tap(world_pos: Vector2) -> void:
	var hit := _find_interactable_at(world_pos)
	if hit != null:
		_target_interactable = hit
		_move_target = hit.global_position
	else:
		_target_interactable = null
		_move_target = world_pos
	_has_target = true

func _find_interactable_at(world_pos: Vector2) -> Node:
	var space := get_world_2d().direct_space_state
	var params := PhysicsShapeQueryParameters2D.new()
	var circle := CircleShape2D.new()
	circle.radius = 12.0
	params.shape = circle
	params.transform = Transform2D(0.0, world_pos)
	params.collide_with_bodies = true
	params.collide_with_areas = true
	for h: Dictionary in space.intersect_shape(params, 8):
		var c: Object = h.get("collider")
		if c != null and c != self and c.has_method("interact"):
			return c
	return null

func _try_interact() -> void:
	if not interact_ray.is_colliding():
		return
	var target = interact_ray.get_collider()
	if target and target.has_method("interact"):
		target.interact()

func face(dir_name: String) -> void:
	var col: int = DIR_FRAME.get(dir_name, 0)
	sprite.region_rect = Rect2(col * 16, 0, 16, 16)

func _face_toward(target_pos: Vector2) -> void:
	var d := target_pos - global_position
	if abs(d.x) > abs(d.y):
		_facing = Vector2.RIGHT if d.x > 0.0 else Vector2.LEFT
	else:
		_facing = Vector2.DOWN if d.y > 0.0 else Vector2.UP
	_update_sprite()

func _update_sprite() -> void:
	var dir_name := "down"
	if _facing.y < -0.5:    dir_name = "up"
	elif _facing.y > 0.5:   dir_name = "down"
	elif _facing.x < -0.5:  dir_name = "left"
	elif _facing.x > 0.5:   dir_name = "right"
	sprite.region_rect = Rect2(DIR_FRAME[dir_name] * 16, 0, 16, 16)
