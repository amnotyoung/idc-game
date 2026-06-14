extends Node
## 헤드리스 스모크 테스트 — 실제 autoload(DialogueManager/TrustManager)가
## 로드/작동하는지, 데이터 수정이 런타임을 깨뜨리지 않는지 검증.
## 실행: godot --headless --path . res://scripts/tools/smoke_test.tscn

func _ready() -> void:
	print("\n===== HEADLESS SMOKE TEST =====")
	var ok := true

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
	var basic := DialogueManager.dialogues["ch3_ratu_greet_basic"]
	var basic_pt: int = basic["choices"][0]["effects"]["ratu_josefa"]
	print("[3] 빈손 인사 점수: %d (기대: 12)" % basic_pt)
	if basic_pt != 12: ok = false

	print("===== %s =====\n" % ("ALL PASS" if ok else "FAIL"))
	get_tree().quit(0 if ok else 1)
