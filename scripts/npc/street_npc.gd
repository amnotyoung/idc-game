extends CharacterBody2D
## 거리 NPC — 좌우 배회 + 인터랙션 시 인사

@export var dialogue_id: String = "bula_generic"
@export var walk_speed: float   = 22.0
@export var walk_range: float   = 32.0   # 시작 위치 기준 이동 반경

@onready var sprite: Sprite2D = $Sprite

const DIR_FRAME = {"down": 0, "left": 1, "right": 2, "up": 3}

var _start_x: float
var _dir: int       = 1   # 1=오른쪽, -1=왼쪽
var _wait_timer: float = 0.0
var _is_waiting: bool  = false
var _walk_timer: float = 0.0

func _ready() -> void:
	_start_x = global_position.x
	# 랜덤 출발 방향
	_dir = 1 if randf() > 0.5 else -1
	_walk_timer = randf_range(1.5, 3.5)
	add_to_group("npc")

func _physics_process(delta: float) -> void:
	if DialogueManager.is_active:
		velocity = Vector2.ZERO
		return

	if _is_waiting:
		_wait_timer -= delta
		velocity = Vector2.ZERO
		_set_sprite("down")
		if _wait_timer <= 0.0:
			_is_waiting = false
			_dir *= -1
			_walk_timer = randf_range(1.5, 3.5)
		return

	# 이동
	var next_x = global_position.x + _dir * walk_speed * delta
	if abs(next_x - _start_x) > walk_range:
		# 반대로 돌아섬
		_is_waiting = true
		_wait_timer = randf_range(0.5, 1.5)
		return

	velocity = Vector2(_dir * walk_speed, 0)
	_set_sprite("right" if _dir > 0 else "left")

	_walk_timer -= delta
	if _walk_timer <= 0.0:
		_is_waiting = true
		_wait_timer = randf_range(0.8, 2.0)

	move_and_slide()

func _set_sprite(dir_name: String) -> void:
	var col = DIR_FRAME.get(dir_name, 0)
	sprite.region_rect = Rect2(col * 16, 0, 16, 16)

func interact() -> void:
	_set_sprite("down")   # 플레이어 쪽 보기
	DialogueManager.start(dialogue_id)
