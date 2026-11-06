# 수업 단계와 공통 통과 기준

같은 문장이나 코드를 강제하지 않습니다. 강사와 수강생은 같은 필수 항목, 기능 범위, 데이터 계약과 검증 근거로 결과를 비교합니다. 템플릿의 빈칸을 채웠다는 사실만으로 통과하지 않습니다.

| 단계 / Skill | 입력 | 산출물 | 문서 통과 기준 |
| --- | --- | --- | --- |
| 요구사항 / requirements-definition | 아이디어·사용자 상황 | requirements-template.md | 목표·입출력·R-ID·예외·관찰 가능한 수용 기준·제약·미정 사항 |
| 기능 분해 / function-breakdown | 요구사항 | function-breakdown-template.md | 모든 핵심 R-ID가 F-ID와 연결되고 데이터 형식·의존성·실패 흐름·검증이 정의됨 |
| MVP / mvp-planning | 요구사항·기능표·시간 | mvp-plan-template.md | 포함·제외·순서·기능 동작과 AI 품질 테스트·가정·미정 사항이 정의됨 |
| 구조 / project-structure-builder | MVP·기존 파일 | project-structure-template.md | 기능과 모듈·API 계약·상태·오류·실행·검증이 연결됨 |
| 구현 / api-service-builder 또는 ai-agent-workflow-builder | 합의한 기능·계약 | API/Agent 양식·요청된 코드 | 정상/오류/종료 경로와 실제 검증 근거가 있음 |
| 디버깅 / debugging-coach | 재현·가린 로그·코드 | 수정·테스트 기록 | 수정 전 재현과 수정 후 결과를 비교함 |
| 검증 / 해당 구현 Skill | 수용 기준·고정 입력 | test-scenario-template.md | 자동/수동·실제 결과·실패/미실행 사유가 구분됨 |
| 리팩토링 / refactoring-coach | 동작 기준·기존 코드 | 수정·회귀 검증 | 요청 범위에서 동작 보존을 확인함 |
| 문서 / readme-report-writer | 실제 코드·검증·기여 | README·final-report-template.md | 재현 가능한 실행 방법과 기여·시연 근거·한계가 있음 |
| 보안 / security-checker | 공유 대상 파일 | 점검·조치 기록 | 비밀값을 노출하지 않고 위치와 조치를 제시함 |

모든 양식은 프로젝트 `templates/`에 있습니다. 단계 말미에는 판정(통과/보완 필요/확인 필요), 근거, 미해결 항목, 다음 권장 작업을 씁니다. 핵심 계약에 영향을 주는 미정 사항은 확인 필요입니다. 후순위 결정은 담당·시점·영향을 적고 현재 범위를 진행할 수 있습니다. 문서 통과는 서비스 실행 통과를 의미하지 않습니다. 사용자가 요청한 단계에서 멈추며, 여러 단계 요청은 그 범위까지 진행합니다.

선택 실습은 [advanced-labs.md](advanced-labs.md), 환경 기준은 [environment.md](environment.md), 팀 제출은 [team-delivery.md](team-delivery.md)를 사용합니다.
