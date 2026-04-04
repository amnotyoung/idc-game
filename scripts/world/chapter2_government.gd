extends Node

@onready var player: CharacterBody2D = get_parent().get_node("Player")
@onready var timoci: CharacterBody2D = get_parent().get_node("Timoci")
@onready var receptionist: CharacterBody2D = get_parent().get_node("Receptionist")

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)

	if not TrustManager.has_flag("appointment_set"):
		# 약속 없이 왔을 때 — 접수처가 돌려보냄
		DialogueManager.start("ch2_no_appointment")
	elif not TrustManager.has_flag("ch2_arrived"):
		DialogueManager.start("ch2_enter_building")
	elif not TrustManager.has_flag("ch2_timoci_met"):
		# 재방문 (노쇼 후)
		DialogueManager.start("ch2_second_visit_arrive")
	else:
		# 면담 완료 후 재방문 — Timoci 대사 업데이트
		timoci.dialogue_id = "ch2_timoci_after_good"

func _on_dialogue_ended(dialogue_id: String) -> void:
	match dialogue_id:
		"ch2_no_appointment":
			# 약속 없음 → 1.5초 후 거리로 복귀
			await get_tree().create_timer(1.5).timeout
			SceneManager.go_to_with_spawn(
				"res://scenes/world/suva_street.tscn",
				Vector2(217, 100)
			)
		"ch2_enter_building":
			TrustManager.set_flag("ch2_arrived")
			# 접수처로 이동 유도 — receptionist와 대화하도록
		"ch2_receptionist":
			# 잠시 후 대기실 서류 내레이션 자동 시작
			await get_tree().create_timer(1.2).timeout
			DialogueManager.start("ch2_waiting_note")
		"ch2_waiting_note":
			TrustManager.set_flag("ch2_saw_note")
			# Timoci 노쇼 트리거
			await get_tree().create_timer(1.0).timeout
			DialogueManager.start("ch2_timoci_noshow_1")
		"ch2_reschedule_ok", "ch2_reschedule_push":
			TrustManager.set_flag("ch2_first_visit_done")
			await get_tree().create_timer(1.5).timeout
			SceneManager.go_to_with_spawn(
				"res://scenes/world/suva_street.tscn",
				Vector2(217, 100)
			)
		"ch2_second_visit_arrive":
			TrustManager.set_flag("ch2_second_visit")
			receptionist.dialogue_id = "ch2_receptionist_2nd"
			await get_tree().create_timer(0.8).timeout
			DialogueManager.start("ch2_timoci_first")
		"ch2_timoci_progress", "ch2_timoci_collaborate":
			TrustManager.set_flag("ch2_timoci_met")
			TrustManager.set_flag("appointment_set")
			timoci.dialogue_id = "ch2_timoci_after_good"
		"ch2_timoci_pressure":
			TrustManager.set_flag("ch2_timoci_met")
			timoci.dialogue_id = "ch2_timoci_after_pressure"
		"ch2_timoci_frustrated":
			TrustManager.set_flag("ch2_timoci_met")
			timoci.dialogue_id = "ch2_timoci_after_frustrated"
