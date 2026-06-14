extends Node
## 5개 경로(A~E) 점수 밸런스 헤드리스 시뮬레이터.
## dialogue effects 는 실제 데이터에서 읽고, 핸들러 보너스(Sela 제출/보조 NPC/메일)는
## 최적 플레이 가정으로 더한 뒤, 실제 TrustManager.check_ending() 으로 판정한다.
## 실행: godot --headless --path . res://scripts/tools/balance_sim.tscn

const KEYS = ["mere", "timoci", "ratu_josefa", "lani", "james"]

# 각 경로 = dialogue 선택 스텝 [node_id, choice_idx] 들 + 핸들러/탐색 보너스
# choice_idx 는 raw choices 배열 인덱스(시뮬은 condition 무시, 경로 설계에 반영)
var PATHS := [
	{
		"name": "A. 정석 최적 (정부→섬→국제, 단서수집, 전부 협력)",
		"steps": [
			["ch1_mere_entrance", 0], ["ch1_mere_honest", 0], ["ch1_mere_warm_a", 0],
			["ch2_timoci_first", 0], ["ch2_timoci_ask_reason", 0], ["ch2_timoci_collaborate", 0],
			["ch3_mere_first", 0],
			["ch3_ratu_greet_prepared", 0], ["ch3_sevusevu_good", 0], ["ch3_sevusevu_reflect", 0],
			["ch3_village_talk", 0], ["ch3_lani_honest", 0],
			["ch3_mere_after_good", 0], ["ch3_lani_after", 0],
			["ch4_james_first", 0], ["ch4_james_history", 0], ["ch4_james_tltb", 0],
			["ch4_james_local_check", 0], ["ch4_james_endorsed", 0],
			["ch5_facilitate", 0], ["ch5_final_choice", 0],
		],
		"bonus": {"timoci": 15+3, "mere": 2+5+6, "ratu_josefa": 2+7+3, "lani": 4+5+3, "james": 3+3},
	},
	{
		"name": "B. 비선형 (섬 먼저, 단서 없이 honest)",
		"steps": [
			["ch1_mere_entrance", 0], ["ch1_mere_honest", 1], ["ch1_mere_warm_b", 0],
			["ch3_mere_first", 0],
			["ch3_ratu_greet_prepared", 0], ["ch3_sevusevu_good", 0], ["ch3_sevusevu_reflect", 0],
			["ch3_village_talk", 1], ["ch3_lani_honest", 0],
			["ch3_mere_after_good", 0], ["ch3_lani_after", 0],
			["ch2_timoci_first", 1], ["ch2_timoci_ask_reason", 0], ["ch2_timoci_collaborate", 0],
			["ch4_james_first", 0], ["ch4_james_history", 0], ["ch4_james_tltb", 0],
			["ch4_james_local_check", 0], ["ch4_james_endorsed", 1],
			["ch5_facilitate", 0], ["ch5_final_choice", 0],
		],
		"bonus": {"timoci": 15+3, "mere": 2+5+6, "ratu_josefa": 2+7+3, "lani": 4+5+3, "james": 3+3},
	},
	{
		"name": "C. APAT 단독 강행 후 마을 만회 (#3 핵심)",
		"steps": [
			["ch1_mere_entrance", 0], ["ch1_mere_honest", 0], ["ch1_mere_warm_a", 0],
			["ch2_timoci_first", 0], ["ch2_timoci_ask_reason", 0], ["ch2_timoci_collaborate", 0],
			# 국제기구 단독 강행 — 마을 신뢰 -8씩
			["ch4_james_first", 0], ["ch4_james_history", 0], ["ch4_james_tltb", 0],
			["ch4_james_local_check", 3], ["ch4_james_solo_tempt", 0],
			# 그 후 마을 풀코스로 만회
			["ch3_mere_first", 0],
			["ch3_ratu_greet_prepared", 0], ["ch3_sevusevu_good", 0], ["ch3_sevusevu_reflect", 0],
			["ch3_village_talk", 0], ["ch3_lani_honest", 0],
			["ch3_mere_after_good", 0], ["ch3_lani_after", 0],
			# 재방문 James good_news(+20) 로 endorsed 승격
			["ch4_james_after_neutral", 0],
			["ch5_facilitate", 0], ["ch5_final_choice", 0],
		],
		"bonus": {"timoci": 15+3, "mere": 2+5+6, "ratu_josefa": 2+7+3, "lani": 4+5+3, "james": 3+3},
	},
	{
		"name": "D. 평범한 협력 (차선 선택 다수)",
		"steps": [
			["ch1_mere_entrance", 1], ["ch1_mere_formal", 0], ["ch1_mere_cold_a", 1],
			["ch2_timoci_first", 1], ["ch2_timoci_ask_reason", 0], ["ch2_timoci_collaborate", 1],
			["ch3_mere_first", 1],
			["ch3_ratu_greet_prepared", 0], ["ch3_sevusevu_good", 1], ["ch3_sevusevu_reflect", 0],
			["ch3_village_talk", 1], ["ch3_lani_honest", 1],
			["ch3_lani_after", 1],
			["ch4_james_first", 1], ["ch4_james_skeptical", 0], ["ch4_james_tltb", 0],
			["ch4_james_local_check", 1],
			["ch5_facilitate", 1], ["ch5_final_choice", 1],
		],
		"bonus": {"timoci": 15, "mere": 3, "ratu_josefa": 4, "lani": 3, "james": 2},
	},
	{
		"name": "E. 단독 강행 + 만회 안 함 (위험 경로)",
		"steps": [
			["ch1_mere_entrance", 1], ["ch1_mere_formal", 1],
			["ch2_timoci_first", 3],
			["ch4_james_first", 2], ["ch4_james_direct", 1], ["ch4_james_tltb", 1],
			["ch4_james_local_check", 3], ["ch4_james_solo_tempt", 0],
			["ch5_facilitate", 1], ["ch5_final_choice", 1],
		],
		"bonus": {"timoci": 2, "mere": 0, "ratu_josefa": 0, "lani": 0, "james": 2},
	},
]

func _ready() -> void:
	print("\n===== 5개 경로 밸런스 시뮬레이션 =====")
	print("(effects=실제 데이터 / bonus=Sela제출·보조NPC·메일 최적가정 / 판정=실제 check_ending)\n")
	for path in PATHS:
		_reset()
		for step in path["steps"]:
			_apply(step[0], step[1])
		for npc in path.get("bonus", {}):
			_add(npc, path["bonus"][npc])
		_report(path["name"])
	print("\n핵심: C(단독 만회)가 'true' 면 #3 가 막다른길이 아님을 실증.")
	get_tree().quit()

func _reset() -> void:
	for k in TrustManager._trust:
		TrustManager._trust[k] = 0

func _add(npc: String, amount: int) -> void:
	if TrustManager._trust.has(npc):
		TrustManager._trust[npc] = clampi(TrustManager._trust[npc] + amount, 0, 100)

func _apply(node_id: String, idx: int) -> void:
	var node: Dictionary = DialogueManager.dialogues.get(node_id, {})
	var choices: Array = node.get("choices", [])
	if node.is_empty():
		push_warning("노드 없음: %s" % node_id)
		return
	if idx >= choices.size():
		push_warning("%s: choice[%d] 없음 (총 %d개)" % [node_id, idx, choices.size()])
		return
	var eff: Dictionary = choices[idx].get("effects", {})
	for npc in eff:
		_add(npc, int(eff[npc]))

func _report(pname: String) -> void:
	var parts := []
	var below := []
	for k in KEYS:
		var v: int = TrustManager.get_trust(k)
		parts.append("%s=%d" % [_short(k), v])
		if v < 70:
			below.append(_short(k))
	var ending: String = TrustManager.check_ending()
	var tag: String = {"true": "[TRUE]", "normal": "[NORMAL]", "bad": "[BAD]"}.get(ending, ending)
	print("%s" % pname)
	print("   %s" % "  ".join(parts))
	if below.is_empty():
		print("   → %s  (5명 전원 70+)\n" % tag)
	else:
		print("   → %s  (70미만: %s)\n" % [tag, ", ".join(below)])

func _short(k: String) -> String:
	var names := {"mere": "Mere", "timoci": "Vik", "ratu_josefa": "Ratu", "lani": "Lani", "james": "Jam"}
	return str(names.get(k, k))
