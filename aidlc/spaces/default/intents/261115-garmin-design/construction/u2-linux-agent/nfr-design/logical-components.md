# U2 Linux 에이전트 논리 실행 자원과 소유 경계

## Sources

[기능 명세](../functional-design/functional-spec.md)의 7개 컴포넌트/기능 상태와 [엔티티 원본](../functional-design/entities.md)의 25개 엔티티를 보존한다. [공유 컴포넌트](../../../inception/domain-design/components.md), [단위 정의](../../../inception/units-generation/unit-of-work.md), [공유 계약](../../../inception/contract-design/contract-summary.md)의 C01·C03~C08·P01~P05, [기술 결정](../nfr-requirements/tech-stack-decisions.md)의 12개 TSD가 경계의 근거다. [성능](../nfr-requirements/performance-requirements.md)·[보안](../nfr-requirements/security-requirements.md)·[용량](../nfr-requirements/scalability-requirements.md)·[복구](../nfr-requirements/reliability-requirements.md)·[관측](../nfr-requirements/observability-requirements.md) 요구사항 및 [설계 Q&A](nfr-design-questions.md)의 OS/저장/검사 선택을 이 경계에 연결한다. 아래 자원은 실행/기술 구성요소이며 새 도메인 엔티티·상시 API 서버·클라우드가 아니다.

<a id="u2-l01"></a>
## U2-L01 — 컴포넌트·공유 자원·실패 영향

소유: 각 행의 기존 컴포넌트. 대응: NFR5.2·NFR5.3·NFR7.2·NFR10.1·NFR11.2.

| 기존 컴포넌트 | 독점 소유 엔티티 | 입력→처리→출력 | 연결 자원/주요 해법 |
|---|---|---|---|
| OperationControl | RuntimeConfiguration, ScheduleRegistration, ExecutionRecord, MaintenanceRequest | 설정 후보/기대 개정·예약/즉시/복귀 목적→검증/실행권/집계→유효 개정·단계별 결과/조치 | CLI·시스템 타이머/oneshot·공통 slice·실행 lock·SQLite 실행/예산 부속 기록; U2-P02/P04·U2-C02·U2-R01/R04·U2-O01/O02 |
| DataAccessPolicy | ServiceConnection, CredentialReference, SharingConsent, RetentionPolicy | 연결/현재 정책·업무 목적/대상→최소 권한·동의/철회·보존 확인→허용/차단 근거 | host-key 암호화 credential·읽기 전용 서비스 전달·SQLite 정책; U2-SEC01/SEC03·U2-O03 |
| ActivityCollection | ActivityRecord, CollectionCursor, CollectionIssue | 유효 수집 범위/pending→P05 적격 확인·페이지/상세 검증/확정→개정 활동·확정 커서/미완료 | Garmin HTTP 어댑터(미적격 비활성)·SQLite 원천/커서; U2-C01/C03·U2-R01/R05 |
| AnalysisPublication | AnalysisSnapshot, RepositoryPublication, RepositoryConflict | 고정 활동 개정/기간·대상→정확 분석/투영·선Detail/후루트·원격 대조→불변 분석/대상별 결과 | SQLite·파생 JSON 파일·유한 분석/Schema 캐시·Drive/GitHub 어댑터; U2-P01/P03·U2-SEC03·U2-R02/R03/R05/R06 |
| PlanAdmission | ReceivedPlanArtifact, ApprovalProof, AdmittedPlanSnapshot, AdmissionAssessment, AdmittedPlanDisposition | 고정 Drive C05/C06/C07·평가 근거/최종 효과 요청→엄격 수신/독립 승인/안전/현재 계보→불변 검증 사본/시점별 판정/처분 | Drive 수신·보호 파일/SQLite·등록 Schema/JCS·승인/안전 검사 경계(미적격 차단); U2-SEC02/SEC04·U2-R02/R07 |
| PlanEvaluation | EvaluationRequest, EvaluationResult | 정확 검증 스냅샷/허용 분석→모델/비용 적격·비스트리밍 요청/근거 재검사→평가/제안/확인실패/미확인 | SQLite·OpenAI HTTP 후보/미정 로컬사설 경계·CPU 제한 자식; U2-P02·U2-SEC04/SEC05·U2-R04/R07 |
| CalendarDelivery | PublicationIntent, CalendarBinding, DeliveryAttempt, CalendarConflict | 정확 계획/처분·평가 근거/시각 값→PlanAdmission 최종 판정 요청·의도/고정ID/조건부 효과·대조→세션별 결과 | SQLite·Calendar HTTP·IANA/tzdb/시계; U2-SEC03/SEC04·U2-R03/R06·U2-O02 |

25개 엔티티는 위에서 각각 한 번만 소유된다. 컴포넌트 간에는 식별자·정확한 불변 버전/결과 참조를 전달한다. 공통 SQLite 파일/HTTP 실행기/검사 라이브러리를 공유해도 도메인 공동 쓰기는 허용하지 않는다. OperationControl은 조정/기술적 공통 예산을 맡고 각 소유자의 성공을 대신 판정하지 않는다. CalendarDelivery→PlanAdmission 최종 판정 요청은 허용하지만 PlanAdmission→PlanEvaluation 역호출 순환을 추가하지 않는다. 시간 설정은 OperationControl이 전달하며 CalendarDelivery가 역호출로 바꾸지 않는다.

OperationControl은 등록 connectionIds와 분석 선택 analysisTargets·Drive 계획 수신 planInboxConnectionId를 별도 개정/저장/복귀한다. 분석0개는 로컬 분석을 보존하며 외부 미게시이고 Drive 분석 해제가 계획 수신을 해제하지 않는다. AnalysisPublication은 선택된 저장소/모든 최종 독자, PlanAdmission은 계획 수신 선택만 소비한다. DataAccessPolicy는 chatgpt FINAL_READER의 credentialReferenceId/endpointReference/modelReference=null과 독립 SharingConsent→C04 service/purpose/targetAlias 대응을 소유한다. 최종 독자 역할을 Linux HTTP 어댑터/직접 실행 권한으로 만들지 않는다. 등록·선택·동의는 서로 대체 불가이며 실제 독자 경로/주체·정책 현재성 미입증은 보류한다.

텍스트 실행도: 일반 CLI/시스템 타이머 → OperationControl → COLLECTION_SYNC의 ActivityCollection→AnalysisPublication 또는 PLAN_CHECK의 PlanAdmission→PlanEvaluation→CalendarDelivery. CalendarDelivery는 평가 근거를 PlanAdmission에 전달해 최종 판정을 얻는다. 모든 외부 요청 소유자는 DataAccessPolicy의 현재 근거와 OperationControl의 영속 예산 경계를 거친다. 이 호출은 프로세스 내부 논리 인터페이스이며 새 네트워크 서버가 아니다.

| 논리 자원/경계 | 기술 관리/도메인 책임 | 실패 영향·격리·복귀 |
|---|---|---|
| 목적별 timer/oneshot·lock | OperationControl, 고정 일반 UID | 해당 목적 새 실행 차단/지연 명시; 다른 목적 설정 보존, 도메인 중복은 CAS/원 의도 별도 검사 |
| 공통 slice·전체 자식 그룹 | OperationControl, 각 자식 소유자 | 한 서비스 OOM/강제 종료는 미완료/미확인; 공유 메모리 압박은 양쪽 영향, 실제 합산 측정 실패면 미검증 |
| SQLite/WAL/보호 로컬 마운트 | 저장 어댑터 기술 관리·각 repository 독점 내용 | DB/장치 실패는 관련 새 효과 모두 차단, 손상 DB 자동 초기화 금지; 읽기 가능 복귀 상태60초 |
| 파생 JSON/임시본 | 각 파일 소유자 | 해당 분석/수신 사본 보류, 이전 유효본·다른 대상 성공 유지; 파일/DB digest 대조 |
| 암호화 credential/호스트 키·읽기 전용 전달 | OS 관리·DataAccessPolicy | 해당 연결 비활성/재등록 조치; 평문 fallback/GUI키링 의존 없음 |
| 프로필별 HTTP/TLS | 각 외부 효과 소유자 | 목적/대상별 timeout/거절/미확인 격리, 원 의도 대조 우선; 다른 확정 결과 취소 안 함 |
| 엄격 JSON/고정 registry/JCS·CPU 자식 | 소비 컴포넌트, U1은 고정 규범만 소유 | 오류 문서/계획 전체 보류; 하위 시간/RSS 제한, 외부 지시 실행 안 함 |
| 안전한 기록/한국어 CLI | 생산 소유자 사실·OperationControl 집계 | 진단 저장 실패도 숨기지 않음, 원문 echo/타 생산자 대리 성공 금지 |

독립 U2 시험은 U1 고정 규범/사례와 U2 자체 합성 대역만 필요하다. 형제 construction 문서·실행기·DB·실제 U3 연결을 필수 의존으로 두지 않는다. 실제 왕복 제품 인수는 별도이며 알려진 모델 위험/활성화 보류는 [U2-O04](observability-design.md#u2-o04)가 원본이다.

<a id="u2-l02"></a>
## U2-L02 — OS 배치와 기술 결정 기록

소유: OperationControl(서비스/타이머·설치 조건), 각 어댑터 소유자(실제 적격), 후속 U2 개발/품질 담당(고정/시험). 대응: NFR8.4·NFR8.6·NFR11.1·NFR11.2.

시스템 관리자에 COLLECTION_SYNC 기본1시간·PLAN_CHECK 기본15분의 독립 timer와 Type=oneshot 서비스를 둔다. 설치 때 확인한 비-root UID/GID와 실제 고정 설치/데이터 경로를 명시한다. AccuracySec=1초·RandomizedDelaySec=0초를 설계 값으로 사용한다. 타이머는 로그인 세션과 분리되나 부팅/로그아웃·절전 복귀·마운트/credential·권한·실제 예정/시작은 Ubuntu에서 시험해야 한다. PC 전원 꺼짐/절전·실행권 대기/중복 억제를 정상 시작≤60초로 대신하지 않는다.

설정 후보는 기존 유효 개정/OS 등록을 먼저 보존한다. 검증한 후보→로컬 개정/등록 의도→고정 OS unit 갱신→실제 등록/내용 대조→예약 상태 결과 확정으로 진행하며 DB와 OS의 단일 원자 확정을 가정하지 않는다. 중간 실패는 기존 유효본/실제 OS 상태·불일치/보류를 표시하고 재대조한다. 실패를 ACTIVE로 바꾸거나 승인하지 않은 이전/새 설정을 임의 선택하지 않는다. 중단은 해당 목적 새 실행을 막으며 진행 효과/미확인은 보존한다.

앱 cutoff570초+정리30초를 보조하도록 oneshot에 TimeoutStartSec=595초·TimeoutStopSec=5초·KillMode=control-group과 최종 강제 종료를 설계한다. RuntimeMaxSec는 oneshot에 적용되지 않으므로 사용 근거로 삼지 않는다. 별도 긴 ExecStop/자동 재시작 연쇄로600초를 늘리지 않는다. 공통 slice MemoryMax=1GiB는 최후 보호이며 실제 RSS 합산 기준과 다르다. CLI가 slice 밖이어도 실제 계측에 포함한다. 실행 제어/측정은 [U2-P02](performance-design.md#u2-p02)·[U2-P04](performance-design.md#u2-p04)가 단일 원본이다.

다음 결정은 Q&A에 따른 설계 선택이다. 구현/설치/운영 적격의 완료를 뜻하지 않는다. 각 행은 동기·선택·대안과 비용/한계를 함께 기록하며 새 ADR 파일을 만들지 않는다.

| 상류 기술 결정 | 문맥/설계 선택·구체 절 | 대안·결과/검증 조건 |
|---|---|---|
| U2-TSD-01 | Rust 설치형·Ubuntu24.04 이상·한 사용자/PC·한국어 CLI 유지; U2-L01·U2-O01 | 타 언어/GUI/클라우드는 미채택; 실제 설치/제거/지원 환경 오류는 미실행 |
| U2-TSD-02 | 독립 시스템 timer/oneshot·로그아웃 실행·Drive 비동기 유지; U2-L02 | 사용자 service+linger는 가능 대안이나 실제 접근/권한 확인 필요; 상시 서버/MCP 필수화 안 함 |
| U2-TSD-03 | 고정 registry1.0.0·Draft2020-12·전체 RFC8785 SHA-256; U2-SEC02 | 파일명/수정시각·부분 hash는 내용/승인 대체 불가; 전체Unicode/숫자 적합성 필요 |
| U2-TSD-04 | 초기 원격 OpenAI 비스트리밍 Chat Completions·tools 없음·store=false; U2-SEC04 | Responses 혼용/자동 제공자 우회 안 함; 모델별 지원 필드 하나/처리위치·비용/품질 적격 필요, Ollama 제외 |
| U2-TSD-05 | Drive metadata/blob 전후·GitHub blobSHA·Calendar 고정ID/GET/If-Match; U2-R03 | 다서비스 원자성/새ID·최신etag 우회 배제; 실제 계정/권한/충돌 대조 미검증 |
| U2-TSD-06 | SQLite WAL+FULL/FK·짧은tx/유일성/CAS·fsync 파일 대조; U2-R01/R02 | 파일 저널만 쓰는 대안은 다중 개정/예산 일관성 복잡; 엔진WAL-reset 수정·장치/동시/중단 시험 필요 |
| U2-TSD-07 | 시스템 timer+일반 UID oneshot·실행권5초·595+5초 종료; U2-L02·U2-C02 | 상주 조정자/사용자linger보다 권한/세션 경계를 명시; 실제 로그아웃/절전/종료상한 미검증 |
| U2-TSD-08 | host-key systemd encrypted credential→읽기 전용 전달; U2-SEC01 | 평문/GUI키링 의존 배제, TPM은 필수 아님; root/계정/디스크반출·건강DB 암호화 보장 아님 |
| U2-TSD-09 | Tokio/reqwest·영속 예약/nextAllowedAt·full jitter·정리 deadline; U2-P02·U2-R04 | 한도별 독립/무한 대기는 실행 상한 우회; 비양보 CPU는 제한 하위경계 필요 |
| U2-TSD-10 | 엄격 parser/schema/JCS·GTA-NUMERIC-1·IANA/tzdb·유한 자원; U2-SEC02·U2-C01·U2-R06 | 범용 Value/float/기본 정밀도 나눗셈/단순key sort만으로 충족 불가; 실제 계산 도구/tzdb 적격 보류 |
| U2-TSD-11 | 허용 필드 구조화 로컬 기록·한국어CLI·100ms RSS/고수위; U2-P04·U2-O01~U2-O03 | 원문 로그/원격 대시보드 배제; 누락/피크 입증 불가는 미검증, 기존 보존 선택 유지 |
| U2-TSD-12 | 승인/안전/현재성·외부 API/비용·확정 모델/수치 규범의 실제 부합 보류; U2-O04 | 모델 표현/수치 규범 확정과 실제 적격은 별도; 파일/해시/대역·추가PC 승인으로 실제 담당별 증거 대체 불가 |

### 구현 후보 고정과 공식 근거

| 역할 | Q&A 설계 후보 | 고정/호환성 확인과 실패 시 결과 |
|---|---|---|
| 로컬 DB | rusqlite0.43.0, 수정 포함 SQLite 안정 엔진 | 실제 engine version/source ID/feature·지원/수정 근거, FULL/WAL/경합/장치 시험; bundled 이름만 적격 아님 |
| HTTP/비동기 | Tokio1.54.1·reqwest0.13.5 | TLS/endpoint/취소·본문/timeout·CPU 비양보/종료 그룹 실제 검사, 실패면 관련 프로필 보류 |
| 엄격 JSON | serde_json1.0.154 | 중복 키가 소실되기 전 검사·String/UTF-8·후행/깊이 적합성 |
| Schema | jsonschema0.62.0 | Draft2020-12·format·고정 registry/등록참조·remote/file fetch 차단 |
| 전체 digest | serde_jcs0.3.0·SHA-256 | UTF-16 속성 정렬/숫자/Unicode·고정 기대digest, 전체extension 포함 |
| 십진 | bigdecimal0.4.11 | 정확 입력/유한합 전용·원천/합계30+18자리; 유리수 중간256자리/최종6자리 HALF_EVEN·wire 정확 대조는 U2-R06으로 별도 구현/검증, 기본 나눗셈 정밀도 금지 |
| 시간대 | chrono+chrono-tz0.10.4 | 실제 chrono버전·IANA_TZDB_VERSION·승인 timingPolicy 대조/DST 경계 |

위 버전은 제공된 Q&A가 확인한 문서 기준 후보다. 실제 선택 Rust toolchain/MSRV·feature·전이 의존 그래프·Cargo.lock·SQLite engine/source ID·tzdb·빌드 식별자를 후속 구현 manifest에 고정하고 통합 빌드/상호운용/경계 시험을 통과해야 한다. chrono의 새 버전이나 미정 SHA 구현의 임의 버전을 발명하지 않는다. 호환성 실패를 자동 최신화/암묵적 대체로 해소하지 않고 해당 선택의 근거/영향을 재검토한다. 이 단계는 패키지 설치/Cargo 파일/제품 코드 작성 없이 설계만 수행한다.

공식 근거는 Q&A의 [systemd255 service](https://www.freedesktop.org/software/systemd/man/255/systemd.service.html)·[timer](https://www.freedesktop.org/software/systemd/man/255/systemd.timer.html)·[kill](https://www.freedesktop.org/software/systemd/man/255/systemd.kill.html)·[resource-control](https://www.freedesktop.org/software/systemd/man/255/systemd.resource-control.html)와 각 해법의 버전별 공식 링크다. 문서 지원을 실제 설치 지원으로 확장하지 않는다. 실제 엔진/의존 호환·마운트/credential·로그아웃/절전·전체 프로세스 종료/RSS·안전/외부 인수는 미검증이다.

## 검증 책임과 한계

후속 개발/품질 담당은 U2-S01~U2-S73의 해당 정상/오류/경계 대역과 U1 공통 고정 사례/NUM-01~NUM-16을 독립 실행한다. U2-S65~71·73의 목적별 선택/등록·저장/재시작·독립 동의/위장/누락, U2-S72의 확정 수치 규범/근거·한도 부합을 포함한다. U2-L01의 소유/결과 흐름·U2-L02의 설정과 실제OS 대조, 각 NFR 문서의 지정 시험/증거를 확인한다. 현재는 Markdown/JSON의 ID·상류/anchor·소유/링크·표/UTF-8/공백·공식 추적 검사만 수행한다. 실제 제품 시험/설치/결제/외부 계정API·의료 안전 완료나 운영 실적을 주장하지 않는다.
