extends Node

@onready var mere: CharacterBody2D   = get_parent().get_node("Mere")
@onready var player: CharacterBody2D = get_parent().get_node("Player")

func _ready() -> void:
	await get_tree().process_frame
	# 오프닝 내레이션 시작
	DialogueManager.dialogue_ended.connect(_on_opening_ended, CONNECT_ONE_SHOT)
	DialogueManager.start("ch1_arrival")

func _on_opening_ended() -> void:
	# 오프닝 끝 → Mere가 문에서 플레이어 쪽으로 걸어옴
	var target = Vector2(player.position.x + 22, player.position.y - 18)
	var tween = get_tree().create_tween()
	tween.tween_property(mere, "position", target, 1.8)\
		 .set_trans(Tween.TRANS_LINEAR)
	tween.tween_callback(_start_mere_dialogue)

func _start_mere_dialogue() -> void:
	DialogueManager.start("ch1_mere_entrance")
