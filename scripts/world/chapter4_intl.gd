extends Node

@onready var player: CharacterBody2D = get_parent().get_node("Player")
@onready var james: CharacterBody2D = get_parent().get_node("James")
@onready var receptionist: CharacterBody2D = get_parent().get_node("Receptionist")

const STREET_SCENE = "res://scenes/world/suva_street.tscn"
const STREET_SPAWN = Vector2(290, 100)

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)

	if not TrustManager.has_flag("ch4_visited"):
		# 정부청사 연결 OR 섬 주민 신뢰(good ending) 중 하나면 입장 가능
		var has_referral = TrustManager.has_flag("ch2_timoci_met")
		var has_community = TrustManager.has_flag("ch3_good_ending")
		if has_referral or has_community:
			DialogueManager.start("ch4_receptionist_intro")
		else:
			DialogueManager.start("ch4_no_connection")
	else:
		# 재방문 — James 결과에 따라 대사 분기
		receptionist.dialogue_id = "ch4_receptionist_after"
		if TrustManager.has_flag("ch4_james_endorsed"):
			james.dialogue_id = "ch4_james_after_endorsed"
		elif TrustManager.has_flag("ch4_tltb_contact"):
			james.dialogue_id = "ch4_james_after_neutral"
		else:
			james.dialogue_id = "ch4_james_after_rejected"

func _exit_to_street(delay: float = 1.5) -> void:
	await get_tree().create_timer(delay).timeout
	SceneManager.go_to_with_spawn(STREET_SCENE, STREET_SPAWN)

func _on_dialogue_ended(dialogue_id: String) -> void:
	match dialogue_id:
		"ch4_no_connection":
			_exit_to_street()
		"ch4_receptionist_intro":
			TrustManager.set_flag("ch4_visited")
			await get_tree().create_timer(0.8).timeout
			DialogueManager.start("ch4_james_first")
		"ch4_james_endorsed":
			TrustManager.set_flag("ch4_james_met")
			TrustManager.set_flag("ch4_tltb_contact")
			TrustManager.set_flag("ch4_james_endorsed")
			james.dialogue_id = "ch4_james_after_endorsed"
			receptionist.dialogue_id = "ch4_receptionist_after"
			TrustManager.save_game()
		"ch4_james_endorsed_neutral":
			TrustManager.set_flag("ch4_james_met")
			TrustManager.set_flag("ch4_tltb_contact")
			james.dialogue_id = "ch4_james_after_neutral"
			receptionist.dialogue_id = "ch4_receptionist_after"
			TrustManager.save_game()
		"ch4_james_rejected":
			TrustManager.set_flag("ch4_james_met")
			james.dialogue_id = "ch4_james_after_rejected"
			receptionist.dialogue_id = "ch4_receptionist_after"
			TrustManager.save_game()
