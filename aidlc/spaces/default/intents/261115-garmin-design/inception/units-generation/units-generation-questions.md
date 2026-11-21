# 구현 단위 설계 확인

## 입력과 유지할 결정

[컴포넌트 목록](../domain-design/components.md), [도메인 ADR](../domain-design/decisions.md), [승인된 요구사항](../requirements-analysis/requirements.md)을 따른다. 8개 논리적 책임과 31개 엔티티 소유자, P0 범위, 승인·평가·게시의 권한 분리는 유지한다. 이번 작업은 단위 설계이며 코드 작성·실제 배포를 시작하지 않는다.

실제 저장 자료의 왕복 흐름과 단위의 빌드/테스트 의존 DAG를 구분한다. 단위의 코드나 테스트가 다른 단위 구현을 필요로 하면 반드시 의존 간선을 둔다. 의존이 없는 단위는 공통 계약·합성 사례와 허용된 대역만으로 자체 검증 가능해야 하며, 모든 단위를 결합한 실제 제품 인수 검증은 별도로 남긴다. 경제적인 개발 순서·일정·병렬 실행 여부는 이 단계에서 결정하지 않는다.

## Q1. 승인된 책임을 어떤 개발·배포 단위로 묶을까요?

A. 3개 단위로 구성한다. U1 u1-exchange-spec은 공통 교환 명세·버전·합성 검증 사례를 관리하는 spec, U2 u2-linux-agent는 CoachingWorkflow 외 7개 컴포넌트를 내부 모듈로 담는 Rust 설치형 service, U3 u3-chatgpt-workflow는 CoachingWorkflow의 ChatGPT 워크플로 정의·지원/수동 저장 안내·검증 사례를 제공하는 spec이다. U2와 U3는 U1에 의존한다. U1은 명세를 소유하고 도메인 엔티티 소유권은 바꾸지 않는다. 공통 계약 변경을 독립 검토할 수 있지만 명세와 양쪽 소비자의 호환성 관리가 필요하다. 개인용 운영 단순성과 계약 경계 검증을 함께 고려해 권장한다. 명세·워크플로 spec의 실제 배포 형식/지원 환경은 후속 계약 설계에서 확인한다.
B. 2개 단위로 구성한다. Linux 프로그램(service)과 ChatGPT 워크플로(spec)로 나누고 공통 교환 명세는 Linux 단위가 관리한다. 배포/설계 단위는 줄지만 워크플로의 명세·테스트가 Linux 단위 산출물에 의존하며 계약 변경이 그 단위에 묶인다. 내부 8개 책임·소유 경계는 유지한다.
C. 8개 단위로 세분화한다. OperationControl은 service, CoachingWorkflow는 spec, 나머지는 Linux 실행 프로그램에 내장하는 library로 각각 관리한다. 도메인별 코드·테스트 경계가 명확하지만 라이브러리 간 빌드 의존·계약 관리와 단위별 설계 부담이 커진다. 공통 자료형 소유로 생길 수 있는 순환 의존은 구체 단위 계획에서 해소해야 한다.
X. Other (please specify)

[Answer]: A. U1 u1-exchange-spec(spec), U2 u2-linux-agent(service), U3 u3-chatgpt-workflow(spec)의 3개 단위로 구성한다. U2와 U3는 U1에 의존하고 도메인 책임·엔티티 소유는 유지한다.

## 단위 분해 계획

| Unit ID | Directory | Kind | 범위·배포 형태 | 의존 |
|---|---|---|---|---|
| U1 | u1-exchange-spec | spec | 분석·정책·목표/계획·승인·상태 교환 명세, 버전/호환 기준, 합성 사례. 소비자가 읽어 쓰는 공통 명세로 배포하며 실제 파일 형식·승인 증명 방식은 Contract Design에서 정한다. 도메인 엔티티의 소유권은 가져오지 않는다. | 없음 |
| U2 | u2-linux-agent | service | Rust 설치형 프로그램과 CLI·설치/제거·예약 실행을 제공한다. OperationControl·DataAccessPolicy·ActivityCollection·AnalysisPublication·PlanAdmission·PlanEvaluation·CalendarDelivery를 내부 모듈로 묶고 각 소유 경계를 보존한다. | U1 |
| U3 | u3-chatgpt-workflow | spec | CoachingWorkflow의 목표·계획 작성·수정·명시적 승인 의사·저장 확인·지원 환경 및 수동 대안 안내를 워크플로 정의로 제공한다. 실제 ChatGPT 실행/읽기/쓰기 지원은 검증 조건이다. | U1 |

- 단위 의존성은 빌드/테스트에 필요한 코드·명세의 방향으로 U2→U1, U3→U1이다. U2와 U3는 상대 구현 없이 U1의 합성 사례·공개 계약으로 자체 검증 가능하도록 범위를 정한다. 코드나 필수 테스트가 상대 구현을 요구하게 되면 해당 간선을 추가하고 단위 계획을 재검토해야 한다.
- 실제 사용의 U2 분석 게시→U3 작성/승인 저장→U2 수신/평가/일정 게시라는 자료 흐름은 빌드 의존 DAG와 구분한다. 결합된 전체 흐름과 실제 권한·승인 신뢰의 인수 검증은 별도로 필요하다.
- 단위별 독립 검증과 호환성 검증, 제품 전체의 실제 연동 인수 검증을 구분한다. 경제적 구현 순서·기간·개발자 배정·병렬 실행은 정하지 않는다.
- 기존 P0와 단일 엔티티 소유, 사용자 승인·평가·게시 구분을 유지한다. U1 명세 제공은 승인 신뢰·외부 지원을 검증 완료했다는 의미가 아니다.

## Decomposition Plan Approval

위 3개 단위의 범위·kind·배포 형태와 의존 관계로 단위 문서를 작성할까요?

Approve Plan
Revise Plan

[Answer]: Approve Plan

## Consolidated Summary Confirmation

- 단위 분해 계획은 Approve Plan으로 승인되었다. 기존 P0, 8개 컴포넌트 책임과 31개 엔티티의 단일 소유를 유지한다. 이번 단계는 문서 설계이며 코드 작성·배포를 시작하지 않는다.
- U1 u1-exchange-spec은 spec으로 공통 교환 명세·버전/호환 기준·합성 검증 사례를 제공한다. 명세의 소유와 도메인 엔티티의 소유를 구별한다. 실제 Drive 형식·승인 증명 방식은 Contract Design에서 정한다.
- U2 u2-linux-agent는 service로 Rust 설치형 프로그램·CLI·설치/제거·예약 실행을 제공한다. CoachingWorkflow 외 7개 컴포넌트를 내부 모듈로 유지하며 각 데이터 소유 경계를 보존한다.
- U3 u3-chatgpt-workflow는 spec으로 CoachingWorkflow의 목표·계획 작성/수정·명시적 승인 의사·저장 확인·지원 환경 및 수동 대안 안내를 제공한다. 실제 ChatGPT 실행·읽기·쓰기 지원은 별도 검증한다.
- 빌드/테스트 의존 관계는 U2→U1, U3→U1로 비순환이다. U2와 U3는 상대 구현 없이 U1의 계약·합성 사례와 허용된 대역으로 자체 검증할 수 있어야 한다. 상대 구현이 필수이면 의존 간선과 단위 계획을 재검토한다.
- 실제 자료 흐름인 Linux 분석 게시→ChatGPT 작성·승인 저장→Linux 수신·평가·Calendar 게시와 빌드 의존 DAG를 구분한다. 단위별 검증·명세 호환 검증·제품 전체 실제 연동 인수 검증을 따로 기록한다.
- 경제적 구현 순서·일정·개발자 배정·병렬 실행 여부는 결정하지 않는다. 의존이 없는 단위의 동시 개발 가능성만 조건과 함께 문서화한다.
- unit-of-work.md, unit-of-work-dependency.md, unit-of-work-story-map.md, traceability.json을 작성한다. 단위별 범위·kind·배포 형태·상대 복잡도·제약, 비순환 의존 YAML·관계도와 텍스트 대체, 기능 요구사항 83개의 단위 연결을 검증하고 독립 검토한다.
- 승인·형식·안전 검증과 LLM 평가·게시 상태를 구별한다. 외부 지원·승인 신뢰·공유 정책 최신성이 검증되지 않았으며 신뢰성 있는 확인이 불가하면 관련 자동화를 보류한다.

Looks correct
Request changes

[Answer]: Looks correct
