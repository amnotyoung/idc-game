extends CharacterBody2D

const SPEED = 80.0

# 상호작용 감지 범위 (플레이어 앞쪽)
@onready var interact_ray: RayCast2D = $InteractRay

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

	velocity = direction * SPEED
	move_and_slide()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		_try_interact()

func _try_interact() -> void:
	if not interact_ray.is_colliding():
		return
	var target = interact_ray.get_collider()
	if target and target.has_method("interact"):
		target.interact()
