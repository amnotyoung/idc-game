extends Node

@onready var ratu: CharacterBody2D = get_parent().get_node("RatuJosefa")
@onready var lani: CharacterBody2D = get_parent().get_node("Lani")
@onready var mere: CharacterBody2D = get_parent().get_node("Mere")

func _ready() -> void:
	await get_tree().process_frame
	DialogueManager.dialogue_ended.connect(_on_dialogue_ended)

	if not TrustManager.has_flag("ch3_arrived"):
		# 첫 방문 — 세부세부 전까지 Lani와 대화 불가
		lani.dialogue_id = ""
		mere.dialogue_id = "ch3_mere_first"
		if TrustManager.has_flag("ch2_timoci_met"):
			DialogueManager.start("ch3_arrive")
		else:
			# 정부청사 안 가고 섬부터 온 경우
			DialogueManager.start("ch3_arrive_early")
	elif TrustManager.has_flag("ch3_visited"):
		# 재방문 — 동의서 or 일반 복원
		if TrustManager.has_flag("ch4_consent_obtained"):
			# 동의서 이미 완료
			ratu.dialogue_id = "ch3_consent_done"
			lani.dialogue_id = "ch3_lani_after"
			mere.dialogue_id = "ch3_mere_consent"
		elif TrustManager.has_flag("ch4_sela_contacted") and TrustManager.has_flag("ch3_good_ending"):
			# Sela 통화 완료 + good ending → 동의서 서명 가능
			ratu.dialogue_id = "ch3_consent_ratu"
			lani.dialogue_id = "ch3_lani_after"
			mere.dialogue_id = "ch3_mere_after_good"
		elif TrustManager.has_flag("ch4_sela_contacted") and not TrustManager.has_flag("ch3_good_ending"):
			# Sela 통화 완료 + neutral ending → Ratu가 서명 거부
			ratu.dialogue_id = "ch3_consent_ratu_neutral"
			lani.dialogue_id = ""
			mere.dialogue_id = "ch3_mere_after_neutral"
		elif TrustManager.has_flag("ch3_good_ending"):
			ratu.dialogue_id = "ch3_ratu_after"
			lani.dialogue_id = "ch3_lani_after"
			mere.dialogue_id = "ch3_mere_after_good"
		else:
			ratu.dialogue_id = "ch3_ratu_after_neutral"
			lani.dialogue_id = ""
			mere.dialogue_id = "ch3_mere_after_neutral"
	else:
		# ch3_arrived는 됐지만 ch3_visited는 아직 — 중간 재진입
		lani.dialogue_id = "ch3_village_talk"
		mere.dialogue_id = "ch3_mere_after_ratu"

func _on_dialogue_ended(dialogue_id: String) -> void:
	match dialogue_id:
		"ch3_arrive", "ch3_arrive_early":
			TrustManager.set_flag("ch3_arrived")
			# Mere와 먼저 대화할 수 있도록 자유 이동 — Ratu는 직접 다가가야 대화
			if TrustManager.has_flag("sevusevu_prepared"):
				ratu.dialogue_id = "ch3_ratu_greet_prepared"
			else:
				ratu.dialogue_id = "ch3_ratu_greet_basic"
		"ch3_sevusevu_good", "ch3_sevusevu_miss":
			# 이제 Lani와 대화 가능
			lani.dialogue_id = "ch3_village_talk"
		"ch3_lani_deflect":
			TrustManager.set_flag("ch3_visited")
			ratu.dialogue_id = ""
			lani.dialogue_id = ""
			TrustManager.save_game()
		"ch3_ratu_close_good":
			TrustManager.set_flag("ch3_visited")
			TrustManager.set_flag("ch3_good_ending")
			ratu.dialogue_id = "ch3_ratu_after"
			lani.dialogue_id = "ch3_lani_after"
			TrustManager.save_game()
		"ch3_ratu_close_neutral":
			TrustManager.set_flag("ch3_visited")
			ratu.dialogue_id = "ch3_ratu_after_neutral"
			lani.dialogue_id = ""
			TrustManager.save_game()
		"ch3_consent_sign":
			TrustManager.set_flag("ch4_consent_obtained")
			ratu.dialogue_id = "ch3_consent_done"
			mere.dialogue_id = "ch3_mere_consent"
			TrustManager.save_game()
