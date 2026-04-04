extends Control

func _ready() -> void:
	if TrustManager.has_save():
		if TrustManager.has_flag("game_complete"):
			# 게임 완료 — 이어하기 대신 완료 표시
			$VBox/ContinueBtn.visible = false
		else:
			$VBox/ContinueBtn.visible = true
	else:
		$VBox/ContinueBtn.visible = false

func _on_new_game_pressed() -> void:
	TrustManager.clear_save()
	SceneManager.go_to("res://scenes/world/chapter1_office.tscn")

func _on_continue_pressed() -> void:
	# 마지막 진행 상태에 따라 적절한 씬으로 (역순 체크)
	if TrustManager.has_flag("ch4_sela_contacted") and TrustManager.has_flag("ch3_visited"):
		# Ch5 진입 조건 충족 — 사무실 경유해서 엔딩으로
		SceneManager.go_to("res://scenes/world/chapter1_office.tscn")
	elif TrustManager.has_flag("ch4_james_met"):
		SceneManager.go_to("res://scenes/world/suva_street.tscn")
	elif TrustManager.has_flag("ch3_visited"):
		SceneManager.go_to("res://scenes/world/suva_street.tscn")
	elif TrustManager.has_flag("ch2_timoci_met"):
		SceneManager.go_to("res://scenes/world/chapter1_office.tscn")
	elif TrustManager.has_flag("appointment_set"):
		SceneManager.go_to("res://scenes/world/suva_street.tscn")
	else:
		SceneManager.go_to("res://scenes/world/chapter1_office.tscn")
