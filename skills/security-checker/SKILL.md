---
name: security-checker
description: 공유 및 배포 전 비밀정보, 인증과 데이터 노출을 점검할 때 사용합니다.
---

## 공통 산출물 계약

- 본문 예시는 설명용입니다. 최종 필수 구조는 `templates/test-scenario-template.md`를 단일 기준으로 사용합니다.
- 프로젝트 설치에서는 프로젝트 루트의 `templates/`, `docs/`, `agents/`를 읽습니다. 전역 설치에서는 `$CODEX_HOME/vibe-frame-kit/`(미설정 시 `~/.codex/vibe-frame-kit/`)의 같은 자료를 읽습니다.
- `docs/course-workflow.md`의 해당 단계 완료 기준으로 통과 / 보완 필요 / 확인 필요와 근거를 기록합니다. 적용되지 않는 항목도 이유를 남깁니다.
- 계획만 요청받으면 코드나 실행 환경을 생성하지 않습니다. 다음 단계는 사용자가 요청한 범위 안에서만 수행합니다.
- 구현·수정 시 `templates/test-scenario-template.md`에 자동/수동 구분, 기대값, 실제 결과, 통과/실패/미실행 및 이유를 기록합니다. 안내만 했으면 실행 완료로 보고하지 않습니다.

# Security Checker

## 1. 목적

이 Skill의 목적은 수강생 프로젝트에서 민감정보와 보안 위험을 점검하는 것입니다.

Codex는 GitHub에 프로젝트를 올리기 전, API Key, token, password, `credentials.json`, `auth.json`, `.env` 파일, 개인정보 포함 데이터가 코드나 문서에 노출되지 않았는지 확인해야 합니다.

보안 점검은 선택 사항이 아닙니다. AI 서비스 프로젝트는 외부 API Key와 사용자 입력 데이터를 자주 다루기 때문에, 공개 저장소에 올리기 전에 반드시 확인해야 합니다.

## 2. 사용 상황

다음과 같은 상황에서 이 Skill을 사용합니다.

- GitHub에 프로젝트를 push하기 전
- README 또는 보고서를 작성하기 전
- `.env` 파일을 만들거나 수정한 후
- OpenAI API, Gemini API, Google API 등 외부 API를 연동한 후
- `credentials.json`, `auth.json` 같은 인증 파일을 사용한 경우
- 사용자 데이터, 로그, 업로드 파일을 저장하는 기능이 있는 경우
- 팀 프로젝트에서 여러 사람이 파일을 수정한 경우
- 저장소를 공개 저장소로 전환하기 전

예시 요청:

```text
GitHub에 올리기 전에 API Key나 민감정보가 들어갔는지 점검해줘.
```

## 3. GitHub에 올리면 안 되는 파일

다음 파일은 GitHub에 올리면 안 됩니다.

| 파일 또는 패턴 | 이유 |
| --- | --- |
| `.env` | 실제 API Key, DB URL, 토큰, 비밀번호가 들어갈 수 있습니다. |
| `.env.local` | 로컬 개발용 실제 환경 변수가 들어갈 수 있습니다. |
| `.env.*` | 환경별 실제 비밀값이 들어갈 수 있습니다. |
| `credentials.json` | Google API 등 인증 정보가 들어갈 수 있습니다. |
| `auth.json` | 인증 토큰 또는 사용자 인증 정보가 들어갈 수 있습니다. |
| `token.json` | OAuth token이 들어갈 수 있습니다. |
| `*.pem` | 개인 키 파일일 수 있습니다. |
| `*.key` | 암호화 키 또는 인증 키일 수 있습니다. |
| `*.p12`, `*.pfx` | 인증서 또는 개인 키가 들어갈 수 있습니다. |
| `secrets.*` | 비밀 설정 파일일 수 있습니다. |
| `private/` | 비공개 자료가 들어갈 수 있습니다. |
| `uploads/` | 사용자 업로드 파일이나 개인정보가 들어갈 수 있습니다. |
| `data/raw/` | 원본 개인정보 데이터가 들어갈 수 있습니다. |
| `logs/` | API Key나 사용자 입력이 로그에 남아 있을 수 있습니다. |

특히 다음 항목은 절대 GitHub에 올리지 않습니다.

- API Key
- token
- password
- `credentials.json`
- `auth.json`
- `.env`

`.gitignore`에 반드시 포함할 예시:

```gitignore
# Environment files
.env
.env.*
!.env.example

# Secrets
credentials.json
auth.json
token.json
*.pem
*.key
*.p12
*.pfx
secrets.*

# Local data and logs
uploads/
data/raw/
logs/
*.log
```

## 4. .env와 .env.example 구분 기준

`.env`와 `.env.example`은 역할이 다릅니다.

| 파일 | GitHub 업로드 여부 | 역할 |
| --- | --- | --- |
| `.env` | 올리면 안 됨 | 실제 API Key, 토큰, 비밀번호 등 비밀값을 저장합니다. |
| `.env.example` | 올려도 됨 | 필요한 환경 변수 이름과 가짜 예시 값을 안내합니다. |

`.env` 예시:

```env
OPENAI_API_KEY=실제값
DATABASE_URL=실제값
```

이 파일은 GitHub에 올리면 안 됩니다.

`.env.example` 예시:

```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=your_database_url_here
```

이 파일은 GitHub에 올릴 수 있습니다.

작성 기준:

- `.env.example`에는 실제 값을 쓰지 않습니다.
- 필요한 변수 이름은 모두 포함합니다.
- 예시 값은 `your_api_key_here`처럼 가짜 값으로 작성합니다.
- README에는 `.env.example`을 복사해 `.env`를 만들라고 안내합니다.

## 5. API Key 관리 기준

API Key는 코드에 직접 작성하지 않습니다.

나쁜 예시:

```python
client = OpenAI(api_key="sk-...")
```

좋은 예시:

```python
import os

api_key = os.getenv("OPENAI_API_KEY")
```

관리 기준:

- API Key는 `.env`에 저장합니다.
- 코드에서는 환경 변수로 불러옵니다.
- README에는 실제 키가 아니라 설정 방법만 적습니다.
- 오류 메시지나 로그에 API Key가 출력되지 않도록 합니다.
- 팀원에게 키를 공유할 때 채팅이나 GitHub issue에 직접 붙여넣지 않습니다.
- 키가 유출되었다면 즉시 해당 키를 폐기하고 새로 발급합니다.
- OpenAI API, Gemini API, Google API 등 모든 외부 API Key에 동일한 기준을 적용합니다.

주의해야 할 이름:

```text
OPENAI_API_KEY
GEMINI_API_KEY
GOOGLE_API_KEY
ANTHROPIC_API_KEY
API_KEY
ACCESS_TOKEN
REFRESH_TOKEN
SECRET_KEY
CLIENT_SECRET
PASSWORD
```

## 6. 개인정보 포함 데이터 처리 기준

수강생 프로젝트에서 사용자 입력, 업로드 파일, 로그에는 개인정보가 포함될 수 있습니다.

개인정보 예시:

- 이름
- 이메일 주소
- 전화번호
- 주소
- 주민등록번호
- 학생 또는 직원 번호
- 회사 내부 문서
- 회의록 원문
- 고객 리뷰 원본
- 상담 기록

처리 기준:

- 개인정보가 포함된 원본 데이터는 GitHub에 올리지 않습니다.
- 샘플 데이터는 가명 처리하거나 인위적으로 만든 예시를 사용합니다.
- 로그에 사용자 입력 전체를 저장하지 않습니다.
- 보고서나 README에 실제 개인정보를 넣지 않습니다.
- 테스트 데이터는 짧고 가짜인 예시를 사용합니다.
- 업로드 파일 저장 기능이 있다면 저장 위치를 `.gitignore`에 포함합니다.

예시:

```text
나쁜 예시: 홍길동, hong@example.com, 010-1234-5678
좋은 예시: 사용자 A, user@example.com, 010-0000-0000
```

## 7. GitHub push 전 점검 기준

GitHub에 push하기 전에 다음 항목을 확인합니다.

체크리스트:

- `.env` 파일이 Git 추적 대상에 포함되지 않았는가?
- `.env.example`에는 실제 값이 아닌 가짜 예시 값만 있는가?
- API Key, token, password가 코드에 직접 적혀 있지 않은가?
- `credentials.json`, `auth.json`, `token.json`이 포함되지 않았는가?
- README와 보고서에 실제 비밀값이 없는가?
- 로그 파일에 API Key나 사용자 입력이 남아 있지 않은가?
- 업로드 파일이나 원본 데이터가 포함되지 않았는가?
- `.gitignore`에 민감 파일 패턴이 포함되어 있는가?
- 테스트 데이터가 개인정보를 포함하지 않는가?

Git 추적 상태 확인 예시:

```bash
git status --short
```

추적 중인 파일 목록 확인 예시:

```bash
git ls-files
```

주의:

- 이미 민감정보를 commit했다면 `.gitignore`에 추가하는 것만으로는 충분하지 않습니다.
- 유출된 API Key는 즉시 폐기하고 새로 발급해야 합니다.
- 공개 저장소에 push된 비밀값은 이미 노출된 것으로 간주합니다.

## 8. 민감정보 검색 명령어

GitHub push 전에는 프로젝트 전체에서 민감정보 후보를 검색합니다.

권장 검색 명령어:

```bash
rg -l "API_KEY|TOKEN|PASSWORD|SECRET|CLIENT_SECRET|ACCESS_TOKEN|REFRESH_TOKEN"
```

환경 파일 검색:

```bash
rg -l "OPENAI_API_KEY|GEMINI_API_KEY|GOOGLE_API_KEY|ANTHROPIC_API_KEY"
```

인증 파일 검색:

```bash
rg --files | rg "credentials\\.json|auth\\.json|token\\.json|\\.env$|\\.env\\."
```

OpenAI Key 형태 검색 예시:

```bash
rg -l "sk-[A-Za-z0-9_-]+"
```

Google API Key 형태 검색 예시:

```bash
rg -l "AIza[0-9A-Za-z_-]+"
```

비밀번호 후보 검색:

```bash
rg -l "password\\s*=|PASSWORD\\s*=|pwd\\s*="
```

Git에 추적 중인 민감 파일 확인:

```bash
git ls-files | rg "\\.env|credentials\\.json|auth\\.json|token\\.json|\\.pem|\\.key"
```

주의:

- 검색은 일치한 파일명만 출력합니다. 비밀값이 포함된 줄을 터미널·도구 결과에 출력하지 않습니다.
- 사용자에게는 "민감정보 후보가 발견됨"과 파일 위치만 알려줍니다.
- 실제 값을 마스킹해서 설명합니다.

마스킹 예시:

```text
OPENAI_API_KEY=[masked]
```

## 9. 산출물 기준

공통 산출물 계약에서 지정한 템플릿을 사용합니다. 추가 분석은 그 결과와 함께 설명합니다.
