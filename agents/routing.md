# Agent Routing

이 문서는 `vibe-frame-kit`에서 사용하는 작업 단계별 Skill 라우팅 기준입니다.

이 Kit는 프로젝트 종류별 라우팅을 사용하지 않습니다. 대신 수강생이 현재 어떤 작업을 하고 있는지에 따라 적절한 Skill을 선택합니다.

## 라우팅 원칙

- 사용자의 프로젝트 주제가 아니라 현재 작업 단계에 따라 Skill을 선택합니다.
- 요구사항이 불명확하면 항상 `requirements-definition`부터 시작합니다.
- 구현 요청이 크거나 모호하면 먼저 `function-breakdown` 또는 `mvp-planning`으로 범위를 줄입니다.
- 오류 요청은 코드 수정 전에 로그와 재현 조건을 확인합니다.
- 보안 정보가 포함될 가능성이 있으면 `security-checker` 기준을 우선 적용합니다.

## 작업 단계별 Skill 라우팅

| 작업 유형 | 사용 조건 | 대표 사용자 요청 예시 | 사용할 Skill 이름 | 작업 결과물 |
| --- | --- | --- | --- | --- |
| 1. 요구사항 정의 | 사용자가 서비스 아이디어만 가지고 있거나, 프로젝트 목표와 사용자가 명확하지 않을 때 사용합니다. | "AI 면접 코칭 서비스를 만들고 싶은데 요구사항부터 정리해줘." | `requirements-definition` | 요구사항 정의서, 대상 사용자, 해결 문제, 핵심 기능 초안 |
| 2. 기능 분해 | 요구사항은 있으나 구현할 기능 단위가 크거나 모호할 때 사용합니다. | "이 서비스를 만들려면 어떤 기능으로 나눠야 해?" | `function-breakdown` | 기능 목록, 우선순위, 기능별 입력/처리/출력 정리 |
| 3. MVP 설계 | 전체 기능 중 첫 번째 버전에 포함할 범위를 정해야 할 때 사용합니다. | "시간이 부족하니까 MVP 범위를 정해줘." | `mvp-planning` | MVP 기능 목록, 제외할 기능, 개발 순서, 성공 기준 |
| 4. 프로젝트 구조 생성 | MVP 범위가 정해졌고 실제 파일과 폴더 구조를 만들거나 제안해야 할 때 사용합니다. | "이제 FastAPI와 React 기준으로 프로젝트 구조를 만들어줘." | `project-structure-builder` | 폴더 구조, 주요 파일 설명, 초기 실행 방식 |
| 5. API 서비스 구현 | 백엔드 API, 라우터, 요청/응답 모델, 외부 API 연동 기능을 구현할 때 사용합니다. | "문서 요약 API 엔드포인트를 구현해줘." | `api-service-builder` | API 코드, 요청/응답 형식, 실행 방법, 간단한 테스트 방법 |
| 6. AI Agent Workflow 설계 | 단일 API 호출이 아니라 여러 단계의 AI 처리 흐름, 도구 사용, 상태 관리가 필요할 때 사용합니다. | "사용자 입력을 분석하고 검색한 뒤 답변하는 Agent Workflow를 설계해줘." | `ai-agent-workflow-builder` | Agent 단계 설계, 도구 사용 흐름, 입출력 구조, 예외 처리 기준 |
| 7. 오류 분석 | 실행 중 에러, 테스트 실패, API 오류, 패키지 설치 문제 등이 발생했을 때 사용합니다. | "이 에러 로그를 보고 원인과 해결 방법을 알려줘." | `debugging-coach` | 원인 분석, 수정 계획, 수정 코드 또는 조치 방법, 재실행 방법 |
| 8. 리팩토링 | 기능은 동작하지만 코드 중복, 복잡도, 가독성, 구조 문제가 있을 때 사용합니다. | "동작은 하는데 코드가 지저분해. 리팩토링해줘." | `refactoring-coach` | 개선된 코드 구조, 변경 이유, 영향 범위, 회귀 확인 방법 |
| 9. README / 보고서 작성 | 프로젝트를 제출하거나 공유하기 위해 문서화가 필요할 때 사용합니다. | "프로젝트 README와 최종 보고서 초안을 작성해줘." | `readme-report-writer` | README, 최종 보고서, 실행 방법, 기술 스택, 한계점과 개선 방향 |
| 10. 보안 점검 | API Key, 토큰, 비밀번호, `.env`, 공개 저장소 업로드 전 점검이 필요할 때 사용합니다. | "GitHub에 올리기 전에 보안상 문제 없는지 확인해줘." | `security-checker` | 보안 점검 결과, 민감 정보 노출 여부, 수정 권장 사항, `.env.example` 안내 |

## 라우팅 예시

### 예시 1: 아이디어만 있는 경우

사용자 요청:

```text
AI로 고객 리뷰를 분석하는 서비스를 만들고 싶어.
```

선택할 Skill:

```text
requirements-definition
```

이유:

아직 사용자, 문제, 핵심 기능, MVP 범위가 정리되지 않았기 때문에 요구사항 정의부터 시작합니다.

### 예시 2: 바로 구현을 요청하지만 범위가 큰 경우

사용자 요청:

```text
AI 학습 관리 플랫폼 전체를 만들어줘.
```

선택할 Skill:

```text
function-breakdown
```

이유:

전체 시스템을 한 번에 만들지 않고, 기능을 작게 분해한 뒤 MVP 범위를 정해야 합니다.

### 예시 3: 에러 로그가 있는 경우

사용자 요청:

```text
서버 실행 중 이런 에러가 나왔어. 로그를 보고 고쳐줘.
```

선택할 Skill:

```text
debugging-coach
```

이유:

오류는 추측으로 해결하지 않고 로그, 발생 위치, 재현 조건을 기준으로 분석해야 합니다.

## Skill 이름 규칙

Skill 이름은 다음 기준을 따릅니다.

- 영어 소문자와 하이픈을 사용합니다.
- 작업 단계가 드러나도록 명확하게 작성합니다.
- 특정 프로젝트 이름이나 기술 스택 이름에 종속되지 않습니다.

예시:

```text
requirements-definition
function-breakdown
mvp-planning
project-structure-builder
api-service-builder
ai-agent-workflow-builder
debugging-coach
refactoring-coach
readme-report-writer
security-checker
```

## 실제 호출과 단계 경계

이 파일은 에이전트 생성 설정이 아니라 Skill 선택 안내입니다. 여러 Agent를 자동 생성하지 않습니다. 이름을 직접 지정하려면 `$requirements-definition`, `$function-breakdown`, `$mvp-planning`, `$project-structure-builder`, `$api-service-builder`, `$ai-agent-workflow-builder`, `$debugging-coach`, `$refactoring-coach`, `$readme-report-writer`, `$security-checker`로 요청합니다.

[수업 단계별 입출력과 완료 기준](../docs/course-workflow.md)을 함께 사용합니다. 이미 제공된 문서는 검토·보완하여 재사용합니다. 구현 가능한 작은 수정은 불필요하게 전체 기획을 다시 시작하지 않습니다. 계획 요청에서는 문서만 작성합니다.
