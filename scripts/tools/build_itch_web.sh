#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GODOT_BIN="${GODOT_BIN:-godot}"

GODOT_VERSION_RAW="$("$GODOT_BIN" --version | awk '{print $1}')"
GODOT_VERSION="${GODOT_VERSION_RAW%%.stable*}"
RELEASE_TAG="${GODOT_VERSION}-stable"
TEMPLATE_ARCHIVE="Godot_v${GODOT_VERSION}-stable_export_templates.tpz"
TEMPLATE_URL="https://github.com/godotengine/godot/releases/download/${RELEASE_TAG}/${TEMPLATE_ARCHIVE}"

TMP_BASE="${TMPDIR:-/tmp}"
TMP_BASE="${TMP_BASE%/}"
CACHE_DIR="${CACHE_DIR:-${TMP_BASE}/godot-${GODOT_VERSION}-web-templates}"
TEMPLATE_DIR="${CACHE_DIR}/templates"
EXPORT_DIR="${EXPORT_DIR:-${TMP_BASE}/aid-world-itch-web}"
ZIP_PATH="${ZIP_PATH:-${PROJECT_ROOT}/builds/aid-world-itch-web.zip}"
PRESET_FILE="${PROJECT_ROOT}/export_presets.cfg"
BACKUP_PRESET=""

restore_preset() {
	if [[ -n "$BACKUP_PRESET" && -f "$BACKUP_PRESET" ]]; then
		mv "$BACKUP_PRESET" "$PRESET_FILE"
	else
		rm -f "$PRESET_FILE"
	fi
}

if [[ -f "$PRESET_FILE" ]]; then
	BACKUP_PRESET="$(mktemp "${TMP_BASE}/aid-world-export-presets.XXXXXX")"
	cp "$PRESET_FILE" "$BACKUP_PRESET"
fi
trap restore_preset EXIT

if [[ ! -f "${TEMPLATE_DIR}/web_nothreads_release.zip" || ! -f "${TEMPLATE_DIR}/web_nothreads_debug.zip" ]]; then
	mkdir -p "$CACHE_DIR"
	echo "Downloading Godot ${GODOT_VERSION} export templates..."
	curl -L -f -o "${CACHE_DIR}/${TEMPLATE_ARCHIVE}" "$TEMPLATE_URL"
	unzip -q "${CACHE_DIR}/${TEMPLATE_ARCHIVE}" \
		templates/web_nothreads_release.zip \
		templates/web_nothreads_debug.zip \
		-d "$CACHE_DIR"
fi

cat > "$PRESET_FILE" <<EOF
[preset.0]

name="Web"
platform="Web"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter="builds/**,scripts/tools/**"
export_path="${EXPORT_DIR}/index.html"
patches=PackedStringArray()
encryption_include_filters=""
encryption_exclude_filters=""
encrypt_pck=false
encrypt_directory=false
script_export_mode=2

[preset.0.options]

custom_template/debug="${TEMPLATE_DIR}/web_nothreads_debug.zip"
custom_template/release="${TEMPLATE_DIR}/web_nothreads_release.zip"
variant/extensions_support=false
variant/thread_support=false
vram_texture_compression/for_desktop=true
vram_texture_compression/for_mobile=false
html/export_icon=true
html/custom_html_shell=""
html/head_include=""
html/canvas_resize_policy=2
html/focus_canvas_on_start=true
html/experimental_virtual_keyboard=false
progressive_web_app/enabled=false
progressive_web_app/ensure_cross_origin_isolation_headers=false
progressive_web_app/offline_page=""
progressive_web_app/display=1
progressive_web_app/orientation=2
progressive_web_app/icon_144x144=""
progressive_web_app/icon_180x180=""
progressive_web_app/icon_512x512=""
progressive_web_app/background_color=Color(0, 0, 0, 1)
EOF

rm -rf "$EXPORT_DIR"
mkdir -p "$EXPORT_DIR" "$(dirname "$ZIP_PATH")"

"$GODOT_BIN" --headless --path "$PROJECT_ROOT" --import --quit
"$GODOT_BIN" --headless --path "$PROJECT_ROOT" --export-release Web "${EXPORT_DIR}/index.html"

(
	cd "$EXPORT_DIR"
	zip -r "$ZIP_PATH" .
)

unzip -t "$ZIP_PATH"
echo "Built itch.io web ZIP: $ZIP_PATH"
