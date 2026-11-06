---
name: api-service-builder
description: API 명세, 입력 검증, 계층 분리와 구현 및 API 테스트가 필요할 때 사용합니다.
---

## 공통 산출물 계약

- 본문 예시는 설명용입니다. 최종 필수 구조는 `templates/api-spec-template.md`를 단일 기준으로 사용합니다.
- 프로젝트 설치에서는 프로젝트 루트의 `templates/`, `docs/`, `agents/`를 읽습니다. 전역 설치에서는 `$CODEX_HOME/vibe-frame-kit/`(미설정 시 `~/.codex/vibe-frame-kit/`)의 같은 자료를 읽습니다.
- `docs/course-workflow.md`의 해당 단계 완료 기준으로 통과 / 보완 필요 / 확인 필요와 근거를 기록합니다. 적용되지 않는 항목도 이유를 남깁니다.
- 계획만 요청받으면 코드나 실행 환경을 생성하지 않습니다. 다음 단계는 사용자가 요청한 범위 안에서만 수행합니다.
- 구현·수정 시 `templates/test-scenario-template.md`에 자동/수동 구분, 기대값, 실제 결과, 통과/실패/미실행 및 이유를 기록합니다. 안내만 했으면 실행 완료로 보고하지 않습니다.

# API Service Builder

## 1. 목적

이 Skill의 목적은 FastAPI 기반 API 서비스를 설계하고 구현하는 것입니다.

Codex는 요구사항 정의서, 기능 분해표, MVP 계획서, 프로젝트 구조를 바탕으로 API 명세를 작성하고, Request/Response 구조, Pydantic schema, router, service, 예외 처리, Swagger 테스트 방법을 함께 정리해야 합니다.

API 서비스는 단순히 엔드포인트를 만드는 데서 끝나지 않습니다. 사용자가 어떤 데이터를 보내고, 서버가 어떻게 처리하며, 어떤 결과를 반환하는지 명확히 정의해야 합니다.

## 2. 사용 상황

다음과 같은 상황에서 이 Skill을 사용합니다.

- FastAPI 기반 백엔드 API를 설계해야 할 때
- AI 요약, 분류, 추천, 검색, 질의응답 등 기능을 API로 제공해야 할 때
- 프론트엔드와 연결할 Request/Response 형식이 필요할 때
- Pydantic schema를 작성해야 할 때
- API router, service, schema 계층을 분리해야 할 때
- Swagger UI에서 API를 테스트해야 할 때
- 외부 AI API 호출을 백엔드 service 계층으로 분리해야 할 때

예시 요청:

```text
회의록 텍스트를 받아서 요약 결과를 반환하는 FastAPI API를 설계하고 구현해줘.
```

## 3. API 명세 작성 방식

API를 구현하기 전에 먼저 API 명세를 작성합니다.

API 명세에는 다음 항목을 포함합니다.

- API 이름
- HTTP Method
- Endpoint 경로
- 기능 설명
- Request Body
- Response Body
- 성공 상태 코드
- 실패 상태 코드
- 주요 예외 상황
- Swagger 테스트 입력 예시

기본 형식:

````markdown
## API 명세

| 항목 | 내용 |
| --- | --- |
| API 이름 |  |
| Method |  |
| Endpoint |  |
| 설명 |  |
| 성공 상태 코드 |  |
| 실패 상태 코드 |  |

### Request Body

```json
{
  "input": "example"
}
```

### Response Body

```json
{
  "result": "example"
}
```

### 예외 상황

| 상황 | 상태 코드 | 응답 메시지 |
| --- | --- | --- |
|  |  |  |
````

API 명세를 먼저 작성하면 프론트엔드, 테스트, README 작성이 쉬워집니다.

## 4. Request / Response 설계 기준

Request와 Response는 명확하고 예측 가능해야 합니다.

Request 설계 기준:

- 필수 입력값과 선택 입력값을 구분합니다.
- 문자열, 숫자, 리스트, 파일 등 데이터 타입을 명확히 합니다.
- 너무 많은 정보를 한 번에 받지 않습니다.
- API Key나 비밀번호를 Request Body에 직접 넣도록 설계하지 않습니다.
- AI 모델 옵션은 처음에는 최소한으로 둡니다.

Response 설계 기준:

- 성공 여부를 알 수 있어야 합니다.
- 핵심 결과를 명확한 필드로 반환합니다.
- 사용자에게 보여줄 메시지와 내부 디버그 정보를 구분합니다.
- 오류 응답 형식을 일관되게 유지합니다.
- 프론트엔드가 바로 사용할 수 있는 구조로 반환합니다.

좋은 Response 예시:

```json
{
  "summary": "회의 핵심 요약입니다.",
  "action_items": [
    "다음 주까지 자료 정리",
    "고객 피드백 분석"
  ],
  "message": "요약이 완료되었습니다."
}
```

나쁜 Response 예시:

```json
{
  "data": "끝"
}
```

문제점:

- 어떤 결과인지 알기 어렵습니다.
- 프론트엔드에서 필드를 활용하기 어렵습니다.
- 사용자에게 보여줄 정보가 부족합니다.

## 5. Pydantic schema 작성 기준

FastAPI에서는 Pydantic schema를 사용해 Request와 Response 구조를 정의합니다.

작성 기준:

- Request schema와 Response schema를 분리합니다.
- 필드 이름은 의미가 드러나도록 작성합니다.
- 필수값은 명확히 표시합니다.
- 기본값이 필요한 경우 이유가 분명해야 합니다.
- 간단한 검증은 Pydantic 필드 제약으로 처리합니다.
- schema 파일은 `app/api/schemas/` 아래에 둡니다.

예시:

```python
from typing import Annotated
from pydantic import BaseModel, StringConstraints


class SummarizeRequest(BaseModel):
    text: Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1)]


class SummarizeResponse(BaseModel):
    summary: str
    action_items: list[str]
    message: str
```

주의:

- 실제 API Key나 토큰을 schema 예시에 넣지 않습니다.
- 너무 복잡한 중첩 구조는 MVP 단계에서 피합니다.
- schema 이름은 기능과 역할이 드러나게 작성합니다.

## 6. router, service, schema 계층 분리 기준

FastAPI 프로젝트는 역할별로 파일을 분리합니다.

기본 분리 기준:

| 계층 | 위치 | 역할 |
| --- | --- | --- |
| router | `app/api/routes/` | HTTP 요청을 받고 응답을 반환합니다. |
| schema | `app/api/schemas/` | Request/Response 데이터 구조를 정의합니다. |
| service | `app/services/` | 실제 처리 로직, AI API 호출, 외부 API 연동을 담당합니다. |

router의 역할:

- Endpoint 경로를 정의합니다.
- Request schema를 받습니다.
- service 함수를 호출합니다.
- Response schema로 결과를 반환합니다.
- HTTPException을 사용해 API 오류를 반환합니다.

service의 역할:

- AI 모델 호출
- 텍스트 전처리
- 결과 가공
- 외부 API 호출
- 핵심 비즈니스 로직 처리

schema의 역할:

- 입력과 출력 데이터 형식 정의
- Swagger 문서 자동 생성 지원
- 입력값 검증 지원

나쁜 구조:

```text
router 파일 안에 AI 호출 코드, 데이터 검증, 결과 가공 로직이 모두 들어 있음
```

좋은 구조:

```text
router는 요청과 응답만 담당
service는 실제 처리 담당
schema는 데이터 구조 담당
```

## 7. 예외 처리 기준

API는 실패 상황을 예측하고 일관된 오류 응답을 제공해야 합니다.

기본 예외 처리 기준:

- 입력값이 누락되거나 빈 문자열·공백 문자열·잘못된 타입이면 `422 Unprocessable Entity`를 반환합니다.
- 요청 데이터 형식이 틀리면 FastAPI/Pydantic의 `422 Unprocessable Entity`를 활용합니다.
- 외부 제공자의 타임아웃·연결 실패·요청 거부·사용 불가능한 응답은 `502 Bad Gateway`로 통일합니다. SDK별 제공자 오류와 응답 해석·검증 실패는 서비스 어댑터에서 `ProviderError`로 변환하고, 라우터는 `TimeoutError`, `ConnectionError`, `ProviderError`를 502로 변환합니다.
- 예상하지 못한 애플리케이션 내부 오류는 `500 Internal Server Error`입니다. 모든 예외를 제공자 오류로 간주하지 않습니다. 사용자에게 원래 예외나 비밀값을 반환하지 않습니다.
- 존재하지 않는 리소스는 `404 Not Found`를 반환합니다.
- 서버 내부 오류는 상세 비밀 정보를 노출하지 않습니다.

오류 응답 예시:

```json
{
  "detail": "Summary provider unavailable"
}
```

주의:

- 실제 API Key, 토큰, 내부 환경 변수 값을 오류 메시지에 포함하지 않습니다.
- 전체 stack trace를 사용자 응답에 그대로 반환하지 않습니다.
- 로그에는 원인 분석에 필요한 정보만 남기고 민감 정보는 제외합니다.

## 8. Swagger 테스트 기준

FastAPI는 기본적으로 Swagger UI를 제공합니다.

기본 접속 주소:

```text
http://127.0.0.1:8000/docs
```

Swagger 테스트 절차:

1. FastAPI 서버를 실행합니다.
2. 브라우저에서 `/docs`에 접속합니다.
3. 테스트할 API를 선택합니다.
4. `Try it out`을 클릭합니다.
5. Request Body에 예시 데이터를 입력합니다.
6. `Execute`를 클릭합니다.
7. 상태 코드와 Response Body를 확인합니다.
8. 빈 입력값 또는 잘못된 입력값도 테스트합니다.

Swagger 테스트 기준:

- 성공 요청이 200 상태 코드를 반환합니다.
- 응답 필드가 API 명세와 일치합니다.
- 잘못된 입력에 대해 적절한 오류가 반환됩니다.
- 민감 정보가 응답에 포함되지 않습니다.
- README에 테스트 방법을 기록할 수 있습니다.

## 9. 산출물 기준

공통 산출물 계약에서 지정한 템플릿을 사용합니다. 추가 분석은 그 결과와 함께 설명합니다.

## 10. 예시 API 명세

아래는 "AI 회의록 요약 API" 예시입니다.

## API 명세

| 항목 | 내용 |
| --- | --- |
| API 이름 | 회의록 요약 API |
| Method | `POST` |
| Endpoint | `/api/summarize` |
| 설명 | 회의록 텍스트를 입력받아 핵심 요약과 할 일 목록을 반환합니다. |
| 성공 상태 코드 | `200 OK` |
| 실패 상태 코드 | `422 Unprocessable Entity`, `502 Bad Gateway`, `500 Internal Server Error` |

### Request Body

```json
{
  "text": "오늘 회의에서는 신규 고객 피드백 분석 일정과 다음 주 발표 자료 준비를 논의했습니다."
}
```

### Response Body

```json
{
  "summary": "신규 고객 피드백 분석 일정과 다음 주 발표 자료 준비가 논의되었습니다.",
  "action_items": [
    "고객 피드백 분석 일정 정리",
    "다음 주 발표 자료 준비"
  ],
  "message": "요약이 완료되었습니다."
}
```

### 예외 상황

| 상황 | 상태 코드 | 응답 메시지 |
| --- | --- | --- |
| 텍스트 누락·빈 문자열·공백·잘못된 타입 | `422 Unprocessable Entity` | FastAPI 기본 검증 오류 `detail` 배열 |
| 제공자 타임아웃·연결 실패·거부·사용 불가능한 응답 | `502 Bad Gateway` | `Summary provider unavailable` |
| 예상하지 못한 애플리케이션 내부 오류 | `500 Internal Server Error` | `Internal Server Error` |

### 예시 Pydantic Schema

```python
from typing import Annotated
from pydantic import BaseModel, StringConstraints


class SummarizeRequest(BaseModel):
    text: Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1)]


class SummarizeResponse(BaseModel):
    summary: str
    action_items: list[str]
    message: str
```

### 예시 파일 배치

```text
backend/
└── app/
    ├── main.py
    ├── api/
    │   ├── routes/
    │   │   └── summarize.py
    │   └── schemas/
    │       └── summarize.py
    └── services/
        └── summarize_service.py
```

### Swagger 테스트 입력

```json
{
  "text": "오늘 회의에서는 신규 고객 피드백 분석 일정과 다음 주 발표 자료 준비를 논의했습니다."
}
```

기대 결과:

- 상태 코드 `200`을 반환합니다.
- `summary`, `action_items`, `message` 필드가 포함됩니다.
- 실제 API Key나 내부 설정값은 응답에 포함되지 않습니다.
