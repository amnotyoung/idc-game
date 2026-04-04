extends CharacterBody2D

@export var npc_id: String = ""
@export var dialogue_id: String = ""

const DIR_FRAME = {"down": 0, "left": 1, "right": 2, "up": 3}

@onready var sprite: Sprite2D = $Sprite

func face(dir_name: String) -> void:
	var col = DIR_FRAME.get(dir_name, 0)
	sprite.region_rect = Rect2(col * 16, 0, 16, 16)

func interact() -> void:
	if DialogueManager.is_active:
		return
	if dialogue_id == "":
		return
	DialogueManager.start(dialogue_id)
