# 기존 설치 업데이트와 GitHub 게시 기록

사용자가 GitHub 업로드와 기존 설치 덮어쓰기 지원 확인을 요청하여 수행했습니다. 최초 클론은 깨끗했고 이후 작업 트리에는 이 대화에서 작성한 수업용 수정본만 있었습니다. 기존 사용자 전역 설치는 변경하지 않았습니다.

## 원격과 게시 방식

원격은 `https://github.com/PieterKim/vibe-frame-kit.git`, 기본 브랜치는 main입니다. 게시 전 원격 기준은 `eb4ff29cafa8cceba238b9d8f81ebaf660a5b904`로 로컬 HEAD와 같았습니다. GitHub API에서 쓰기 권한과 main 비보호 상태를 확인했습니다. 검증한 수정본을 main에 커밋하고 force 없이 fast-forward push합니다. PR·merge는 요청하지 않아 수행하지 않습니다. 실제 게시 결과와 SHA는 GitHub main 커밋 이력 및 최종 응답으로 확인합니다.

## 검증과 덮어쓰기 조건

일반 회귀 검사 15개와 원래 설치본 통합 검사 4개 그룹(14개 하위 시나리오)이 통과했습니다. PowerShell·Windows Git Bash에서 원본 Kit 파일의 LF/CRLF, 백업·업데이트·동일 재설치, 사용자 추가·수정·충돌, 실제 파일 잠금 실패 후 롤백·재시도를 확인했습니다. 새 Codex 세션의 실제 skills/list에서도 10개를 확인했습니다. native macOS/Linux, 모델을 통한 호출·출력 품질, 실제 외부 API·Gmail 발송은 미실행입니다.

수정하지 않은 지원 원래 버전은 `--migrate-legacy`로 백업 후 덮어쓸 수 있습니다. 사용자 수정이 있으면 강제 덮어쓰지 않습니다. 명령과 경로는 [설치 안내](install-test.md#원래-전역-설치본-업데이트)를 확인합니다. 업데이트 시험은 임시 CODEX_HOME에서만 수행했습니다.
