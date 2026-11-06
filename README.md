# vibe-frame-kit

`vibe-frame-kit`은 재직자 AI 서비스 개발 과정 수강생들이 Codex를 활용해 프로젝트를 진행할 수 있도록 돕는 공통 Vibe Frame Kit입니다.

이 저장소는 특정 AI 서비스의 완성 코드를 제공하기보다, 어떤 프로젝트를 만들든 공통으로 적용할 수 있는 개발 흐름, 프롬프트, 템플릿, 설정 기준을 제공하는 것을 목표로 합니다.

## 1. Kit 소개

AI 서비스 프로젝트는 아이디어만으로 바로 구현을 시작하면 요구사항이 불명확해지고, 기능 범위가 커지거나, 오류 분석과 테스트가 뒤로 밀리기 쉽습니다.

이 Kit는 Codex와 함께 프로젝트를 진행할 때 다음과 같은 공통 기준을 제공합니다.

- 요구사항을 먼저 정리합니다.
- 기능을 작은 단위로 분해합니다.
- MVP 범위를 정하고 우선순위를 정합니다.
- 프로젝트 구조를 일관되게 만듭니다.
- 기능 구현, 오류 분석, 테스트, 리팩토링을 단계적으로 진행합니다.
- README와 최종 보고서까지 프로젝트 산출물로 정리합니다.

## 2. 사용 대상

이 Kit는 다음과 같은 수강생과 프로젝트에 적합합니다.

- 재직자 AI 서비스 개발 과정 수강생
- Codex를 활용해 AI 서비스 프로젝트를 진행하려는 학습자
- 프로젝트 요구사항 정리와 기능 분해가 익숙하지 않은 입문자
- 팀 프로젝트에서 공통 개발 절차가 필요한 팀
- README, 보고서, 테스트 계획 등 산출물 작성 기준이 필요한 학습자

특정 프레임워크나 언어에 종속된 Kit가 아니므로 Python, JavaScript, TypeScript, FastAPI, Flask, React, Streamlit 등 다양한 AI 서비스 프로젝트에 적용할 수 있습니다.

## 3. Kit가 제공하는 개발 흐름

이 Kit는 아래 흐름을 기본 개발 프로세스로 사용합니다.

```text
요구사항 정의
→ 기능 분해
→ MVP 설계
→ 프로젝트 구조 생성
→ 기능 구현
→ 오류 분석
→ 테스트
→ 리팩토링
→ README / 보고서 작성
```

각 단계의 목적은 다음과 같습니다.

| 단계 | 목적 |
| --- | --- |
| 요구사항 정의 | 만들 서비스의 목표, 사용자, 주요 문제를 정리합니다. |
| 기능 분해 | 큰 아이디어를 구현 가능한 기능 단위로 나눕니다. |
| MVP 설계 | 가장 먼저 완성할 최소 기능 범위를 정합니다. |
| 프로젝트 구조 생성 | 폴더, 파일, 실행 방식을 일관되게 구성합니다. |
| 기능 구현 | Codex와 함께 작은 작업 단위로 코드를 작성합니다. |
| 오류 분석 | 에러 메시지, 원인, 해결 방법을 기록합니다. |
| 테스트 | 핵심 기능이 의도대로 동작하는지 확인합니다. |
| 리팩토링 | 중복, 복잡도, 가독성 문제를 개선합니다. |
| README / 보고서 작성 | 프로젝트 결과와 사용 방법을 문서화합니다. |

## 4. 저장소 구조

```text
vibe-frame-kit/
├── README.md
├── AGENTS.md
├── agents/
│   └── routing.md
├── skills/
│   ├── requirements-definition/
│   ├── function-breakdown/
│   ├── mvp-planning/
│   ├── project-structure-builder/
│   ├── api-service-builder/
│   ├── ai-agent-workflow-builder/
│   ├── debugging-coach/
│   ├── refactoring-coach/
│   ├── readme-report-writer/
│   └── security-checker/
├── prompts/
│   ├── 01-requirements.md
│   ├── 02-function-breakdown.md
│   ├── 03-mvp-planning.md
│   ├── 04-project-structure.md
│   ├── 05-feature-build.md
│   ├── 06-debugging.md
│   ├── 07-refactoring.md
│   ├── 08-readme-report.md
│   └── 09-security-check.md
├── templates/
│   ├── requirements-template.md
│   ├── function-breakdown-template.md
│   ├── mvp-plan-template.md
│   ├── api-spec-template.md
│   ├── agent-workflow-template.md
│   ├── test-scenario-template.md
│   ├── readme-template.md
│   └── final-report-template.md
├── config/
│   ├── lean-skills.txt
│   └── codex.config.sample.toml
├── scripts/
│   ├── install.ps1
│   └── install.sh
├── docs/
│   ├── student-guide.md
│   ├── instructor-guide.md
│   └── security-checklist.md
└── .gitignore
```

각 폴더와 파일의 역할은 다음과 같습니다.

| 경로 | 설명 |
| --- | --- |
| `README.md` | Kit의 목적, 사용 방법, 전체 구조를 설명합니다. |
| `AGENTS.md` | Codex가 프로젝트에서 따를 공통 작업 규칙을 정의합니다. |
| `agents/routing.md` | 작업 단계별로 어떤 역할 또는 흐름을 사용할지 정리합니다. |
| `skills/` | 요구사항 정의, 기능 분해, MVP 설계, 구현, 디버깅, 문서화, 보안 점검 Skill을 보관합니다. |
| `prompts/` | 수강생이 복사해서 사용할 수 있는 단계별 프롬프트를 보관합니다. |
| `templates/` | 요구사항 정의서, 기능 분해표, MVP 계획서, API 명세서, 테스트 시나리오, README, 최종 보고서 양식을 보관합니다. |
| `config/` | 기본 Skill 목록과 Codex 설정 샘플을 보관합니다. |
| `scripts/` | Windows/macOS/Linux 설치 스크립트를 보관합니다. |
| `docs/` | 수강생 가이드, 강사 가이드, 보안 체크리스트를 보관합니다. |
| `.gitignore` | Git에 포함하지 않을 파일과 폴더를 정의합니다. |

## 5. 설치 방법

Python 3.11+와 Git을 준비하고 [안전한 설치 및 확인](docs/install-test.md)을 따릅니다. 기본은 프로젝트 범위 설치이며 전역 설치는 명시적으로 선택합니다.

## 6. 사용 예시

예를 들어 "AI 회의록 요약 서비스"를 만든다고 가정합니다.

1. `templates/`의 요구사항 템플릿을 사용해 서비스 목표와 사용자를 정리합니다.
2. `prompts/`의 기능 분해 프롬프트를 Codex에 입력해 주요 기능을 나눕니다.
3. MVP 설계 템플릿으로 첫 번째 버전에 포함할 기능만 선택합니다.
4. Codex에게 MVP 기준의 프로젝트 구조 생성을 요청합니다.
5. 기능별로 구현을 진행하고, 오류가 발생하면 오류 분석 템플릿에 기록합니다.
6. 테스트 계획을 작성하고 핵심 기능을 검증합니다.
7. 리팩토링 후 README와 최종 보고서를 작성합니다.

Codex에 요청할 때는 다음처럼 단계와 산출물을 명확히 말하는 것이 좋습니다.

```text
나는 AI 회의록 요약 서비스를 만들고 있어.
먼저 요구사항 정의 단계부터 진행하고 싶어.
사용자, 핵심 문제, 주요 기능, MVP 범위를 정리해줘.
```

또는 구현 단계에서는 다음처럼 요청할 수 있습니다.

```text
현재 MVP 기능 중 파일 업로드 기능을 구현하려고 해.
기존 프로젝트 구조를 먼저 확인하고,
필요한 파일만 수정해서 동작 가능한 형태로 만들어줘.
```

## 7. 주의사항

- Codex가 생성한 코드는 반드시 직접 실행하고 확인해야 합니다.
- 한 번에 너무 큰 작업을 요청하기보다 작은 기능 단위로 나누어 요청하는 것이 좋습니다.
- 오류의 재현 흐름은 유지하되 토큰·비밀번호·개인정보를 가린 관련 로그를 제공합니다.
- 프로젝트 요구사항이 바뀌면 README, 요구사항 문서, MVP 문서도 함께 수정해야 합니다.
- Codex의 제안이 항상 최선은 아니므로 수강생이 직접 판단하고 검토해야 합니다.
- 팀 프로젝트에서는 파일 수정 전후로 역할과 작업 범위를 명확히 공유해야 합니다.

## 8. 보안 안내

AI 서비스 프로젝트에서는 API 키, 비밀번호, 토큰 같은 민감 정보가 자주 사용됩니다. 다음 내용을 반드시 지켜야 합니다.

- `.env` 파일은 Git에 커밋하지 않습니다.
- API 키, 비밀번호, 인증 토큰을 README나 보고서에 직접 적지 않습니다.
- 민감 정보 예시는 `.env.example`처럼 가짜 값으로만 작성합니다.
- Codex에 실제 비밀번호나 개인 인증 정보를 입력하지 않습니다.
- 외부 API를 사용할 때는 사용량, 요금, 권한 범위를 확인합니다.
- 배포 전에는 공개 저장소에 민감 정보가 포함되어 있지 않은지 확인합니다.

예시:

```env
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
```

## 9. 라이선스 안내

이 저장소의 라이선스는 아직 확정되지 않았습니다.

수업, 개인 학습, 팀 프로젝트에서 자유롭게 사용할 수 있도록 공개할 예정이라면 `MIT License`를 권장합니다. 실제 GitHub 저장소로 공개하기 전에는 `LICENSE` 파일을 추가하고, README의 라이선스 안내도 확정된 내용으로 업데이트해야 합니다.

## 공통 기준과 검증

AGENTS.md는 공통 원칙, [routing](agents/routing.md)은 Skill 선택, Skill은 판단·절차, template은 필수 결과 구조, prompt는 작업 요청입니다. [수업 단계와 통과 기준](docs/course-workflow.md)을 기준으로 결과를 비교합니다. `config/codex.config.sample.toml`은 설명용 정책 예시이며 Codex가 읽는 실제 설정이 아닙니다. `config.toml`로 복사하지 않습니다.

- [설치와 실제 Skill 확인](docs/install-test.md)
- [환경·도구와 남은 결정](docs/environment.md)
- [선택형 후반 실습](docs/advanced-labs.md)
- [협업과 발표](docs/team-delivery.md)
- [대표 예제와 검증 결과](docs/verification-report.md)

저장소 무결성과 설치 동작: `python scripts/verify.py`. 이는 모델의 실제 Skill 선택·응답 품질을 증명하지 않으며 별도 수동 검증이 필요합니다.

## 기존 설치 업데이트

원래 배포 파일을 수정하지 않았다면 명시적 마이그레이션으로 백업 후 덮어쓸 수 있습니다. PowerShell은 `powershell -File scripts/install.ps1 -Scope global -MigrateLegacy -DryRun`, Bash는 `bash scripts/install.sh --scope global --migrate-legacy --dry-run`으로 먼저 확인합니다. 실제 적용 명령과 보존·충돌 조건은 [설치본 업데이트 안내](docs/install-test.md#원래-전역-설치본-업데이트)를 따릅니다. 사용자 수정 파일과 다른 설정은 강제로 덮어쓰지 않습니다.
