extends Node

signal accept_pressed
signal back_pressed

var move_vector: Vector2 = Vector2.ZERO

func set_move_vector(value: Vector2) -> void:
	move_vector = value.limit_length(1.0)

func clear_move_vector() -> void:
	move_vector = Vector2.ZERO

func press_accept() -> void:
	accept_pressed.emit()

func press_back() -> void:
	back_pressed.emit()
