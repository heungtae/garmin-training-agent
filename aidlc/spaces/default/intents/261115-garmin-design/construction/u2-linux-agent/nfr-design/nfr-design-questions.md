# U2 Linux 에이전트 — 비기능 설계 확인

- 단위: U2 `u2-linux-agent` (`service`), Standard 깊이/검증 전략.
- 근거: [성능 요구사항](../nfr-requirements/performance-requirements.md), [보안 요구사항](../nfr-requirements/security-requirements.md), [용량 요구사항](../nfr-requirements/scalability-requirements.md), [복구 요구사항](../nfr-requirements/reliability-requirements.md), [관측 요구사항](../nfr-requirements/observability-requirements.md), [기술 결정/선정 조건](../nfr-requirements/tech-stack-decisions.md), [기능 명세](../functional-design/functional-spec.md), [공유 계약](../../../inception/contract-design/contract-summary.md).
- 현재는 QUESTION-ONLY다. 이후 산출물은 performance-design.md·security-design.md·scalability-design.md·reliability-design.md·observability-design.md·logical-components.md·traceability.json이며 지금 생성하지 않는다.

## 기존 결정

Rust 설치형·Ubuntu 24.04 이상·한 사용자/한 PC·한국어 CLI·로그아웃 중 예약 실행을 유지한다. 승인한 상세 NFR 39개와 Q1~Q3의 기준 부하/성능·600초 실행/요청 예산·복구 목표를 완화하지 않는다. 제품 코드·설치·시스템 설정·비밀 등록·외부 계정/API 호출·결제를 현재 실행하지 않는다.

실제 공급자/모델/비용/호출 한도·원 정책 현재성/승인/안전·Garmin 상세 계약·정밀도/tzdb와 기존 기능 모델의 세 위험은 미해소로 유지한다. Ollama는 제외한다. 기존 모델을 몰래 보완하거나 관련 실제 경로의 적격성을 선언하지 않는다.

## 공식 자료 확인

아래는 기술 설계 후보/제약의 근거이며 실제 대상 PC 설치·지원 실적이 아니다. 조회일: 2026-11-21. 최신 기능을 Ubuntu 24.04의 실행 환경이 지원한다고 추정하지 않도록 버전이 고정된 systemd 255 문서와 실제 설치 버전 확인을 구별한다.

| 공식 자료 | 확인한 내용·설계에 미치는 영향 |
|---|---|
| [systemd 255 loginctl](https://www.freedesktop.org/software/systemd/man/255/loginctl.html) | enable-linger는 해당 사용자 관리자를 부팅 때 시작하고 로그아웃 뒤에도 유지한다. 사용자 서비스 경로는 linger/접근권한 등 실제 환경 확인이 필요하며 로그인 세션만으로 실행을 보장하지 않음 |
| [systemd 255 timer](https://www.freedesktop.org/software/systemd/man/255/systemd.timer.html) | 타이머가 서비스를 활성화하며 이미 활성인 같은 서비스는 새 인스턴스를 만들지 않는다. timer 정밀도·절전/복귀·독립 주기와 앱의 영속 중복/예산 검사를 함께 설계해야 함 |
| [systemd 255 exec](https://www.freedesktop.org/software/systemd/man/255/systemd.exec.html)·[creds](https://www.freedesktop.org/software/systemd/man/255/systemd-creds.html) | LoadCredentialEncrypted와 호스트/TPM 기반 자격자료 암호화를 제공한다. 호스트 키는 root 접근 대상이며 실제 서비스 관리자/설치 버전·키/저장장치·로그아웃 접근 적격성 확인 필요. 최신 사용자별 암호화 기능이 255에서도 된다고 가정하지 않음 |
| [SQLite PRAGMA](https://www.sqlite.org/pragma.html) | WAL의 synchronous=FULL은 각 트랜잭션 commit에 추가 WAL sync를 수행한다. 내장 영속 저장 후보로 비교하되 실제 파일시스템/저장장치·권한·디스크 실패·성능 검증을 대신하지 않음 |

## Q1. [운영 담당자] 설치·시스템 설정 시 관리자 권한 사용 가능 여부

로그아웃 중 예약 실행과 비밀 보호 방식을 결정하려면 운영 PC에서 필요한 OS 설정에 관리자 권한을 사용할 수 있는지 알아야 한다. 이전 답변에는 Ubuntu/로그아웃 조건은 있지만 sudo/관리자 권한의 가용 여부는 없다. 이 답변은 설계의 운영 조건이며 지금 설치나 설정 변경을 실행하는 승인이 아니다.

A. 필요한 설치·제거·OS 설정·보호된 비밀 등록/갱신에는 관리자 권한을 사용할 수 있다. 권한이 필요한 작업만 명시하고 에이전트의 평상시 수집/분석/평가/게시 프로세스는 일반 사용자 권한으로 실행하도록 설계한다.
B. 관리자 권한을 사용할 수 없다. 사용자 범위 설치/설정만 대상으로 설계하고, 필요한 linger·비밀 접근·파일시스템 조건이 미리 충족되지 않으면 로그아웃 자동 실행은 미지원/보류로 표시한다. 로그아웃 실행 요구사항 자체를 삭제하거나 충족됐다고 주장하지 않는다.
X. Other (please specify)

[Answer]: A. 필요한 설치·제거·OS 설정·보호된 비밀 등록/갱신에는 관리자 권한을 사용할 수 있다. 권한이 필요한 작업만 명시하고 에이전트의 평상시 수집/분석/평가/게시 프로세스는 일반 사용자 권한으로 실행하도록 설계한다.

## 후속 설계와 확인

Q1에 따라 예약 실행·서비스 관리자와 비밀 보호 경계를 먼저 정한다. 로컬 영속 저장·단일 실행권/원자 확정·의도/예산/대기 상태, 유한 큐/동시성·바이트/깊이·백오프/정리 여유·안전한 기록/계측 및 실제 라이브러리/버전 선정 근거를 구체화한다. 필요한 실제 사용자 판단은 좁은 후속 질문으로 해소하고 문서 생성 전에 전체 답변 요약을 별도로 확인한다. 실제 환경/공급자 적격성 없는 후보는 활성화 완료로 표현하지 않는다.

## Q1을 반영한 설계 제안

아래는 관리자 권한 사용 가능 답변과 승인 NFR을 바탕으로 한 **구체 설계 제안**이다. 아직 사용자 요약 확인 전이며 실행/지원 실적이 아니다. 기존 기능 모델·wire를 바꾸는 결정은 포함하지 않는다.

### 예약 실행과 관리 권한

- systemd **시스템 관리자**의 수집/동기화·계획 확인 타이머와 각 `Type=oneshot` 서비스를 선택한다. 서비스에는 설치 때 확인한 비-root 일반 사용자 UID/GID를 명시한다. root로 수집/분석/LLM/Calendar 처리를 실행하지 않는다.
- 시스템 타이머는 로그인 세션과 분리한다. 사용자 서비스+linger는 대안으로 비교하되 현재 기본 경로로 채택하지 않는다. 로그아웃·부팅·절전 복귀·데이터 경로 접근·환경/권한은 실제 Ubuntu에서 검증해야 한다.
- 설치/제거·타이머 등록/변경/중단/재개·암호화 비밀 등록/갱신처럼 OS 권한이 필요한 CLI 관리 작업은 필요한 관리자 인증을 명시한다. 로컬 상태/설정 읽기와 계산은 일반 사용자 권한이다. 예약 자동 처리 때 매번 sudo 질문을 요구하거나 별도 계획 게시 승인을 추가하지 않는다. 관리 권한과 계획의 인간 승인 검증은 서로 다른 경계다.
- CLI가 특권을 사용할 때 허용 작업·고정 unit/설치 경로·검증된 설정값만 취급한다. 외부 문서/명령 문자열·임의 실행 경로·범용 root 셸·권한 없는 unit 생성은 허용하지 않는다. 새 상시 서버/비밀 브로커·범용 Polkit/sudo 우회 권한을 도입하지 않는다.
- 기본 수집/동기화 1시간·계획 확인 15분을 각각 관리한다. 타이머 정밀도 제안은 AccuracySec=1초·RandomizedDelaySec=0초다. 실제 설정 개정과 OS 등록 결과를 대조하며 중간 실패를 숨기지 않는다. 기존 유효 설정 보존·불일치 보류/재대조를 거쳐 새 개정을 확정한다.
- 앱은 실행 시작 후 570초에 새 작업을 중단하고 남은 30초를 상태 확정/정리에 배정한다. 정리가 끝나면 즉시 종료한다. oneshot에는 RuntimeMaxSec가 적용되지 않으므로 OS 보조 제한으로 TimeoutStartSec=595초·TimeoutStopSec=5초·KillMode=control-group과 강제 종료를 제안한다. 별도 긴 ExecStop 연쇄/자동 재시작으로 600초를 연장하지 않는다. 실제 프로세스/OS 종료 상한을 측정하고 충족 전 운영 적격성을 주장하지 않는다.
- 타이머가 같은 서비스의 중복 활성화를 줄여도 CLI/두 목적/재시작의 도메인 중복을 해결한 것으로 보지 않는다. 목적별 OS 실행권과 DB 기대 개정/유일성·원 의도/고정 원격 ID 검사를 함께 적용한다.

근거: [systemd 255 service](https://www.freedesktop.org/software/systemd/man/255/systemd.service.html), [kill](https://www.freedesktop.org/software/systemd/man/255/systemd.kill.html), [timer](https://www.freedesktop.org/software/systemd/man/255/systemd.timer.html), [exec](https://www.freedesktop.org/software/systemd/man/255/systemd.exec.html).

### 로컬 영속성과 복구

- 내장 SQLite·WAL·synchronous=FULL·foreign_keys=ON을 선택한다. 사용자/목적별 실행·기대 개정·원천 커서·확정 자료·불변 의도/시도·요청/비용 예약·다음 허용 시각을 같은 로컬 영속 경계에서 관리한다. 외부 네트워크 요청 중 DB 쓰기 트랜잭션을 유지하지 않는다.
- 로컬 고정 데이터 디렉터리는 설치 때 해당 일반 사용자가 로그아웃 후에도 접근 가능한 경로로 정하고, 기본 후보는 `/var/lib/garmin-training-agent/`다. 디렉터리 0700·파일 0600/UMask0077과 경로/소유·심볼릭 링크 검사를 적용한다. 네트워크 파일시스템·로그아웃 시 사라지는 홈 마운트에 WAL 동작을 가정하지 않는다.
- 엔진은 WAL-reset 수정이 확인된 지원 안정 버전만 허용한다. 일반 릴리스의 수정 기준은 3.51.3 이후이며 구버전은 공식 backport 입증이 필요하다. 철회 릴리스는 선정하지 않는다. rusqlite의 bundled 선택만으로 수정 포함을 가정하지 않고, 실제 SQLite 버전·source ID/빌드·수정 근거를 구현 manifest에 고정/검사한다.
- 짧은 트랜잭션과 유일 키/기대 개정으로 상태를 확정한다. DB busy 대기는 최대 2초와 남은 실행 시간 중 짧은 값으로 제한한다. 목적별 실행권 대기 5초와 별개이며 실제 접근마다 반복해 전체 예산을 우회하지 않는다.
- 외부 효과 전 의도/정확한 내용·원 대상·예산 예약을 commit한다. 외부 응답 뒤 실제 조회/내용을 대조해 결과를 별도 commit한다. 전송 여부가 불명인 예약·시도는 재시작으로 반환/초기화하지 않고 미확인으로 보존한다. SQLite 트랜잭션이 외부 서비스와 원자적이라고 주장하지 않는다.
- JSON 파생 파일은 같은 보호 루트에서 임시 완전본→검증→파일 동기화/원자 교체→디렉터리 동기화 순서로 확정한다. DB와 파일 사이 중단은 digest/의도 기반 대조로 복구하고 DB·파일의 단일 원자 commit을 가정하지 않는다. 확정 참조가 없는 임시 파일을 게시하지 않는다.
- 복구는 로컬 미완료·커서·원격 미확인 의도를 먼저 식별하고 60초 내 다음 상태를 표시한다. 쓰기/과금 결과 불명은 원 의도와 원격 고정 ID/내용부터 대조한다. 손상된 DB를 조용히 새 DB로 교체하지 않는다. 디스크 오류·로컬 확정 실패면 새 효과를 차단하고 기존 유효본을 보존한다. 자동 백업/디스크 소실 복원 기능을 추가하지 않는다.

근거: [SQLite WAL 및 WAL-reset 수정](https://www.sqlite.org/wal.html), [PRAGMA](https://www.sqlite.org/pragma.html), [공식 릴리스 공지](https://ftp.sqlite.org/news.html), [rusqlite](https://docs.rs/rusqlite/0.43.0/rusqlite/). 이 설계는 장치의 동기화/원자성·실제 장애 보존을 입증하지 않으며 통제 시험과 실제 설치 적격성을 별도 요구한다.

### 비밀·전송·입력 보호

- systemd 255 계열에서 확인한 `systemd-creds`·`LoadCredentialEncrypted`를 시스템 서비스 경로에 사용한다. 호스트 키로 보호한 암호화 저장을 기본 제안으로 삼아 TPM을 새 필수 하드웨어로 요구하지 않는다. TPM 보호는 실제 환경/운영 조건을 별도 확인하기 전 자동 전제로 삼지 않는다.
- 관리자는 허용된 비밀 등록/갱신 절차에서만 비밀을 입력하고, 에이전트는 서비스에 전달된 읽기 전용 자격자료를 메모리에서 사용한다. 비밀값을 argv·환경 설정 파일·로그·DB·분석/계획·진단에 복사하지 않는다. GARMIN_API_KEY는 기존 참조 이름만 유지하며 실제 인증 헤더/계약을 추측하지 않는다.
- 일반 사용자 서비스와 보호된 로컬 자료 접근을 제약하고 NoNewPrivileges·쓰기 경로 제한·core dump 금지를 설계한다. 호스트 키와 데이터가 있는 디스크 자체의 반출·root 또는 소유 계정 침해·메모리/절전 이미지에 대한 완전 보호를 이 선택으로 보장하지 않는다. 전체 건강 DB의 저장 시 암호화나 디스크 암호화를 이미 제공한다고 주장하지 않는다.
- GUI 로그인 키링의 잠금 해제를 로그아웃 실행의 숨은 전제로 쓰지 않는다. 암호화 자격자료/키·마운트·서비스 접근을 검증하지 못하면 해당 외부 기능을 보류하며 평문 설정으로 자동 fallback하지 않는다. CLI 즉시 실행도 비밀을 직접 출력/복호화해서 전달하지 않고 관리되는 동일 서비스 경로를 사용한다.
- 외부 HTTP는 reqwest/Tokio·TLS 검증을 사용하는 어댑터를 제안한다. 임의 인증서 검증 해제·자동 proxy/redirect·원격 payload의 URL/검증기 선택을 허용하지 않는다. 실제 공급자에 필요한 proxy/redirect/endpoint는 별도 명시·적격화·동의/예산 검사를 거쳐야 한다.
- 연결/전체 응답 deadline과 raw/복호화·압축 해제 후 크기 제한을 모두 확인한다. 연결부터 본문 끝까지의 시간 제한과 전체 실행 deadline을 함께 적용한다. CPU 파싱/Schema/JCS/계산은 크기/반복을 제한하고 중단 가능한 작업 단위로 나눈다. 양보하지 않는 계산에는 Tokio timeout만으로 시간 상한을 주장하지 않고, 필요 시 비밀을 전달하지 않는 제한된 하위 프로세스와 프로세스 그룹 종료로 경계를 강제한다.
- UTF-8·중복 키 탐지·단일 객체/후행 검사 후 고정 로컬 registry의 Draft2020-12 검사를 수행한다. 원격/file retriever를 비활성화하고 등록 참조만 해석한다. format 검사를 명시적으로 설정하고 기간/정책/전체 내용/계보·승인/안전은 독립 의미 검사로 유지한다.
- 실제 모든 분석 경로의 정확한 grant/필드 집합·withheld·파생 유출·업무 목적 동의를 요청 직전 재확인한다. 구조/해시·암호화 저장·로컬 DB 존재를 실제 권한/승인/최신성의 증거로 대신하지 않는다.

근거: [systemd 255 exec](https://www.freedesktop.org/software/systemd/man/255/systemd.exec.html)·[creds](https://www.freedesktop.org/software/systemd/man/255/systemd-creds.html), [reqwest timeout](https://docs.rs/reqwest/0.13.5/reqwest/struct.ClientBuilder.html), [Tokio timeout의 비양보 계산 한계](https://docs.rs/tokio/1.54.1/tokio/time/fn.timeout.html), [jsonschema](https://docs.rs/jsonschema/0.62.0/jsonschema/).

### 제안하는 유한 설계 프로필

다음은 문서 작성 전 확인받을 초기 설계/합성 경계 시험 값이다. wire 필드·실제 API 쿼터·계정/모델 토큰 한도 또는 제품의 총 자료량 상한을 바꾸지 않는다. 구현·실제 공급자/장치 검증 전 운영 적격 프로필로 자동 활성화하지 않는다.

| 항목 | 제안 값·적용 |
|---|---|
| 기존 승인 성능·요청 제한 | Q1~Q3의 2코어/4 GiB·10000활동/300세션, CLI p95 2초/분석 60초·RSS 합산1GiB·예약60초, 연결10초/일반30초/LLM120초·최초 포함3회·목적별600초/100회·실행권5초/하위60초·복구상태60초 유지 |
| 한 문서/HTTP 요청·응답 | 입력/출력 각각 8 MiB. 원시·해제 후 각 크기를 확인하고 Content-Length만 신뢰하지 않음. C03은 등록 Detail로 분할하며 한도 초과를 조용히 절단하지 않음 |
| 한 실행의 입출력 누적 | 입력·출력 각각 64 MiB. 한도 전 정리하고 미완료/커서 유지. 여러 문서/시도를 합산하며 반복 요청으로 우회하지 않음 |
| JSON 깊이 | 최상위 컨테이너 깊이1, 배열/객체 중첩 각각+1, 최대64. 초과는 RESOURCE_LIMIT/미완료로 보류 |
| 십진 문자열 처리 자원 | 입력 숫자 문자열의 부호/소수점 제외 숫자 자릿수 최대1024. 정확 합계의 자리 증가도 같은 자원 한도에서 검사, 초과는 명시 보류. 새 의미 범위/반올림 규칙으로 치환하지 않음 |
| 예약 목적·활성 실행 | 목적별 활성1개, 두 목적 최대2개. 같은 목적의 추가 실행은 실행권 대기 최대5초 후 명시 중복 억제/대기. 두 목적이 공유하는 도메인/DB·서비스/예산은 별도 동시 검사 |
| 전송/CPU 하위 작업 | 목적별 동시 네트워크1개·CPU 하위 프로세스 최대1개. 활성 작업 중 대기·파싱·하위 프로세스도 시간/RSS·호출/입출력 예산에 포함 |
| 메모리 내 대기 묶음 | 목적별 최대32개 식별자, 초과는 영속 미완료/원천 cursor로 남김. 32개를 전체 활동/세션 상한으로 해석하거나 버리지 않음 |
| 백오프/지터 | 확인된 일시 실패에만 최초 포함3회. 재시도1부터 지터 범위 0~min(30초,1초×2^(재시도번호-1)). 공급자 Retry-After와 비교해 더 늦은 시각을 준수. 현재 예산/정리 여유를 넘으면 다음 허용 시각 보존 후 종료 |
| DB busy 대기 | 최대2초와 남은 실행 예산 중 짧은 값. 대기 중 외부 효과를 보내거나 긴 트랜잭션을 유지하지 않음 |
| 앱/OS 종료 | 새 작업 cutoff570초, 정리 여유30초, Type=oneshot의 TimeoutStartSec595초+TimeoutStopSec5초·프로세스 그룹 종료. 하위 작업의60초는 남은시간/정리 여유와 함께 더 짧게 제한 |
| 타이머 | 목적별 기본1시간/15분, AccuracySec1초·RandomizedDelaySec0초. 절전/전원·현재성/실행권 미충족의 지연은 별도 표시 |
| 메모리 보호/계측 | 관리 서비스들을 공통 slice에 넣어 MemoryMax=1 GiB를 최후 보호로 제안. cgroup 메모리를 RSS와 동일시하지 않고 CLI/양쪽 목적/관련 하위를 포함한 실제 RSS 합산을 별도 계측. OOM/계측 누락은 합격 아님 |
| 계측·검사 | 합산 RSS 100ms 간격 표본과 종료 시 ru_maxrss 등 고수위/OS 사건을 함께 기록. 표본 간 피크 검증 한계를 명시하며 한도 준수 입증 불가면 미검증. 준비5회+측정20회19번째 p95·첫실행5회·예약조건별5회는 기존 기준 유지 |

공급자·서비스별 집계 한도/기간별 호출·비용 예산과 현재 정책/권한은 위 값보다 우선한다. 실제 한도가 더 엄격하면 적용하고 미확보이면 관련 요청을 보류한다. 알 수 없는 비용/결과 예약은 보수적으로 유지한다. 재시작/즉시 실행·새 예약으로 대기/예산을 초기화하지 않는다.

### 구현 기술의 설계 기준과 적격성

다음 버전은 공식 게시 문서에서 확인한 설계 기준 후보를 명시한 것이다. 아직 의존 그래프/MSRV·OS·통합 빌드/실행을 검증하지 않았다. 최종 구현은 실제 선택한 버전/feature·Rust toolchain·SQLite 엔진/source ID·tzdb·빌드 식별자·Cargo.lock을 고정하고 경계/상호운용 검사를 통과해야 한다. 호환성 실패 시 임의 대체/자동 최신화하지 않고 해당 선택을 재검토한다.

| 역할 | 설계 기준 후보 | 필수 검증 |
|---|---|---|
| 로컬 저장 | rusqlite 0.43.0, 수정 포함 SQLite 안정 엔진·bundled 빌드 기준 | 실제 엔진의 WAL-reset 수정·트랜잭션/FULL·경로/장치·동시/중단/디스크 오류·기준 성능. bundled 이름만으로 수정/지원 완료 아님 |
| 비동기/HTTP | Tokio1.54.1·reqwest0.13.5, TLS 검증·명시 deadline/본문/동시 한도 | 네트워크·본문·취소/미확인 비용·정리/하위 종료, endpoint/redirect/proxy·실제 모델/토큰 필드는 공급자 적격성 별도 |
| 엄격 JSON | serde_json1.0.154와 중복키/깊이/UTF-8·단일객체/후행 검사 경계 | Value 파싱으로 중복키가 소실된 뒤 검사하지 않음. 문자열은 String 경로로 읽고 잘못된 Unicode를 자동 수선하지 않음 |
| Schema | jsonschema0.62.0·Draft2020-12·고정 로컬 registry | 원격/file fetch 없음, 등록 참조/조건/format·자원 경계. 구조만으로 의미/정책/승인 합격 금지 |
| 전체 내용 결합 | serde_jcs0.3.0·SHA-256 | RFC8785의 UTF-16 속성 정렬·숫자/Unicode 경계·전체 필드/고정 기대digest를 검증. 단순 key sort·도구 이름으로 일반 적격성을 주장하지 않음 |
| 십진 계산 | bigdecimal0.4.11·문자열 원값/정확 합계 | 부동소수점 경유 금지·0/누락/추정/withheld 구별·자원 초과 보류. 반복 소수 wire 표현/정밀도 미해결은 관련 계산 적격 판정 보류이며 라이브러리로 해소하지 않음 |
| 시간대 | chrono+chrono-tz0.10.4·IANA_TZDB_VERSION 식별 | 실제 선택 chrono버전·번들 tzdb버전을 manifest/승인 timingPolicy에 대조, DST ambiguous/none 보류·경과시간/기간 경계. 문서 버전을 실제 tzdb 적격 완료로 쓰지 않음 |

추가 공식 근거: [serde_json](https://docs.rs/serde_json/1.0.154/serde_json/de/struct.Deserializer.html), [serde_jcs](https://docs.rs/serde_jcs/0.3.0/serde_jcs/), [bigdecimal](https://docs.rs/bigdecimal/0.4.11/bigdecimal/), [chrono-tz](https://docs.rs/chrono-tz/0.10.4/chrono_tz/), [메모리 보호](https://www.freedesktop.org/software/systemd/man/255/systemd.resource-control.html). crate·버전 후보의 문서 지원과 U1 공통 적합성/제품 실행 적격성은 별개다. 새 패키지를 설치하거나 Cargo 파일/제품 코드를 작성하지 않는다.

### 관측·실패 격리·소유와 남는 조건

- 소유 컴포넌트 7개와 기존 엔티티25개를 유지한다. OS 타이머/서비스·공통 slice·로컬 SQLite/파생 파일·자격자료 전달·HTTP 어댑터·검사/계측을 논리 실행 자원으로 연결하고 새로운 도메인 엔티티/상시 API 서버를 추가하지 않는다.
- 목적/대상별 실패를 격리하고 부분 성공·원 요청 전체 세션/과거 skip·현재 오류/마지막 성공을 보존한다. 네트워크 실패가 로컬 확정/다른 저장소 성공을 취소하지 않게 한다. 미확인 쓰기는 먼저 대조하고 최신 etag/새 객체로 우회하지 않는다.
- 안전한 한국어 CLI와 허용 필드만의 구조화 로컬 기록을 제안한다. 실행·의도/시도·계획/버전/digest·세션·단계·안전한 오류code·건수/지연/예산/다음조치를 연결한다. 요청/응답/건강 원문·비밀/보호 참조는 로그에 넣지 않는다. journald는 안전한 서비스 상태만 받고 앱 기록은 기존 보존 선택을 따른다. 새 로그 일수·중앙 모니터링·대시보드/경보 서비스·자동 백업을 추가하지 않는다.
- 분석 재계산은 원천 개정/고정 명세·정책 digest·기간/시간대/tzdb/계산 프로필과 구현 빌드를 고정한 결과만 재사용한다. 정책/승인·권한/현재성은 캐시된 성공으로 대체하지 않는다. 고정 Schema 검사기 등은 유한 캐시로 관리하고 선택 릴리스/도구 프로필 변경 시 재생성한다.
- 기존 ChatGPT serviceName 부재, connectionIds의 활성 분석 대상/필수 전달 연결 의미, 반복 소수 정밀도 위험은 유지한다. 이번 설계가 새 enum/매핑/반올림 규칙으로 몰래 해소하지 않으며 해당 실제 바인딩/계산 적격성은 보류한다.
- C06 인간 승인·C04 현재성/철회·안전·Garmin 상세 계약·실제 ChatGPT/Drive/GitHub/Calendar/C08·원격 OpenAI 모델/비용·로컬/사설 제공자/처리 위치/하드웨어는 미검증이다. Ollama 제외를 유지하며 설계/합성 검사로 P0 실제 인수를 완료하지 않는다.

## Consolidated Summary Confirmation

- 관리자는 필요한 설치·제거·OS/타이머 설정·비밀 등록/갱신에만 사용한다. systemd 시스템 타이머+oneshot을 선택하고 실제 작업은 지정 일반 사용자로 실행한다. 평상시 자동 작업에 추가 sudo 질문이나 계획 승인 단계를 넣지 않는다.
- 로컬 저장은 SQLite WAL+FULL 동기화·짧은 트랜잭션/유일성/기대 개정으로 설계하고 WAL-reset 수정이 확인된 엔진만 허용한다. 의도·미완료·커서·예산 예약/대기 시각을 영속 보존하며 외부 효과와의 원자성을 가정하지 않는다.
- 비밀은 호스트 키 기반 systemd 암호화 자격자료로 서비스에 전달한다. TPM을 새 필수 사양으로 요구하지 않고, 비밀을 argv/환경 설정·DB·로그·공유 자료에 넣지 않는다. 실제 접근/키/마운트/로그아웃 환경 미적격이면 평문 fallback 없이 보류한다.
- 기존 성능/복구 목표와 요청 한도는 유지한다. 추가 제안 프로필은 문서/HTTP 입력·출력 각8MiB·실행 누적 각64MiB·JSON 깊이64·십진 숫자1024자리·목적별 활성1/네트워크1/CPU하위1·메모리 대기32개·DB busy2초다. 초과는 조용한 삭제/절단/완료 승격 없이 미완료로 보존한다.
- 재시도는 최초 포함3회 안에서 1초 기반 지수 full jitter(최대30초)와 공급자 대기 지시 중 더 늦은 시각을 따른다. 앱은570초에 새 작업을 멈추고30초 정리 여유를 확보하며 OS 보조 제한595초+종료5초로600초 상한을 설계한다. 서비스 그룹 종료와 실제 RSS 합산/계측 한계·기존 p95/예약 검증 기준을 유지한다.
- Rust 구현 기술은 rusqlite·Tokio/reqwest·serde_json/jsonschema·serde_jcs/SHA-256·bigdecimal·chrono/chrono-tz를 문서에 명시한 버전 기준 후보로 제안한다. 실제 의존/엔진/tzdb/빌드/lock 고정과 적합성 검증 전 호환/운영 적격을 주장하지 않는다.
- 기존7개 컴포넌트/25개 엔티티·원 요청 범위/부분 성공·한국어 CLI와 안전한 로컬 기록을 유지한다. 현재 정책/권한/승인은 캐시하지 않고 실제 요청 직전 확인한다. 새 서버/클라우드/대시보드·보존 일수/자동 백업·의료 임계값을 추가하지 않는다.
- 실제 승인·정책 최신성·안전·외부 연동·모델/비용과 기존 세 모델 위험은 미해소다. Ollama는 제외한다. 이번 확인은 비기능 설계 문서 작성용이며 설치·코드·관리자 설정 변경·실제 API/결제를 실행하는 승인이 아니다.

위 내용으로 U2 비기능 설계 문서를 작성할 입력이 맞나요?

- Looks correct
- Request changes

[Answer]: Looks correct

## 현재 상류 입력 보완 — 2026-11-22

위 질문/답변과 당시 제안은 역사 기록으로 보존한다. 현재 설계의 모델·계산 기준은 수정된 [기능 명세](../functional-design/functional-spec.md)·[엔티티](../functional-design/entities.md)·[기술 결정](../nfr-requirements/tech-stack-decisions.md)·[공유 계약](../../../inception/contract-design/contract-summary.md#numeric-profile-v1)을 따른다. 이 보완은 새 사용자 응답이나 승인 기록이 아니다.

- chatgpt FINAL_READER와 독립 SharingConsent→C04 대응이 확정되었다. credentialReferenceId/endpointReference/modelReference=null이며 Linux 호출 어댑터/실행 권한이 아니다. 실제 독자 계정/도구 경로·주체 대응·정책 현재성은 별도 검증한다.
- connectionIds는 등록, analysisTargets는 저장소/최종 독자별 분석 활성 선택, planInboxConnectionId는 별도 Drive 계획 수신 선택이다. 분석0개/Drive 분석 중단은 계획 수신 선택을 바꾸지 않는다. U2-S65~71·73으로 저장·재시작·독립 동의/철회·위장/누락을 검증한다.
- GTA-NUMERIC-1은 원천/정확 합계 정수30+소수18자리·중간 유리수 분자/분모 각각256자리·속도/페이스 최종6자리 HALF_EVEN·wire 정규형 정확 대조로 확정되었다. 일반 parser1024자리 상한은 더 엄격한 의미 한도를 완화하지 않는다. BigDecimal 후보는 정확 입력/합계에만 사용하며 무제한 나눗셈/기본 정밀도로 파생값을 결정하지 않는다. U2-S72/NUM-01~16 및30/31·18/19·256/257 경계를 후속 실행한다.
- 기존 OS/저장/성능/복구 선택을 유지한다. 과거의 세 모델 미정 문구는 현재 표현/수치 규범의 미정을 뜻하지 않는다. 실제 구현 부합·계산 도구/tzdb·외부 권한/승인·안전/현재성·공급자/비용 적격성은 여전히 미검증이며 관련 활성화 보류를 유지한다.


