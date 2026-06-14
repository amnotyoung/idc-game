extends Control

@onready var subtitle: Label = $Subtitle
@onready var new_game_btn: Button = $VBox/NewGameBtn
@onready var continue_btn: Button = $VBox/ContinueBtn

var _continue_available := false

func _ready() -> void:
	LanguageManager.language_changed.connect(_refresh_texts)
	subtitle.mouse_filter = Control.MOUSE_FILTER_STOP
	subtitle.gui_input.connect(_on_subtitle_gui_input)
	_continue_available = TrustManager.has_save() and not TrustManager.has_flag("game_complete")
	if _continue_available:
		continue_btn.pressed.connect(_on_continue_pressed)
	continue_btn.visible = _continue_available
	_refresh_texts(LanguageManager.current_locale)

func _refresh_texts(_locale: String) -> void:
	var toggle_text := "EN" if LanguageManager.current_locale == "ko" else "한국어"
	subtitle.text = "%s  %s" % [LanguageManager.text("title_subtitle"), toggle_text]
	new_game_btn.text = LanguageManager.text("title_new_game")
	continue_btn.text = LanguageManager.text("title_continue")

func _on_language_toggle_pressed() -> void:
	var next_locale := "en" if LanguageManager.current_locale == "ko" else "ko"
	LanguageManager.set_locale(next_locale)

func _on_subtitle_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_on_language_toggle_pressed()
	elif event is InputEventScreenTouch and event.pressed:
		_on_language_toggle_pressed()

func _on_new_game_pressed() -> void:
	TrustManager.clear_save()
	SceneManager.go_to("res://scenes/world/chapter1_office.tscn")

func _on_continue_pressed() -> void:
	# 마지막 진행 상태에 따라 적절한 씬으로 (역순 체크)
	if TrustManager.has_flag("ch4_consent_submitted"):
		# 동의서 제출 완료 — 사무실 경유해서 엔딩으로
		SceneManager.go_to("res://scenes/world/chapter1_office.tscn")
	elif TrustManager.has_flag("ch4_consent_obtained"):
		# Ratu 서명 받음 — 정부청사 Sela에게 제출해야
		SceneManager.go_to("res://scenes/world/suva_street.tscn")
	elif TrustManager.has_flag("ch4_sela_contacted"):
		# Sela 만남 완료 — 나이탬바 가서 서명 받아야
		SceneManager.go_to("res://scenes/world/suva_street.tscn")
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
