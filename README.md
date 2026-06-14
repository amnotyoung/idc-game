# Aid World

피지(Fiji)를 배경으로 한 **국제개발협력(IDC) 내러티브 게임**입니다. 플레이어는 수자원 개발 사업의 담당자가 되어, 수바(Suva)의 정부·국제기구와 나이탬바(Naitamba) 섬 주민들 사이를 오가며 **신뢰·협력·주민 주체성**의 가치를 배워 나갑니다.

> 단순히 "올바른 선물을 사 가는" 게임이 아닙니다. 점수는 대화에서의 **태도**(경청, 협력, 솔직함)로 결정되며, 어떤 순서로 누구를 만나든 최선의 결말에 도달할 수 있습니다.

## 게임 개요

| | |
|---|---|
| **장르** | 탑다운 2D 내러티브 어드벤처 |
| **엔진** | Godot 4.6 (GL Compatibility) |
| **언어** | 한국어 |
| **해상도** | 320×180 픽셀아트 (1280×720 출력) |
| **플레이 시간** | 약 1~2시간 |
| **배경** | 피지 수바 + 나이탬바 섬 (Lomaiviti 주 외곽 섬 모티브) |

## 주요 특징

- **비선형 진행** — 수바 거리 → 정부청사 → 국제기구 → 나이탬바를 어떤 순서로든 방문할 수 있고, 어떤 경로로도 True 엔딩에 도달할 수 있습니다.
- **태도 기반 신뢰 시스템** — 5명의 이해관계자(Mere·Vikash·Sela·James·Ratu Josefa·Lani)와의 신뢰도가 대화 선택지의 태도로 쌓이며, 엔딩을 결정합니다.
- **만회 메커닉** — 실수해도 이메일·NPC 대화 보너스로 신뢰를 회복할 수 있어, 한 번의 잘못된 선택이 게임을 막지 않습니다.
- **현실적 묘사** — 피지는 상위중소득국이라는 사실에 기반해, 빈곤을 과장하지 않고 "기존 인프라 유지보수 부재"라는 실제 개발협력의 문제를 다룹니다.

## 등장인물

| 이름 | 소속 | 역할 |
|------|------|------|
| 주인공 | KODA | 플레이어 (성별 중립) |
| Mere | Pacific Roots NGO | 현장 활동가 |
| Vikash | 국가계획부 | ODA 심사 |
| Sela | 토지청 | 토지 동의 |
| James | APAT | 기술자문 |
| Ratu Josefa | 나이탬바 마을 | 추장 |
| Lani | 나이탬바 마을 | 청년회 리더 |
| Wati | KODA | 현지 직원 (튜토리얼) |

## 실행 방법

1. [Godot Engine 4.6](https://godotengine.org/download) 이상을 설치합니다.
2. 이 저장소를 클론합니다.
   ```bash
   git clone https://github.com/amnotyoung/idc-game.git
   ```
3. Godot에서 `project.godot`를 열고 실행(F5)합니다.

## itch.io 웹 빌드

Godot CLI와 `curl`, `unzip`, `zip`이 설치된 환경에서 아래 명령을 실행하면 itch.io HTML 게임 업로드용 ZIP을 생성합니다.

```bash
scripts/tools/build_itch_web.sh
```

생성 파일:

```bash
builds/aid-world-itch-web.zip
```

스크립트는 현재 Godot 버전에 맞는 Web no-threads export template을 내려받아 `/tmp`에 캐시하고, `index.html`이 ZIP 최상위에 오도록 패키징합니다. itch.io에서는 `Kind of project`를 `HTML`로 설정하고, 업로드 파일에 `This file will be played in the browser`를 체크하면 됩니다.

## 프로젝트 구조

```
scripts/
  systems/   — trust_manager, dialogue_manager, scene_manager
  player/    — player.gd (걷기/달리기, Shift 토글)
  npc/       — npc_base, street_npc
  ui/        — dialogue_box, title_screen
  world/     — 챕터별 월드 로직 (office / government / island / intl / ending)
  tools/     — PIL 기반 배경·스프라이트 생성기

data/dialogues/  — chapter1~5.json, street_npcs.json (대화 데이터)

scenes/
  ui/        — title_screen, dialogue_box
  world/     — chapter1_office, government_building, naitamba_island,
                intl_org_office, suva_street, ending_scene

docs/design/  — story, characters, 레퍼런스 자료
```

## 크레딧

- 일부 스프라이트는 [Kenney](https://kenney.nl/) 에셋을 기반으로 제작되었습니다.
- 웹 빌드의 한글 UI 표시에 [Nanum Gothic](https://fonts.google.com/specimen/Nanum+Gothic)을 사용합니다. 폰트는 SIL Open Font License 1.1로 배포됩니다.
- 본 게임은 국제개발협력의 가치를 전달하기 위한 교육·창작 목적의 프로젝트입니다.
