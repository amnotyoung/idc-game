extends StaticBody2D

@export var dialogue_id: String = ""

func interact() -> void:
	if DialogueManager.is_active:
		return
	if dialogue_id == "":
		return
	DialogueManager.start(dialogue_id)
