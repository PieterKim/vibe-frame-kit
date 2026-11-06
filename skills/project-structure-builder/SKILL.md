---
name: project-structure-builder
description: 합의한 MVP의 모듈 및 데이터 계약을 설계하거나 요청된 초기 구조를 생성할 때 사용합니다.
---

## 공통 산출물 계약

- 본문 예시는 설명용입니다. 최종 필수 구조는 `templates/project-structure-template.md`를 단일 기준으로 사용합니다.
- 프로젝트 설치에서는 프로젝트 루트의 `templates/`, `docs/`, `agents/`를 읽습니다. 전역 설치에서는 `$CODEX_HOME/vibe-frame-kit/`(미설정 시 `~/.codex/vibe-frame-kit/`)의 같은 자료를 읽습니다.
- `docs/course-workflow.md`의 해당 단계 완료 기준으로 통과 / 보완 필요 / 확인 필요와 근거를 기록합니다. 적용되지 않는 항목도 이유를 남깁니다.
- 계획만 요청받으면 코드나 실행 환경을 생성하지 않습니다. 다음 단계는 사용자가 요청한 범위 안에서만 수행합니다.
- 구현·수정 시 `templates/test-scenario-template.md`에 자동/수동 구분, 기대값, 실제 결과, 통과/실패/미실행 및 이유를 기록합니다. 안내만 했으면 실행 완료로 보고하지 않습니다.

# Project Structure Builder

## 1. 목적

이 Skill의 목적은 AI 서비스 개발을 위한 기본 프로젝트 구조를 생성하는 것입니다.

Codex는 요구사항 정의서, 기능 분해표, MVP 계획서를 바탕으로 수업 시간 안에 구현 가능한 프로젝트 폴더와 파일 구조를 제안하거나 생성해야 합니다.

기본 구조는 Python과 FastAPI 백엔드를 중심으로 하며, 이후 LangChain 또는 LangGraph, OpenAI API 또는 Gemini API, FAISS 또는 ChromaDB, React/Next/Nuxt 프론트엔드로 확장할 수 있어야 합니다.

## 2. 사용 상황

다음과 같은 상황에서 이 Skill을 사용합니다.

- MVP 범위가 정해졌고 실제 프로젝트 폴더를 만들어야 할 때
- FastAPI 기반 AI 서비스 백엔드 구조가 필요할 때
- OpenAI API 또는 Gemini API 연동을 고려한 구조가 필요할 때
- LangChain 또는 LangGraph 기반 Agent Workflow 확장을 염두에 둘 때
- FAISS 또는 ChromaDB 기반 벡터 검색 기능을 나중에 추가할 수 있어야 할 때
- React, Next, Nuxt 등 프론트엔드를 나중에 붙일 수 있는 구조가 필요할 때
- 수강생이 프로젝트 파일을 어디에 만들어야 할지 모를 때

Codex는 프로젝트 구조를 만들기 전에 관련 요구사항과 기존 파일을 먼저 확인해야 합니다.

## 3. 기본 백엔드 폴더 구조

백엔드는 Python과 FastAPI를 기본으로 구성합니다.

권장 기본 구조:

```text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── api/
│   │   ├── routes/
│   │   │   └── health.py
│   │   └── schemas/
│   ├── services/
│   │   └── ai_service.py
│   ├── agents/
│   │   └── workflow.py
│   ├── vectorstores/
│   │   └── README.md
│   ├── models/
│   └── utils/
├── tests/
├── requirements.txt
└── README.md
```

각 폴더의 역할:

| 경로 | 역할 |
| --- | --- |
| `backend/app/main.py` | FastAPI 애플리케이션 진입점입니다. |
| `backend/app/core/config.py` | 환경 변수와 설정값을 관리합니다. |
| `backend/app/core/security.py` | 인증, 토큰, 보안 관련 유틸리티를 둘 수 있습니다. |
| `backend/app/api/routes/` | API 라우터를 기능별로 분리합니다. |
| `backend/app/api/schemas/` | 요청과 응답 데이터 구조를 정의합니다. |
| `backend/app/services/` | AI 호출, 외부 API 연동, 핵심 비즈니스 로직을 둡니다. |
| `backend/app/agents/` | LangChain 또는 LangGraph 기반 Agent Workflow를 둡니다. |
| `backend/app/vectorstores/` | FAISS 또는 ChromaDB 연동 코드를 확장할 수 있는 위치입니다. |
| `backend/app/models/` | 데이터 모델 또는 DB 모델을 둡니다. |
| `backend/app/utils/` | 공통 유틸리티 함수를 둡니다. |
| `backend/tests/` | 백엔드 테스트 코드를 둡니다. |

처음부터 모든 파일에 복잡한 코드를 넣지 않습니다. MVP에 필요한 최소 파일만 만들고, 확장 가능성을 위해 폴더를 분리합니다.

## 4. 선택적 프론트엔드 폴더 구조

프론트엔드가 필요한 경우 `frontend/` 폴더를 추가합니다.

React, Next, Nuxt 중 어떤 프레임워크를 사용할지는 수업 조건과 프로젝트 목표에 따라 결정합니다.

권장 기본 구조:

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   │   └── api.ts
│   ├── styles/
│   └── utils/
├── public/
├── package.json
└── README.md
```

각 폴더의 역할:

| 경로 | 역할 |
| --- | --- |
| `frontend/src/components/` | 재사용 가능한 UI 컴포넌트를 둡니다. |
| `frontend/src/pages/` | 화면 단위 파일을 둡니다. Next 또는 Nuxt에서는 프레임워크 규칙에 맞게 조정합니다. |
| `frontend/src/services/api.ts` | 백엔드 API 호출 함수를 둡니다. |
| `frontend/src/styles/` | CSS 또는 스타일 관련 파일을 둡니다. |
| `frontend/src/utils/` | 프론트엔드 공통 유틸리티를 둡니다. |
| `frontend/public/` | 정적 파일을 둡니다. |

프론트엔드가 MVP에 꼭 필요하지 않다면 먼저 FastAPI API와 간단한 테스트 방식으로 MVP를 검증할 수 있습니다.

## 5. .env.example 작성 기준

`.env.example`은 실제 비밀값이 아니라 필요한 환경 변수 이름과 예시 값을 보여주는 파일입니다.

작성 기준:

- 실제 API Key, 토큰, 비밀번호를 작성하지 않습니다.
- 예시 값은 `your_api_key_here`처럼 가짜 값으로 작성합니다.
- OpenAI와 Gemini 중 하나만 써도 되지만, 확장 가능성을 위해 둘 다 예시로 둘 수 있습니다.
- 사용하지 않는 환경 변수는 README에서 선택 사항으로 표시합니다.
- `.env` 파일은 Git에 커밋하지 않도록 `.gitignore`에 포함합니다.

예시:

```env
# AI provider
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
AI_PROVIDER=openai

# Vector database
VECTOR_DB_PROVIDER=faiss
CHROMA_DB_PATH=./data/chroma
FAISS_INDEX_PATH=./data/faiss/index

# App
APP_ENV=development
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

주의:

- Codex는 실제 `.env` 값을 출력하지 않습니다.
- 사용자가 실제 키를 제공해도 문서나 코드에 다시 노출하지 않습니다.

## 6. requirements.txt 작성 기준

`requirements.txt`는 MVP 실행에 필요한 최소 의존성부터 작성합니다.

기본 포함 권장 패키지:

```text
fastapi
uvicorn
python-dotenv
pydantic
```

OpenAI API를 사용할 경우:

```text
openai
```

Gemini API를 사용할 경우:

```text
google-genai
```

LangChain 또는 LangGraph 확장이 필요한 경우:

```text
langchain
langgraph
```

FAISS 또는 ChromaDB 확장이 필요한 경우:

```text
faiss-cpu
chromadb
```

작성 원칙:

- MVP에서 사용하지 않는 패키지를 무리하게 넣지 않습니다.
- 수업 환경에서 설치가 어려운 패키지는 선택 사항으로 분리합니다.
- 패키지 버전 고정이 필요하면 수업 환경에서 검증한 뒤 작성합니다.
- `requirements.txt`에는 비밀값이나 환경 변수 값을 넣지 않습니다.

## 7. README 초기 작성 기준

프로젝트 구조를 생성할 때 README도 함께 초기 작성합니다.

README 초기 문서에는 다음 항목을 포함합니다.

- 프로젝트명
- 프로젝트 소개
- MVP 목표
- 주요 기능
- 기술 스택
- 폴더 구조
- 설치 방법
- 환경 변수 설정 방법
- 실행 방법
- API 사용 예시
- 테스트 또는 수동 확인 방법
- 향후 개선 방향

README는 완성 후에만 작성하는 문서가 아닙니다. 프로젝트 초기에 작성해두면 수강생이 현재 목표와 실행 방법을 잃지 않고 개발할 수 있습니다.

## 8. 프로젝트 구조 생성 절차

Codex는 다음 순서로 프로젝트 구조를 생성합니다.

1. 요구사항 정의서, 기능 분해표, MVP 계획서를 확인합니다.
2. 기존 프로젝트 파일이 있는지 확인합니다.
3. 백엔드만 필요한지, 프론트엔드도 필요한지 판단합니다.
4. 기본 기술 스택을 확인합니다.
5. MVP에 필요한 최소 폴더와 파일을 정합니다.
6. `.env.example`, `.gitignore`, `requirements.txt`, README 초기 문서를 포함합니다.
7. 실제 비밀값이 포함되지 않도록 확인합니다.
8. 실행 명령과 확인 방법을 README에 적습니다.
9. 생성된 구조를 사용자에게 요약합니다.

파일 생성 시 주의할 점:

- 기존 파일을 임의로 삭제하지 않습니다.
- 기존 구조가 있으면 그 구조를 우선 존중합니다.
- 불필요하게 복잡한 아키텍처를 만들지 않습니다.
- MVP에 필요 없는 고급 기능은 문서의 후순위로만 남기며 파일은 만들지 않습니다.
- 사용자가 이해할 수 있도록 각 폴더의 목적을 설명합니다.

## 9. 예시 폴더 구조

아래는 AI 서비스 프로젝트의 기본 예시 구조입니다.

```text
ai-service-project/
├── README.md
├── .gitignore
├── .env.example
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   └── summarize.py
│   │   │   └── schemas/
│   │   │       └── summarize.py
│   │   ├── services/
│   │   │   └── ai_service.py
│   │   ├── agents/
│   │   │   └── workflow.py
│   │   ├── vectorstores/
│   │   │   └── README.md
│   │   ├── models/
│   │   └── utils/
│   └── tests/
│       └── test_health.py
├── frontend/
│   ├── README.md
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       │   └── api.ts
│       ├── styles/
│       └── utils/
└── docs/
    ├── requirements.md
    ├── mvp-plan.md
    └── test-plan.md
```

최소 MVP만 빠르게 시작할 때는 아래처럼 더 작게 시작할 수 있습니다.

```text
ai-service-project/
├── README.md
├── .gitignore
├── .env.example
└── backend/
    ├── requirements.txt
    └── app/
        ├── main.py
        ├── api/
        │   └── routes/
        │       └── health.py
        └── services/
            └── ai_service.py
```

## Gemini SDK 선택

신규 Gemini 실습은 `google-genai`의 `from google import genai`와 `genai.Client()`를 사용합니다. 모델명은 환경 기준 결정 전 임의 확정하지 않습니다. 실제 키 없이 연결을 실행하지 않습니다. 공식 안내: https://ai.google.dev/gemini-api/docs/libraries .
