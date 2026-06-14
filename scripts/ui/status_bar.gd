extends CanvasLayer

@export var time_label: String = "2024.03"
@export var location_label: String = ""

@onready var context_label: Label = $Bar/Row/ContextLabel
@onready var stakeholders_box: HBoxContainer = $Bar/Row/Stakeholders

const LOCATION_BY_SCENE = {
	"res://scenes/world/chapter1_office.tscn": "KODA 사무소",
	"res://scenes/world/suva_street.tscn": "수바 거리",
	"res://scenes/world/government_building.tscn": "정부청사",
	"res://scenes/world/intl_org_office.tscn": "국제기구",
	"res://scenes/world/naitamba_island.tscn": "나이탬바",
	"res://scenes/world/ending_scene.tscn": "최종 협의",
}

const STAKEHOLDERS = [
	{"id": "mere", "short": "Mere", "name": "Mere"},
	{"id": "timoci", "short": "Vik", "name": "Vikash"},
	{"id": "ratu_josefa", "short": "Ratu", "name": "Ratu Josefa"},
	{"id": "lani", "short": "Lani", "name": "Lani"},
	{"id": "james", "short": "Jam", "name": "James"},
]

## 신뢰가 낮을 때(호의적 미만) tooltip 에 띄우는 부드러운 회복 힌트.
## 점수를 사람 등급으로 보지 않게, "다음에 해볼 행동"으로 안내한다.
const RECOVERY_HINTS = {
	"mere": "현장 조사 결과를 함께 정리하자고 해보세요.",
	"timoci": "토지청 동의서를 준비해 다시 찾아가 보세요.",
	"ratu_josefa": "섬 주민들의 이야기를 더 들어보세요.",
	"lani": "마을이 직접 관리하는 방안을 함께 이야기해보세요.",
	"james": "공동 기술자 교육 프로그램을 제안해보세요.",
}

var _chips: Dictionary = {}

func _ready() -> void:
	layer = 20
	if location_label == "":
		var scene_path := ""
		if get_tree().current_scene:
			scene_path = get_tree().current_scene.scene_file_path
		location_label = LOCATION_BY_SCENE.get(scene_path, "현재 위치")

	_build_chips()
	_refresh_context()
	_refresh_all()
	if not TrustManager.trust_changed.is_connected(_on_trust_changed):
		TrustManager.trust_changed.connect(_on_trust_changed)

func set_location(value: String) -> void:
	location_label = value
	_refresh_context()

func set_time(value: String) -> void:
	time_label = value
	_refresh_context()

func _build_chips() -> void:
	for child in stakeholders_box.get_children():
		stakeholders_box.remove_child(child)
		child.queue_free()
	_chips.clear()

	for item in STAKEHOLDERS:
		var chip := PanelContainer.new()
		chip.custom_minimum_size = Vector2(39, 12)
		chip.mouse_filter = Control.MOUSE_FILTER_PASS

		var label := Label.new()
		label.add_theme_font_size_override("font_size", 5)
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		label.clip_text = true
		chip.add_child(label)
		stakeholders_box.add_child(chip)
		_chips[item["id"]] = {"panel": chip, "label": label, "meta": item}

func _refresh_context() -> void:
	context_label.text = "%s | %s" % [time_label, location_label]

func _refresh_all() -> void:
	for item in STAKEHOLDERS:
		_refresh_chip(item["id"])

func _on_trust_changed(npc_id: String, _new_value: int) -> void:
	_refresh_chip(npc_id)

func _refresh_chip(npc_id: String) -> void:
	if not _chips.has(npc_id):
		return
	var entry: Dictionary = _chips[npc_id]
	var value := TrustManager.get_trust(npc_id)
	var tier := _tier_label(value)
	var label: Label = entry["label"]
	var panel: PanelContainer = entry["panel"]
	var meta: Dictionary = entry["meta"]

	# 최근 변화량 (이전 표시값 대비) — 만회 루프를 눈에 보이게
	var prev: int = entry.get("last", value)
	var delta := value - prev
	entry["last"] = value

	label.text = "%s %d" % [meta["short"], value]

	# tooltip: 이름·단계·점수 + 최근 변화 + (낮을 때) 회복 힌트
	var tip := "%s: %s (%d)" % [meta["name"], tier, value]
	if delta != 0:
		tip += "  최근 %+d" % delta
	if value < 50 and RECOVERY_HINTS.has(npc_id):
		tip += "\n→ " + RECOVERY_HINTS[npc_id]
	panel.tooltip_text = tip

	var style := StyleBoxFlat.new()
	style.bg_color = _tier_color(value)
	style.border_color = Color(1, 1, 1, 0.18)
	style.border_width_left = 1
	style.border_width_top = 1
	style.border_width_right = 1
	style.border_width_bottom = 1
	style.corner_radius_top_left = 2
	style.corner_radius_top_right = 2
	style.corner_radius_bottom_left = 2
	style.corner_radius_bottom_right = 2
	style.content_margin_left = 1
	style.content_margin_right = 1
	style.content_margin_top = 0
	style.content_margin_bottom = 0
	panel.add_theme_stylebox_override("panel", style)

	# 변화 시 잠깐 플래시 — "방금 한 선택이 관계에 영향을 줬다"는 즉각 피드백
	# 상승은 따뜻한 빛, 하락은 붉은 빛으로 짧게 빛났다가 원복
	if delta != 0:
		panel.modulate = Color(1.5, 1.5, 1.2) if delta > 0 else Color(1.7, 0.7, 0.7)
		var tw := panel.create_tween()
		tw.tween_property(panel, "modulate", Color(1, 1, 1), 0.5)

func _tier_label(value: int) -> String:
	if value >= 70:
		return "협력적"
	if value >= 50:
		return "호의적"
	if value >= 25:
		return "사무적"
	return "경계"

func _tier_color(value: int) -> Color:
	if value >= 70:
		return Color(0.12, 0.48, 0.28, 0.88)
	if value >= 50:
		return Color(0.18, 0.34, 0.62, 0.88)
	if value >= 25:
		return Color(0.38, 0.36, 0.31, 0.88)
	return Color(0.55, 0.20, 0.18, 0.88)
