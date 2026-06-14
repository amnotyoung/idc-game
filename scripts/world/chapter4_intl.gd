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
			# James 출장 중 — 스프라이트 숨김 (접수처만 보임)
			james.visible = false
			var col = james.get_node_or_null("CollisionShape2D")
			if col:
				col.set_deferred("disabled", true)
			DialogueManager.start("ch4_no_connection")
	else:
		# 재방문 — James 결과에 따라 대사 분기
		receptionist.dialogue_id = "ch4_receptionist_after"
		if TrustManager.has_flag("ch4_consent_obtained"):
			# 동의서 획득 후
			james.dialogue_id = "ch4_james_after_consent"
		elif TrustManager.has_flag("ch4_james_endorsed"):
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
			# James에게 직접 다가가서 말 걸기
			james.dialogue_id = "ch4_james_first"
			receptionist.dialogue_id = "ch4_receptionist_after"
		"ch4_james_endorsed", "ch4_james_endorsed_detail", "ch4_james_endorsed_brief":
			TrustManager.set_flag("ch4_james_met")
			TrustManager.set_flag("ch4_tltb_contact")
			TrustManager.set_flag("ch4_james_endorsed")
			james.dialogue_id = "ch4_james_after_endorsed"
			receptionist.dialogue_id = "ch4_receptionist_after"
			TrustManager.save_game()
		"ch4_james_yangona_tip", "ch4_james_solo_path":
			# 단독 강행도 James 연결(tltb_contact)은 유지 → 마을 재방문으로 만회 가능
			TrustManager.set_flag("ch4_james_met")
			TrustManager.set_flag("ch4_tltb_contact")
			james.dialogue_id = "ch4_james_after_neutral"
			receptionist.dialogue_id = "ch4_receptionist_after"
			TrustManager.save_game()
		"ch4_james_good_news":
			# 재방문 시 Ratu 동의 보고 → endorsed로 승격
			TrustManager.set_flag("ch4_james_endorsed")
			james.dialogue_id = "ch4_james_after_consent"
			TrustManager.save_game()
		"ch4_james_rejected":
			TrustManager.set_flag("ch4_james_met")
			james.dialogue_id = "ch4_james_after_rejected"
			receptionist.dialogue_id = "ch4_receptionist_after"
			TrustManager.save_game()
