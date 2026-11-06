# 04. 프로젝트 구조 생성 프롬프트

아래 내용을 채운 뒤 Codex에 그대로 붙여넣어 사용하세요.

```text
아래 MVP 계획서를 바탕으로 AI 서비스 개발 프로젝트의 기본 구조를 설계해줘.

작업 모드: 설계만. 실제 파일 생성은 내가 명시적으로 생성 모드를 요청한 경우에만 수행해줘.

## MVP 계획서
여기에 MVP 계획서를 붙여넣어줘.

## 사용할 기술 스택
- Backend:
- AI API:
- Agent Workflow:
- Vector DB:
- Frontend:
- 기타:

## 구조 생성 기준
- Python과 FastAPI 기반 백엔드 구조를 기본으로 해줘.
- Agent가 필요한 MVP에서만 LangChain 또는 LangGraph를 고려해줘.
- OpenAI API 또는 Gemini API를 환경 변수로 연동할 수 있게 해줘.
- 검색이 필요한 MVP에서만 FAISS 또는 ChromaDB를 고려해줘.
- 프론트엔드가 MVP에 필요한지 먼저 판단해줘.
- 실제 API Key나 비밀번호는 절대 작성하지 말고 `.env.example` 예시만 제안해줘. 생성 모드라면 파일을 만들어줘.

## 요청 사항
다음 항목을 포함해줘.

- 생성할 폴더 구조
- 각 폴더와 파일의 역할
- `.env.example` 예시
- `requirements.txt` 초안
- README 초기 내용
- 실행 방법

기존 파일이 있다면 먼저 확인하고, 기존 코드를 임의로 삭제하지 말아줘.

## 공통 산출물 요청
`$project-structure-builder`를 사용하고 `templates/project-structure-template.md`를 최종 필수 구조로 작성해줘. 앞서 제공한 문서는 재사용하고, R-ID → F-ID → MVP → 계약 → T-ID 연결을 유지해줘. 예외·실패 흐름·AI 품질(해당 시)과 미정 사항을 빠뜨리지 마. 마지막에 단계 판정과 근거를 적고 계획 요청에서는 코드 생성이나 다음 단계 진행을 하지 마.
```
