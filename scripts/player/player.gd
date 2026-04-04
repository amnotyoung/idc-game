extends CharacterBody2D

const SPEED = 80.0

@onready var interact_ray: RayCast2D = $InteractRay
@onready var sprite: Sprite2D = $Sprite

# 스프라이트시트 열 순서: 0=하, 1=좌, 2=우, 3=상
const DIR_FRAME = {
	"down":  0,
	"left":  1,
	"right": 2,
	"up":    3,
}

var _facing: Vector2 = Vector2.DOWN

func _physics_process(_delta: float) -> void:
	if DialogueManager.is_active:
		velocity = Vector2.ZERO
		return

	var direction := Vector2(
		Input.get_axis("ui_left", "ui_right"),
		Input.get_axis("ui_up", "ui_down")
	).normalized()

	if direction != Vector2.ZERO:
		_facing = direction
		interact_ray.target_position = _facing * 14.0
		_update_sprite()

	velocity = direction * SPEED
	move_and_slide()

func _update_sprite() -> void:
	var dir_name := "down"
	if _facing.y < -0.5:    dir_name = "up"
	elif _facing.y > 0.5:   dir_name = "down"
	elif _facing.x < -0.5:  dir_name = "left"
	elif _facing.x > 0.5:   dir_name = "right"
	var col: int = DIR_FRAME[dir_name]
	sprite.region_rect = Rect2(col * 16, 0, 16, 16)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		_try_interact()

func _try_interact() -> void:
	if not interact_ray.is_colliding():
		return
	var target = interact_ray.get_collider()
	if target and target.has_method("interact"):
		target.interact()
