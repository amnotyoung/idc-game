extends Node

signal language_changed(locale: String)

const DEFAULT_LOCALE := "ko"
const SUPPORTED_LOCALES := ["ko", "en"]
const SETTINGS_PATH := "user://settings.json"

var current_locale: String = DEFAULT_LOCALE

const UI_TEXT := {
	"title_subtitle": {
		"ko": "나이탬바 섬 이야기",
		"en": "A Naitamba Island Story",
	},
	"title_new_game": {
		"ko": "새 게임",
		"en": "New Game",
	},
	"title_continue": {
		"ko": "이어하기",
		"en": "Continue",
	},
	"dialogue_back_q": {
		"ko": "이전(q)",
		"en": "Back(q)",
	},
	"dialogue_back_tooltip": {
		"ko": "뒤로 (Q)",
		"en": "Back (Q)",
	},
	"dialogue_back_mobile": {
		"ko": "이전",
		"en": "Back",
	},
	"hint_exit_up": {
		"ko": "▲ 나가기",
		"en": "▲ Exit",
	},
	"hint_exit_down": {
		"ko": "▼ 나가기",
		"en": "▼ Exit",
	},
	"hint_project_file": {
		"ko": "[사업파일]",
		"en": "[File]",
	},
	"hint_computer": {
		"ko": "[컴퓨터]",
		"en": "[PC]",
	},
	"hint_receptionist": {
		"ko": "접수처",
		"en": "Reception",
	},
	"hint_koda_office": {
		"ko": "▲ KODA 사무소",
		"en": "▲ KODA Office",
	},
	"hint_koda_meeting": {
		"ko": "▲ KODA 사무소 [회의]",
		"en": "▲ KODA Office [Meeting]",
	},
	"hint_government": {
		"ko": "▲ 정부청사",
		"en": "▲ Gov't",
	},
	"hint_intl_org": {
		"ko": "▲ 국제기구 사무소",
		"en": "▲ APAT Office",
	},
	"hint_harbor": {
		"ko": "▼ 항구 (나이탬바 섬)",
		"en": "▼ Harbor (Naitamba)",
	},
	"hint_dock_suva": {
		"ko": "▼ 선착장 (수바 행)",
		"en": "▼ Dock (to Suva)",
	},
	"sea_caption_suva_to_naitamba": {
		"ko": "수바에서 배로 2시간 — 나이탬바 섬",
		"en": "Two hours by boat from Suva — Naitamba Island",
	},
	"email_no_recipient": {
		"ko": "아직 보낼 사람이 없다. 먼저 이해관계자들을 만나야 한다.",
		"en": "There is no one to email yet. Meet the stakeholders first.",
	},
	"email_default_reply": {
		"ko": "에게서 답장이 왔다.",
		"en": " replied.",
	},
	"report_title": {
		"ko": "— 관계 성적표 —",
		"en": "— Relationship Report —",
	},
	"ending_true_label": {
		"ko": "True Ending — 마을이 주인이 되다",
		"en": "True Ending — The Village Takes Ownership",
	},
	"ending_normal_label": {
		"ko": "Normal Ending — 아직 갈 길이 남다",
		"en": "Normal Ending — There Is Still Work To Do",
	},
	"ending_bad_label": {
		"ko": "Bad Ending — 10년 전의 반복",
		"en": "Bad Ending — Ten Years Repeated",
	},
}

const EMAIL_REPLIES := {
	"mere": {
		"cold": {
			"ko": "에게 메일을 보냈다. 읽음 표시만 떴다.",
			"en": " was sent an email. Only a read receipt came back.",
		},
		"formal": {
			"ko": "에게서 답장이 왔다. \"확인했습니다.\"",
			"en": " replied: \"Received.\"",
		},
		"warm": {
			"ko": "에게서 답장이 왔다. \"고마워요. 현장 조사 결과 정리되면 공유할게요.\"",
			"en": " replied: \"Thanks. I'll share the field findings once they are organized.\"",
		},
		"ally": {
			"ko": "에게서 답장이 왔다. \"좋은 소식이네요! 다음 주에 만나서 같이 정리해요. ☺\"",
			"en": " replied: \"Good news! Let's meet next week and sort it out together. :)\"",
		},
	},
	"timoci": {
		"cold": {
			"ko": "에게 메일을 보냈다. 자동 부재중 답장이 돌아왔다.",
			"en": " was sent an email. An automatic out-of-office reply came back.",
		},
		"formal": {
			"ko": "에게서 답장이 왔다. \"수신 확인합니다.\"",
			"en": " replied: \"Receipt confirmed.\"",
		},
		"warm": {
			"ko": "에게서 답장이 왔다. \"서류 확인했습니다. 궁금한 점 있으면 연락주세요.\"",
			"en": " replied: \"I reviewed the documents. Contact me if you have questions.\"",
		},
		"ally": {
			"ko": "에게서 답장이 왔다. \"진전이 있네요. 장관 보고 일정 조율해볼게요.\"",
			"en": " replied: \"This is progress. I'll coordinate the ministerial briefing schedule.\"",
		},
	},
	"ratu_josefa": {
		"cold": {
			"ko": "에게 Lani를 통해 전달했다. 답이 없었다.",
			"en": " was reached through Lani. No answer came back.",
		},
		"formal": {
			"ko": "에게서 Lani를 통해 전달이 왔다. \"알겠소.\"",
			"en": " sent a message through Lani: \"Understood.\"",
		},
		"warm": {
			"ko": "에게서 Lani를 통해 전달이 왔다. \"다음에 올 때 양고나 가져오시오.\"",
			"en": " sent a message through Lani: \"Bring yaqona next time you come.\"",
		},
		"ally": {
			"ko": "에게서 Lani를 통해 전달이 왔다. \"마을 사람들도 기대하고 있소.\"",
			"en": " sent a message through Lani: \"The village is waiting too.\"",
		},
	},
	"lani": {
		"cold": {
			"ko": "에게 메일을 보냈다. 읽지 않은 것 같다.",
			"en": " was sent an email. It does not seem to have been read.",
		},
		"formal": {
			"ko": "에게서 답장이 왔다. \"네, 알겠어요.\"",
			"en": " replied: \"Okay, I understand.\"",
		},
		"warm": {
			"ko": "에게서 답장이 왔다. \"마을 사람들한테 전할게요. 고마워요.\"",
			"en": " replied: \"I'll tell the village. Thank you.\"",
		},
		"ally": {
			"ko": "에게서 답장이 왔다. \"Josua 삼촌이랑 교육 일정 논의 중이에요!\"",
			"en": " replied: \"I'm discussing the training schedule with Uncle Josua!\"",
		},
	},
	"james": {
		"cold": {
			"ko": "에게 메일을 보냈다. 답장이 없다.",
			"en": " was sent an email. There was no reply.",
		},
		"formal": {
			"ko": "에게서 답장이 왔다. \"Noted. Thanks.\"",
			"en": " replied: \"Noted. Thanks.\"",
		},
		"warm": {
			"ko": "에게서 답장이 왔다. \"APAT 쪽도 업데이트할게요. 진전 있으면 알려주세요.\"",
			"en": " replied: \"I'll update APAT as well. Let me know when there is progress.\"",
		},
		"ally": {
			"ko": "에게서 답장이 왔다. \"Great progress! 기술자 교육 커리큘럼 초안 보낼게요.\"",
			"en": " replied: \"Great progress! I'll send a draft technician training curriculum.\"",
		},
	},
}

func _ready() -> void:
	_load_settings()
	TranslationServer.set_locale(current_locale)

func set_locale(locale: String) -> void:
	if locale == current_locale:
		return
	if locale not in SUPPORTED_LOCALES:
		push_warning("Unsupported locale: " + locale)
		return
	current_locale = locale
	TranslationServer.set_locale(current_locale)
	_save_settings()
	language_changed.emit(current_locale)

func text(key: String) -> String:
	var entry: Dictionary = UI_TEXT.get(key, {})
	return entry.get(current_locale, entry.get(DEFAULT_LOCALE, key))

func email_reply(npc_id: String, tier: String) -> String:
	var npc_entry: Dictionary = EMAIL_REPLIES.get(npc_id, {})
	var tier_entry: Dictionary = npc_entry.get(tier, {})
	return tier_entry.get(current_locale, tier_entry.get(DEFAULT_LOCALE, text("email_default_reply")))

func is_english() -> bool:
	return current_locale == "en"

func _load_settings() -> void:
	if not FileAccess.file_exists(SETTINGS_PATH):
		return
	var file = FileAccess.open(SETTINGS_PATH, FileAccess.READ)
	if not file:
		return
	var json = JSON.new()
	if json.parse(file.get_as_text()) != OK:
		return
	var data = json.get_data()
	var saved_locale: String = data.get("language", DEFAULT_LOCALE)
	if saved_locale in SUPPORTED_LOCALES:
		current_locale = saved_locale

func _save_settings() -> void:
	var file = FileAccess.open(SETTINGS_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify({"language": current_locale}))
