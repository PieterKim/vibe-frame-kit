# 안전한 설치와 확인

Python 3.11+와 Git을 준비합니다. 설치는 네트워크·유료 API·인증 정보 접근을 하지 않습니다. 소스를 먼저 모두 검사하고 충돌은 쓰기 전에 중단합니다. 기본 설치는 기존 다른 Skill·AGENTS·Codex config.toml을 덮어쓰지 않습니다. 원래 Kit만 명시적으로 갱신하는 마이그레이션은 아래 별도 절차를 사용합니다.

## 프로젝트 설치 (기본)

Kit 저장소를 복제한 뒤 Kit 루트에서 실행합니다. `../my-project`는 실제 수업 프로젝트 경로로 바꿉니다.

```powershell
git clone https://github.com/PieterKim/vibe-frame-kit.git
cd vibe-frame-kit
python scripts/install.py --project ../my-project --dry-run
python scripts/install.py --project ../my-project
# Windows 래퍼
powershell -File scripts/install.ps1 -Project ../my-project
```

```bash
# macOS/Linux; Kit 루트에서
bash scripts/install.sh --project ../my-project --dry-run
bash scripts/install.sh --project ../my-project
```

프로젝트의 `.agents/skills/<name>/SKILL.md`, AGENTS.md, agents, templates, prompts, docs, config와 `scripts/check-environment.py`에 설치됩니다. docs/config는 교육 자료이며 Codex 설정 파일로 등록되지 않습니다. 기존 AGENTS.md와 내용이 다르면 자동 병합하지 않고 중단합니다. 기존 지침을 백업하고 필요한 공통 규칙을 수동 통합한 경우에는 Skill만 수동 설치하거나 별도 깨끗한 프로젝트로 설치합니다. 충돌을 해결하려고 기존 파일을 삭제하지 않습니다.

## 선택적 전역 설치

```powershell
python scripts/install.py --scope global --dry-run
python scripts/install.py --scope global
```

CODEX_HOME이 있으면 그 위치, 없으면 `~/.codex`를 사용합니다. Skill만 `skills/`에, 참고 자료와 단독 실행 환경 점검기는 `vibe-frame-kit/`에 둡니다. 전역 AGENTS.md/config.toml은 보존합니다. 전역 설치 후 수업 프로젝트에서 `vibe-frame-kit/AGENTS.md`를 명시적으로 읽도록 요청해야 공통 지침이 적용됩니다. 다른 프로젝트에 공통 수업 규칙을 자동 강제하지 않습니다.

## 재설치·실패·복구

`.vibe-frame-kit-install.json`은 설치된 파일의 해시를 기록합니다. 동일 버전 재설치는 변경 0개입니다. 설치 이후 수정한 파일은 충돌로 보존합니다. 업데이트 전 변경 파일 원본과 recovery.json은 `.vibe-frame-kit-backups/`(전역은 `vibe-frame-kit-backups/`)에 남깁니다. 처리 중 오류가 나면 변경한 파일만 복구하고 새 빈 디렉터리는 남을 수 있습니다. 프로세스 강제 종료나 전원 중단은 자동 복구가 보장되지 않으므로 journal의 existing/created 목록으로 검토합니다. 전체 디렉터리를 지우지 않습니다. 백업·manifest는 학생 프로젝트 Git에서 제외하세요. 상위 경로의 링크/심볼릭 링크는 허용하지 않습니다.

## 실제 Codex 인식과 호출

파일 복사 통과와 실제 클라이언트 인식은 별도입니다. 설치된 프로젝트를 새 Codex 세션으로 열고 Skill 목록에 10개 이름이 나타나는지 확인합니다. 각 이름은 `agents/routing.md`에 있습니다. `$requirements-definition`처럼 직접 호출하고 어떤 Skill을 적용했는지 확인합니다. 계획 요청에서는 코드가 생성되지 않아야 합니다. 목록이나 명시 호출을 확인하지 못했다면 미실행으로 기록합니다. 기존 실행 세션에는 새로 설치한 목록이 반영되지 않을 수 있습니다.

자동 검증: Kit 루트에서 `python scripts/verify.py`. OS별 실제 실행 여부와 모델 호출 여부는 [verification-report.md](verification-report.md)에 기록합니다.

## 원래 전역 설치본 업데이트

원래 설치기는 `~/.codex`에 AGENTS.md와 agents/skills/config/prompts/templates/docs를 복사했지만 설치 manifest를 남기지 않았습니다. 따라서 일반 설치는 기존 내용을 사용자 파일로 보고 충돌로 중단합니다. `--migrate-legacy`를 명시하면 기준 커밋 `eb4ff29cafa8cceba238b9d8f81ebaf660a5b904`의 원래 배포 파일과 일치하는 파일만 백업 후 교체합니다. 인식 기준은 `config/legacy-install-manifest.json`에 있으며 CRLF/LF 차이만 허용합니다.

Kit 저장소의 사용자 변경을 먼저 보존한 뒤 최신 main을 가져옵니다. 다른 사람의 변경이나 로컬 수정을 강제로 지우지 않습니다.

```powershell
git pull --ff-only
powershell -File scripts/install.ps1 -Scope global -MigrateLegacy -DryRun
powershell -File scripts/install.ps1 -Scope global -MigrateLegacy
```

```bash
git pull --ff-only
bash scripts/install.sh --scope global --migrate-legacy --dry-run
bash scripts/install.sh --scope global --migrate-legacy
```

CODEX_HOME을 설정한 설치라면 그 값을 그대로 사용하고, 미설정이면 `~/.codex`에 적용합니다. 위 명령은 실제 설치를 바꾸므로 먼저 dry-run 결과와 대상 경로를 확인합니다. 테스트를 위해 HOME을 바꾸거나 실제 사용자 전역 폴더에 모의 파일을 만들지 않습니다.

- 수정하지 않은 원래 Skill·AGENTS·템플릿 등은 백업 후 최신 내용으로 교체합니다. 원래 경로의 참조를 살리기 위해 기존 자료 경로와 새 `vibe-frame-kit/` 자료 폴더를 함께 관리합니다.
- 사용자가 추가한 별도 파일·다른 Skill·config.toml은 보존합니다.
- 기존 Kit 파일을 사용자가 수정했거나 새 설치 파일과 경로가 충돌하면 전체 쓰기 전에 중단합니다. 강제 덮어쓰기 옵션은 없습니다. 기존 내용을 별도로 보존·비교하거나 깨끗한 프로젝트 범위 설치를 사용합니다.
- 지원 기준 버전이 아니면 자동 인식하지 않습니다. 새 프로젝트 범위로 설치하거나 직접 비교합니다.
- 성공 후 manifest가 생기므로 이후에는 `-MigrateLegacy`/`--migrate-legacy` 없이 같은 전역 설치 명령을 사용합니다. 사용자 수정 파일은 계속 충돌로 보존하고, 동일 버전 재설치는 변경 0개입니다.
- 교체 전 원본은 `vibe-frame-kit-backups/install-*/`에 보관합니다. 처리 중 실패하면 바뀐 파일을 원복하고 manifest도 복구합니다. 문제 원인을 해결한 뒤 같은 마이그레이션 명령으로 재시도합니다. 전원 중단·프로세스 강제 종료는 recovery.json을 검토해야 합니다.

검증 명령: Git checkout의 Kit 루트에서 `python scripts/verify-legacy.py`. Windows PowerShell·Git Bash와 기준 커밋이 필요합니다. 원래 설치기의 출력 파일을 임시 CODEX_HOME에 재현하고 업데이트·충돌·백업·실패 복구를 확인합니다. 원래 설치기 자체는 HOME을 고정 사용하므로 실제 사용자 폴더 보호를 위해 실행하지 않습니다. macOS/Linux에서 이 Windows 통합 검증을 통과했다고 주장하지 않습니다.
