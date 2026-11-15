# Garmin Training Agent

AWS AI-DLC를 이용해 개발을 진행하기 위한 초기 저장소다.
제품 범위, Garmin 연동 방식, 기술 스택은 아직 정하지 않았다.

## 구조

```text
AGENTS.md                         프로젝트 작업 지침 + 공식 AI-DLC 안내
.agents/skills/                   공식 Codex AI-DLC 스킬
.codex/                           공식 AI-DLC 설정, 에이전트, 훅, 도구
aidlc/spaces/default/
    memory/                       조직/프로젝트 규칙과 단계별 규칙
    knowledge/documents/          요구사항 및 참고 자료 원본
    intents/                      향후 작업별 계획·설계·검증 기록
docs/
    decisions/                    프로젝트 공통 설계 결정(ADR)
```

`aidlc/` 안의 intent와 상태 파일은 실제 워크플로가 시작될 때 엔진이 생성한다.
아직 실행 중인 제품 개발 intent는 없다. 앱 소스와 테스트 디렉터리는 기술 선택 후 만든다.

## 시작하기

필수 도구: Bun, Codex CLI 0.145.0 이상. 기존 Codex 모델 및 인증 설정을 사용한다.

```bash
cd /path/to/garmin-training-agent
bun .codex/tools/aidlc.ts doctor
codex
```

새 Codex 세션에서 프로젝트를 신뢰하고, 훅 신뢰 안내가 나오면 확인한다.
이후 다음 요청으로 제품 정의부터 시작할 수 있다.

```text
$aidlc Garmin Training Agent의 목표 사용자, 핵심 기능, Garmin 연동 요구사항부터 정의해 줘.
```

진행 상태는 `$aidlc --status`, 환경 점검은 `$aidlc --doctor`로 확인한다.
기본 구조 구성만 완료했으며 앱 빌드, Garmin 실연동, 배포는 수행하지 않았다.

## AI-DLC 버전 및 갱신

공식 [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)의
**v2.11.4** copy runtime 중 Codex 구성을 사용한다. Bun으로 실행하므로 전역 aidlc 설치는 필요 없다.
외부 MCP 서버는 추가하지 않았다.

원본 배포 파일: `aidlc-copy-runtime-2.11.4.tar.gz`

SHA-256: `6afc1a6e58773918764b3a8aae23ff8f2b9629a8da74b17a2a5b8fccfc8eea3a`

갱신 시 공식 릴리스와 체크섬을 확인하고 공식 config 명령을 사용한다.
`AGENTS.md`의 AI-DLC 마커 바깥 지침과 `memory/project.md`를 유지한다.

- [공식 시작 안내](https://awslabs.github.io/aidlc-workflows/guide/01-getting-started/)
- [Codex 안내](https://awslabs.github.io/aidlc-workflows/guide/harnesses/codex-cli/)
