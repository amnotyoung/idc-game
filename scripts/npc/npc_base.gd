extends CharacterBody2D

@export var npc_id: String = ""
@export var dialogue_id: String = ""

func interact() -> void:
	if DialogueManager.is_active:
		return
	if dialogue_id == "":
		return
	DialogueManager.start(dialogue_id)
