# 변경 및 검증 보고서

기준일: 2026-11-06. 원격 main HEAD `eb4ff29cafa8cceba238b9d8f81ebaf660a5b904`를 새 작업 폴더에 복제했습니다. 최초 작업 트리는 깨끗했고 사용자 변경은 없었습니다. 초기 수정 단계에서는 원격 게시·push·PR·merge·커밋을 수행하지 않았습니다. 이후 사용자의 GitHub 업로드 요청에 따라 게시 전 원격을 재확인하고 main 커밋·push를 진행합니다. 실제 게시 SHA는 GitHub 커밋 이력과 최종 게시 결과를 확인합니다.

## 단계별 결과

| 단계 | 결과 | 변경과 확인 |
| --- | --- | --- |
| 1. 공통 원칙·라우팅 | 완료 | AGENTS·README·routing 역할 분리, 수업 입출력·통과 기준 문서, 설명용 TOML 구분 |
| 2. Skill·설치 | 수정 완료; 일부 수동 검증 미실행 | 10개 YAML, 프로젝트 기본·전역 선택, 사전 검사·충돌 보존·해시·백업·롤백·CODEX_HOME; 실제 목록 10개 발견 |
| 3. 기획 정합성 | 완료 | 요구사항·기능·MVP·신규 구조 템플릿, 추적·예외·데이터·품질·미정·단계 판정; 복사용 프롬프트 내부에 기준 포함 |
| 4. 구현·검증 | 완료 | 입력 422 통일, 업로드 계약, google-genai, 제한 재시도·실패 종료·외부 작업 원장; 실제/미실행 기록 |
| 5. 환경 기준 | 완료; 강사 결정 대기 | Codex/MCP/Python/Node 필수·선택 분리; 모델·서버·수업 버전 미정 유지 |
| 6. 후반·협업 | 완료 | 선택 RAG·LangGraph·MCP/Gmail, PR·리뷰·발표·기여 근거·로그 가림 |
| 7. 대표 예제 | 모의 검증 완료; 실제 모델 평가 미실행 | 회의록 예제 계약, 안전한 API·Workflow, 자동 검사와 실제 Skill 목록 확인 |

## 자동 검증: 15개 통과, 실패 0개

명령(Kit 루트): `python scripts/verify.py --api --codex-discovery`.

- Skill metadata·템플릿 참조, 로컬 Markdown 링크
- 프로젝트 dry-run·설치·동일 재설치(변경 0개)·사용자 수정 충돌 보존
- 기존 전역 AGENTS.md/config.toml과 다른 Skill 보존
- CODEX_HOME 실제 CLI 설치 위치
- 프로젝트·전역 설치본의 환경 점검기를 설치 폴더에서 실행(원본 Kit·추가 의존성 불필요)
- 파일 충돌이 뒤에서 발견돼도 전체 쓰기 전에 중단
- 관리 파일 정상 업그레이드와 원본 백업
- 설치 중 오류 주입 후 파일·manifest 롤백
- 소스 누락 시 대상 변경 없음
- 모의 API: 정상 200 및 필드, 누락·빈 문자열·공백·숫자·null 모두 422, 제공자 타임아웃·연결 실패·정규화된 제공자 오류·잘못된 응답 구조는 502, 예상하지 못한 내부 오류는 500이며 원래 오류 내용 비노출
- 문서의 Pydantic Schema 두 예제와 실행 예제의 schema 일치
- 재시도 한도 도달 종료·첫 성공 종료, 성공 작업 재요청과 결과 불확실 작업의 재실행 방지

별도로 로컬 공식 `skill-creator/scripts/quick_validate.py`를 `python -X utf8`로 실행하여 Skill 10개 모두 유효함을 확인했습니다. 이 검증기는 기본 Windows 인코딩에서 한국어를 읽지 못해 UTF-8 모드를 사용했습니다.

실제 Codex app-server의 `initialize` → `skills/list`를 사용했습니다. 새 프로젝트 경로의 enabled Skill 10개와 오류 0개를 확인했습니다. 스레드나 모델 turn은 생성하지 않았습니다. 기존 사용자 전역 `.codex/skills/`에는 이전 YAML 없는 Skill 10개의 경고가 별도로 나타났으며 변경하지 않았습니다. 기존 설치 사용자는 새 프로젝트 범위로 먼저 검증하거나 전역 충돌 파일을 검토해야 합니다.

PowerShell 래퍼의 dry-run·설치·재설치, Windows Git Bash의 문법 검사·dry-run·설치·재설치가 통과했습니다. Git Bash는 Windows의 실행 불가능한 python3 별칭을 발견하여 유효한 python으로 대체하도록 고쳤습니다. 이 결과는 실제 macOS/Linux 통과를 의미하지 않습니다.

## 환경과 실행 제약

Windows 11 / Python 3.14.6 / Codex CLI 0.142.4 / Git 2.55.0.windows.1 / PowerShell 7.6.5. 모의 API 검증은 FastAPI 0.141.1 / Pydantic 2.12.5 / httpx 0.28.1에서 수행했습니다. 이 버전들은 관찰된 검증 환경이며 수업 표준으로 확정한 값이 아닙니다.

최초 sandbox 기본 임시 폴더는 쓰기가 거부되어 workspace 안의 TEMP/TMP로 변경했습니다. sandbox의 외부 설치 패키지 읽기 지연 때문에 API 검증은 승인된 로컬 실행으로 수행했습니다. 정체된 이 작업의 프로세스는 종료했습니다. GitHub 복제는 네트워크 권한을 받아 완료했습니다. 자동 승인 심사 거절은 없었습니다.

## 수동 검토와 미실행

수동 문서 검토에서는 공통 템플릿 연결, R-ID→F-ID→MVP→T-ID, 모의 예제의 기능 범위·데이터·오류 계약을 대조했습니다. 실제 모델이 작성한 산출물에 대한 채점은 아닙니다.

| 미실행 | 이유·다음 조치 |
| --- | --- |
| 실제 macOS/Linux 설치 | 현재 실행 환경은 Windows; 강사가 대상 OS에서 install-test.md 재현 |
| 실제 클라이언트 `$skill-name` 호출·자동 라우팅·계획 경계 | 모델 turn을 실행하지 않음; 수업 클라이언트/모델 확정 후 10개 호출과 문서 품질 비교 |
| 실제 AI 요약 품질 | 유료 API 호출 없이 모의 처리만 검증; 고정 입력의 사실·금액·날짜·출처 기준으로 별도 평가 |
| 실제 RAG·LangGraph·MCP/Gmail | 도구·버전·테스트 계정 미정; 선택 실습 시 연결 및 실패·재개 검증 |
| 실제 메일 발송 | 발송하지 않음; 승인된 대상·내용 및 중복 방지 확인 후 별도 실습 |
| 브라우저 Swagger 시연 | ASGI TestClient로 API 계약을 검증; 수동 시연은 별도 수행 |

남은 강사 결정은 Codex 클라이언트/모델, 공통 MCP 및 인증 범위, 대상 OS와 수업 패키지 버전입니다. 저장소 라이선스도 기존처럼 미확정이며 임의 변경하지 않았습니다. 프로세스 강제 종료 중 설치 복구는 백업 journal 검토가 필요합니다. 모의 외부 작업 원장은 메모리 예제이므로 운영 환경에서는 영속 저장·동시성 제어가 추가로 필요합니다.

## 공식 근거

Gemini 교체는 [Google Gen AI SDK](https://github.com/googleapis/python-genai) 및 [이전 SDK 지원 종료 안내](https://github.com/google-gemini/deprecated-generative-ai-python)를 확인했습니다. Skill 형식은 로컬 skill-creator 지침과 실제 Codex 목록 API로 검증했습니다. 웹 문서만으로 실제 호출 통과를 주장하지 않습니다.

## 독립 검토 후 보완

외부 처리 실패 계약의 범위를 명확히 통일했습니다. `TimeoutError`·`ConnectionError`·SDK 어댑터가 정규화한 `ProviderError`, 그리고 제공자가 반환한 잘못된 응답 구조는 502입니다. 실제 예제는 응답 구조를 검증하여 `ProviderError`로 변환합니다. 예상하지 못한 애플리케이션 `RuntimeError`는 500으로 남기며 내부 내용을 숨깁니다. Skill·API 템플릿·실행 예제·예제 설명을 같은 기준으로 수정하고 타임아웃 외 실패·잘못된 응답·내부 버그를 테스트했습니다.

설치 payload에는 단독 실행용 `scripts/check-environment.py`만 명시적으로 추가했습니다. 프로젝트 설치는 프로젝트 루트, 전역 설치는 `$CODEX_HOME/vibe-frame-kit/`에서 문서의 동일 명령을 실행합니다. 두 범위 모두 새 임시 위치에 실제 설치하고 원본 경로 밖에서 성공적으로 실행했습니다. 점검기는 기존 충돌 보존·manifest·백업·롤백의 적용 대상이며 설치기·회귀 검사기를 무분별하게 복사하지 않습니다.

보완 후 전체 15개 검사, 실제 Codex Skill 목록 10개, 공식 Skill 형식 10개, PowerShell·Git Bash 설치/재설치와 `git diff --check`를 재검증했습니다. 이전 미실행 범위는 그대로입니다. 이후 사용자가 GitHub 게시를 요청하여 원격 게시 금지는 해제됐으며 PR·merge는 요청하지 않았습니다.

## 기존 설치 업데이트 검증

사용자 요청으로 `--migrate-legacy`(PowerShell `-MigrateLegacy`)를 추가했습니다. 일반 설치는 기존 충돌을 계속 보존합니다. 명시적 마이그레이션은 기준 원래 버전의 해시와 일치하는 Kit 파일만 백업 후 교체하고 원래 자료 경로와 새 자료 패키지를 함께 관리합니다. 사용자 수정·새 파일 경로 충돌은 전체 쓰기 전에 중단하며 config.toml과 다른 Skill·개인 파일을 보존합니다. 지원 기준 버전 외에는 자동 인식하지 않습니다.

`python scripts/verify-legacy.py`에서 PowerShell·Git Bash의 4개 테스트 그룹(14개 하위 시나리오)이 통과했습니다. LF/CRLF 원본, dry-run, 마이그레이션, 재설치 변경 0개, 사용자 추가 파일, 수정한 원본·마이그레이션 후 수정·새 경로 충돌, 원본 백업, 실제 파일 잠금으로 발생한 중간 실패와 원복·재시도를 확인했습니다. 최초 실행에서 검증 도중 문서를 동시에 갱신하여 변경 0개 조건이 한 번 실패했고, 작업본을 고정한 전체 재실행은 모두 통과했습니다.

원래 설치기의 출력 파일 배치를 Git 원본으로 임시 CODEX_HOME에 재현했습니다. 원래 설치기 자체는 실제 HOME을 고정 사용하므로 실행하지 않았습니다. 실제 사용자 전역 설치·설정은 변경하지 않았습니다. 전체 일반 검사 15개와 실제 Skill 목록 조회도 다시 통과했습니다. 정확한 적용 명령과 조건은 [설치 안내](install-test.md#원래-전역-설치본-업데이트), 게시 전 검토는 [업데이트 및 게시 기록](update-and-publish.md)을 확인합니다.

## 변경 파일

- `.gitignore`
- `AGENTS.md`
- `README.md`
- `agents/routing.md`
- `config/codex.config.sample.toml`
- `config/legacy-install-manifest.json`
- `docs/advanced-labs.md`
- `docs/course-workflow.md`
- `docs/environment.md`
- `docs/install-test.md`
- `docs/instructor-guide.md`
- `docs/student-guide.md`
- `docs/team-delivery.md`
- `docs/update-and-publish.md`
- `docs/verification-report.md`
- `docs/verification-results.json`
- `examples/meeting-summary/README.md`
- `examples/meeting-summary/api.py`
- `examples/meeting-summary/workflow.py`
- `prompts/01-requirements.md`
- `prompts/02-function-breakdown.md`
- `prompts/03-mvp-planning.md`
- `prompts/04-project-structure.md`
- `prompts/05-feature-build.md`
- `prompts/06-debugging.md`
- `prompts/07-refactoring.md`
- `prompts/08-readme-report.md`
- `prompts/09-security-check.md`
- `scripts/check-environment.py`
- `scripts/install.ps1`
- `scripts/install.py`
- `scripts/install.sh`
- `scripts/verify-legacy.py`
- `scripts/verify.py`
- `skills/ai-agent-workflow-builder/SKILL.md`
- `skills/api-service-builder/SKILL.md`
- `skills/debugging-coach/SKILL.md`
- `skills/function-breakdown/SKILL.md`
- `skills/mvp-planning/SKILL.md`
- `skills/project-structure-builder/SKILL.md`
- `skills/readme-report-writer/SKILL.md`
- `skills/refactoring-coach/SKILL.md`
- `skills/requirements-definition/SKILL.md`
- `skills/security-checker/SKILL.md`
- `templates/agent-workflow-template.md`
- `templates/api-spec-template.md`
- `templates/final-report-template.md`
- `templates/function-breakdown-template.md`
- `templates/mvp-plan-template.md`
- `templates/project-structure-template.md`
- `templates/requirements-template.md`
- `templates/test-scenario-template.md`
