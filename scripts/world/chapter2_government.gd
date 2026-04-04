extends Node

@onready var player: CharacterBody2D = get_parent().get_node("Player")
@onready var timoci: CharacterBody2D = get_parent().get_node("Timoci")
@onready var receptionist: CharacterBody2D = get_parent().get_node("Receptionist")

const STREET_SCENE = "res://scenes/world/suva_street.tscn"
const STREET_SPAWN = Vector2(217, 100)

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)

	if not TrustManager.has_flag("appointment_set"):
		DialogueManager.start("ch2_no_appointment")
	elif not TrustManager.has_flag("ch2_arrived"):
		DialogueManager.start("ch2_enter_building")
	elif not TrustManager.has_flag("ch2_timoci_met"):
		DialogueManager.start("ch2_second_visit_arrive")
	else:
		# 면담 완료 후 재방문 — 결과에 따라 대사 분기
		if TrustManager.has_flag("ch2_meeting_frustrated"):
			timoci.dialogue_id = "ch2_timoci_after_frustrated"
		elif TrustManager.has_flag("ch2_meeting_pressure"):
			timoci.dialogue_id = "ch2_timoci_after_pressure"
		else:
			timoci.dialogue_id = "ch2_timoci_after_good"
		receptionist.dialogue_id = "ch2_receptionist_after"

func _exit_to_street(delay: float = 1.5) -> void:
	await get_tree().create_timer(delay).timeout
	SceneManager.go_to_with_spawn(STREET_SCENE, STREET_SPAWN)

func _on_dialogue_ended(dialogue_id: String) -> void:
	match dialogue_id:
		"ch2_no_appointment":
			_exit_to_street()
		"ch2_enter_building":
			TrustManager.set_flag("ch2_arrived")
		"ch2_receptionist":
			await get_tree().create_timer(1.2).timeout
			DialogueManager.start("ch2_waiting_note")
		"ch2_waiting_note":
			TrustManager.set_flag("ch2_saw_note")
			await get_tree().create_timer(1.0).timeout
			DialogueManager.start("ch2_timoci_noshow_1")
		"ch2_reschedule_ok", "ch2_reschedule_push":
			TrustManager.set_flag("ch2_first_visit_done")
			_exit_to_street()
		"ch2_second_visit_arrive":
			TrustManager.set_flag("ch2_second_visit")
			receptionist.dialogue_id = "ch2_receptionist_2nd"
			await get_tree().create_timer(0.8).timeout
			DialogueManager.start("ch2_timoci_first")
		"ch2_timoci_progress", "ch2_timoci_collaborate":
			TrustManager.set_flag("ch2_timoci_met")
			TrustManager.set_flag("appointment_set")
			timoci.dialogue_id = "ch2_timoci_after_good"
			TrustManager.save_game()
		"ch2_timoci_pressure":
			TrustManager.set_flag("ch2_timoci_met")
			TrustManager.set_flag("ch2_meeting_pressure")
			timoci.dialogue_id = "ch2_timoci_after_pressure"
			TrustManager.save_game()
		"ch2_timoci_frustrated":
			TrustManager.set_flag("ch2_timoci_met")
			TrustManager.set_flag("ch2_meeting_frustrated")
			timoci.dialogue_id = "ch2_timoci_after_frustrated"
			TrustManager.save_game()
