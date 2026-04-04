extends Control

func _ready() -> void:
	if TrustManager.has_save():
		$VBox/ContinueBtn.visible = true
	else:
		$VBox/ContinueBtn.visible = false

func _on_new_game_pressed() -> void:
	TrustManager.clear_save()
	SceneManager.go_to("res://scenes/world/chapter1_office.tscn")

func _on_continue_pressed() -> void:
	# 마지막 진행 상태에 따라 적절한 씬으로
	if TrustManager.has_flag("ch3_visited"):
		SceneManager.go_to("res://scenes/world/naitamba_island.tscn")
	elif TrustManager.has_flag("ch2_timoci_met"):
		SceneManager.go_to("res://scenes/world/chapter1_office.tscn")
	elif TrustManager.has_flag("appointment_set"):
		SceneManager.go_to("res://scenes/world/suva_street.tscn")
	else:
		SceneManager.go_to("res://scenes/world/chapter1_office.tscn")
