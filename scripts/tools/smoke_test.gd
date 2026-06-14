extends Node
## 헤드리스 스모크 테스트 — 실제 autoload(DialogueManager/TrustManager)가
## 로드/작동하는지, 데이터 수정이 런타임을 깨뜨리지 않는지 검증.
## 실행: godot --headless --path . res://scripts/tools/smoke_test.tscn

func _ready() -> void:
	print("\n===== HEADLESS SMOKE TEST =====")
	var ok := true
	LanguageManager.current_locale = LanguageManager.DEFAULT_LOCALE
	TranslationServer.set_locale(LanguageManager.DEFAULT_LOCALE)
	DialogueManager._load_dialogues()

	# [1] 대화 데이터가 실제 엔진에서 파싱/로드되는가
	var n := DialogueManager.dialogues.size()
	print("[1] DialogueManager 로드: %d개 노드" % n)
	if n < 140:
		print("    X 노드 수 비정상"); ok = false

	# [2] 핵심 흐름 노드 존재
	for id in ["ch1_arrival", "ch5_final_choice", "ch5_resolve",
			"ch3_ratu_close_good_sign", "ch2_sela_no_referral"]:
		if not DialogueManager.dialogues.has(id):
			print("    X 핵심 노드 누락: %s" % id); ok = false

	# [3] 삭제한 죽은 노드가 실제로 사라졌는가
	for id in ["ch1_mere_farewell", "ch1_mere_revisit", "ch4_james_endorsed_neutral"]:
		if DialogueManager.dialogues.has(id):
			print("    X 삭제됐어야 할 노드 잔존: %s" % id); ok = false

	# [4] B2 수정 검증 — no_referral 이 양식 건네는 라인을 포함하는가
	var nr_lines := ""
	for l in DialogueManager.dialogues["ch2_sela_no_referral"].get("lines", []):
		nr_lines += l.get("text", "")
	if "양식" not in nr_lines:
		print("    X ch2_sela_no_referral 에 양식 언급 없음(B2 미반영)"); ok = false

	# [5] 엔딩 판정 — 실제 TrustManager.check_ending() 로직
	var keys := ["mere", "timoci", "ratu_josefa", "lani", "james"]
	for k in keys: TrustManager._trust[k] = 75
	var e_true := TrustManager.check_ending()
	print("[2] 엔딩 판정 (실제 로직):")
	print("    5명 75점        -> '%s'  (기대: true)" % e_true)
	if e_true != "true": ok = false
	TrustManager._trust["james"] = 40
	var e_norm := TrustManager.check_ending()
	print("    4명 70+         -> '%s'  (기대: normal)" % e_norm)
	if e_norm != "normal": ok = false
	TrustManager._trust["lani"] = 40
	TrustManager._trust["timoci"] = 40
	var e_bad := TrustManager.check_ending()
	print("    2명만 70+       -> '%s'  (기대: bad)" % e_bad)
	if e_bad != "bad": ok = false

	# [6] D3 검증 — 빈손 인사 점수가 12인가
	var basic: Dictionary = DialogueManager.dialogues["ch3_ratu_greet_basic"]
	var basic_pt: int = basic["choices"][0]["effects"]["ratu_josefa"]
	print("[3] 빈손 인사 점수: %d (기대: 12)" % basic_pt)
	if basic_pt != 12: ok = false

	# [7] 영어 대화 데이터도 같은 구조로 로드되는가
	LanguageManager.current_locale = "en"
	TranslationServer.set_locale("en")
	DialogueManager._load_dialogues()
	var en_n := DialogueManager.dialogues.size()
	print("[4] English dialogue load: %d nodes" % en_n)
	if en_n != n:
		print("    X English dialogue node count mismatch"); ok = false
	var en_intro := ""
	for l in DialogueManager.dialogues["ch1_arrival"].get("lines", []):
		en_intro += l.get("text", "")
	if "Suva, Fiji" not in en_intro:
		print("    X English ch1_arrival text not loaded"); ok = false

	# [8] 타이틀 화면 언어 선택 UI가 초기화되는가
	LanguageManager.current_locale = LanguageManager.DEFAULT_LOCALE
	TranslationServer.set_locale(LanguageManager.DEFAULT_LOCALE)
	var title_packed: PackedScene = load("res://scenes/ui/title_screen.tscn")
	var title_scene: Control = title_packed.instantiate()
	await get_tree().process_frame
	get_tree().root.add_child(title_scene)
	await get_tree().process_frame
	var subtitle_label: Label = title_scene.get_node("Subtitle")
	print("[5] Title language toggle: %s" % subtitle_label.text)
	if "EN" not in subtitle_label.text:
		print("    X title language toggle not initialized"); ok = false
	title_scene.queue_free()

	print("===== %s =====\n" % ("ALL PASS" if ok else "FAIL"))
	get_tree().quit(0 if ok else 1)
