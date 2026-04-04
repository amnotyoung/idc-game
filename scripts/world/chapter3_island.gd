extends Node

@onready var ratu: CharacterBody2D = get_parent().get_node("RatuJosefa")
@onready var lani: CharacterBody2D = get_parent().get_node("Lani")

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)

	if not TrustManager.has_flag("ch3_arrived"):
		# 첫 방문 — 세부세부 전까지 Lani와 대화 불가
		lani.dialogue_id = ""
		DialogueManager.start("ch3_arrive")
	elif TrustManager.has_flag("ch3_visited"):
		# 재방문 — 결말에 따라 복원
		if TrustManager.has_flag("ch3_good_ending"):
			ratu.dialogue_id = "ch3_ratu_after"
			lani.dialogue_id = "ch3_lani_after"
		else:
			ratu.dialogue_id = "ch3_ratu_after_neutral"
			lani.dialogue_id = ""
	else:
		# ch3_arrived는 됐지만 ch3_visited는 아직 — 중간 재진입
		lani.dialogue_id = "ch3_village_talk"

func _on_dialogue_ended(dialogue_id: String) -> void:
	match dialogue_id:
		"ch3_arrive":
			TrustManager.set_flag("ch3_arrived")
			await get_tree().create_timer(0.5).timeout
			if TrustManager.has_flag("sevusevu_prepared"):
				DialogueManager.start("ch3_ratu_greet_prepared")
			else:
				DialogueManager.start("ch3_ratu_greet_basic")
		"ch3_sevusevu_good", "ch3_sevusevu_miss":
			# 이제 Lani와 대화 가능
			lani.dialogue_id = "ch3_village_talk"
		"ch3_lani_deflect":
			TrustManager.set_flag("ch3_visited")
			ratu.dialogue_id = ""
			lani.dialogue_id = ""
		"ch3_ratu_close_good":
			TrustManager.set_flag("ch3_visited")
			TrustManager.set_flag("ch3_good_ending")
			ratu.dialogue_id = "ch3_ratu_after"
			lani.dialogue_id = "ch3_lani_after"
		"ch3_ratu_close_neutral":
			TrustManager.set_flag("ch3_visited")
			ratu.dialogue_id = "ch3_ratu_after_neutral"
			lani.dialogue_id = ""
