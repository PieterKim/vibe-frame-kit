---
name: ai-agent-workflow-builder
description: 다단계 AI 처리의 역할, 상태, 조건 분기와 제한된 재시도를 설계할 때 사용합니다.
---

## 공통 산출물 계약

- 본문 예시는 설명용입니다. 최종 필수 구조는 `templates/agent-workflow-template.md`를 단일 기준으로 사용합니다.
- 프로젝트 설치에서는 프로젝트 루트의 `templates/`, `docs/`, `agents/`를 읽습니다. 전역 설치에서는 `$CODEX_HOME/vibe-frame-kit/`(미설정 시 `~/.codex/vibe-frame-kit/`)의 같은 자료를 읽습니다.
- `docs/course-workflow.md`의 해당 단계 완료 기준으로 통과 / 보완 필요 / 확인 필요와 근거를 기록합니다. 적용되지 않는 항목도 이유를 남깁니다.
- 계획만 요청받으면 코드나 실행 환경을 생성하지 않습니다. 다음 단계는 사용자가 요청한 범위 안에서만 수행합니다.
- 구현·수정 시 `templates/test-scenario-template.md`에 자동/수동 구분, 기대값, 실제 결과, 통과/실패/미실행 및 이유를 기록합니다. 안내만 했으면 실행 완료로 보고하지 않습니다.

# AI Agent Workflow Builder

## 1. 목적

이 Skill의 목적은 AI Agent 또는 LangGraph 기반 workflow를 설계하는 것입니다.

Codex는 특정 프로젝트에 종속되지 않는 공통 기준으로 Agent의 역할, 입력, 처리, 출력, 순차 처리, 조건 분기, 검증 흐름을 정의해야 합니다.

이 Skill은 단일 AI API 호출만으로 해결하기 어려운 작업에 사용합니다. 예를 들어 입력 분석, 정보 검색, 결과 생성, 검증, 재시도, 최종 응답 정리처럼 여러 단계가 필요한 경우 Agent Workflow를 설계합니다.

## 2. 사용 상황

다음과 같은 상황에서 이 Skill을 사용합니다.

- AI 처리가 여러 단계로 나뉘는 경우
- 입력 내용에 따라 다른 처리 경로가 필요한 경우
- 검색, 요약, 분류, 생성, 검증을 조합해야 하는 경우
- 결과 품질을 검토하는 검증 Agent가 필요한 경우
- LangGraph 기반 node/edge/state 구조로 확장하고 싶은 경우
- 단순 API 함수보다 Agent Workflow 설계가 필요한 경우
- 사용자 요청을 분석한 뒤 적절한 도구 또는 처리 방식을 선택해야 하는 경우

예시 요청:

```text
사용자 질문을 분석하고, 필요하면 문서를 검색한 뒤 답변을 생성하는 Agent Workflow를 설계해줘.
```

## 3. Agent 역할 분해 기준

Agent는 하나의 큰 AI 작업을 여러 역할로 나누어 처리할 때 사용합니다.

역할 분해 기준:

- 하나의 Agent는 하나의 명확한 책임을 가집니다.
- 입력과 출력이 명확해야 합니다.
- 다른 Agent와 연결될 수 있어야 합니다.
- 실패하거나 품질이 낮을 때 대체 흐름을 정의할 수 있어야 합니다.
- MVP 단계에서는 Agent 수를 과도하게 늘리지 않습니다.

대표 Agent 역할:

| Agent 역할 | 설명 |
| --- | --- |
| Input Analyzer | 사용자 입력의 목적, 유형, 필요한 작업을 분석합니다. |
| Planner | 작업 순서와 필요한 도구를 결정합니다. |
| Retriever | 문서, DB, 벡터스토어, 외부 API에서 필요한 정보를 찾습니다. |
| Processor | 요약, 분류, 추출, 변환 등 핵심 AI 처리를 수행합니다. |
| Generator | 사용자에게 보여줄 답변이나 결과물을 생성합니다. |
| Validator | 결과의 형식, 누락, 품질, 안전성을 검토합니다. |
| Formatter | 최종 결과를 표, JSON, Markdown 등 요구 형식으로 정리합니다. |

MVP에서는 보통 다음 3개에서 4개 역할만으로 시작합니다.

```text
Input Analyzer
→ Processor 또는 Retriever
→ Generator
→ Validator
```

## 4. Agent별 입력/처리/출력 정의 방식

각 Agent는 입력, 처리, 출력을 반드시 구분해서 정의합니다.

기본 형식:

| Agent | 입력 | 처리 | 출력 |
| --- | --- | --- | --- |
|  |  |  |  |

작성 기준:

- 입력: 이전 단계에서 받은 데이터 또는 사용자 입력을 적습니다.
- 처리: Agent가 수행할 판단, 검색, 생성, 검증 작업을 적습니다.
- 출력: 다음 Agent 또는 사용자에게 전달할 결과를 적습니다.

예시:

| Agent | 입력 | 처리 | 출력 |
| --- | --- | --- | --- |
| Input Analyzer | 사용자 질문 | 질문 유형과 필요한 정보 판단 | `task_type`, `needs_retrieval` |
| Retriever | 검색 필요 여부, 검색 질의 | 문서 또는 벡터스토어 검색 | 관련 문서 목록 |
| Generator | 사용자 질문, 관련 문서 | 답변 초안 생성 | 답변 초안 |
| Validator | 답변 초안, 요구 형식 | 누락 정보와 형식 오류 확인 | 검증 결과, 수정 요청 |
| Formatter | 검증된 답변 | Markdown 형식으로 정리 | 최종 답변 |

## 5. 순차 처리 workflow

순차 처리 workflow는 모든 입력이 같은 단계 순서로 처리되는 구조입니다.

사용 상황:

- 처리 흐름이 단순하고 고정되어 있을 때
- 입력 분석, 처리, 검증, 출력이 항상 필요한 경우
- MVP 단계에서 빠르게 Agent 흐름을 만들 때

기본 구조:

```text
사용자 입력
→ 입력 분석 Agent
→ 처리 Agent
→ 결과 생성 Agent
→ 검증 Agent
→ 최종 출력
```

설계 기준:

- 각 단계의 입력과 출력이 다음 단계와 연결되어야 합니다.
- 중간 결과를 저장하거나 로그로 남길 수 있어야 합니다.
- 실패 가능성이 높은 단계에는 오류 처리 기준을 둡니다.
- 처음부터 복잡한 분기를 만들지 않고 단순 흐름으로 시작합니다.

## 6. 조건 분기 workflow

조건 분기 workflow는 입력 또는 중간 결과에 따라 다른 경로를 선택하는 구조입니다.

사용 상황:

- 검색이 필요한 요청과 필요 없는 요청을 구분해야 할 때
- 입력 유형에 따라 요약, 분류, 추천 등 다른 처리를 해야 할 때
- 검증 결과가 실패이면 다시 생성해야 할 때
- 사용자 입력이 부족하면 추가 질문을 해야 할 때

기본 구조:

```text
사용자 입력
→ 입력 분석 Agent
→ 조건 판단
  ├─ 검색 필요: Retriever → Generator
  ├─ 검색 불필요: Generator
  └─ 정보 부족: Clarification Question
→ Validator
→ 최종 출력
```

조건 분기 작성 기준:

| 조건 | 이동할 단계 | 설명 |
| --- | --- | --- |
| `needs_retrieval = true` | Retriever | 외부 정보나 문서 검색이 필요합니다. |
| `needs_retrieval = false` | Generator | 입력만으로 답변 생성이 가능합니다. |
| `input_is_insufficient = true` | Clarification | 사용자에게 추가 정보를 요청합니다. |
| `validation_passed = false` | Generator 또는 Processor | 결과를 수정하거나 재생성합니다. |
| `validation_passed = true` | Formatter | 최종 출력 형식으로 정리합니다. |

## 7. 검증 Agent 구성 방식

검증 Agent는 AI가 생성한 결과를 그대로 사용자에게 전달하기 전에 품질과 형식을 확인하는 역할입니다.

검증 Agent가 확인할 항목:

- 사용자의 요청에 답했는가?
- 필수 항목이 누락되지 않았는가?
- 출력 형식을 지켰는가?
- 근거 없이 단정하지 않았는가?
- 보안 정보나 민감 정보가 포함되지 않았는가?
- 오류나 모순이 있는가?
- 후속 단계에서 사용할 수 있는 구조인가?

검증 결과 형식:

```json
{
  "passed": true,
  "issues": [],
  "revision_instruction": ""
}
```

실패 예시:

```json
{
  "passed": false,
  "issues": [
    "MVP 범위가 너무 큽니다.",
    "출력 결과가 명확하지 않습니다."
  ],
  "revision_instruction": "MVP 기능을 3개 이하로 줄이고 출력 결과를 구체화하세요."
}
```

검증 Agent 사용 원칙:

- 검증 Agent는 새 기능을 임의로 추가하지 않습니다.
- 검증 결과는 수정 가능한 지시로 작성합니다.
- MVP 단계에서는 검증 기준을 3개에서 5개 정도로 단순하게 유지합니다.
- 보안 관련 결과는 반드시 민감 정보 노출 여부를 확인합니다.

## 8. LangGraph로 확장 가능한 구조

LangGraph로 확장할 때는 Agent Workflow를 state, node, edge, conditional edge로 나누어 생각합니다.

기본 개념:

| LangGraph 요소 | 이 Skill에서의 의미 |
| --- | --- |
| State | workflow 전체에서 공유되는 데이터입니다. |
| Node | 하나의 Agent 또는 처리 함수입니다. |
| Edge | 다음 단계로 이동하는 연결입니다. |
| Conditional Edge | 조건에 따라 다른 Node로 이동하는 연결입니다. |
| End | 최종 결과를 반환하는 종료 지점입니다. |

State 설계 예시:

```python
from typing import TypedDict


class WorkflowState(TypedDict):
    user_input: str
    task_type: str
    needs_retrieval: bool
    retrieved_context: list[str]
    draft_output: str
    validation_passed: bool
    final_output: str
```

Node 설계 예시:

```text
analyze_input
retrieve_context
generate_output
validate_output
format_output
```

Conditional Edge 예시:

```text
analyze_input
→ needs_retrieval가 true이면 retrieve_context
→ needs_retrieval가 false이면 generate_output
```

LangGraph 확장 기준:

- 처음에는 함수 기반 workflow로 설계해도 됩니다.
- 상태로 공유해야 하는 값만 State에 넣습니다.
- Node는 작고 테스트 가능한 함수로 만듭니다.
- 조건 분기는 명확한 boolean 또는 enum 값으로 판단합니다.
- 복잡한 graph를 처음부터 만들지 않고 MVP 흐름부터 구성합니다.

## 9. 산출물 기준

공통 산출물 계약에서 지정한 템플릿을 사용합니다. 추가 분석은 그 결과와 함께 설명합니다.

## 10. workflow 다이어그램 예시

아래는 공통 Agent Workflow를 텍스트로 표현한 예시입니다.

```text
[Start]
  ↓
[Input Analyzer]
  - 사용자 입력 분석
  - 작업 유형 판단
  - 검색 필요 여부 판단
  ↓
{조건 분기}
  ├─ 검색 필요
  │    ↓
  │  [Retriever]
  │    - 문서 또는 벡터스토어 검색
  │    - 관련 근거 수집
  │    ↓
  │  [Generator]
  │    - 사용자 입력과 검색 결과를 바탕으로 답변 생성
  │
  ├─ 검색 불필요
  │    ↓
  │  [Generator]
  │    - 사용자 입력만으로 답변 생성
  │
  └─ 정보 부족
       ↓
     [Clarification]
       - 사용자에게 필요한 추가 정보 질문
       ↓
     [End]

[Generator]
  ↓
[Validator]
  - 필수 항목 누락 확인
  - 형식 오류 확인
  - 민감 정보 노출 확인
  ↓
{검증 결과}
  ├─ 통과
  │    ↓
  │  [Formatter]
  │    - 최종 출력 형식 정리
  │    ↓
  │  [End]
  │
  └─ 실패
       ↓
     [Generator]
       - 검증 결과를 반영해 재생성
```

간단한 순차 workflow만 필요한 경우에는 아래처럼 축소할 수 있습니다.

```text
[Start]
→ [Input Analyzer]
→ [Processor]
→ [Validator]
→ [Formatter]
→ [End]
```

## 실패·재시도와 외부 작업

`templates/agent-workflow-template.md`의 attempt/max_attempts, 실패 종료, completed_actions를 설계에 포함합니다. 본문의 재생성 화살표는 반드시 시도 한도 내에서만 허용합니다. 시간 초과는 성공 여부가 불확실할 수 있으므로 발송·등록을 즉시 재실행하지 않습니다. 결과 조회가 불가능하면 중단하고 불확실을 보고합니다. 선택 실습만 `docs/advanced-labs.md`를 적용합니다.
