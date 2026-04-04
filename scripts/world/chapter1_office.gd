extends Node

func _ready() -> void:
	# 씬 시작 시 오프닝 대화 자동 실행
	await get_tree().process_frame
	DialogueManager.start("ch1_arrival")
