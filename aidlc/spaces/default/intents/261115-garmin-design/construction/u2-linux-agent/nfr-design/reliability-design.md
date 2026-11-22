# U2 Linux 에이전트 무결성과 복구 설계

## Sources

[복구 요구사항](../nfr-requirements/reliability-requirements.md)의 NFR5.3~NFR5.7·NFR6.1~NFR6.3·NFR8.9~NFR8.12·NFR9.3, [성능 요구사항](../nfr-requirements/performance-requirements.md)의 NFR8.5~NFR8.6, [용량 요구사항](../nfr-requirements/scalability-requirements.md)의 NFR5.2, [기술 결정](../nfr-requirements/tech-stack-decisions.md)의 U2-TSD-05~07·09~10·12, [기능 명세](../functional-design/functional-spec.md)의 F02~F11 및 상태 전이, [공유 계약](../../../inception/contract-design/contract-summary.md)의 C03·C05~C08·CR03~CR06·CR10~CR12·P01~P05를 구체화한다. 구체 저장/종료/재시도 후보는 [설계 Q&A](nfr-design-questions.md)다. 아래는 설계와 후속 시험 계획이며 실제 복구 실적이 아니다.

<a id="u2-r01"></a>
## U2-R01 — SQLite 로컬 확정과 실행 복귀

대응: NFR5.2·NFR5.3·NFR8.12. 소유: 각 엔티티 소유자(내용/전이), OperationControl(실행/로컬 복귀), 공통 저장 어댑터(기술 경계). 규칙: BR1.2·BR1.6·BR1.7·BR3.3·BR3.5.

내장 SQLite를 WAL·synchronous=FULL·foreign_keys=ON으로 사용한다. rusqlite0.43.0의 bundled는 빌드 후보이며 엔진 적격성을 뜻하지 않는다. 실제 엔진은 WAL-reset 수정이 확인된 지원 안정 릴리스만 허용한다. 일반 수정 기준3.51.3 이후, 구버전은 공식 backport 증명이 필요하고 철회 릴리스는 제외한다. 실제 SQLite version/source ID·빌드 feature·수정 근거를 manifest에 고정/검사하며 미입증 엔진에서 외부 효과를 활성화하지 않는다. 근거는 Q&A의 [SQLite WAL](https://www.sqlite.org/wal.html)·[PRAGMA](https://www.sqlite.org/pragma.html)·[공식 릴리스 공지](https://ftp.sqlite.org/news.html)·[rusqlite](https://docs.rs/rusqlite/0.43.0/rusqlite/)다.

설정/예약/실행·확정 활동과 개정·커서/pending·불변 의도/시도·호출/비용 예약/nextAllowedAt을 같은 로컬 DB 경계에서 보존한다. 이들은 기존 엔티티의 저장 부속 기록이며 새 도메인 엔티티가 아니다. 공유 DB를 모든 컴포넌트 공동 쓰기 인터페이스로 삼지 않고 소유 repository만 자기 자료를 변경한다. 기대 개정 CAS·유일 키·FK로 오래된 덮어쓰기/중복 관계를 거절한다. 기술적 공통 예산 예약은 OperationControl 경계를 통해 동일 저장 트랜잭션에서 직렬화한다.

입력 검증→짧은 트랜잭션→기대 개정/유일성 확인→내용/의도/참조 commit→결과 반환 순서다. 네트워크 중 쓰기 트랜잭션을 유지하지 않는다. busy는 최대2초와 남은 실행 예산 중 짧은 값으로 제한하고 재시도마다 전체 deadline을 새로 만들지 않는다. read transaction도 네트워크/장기 계산 동안 유지하지 않으며 분석 고정 개정은 불변 참조로 다시 읽는다. DB lock/디스크 가득 참/읽기 전용/commit 실패면 새 외부 전송 없이 이전 유효본과 미완료를 유지하고 조치를 반환한다. 장치의 sync/원자성이 실제로 지켜지는지는 통제 중단 시험이 필요하다.

재시작은 로컬 저장을 먼저 열어 RUNNING/IN_PROGRESS 중단·pendingRanges·확정 커서·미확인 의도·예산 예약/대기 시각을 식별한다. 기존 종료 기록을 RUNNING으로 덮지 않고 새 실행이 recoveryHint/childWorkRefs로 연결한다. 정상 읽기 장치/기준 부하에서 프로세스 시작~다음 대조/재개/보류 표시≤60초를 목표로 한다. 원격 복구 완료≤60초를 뜻하지 않는다. 손상 DB를 조용히 새 DB로 교체하지 않고 진단/새 효과 차단으로 멈춘다. 디스크 소실 복원/자동 백업은 범위 밖이다.

검증 설계: U2-S02·U2-S06·U2-S11·U2-S27·U2-S28·U2-S59·U2-S62의 commit 전/중/후 종료·경합·읽기 전용·디스크 가득 참에서 기존 확정 손실0건·미확정 성공0건·복귀 표시60초·현재성 재검사 전 외부 재개0건을 확인한다. 실제 엔진/장치/장애 보존은 미검증이다.

<a id="u2-r02"></a>
## U2-R02 — DB와 파생 파일 사이의 확정

대응: NFR5.3·NFR5.6. 소유: AnalysisPublication(분석/파생 JSON), PlanAdmission(수신 사본), 각 파일 소유자. 규칙: BR3.3·BR4.4·BR6.12.

JSON 파일은 보호된 같은 로컬 파일시스템/루트에서 임시 완전본 작성→U2-SEC02 검증/기대 전체 digest→파일 fsync→원자 교체→부모 디렉터리 동기화→소유자의 DB 확정 참조 연결 순서로 확정한다. 교체가 기존 유효 참조의 내용을 바꾸지 않도록 새 불변 버전 경로를 사용하고, 최신 탐색 참조 변경은 별도 확인한다. 보안 경로/권한은 [U2-SEC01](security-design.md#u2-sec01)을 따른다. DB·파일이 단일 원자 commit이라는 가정은 없다.

| 중단 경계 | 복귀 처리 | 외부 효과 |
|---|---|---|
| 임시 작성/검증 중 | 확정 참조 없음·이전 유효본 유지, 임시본은 미확정 | 게시 금지 |
| 파일 동기화/교체/디렉터리 동기화 중 | 경로/내용/digest와 원 의도 대조, 불완전하면 보류 | 확정 참조 연결 전 금지 |
| 파일 완전본 존재·DB 참조 commit 전 | 원 의도/기대 개정과 완전본 재검증 후 참조 확정 후보 | 확정 뒤만 가능 |
| DB 확정 뒤 파일 접근 불가/불일치 | 참조를 정상으로 표시하지 않고 갱신 필요/저장 실패, 유효 이전 개정 보존 | 관련 신규 게시 차단 |

외부 효과가 필요한 의도는 전송 전에 DB commit되어야 한다. 로컬 파일 완전본만 있다는 이유로 게시하지 않는다. 파일 오류가 다른 대상의 이미 확인된 성공을 취소하지 않는다. 임시본 정리도 미해소 의도/대조 증거를 선삭제하지 않는 [U2-O03](observability-design.md#u2-o03)을 따른다.

검증 설계: U2-S11·U2-S18·U2-S19·U2-S27·U2-S28·U2-S59에서 각 파일/DB 경계 중단·fsync/rename/dir sync 실패와 재시작을 주입한다. 이전 유효본 또는 새 완전본만 참조, 미확정 게시0건이 필요하다. 실제 파일시스템 sync/rename 의미는 설치 환경에서 확인해야 한다.

<a id="u2-r03"></a>
## U2-R03 — 원격 미확인·충돌 대조와 부분 성공

대응: NFR5.4·NFR8.12. 소유: AnalysisPublication(저장소), CalendarDelivery(일정), PlanEvaluation(결과/과금). 규칙: BR3.6·BR7.5·BR9.4·BR9.6.

외부 효과 전 정확한 내용/digest·원 대상/고정 객체/세션 ID·기대 원격 버전·승인/정책 계보·예산 예약을 로컬 commit한다. 응답 후 실제 원격 내용을 다시 읽어 원 의도와 대조한 뒤 별도 commit한다. DB와 원격 효과의 원자성은 가정하지 않는다. timeout/강제 종료/응답 유실은 미전송·취소·미과금의 증거가 아니다. 전송 여부/비용 불명 예약과 시도는 OUTCOME_UNKNOWN으로 남긴다.

| 대조 결과 | 결과와 재개 |
|---|---|
| 고정 원 대상/ID의 실제 내용·소유 계보가 원 의도와 일치 | 해당 성공 확인/연결 복구; 새 쓰기 없음 |
| 실제 내용/소유/기대 버전 불일치 또는 사용자 수정 | CONFLICT, 명시 해결/재검증 전 효과 중단 |
| 조회 실패·권한/정책 불명 | OUTCOME_UNKNOWN/보류 유지, 새 효과 없음 |
| 실제 미반영을 확인 | 현재 내용·권한/정책·승인/안전·시각·남은 예산 재검사 후 같은 원 의도 재시도 후보 |

GitHub는 읽은 blob SHA 조건을 유지한다. Drive는 metadata-before→blob→metadata-after와 실제 내용을 대조하며 새 이름/객체로 우회하지 않는다. Calendar는 P03의 고정 ID·원 의도·GET/If-Match를 사용한다. 409/412를 최신 etag로 무조건 다시 쓰지 않고 marker/이름만으로 소유를 인정하지 않는다. lookup은 DeliveryAttempt의 새 LOOKUP 시도로 계보에 남기며 원 시도 결과를 지우지 않는다.

과거가 된 세션도 이전 미확인 CREATE부터 대조한다. 일치면 기존 효과를 확인하고, 조회 불가/불일치면 미확인/충돌을 유지한다. 실제 미생성 확인 뒤 시작≤현재일 때만 SKIPPED_PAST이며 새 생성/시간 이동/실제 운동 변경은 없다. 원 요청의 모든 세션은 [U2-O02](observability-design.md#u2-o02)의 분모에 남긴다. 한 대상의 성공을 다른 대상의 실패로 되돌리지 않고 부분 결과를 보존한다.

검증 설계: U2-S29·U2-S30·U2-S47·U2-S52~U2-S59에서 전송 후 응답 유실·GET 실패·409/412·사용자 수정·과거 시각 경과를 비교한다. 대조 전 재전송/새ID·논리 중복0건·필수 결과 일치가 필요하다. 실제 원격 원자성/대조/삭제 복원은 미검증이다.

<a id="u2-r04"></a>
## U2-R04 — 영속 예산·백오프·시계 대응

대응: NFR6.3·NFR8.9·NFR8.10·NFR8.11. 소유: OperationControl(공통 예산/시계), 각 요청 소유자(요청 분류/재검사), PlanEvaluation(비용). 규칙: BR2.8·BR8.1·BR8.6.

모든 읽기·목록/상세·metadata·대조·쓰기·재시도·LLM 실제 전송마다 먼저 영속 예약한다. 목적별 실행100회, 두 목적 공통 서비스별 집계와 기간별 호출/비용 예산을 하나의 짧은 저장 경계에서 확인한다. 실제 가격/쿼터/기간/양의 비용 예산이 미확보이면 관련 활성화를 보류하며 Q&A 숫자로 운영 허용을 만들지 않는다. 예약 실패면 전송0건이다. 미전송이 입증되지 않은 예약·비용은 반환/초기화하지 않고 보수적으로 유지해 대조한다. 이후 예약/즉시/재시작이 기간 예산을 초기화하지 않는다.

논리 요청은 최초 포함 최대3회다. 확인된 일시 실패에만 재시도하며 재시도번호n=1부터 지연은 full jitter `0..min(30초, 1초×2^(n-1))`로 선택한다. 공급자 Retry-After와 비교해 더 늦은 nextAllowedAt을 영속화한다. 영구 입력/권한 오류는 사용자 조치 전 반복하지 않고, 결과/쓰기/과금 미확인은 먼저 U2-R03 대조를 거친다. 지터가0이어도 공급자 대기를 단축하지 않는다. 별도 circuit-breaker 임계값/탐색 호출을 발명하지 않고 이 영속 대기/실패 분류로 신규 호출을 억제한다.

실행 경과·대기·DB busy·deadline은 단조 시계로 측정한다. Retry-After 지연 초는 수신 단조 시각의 현재 실행 deadline과 신뢰된 UTC 대응을 함께 기록하고, HTTP-date는 신뢰된 수신 현재 시각/공급자 규약으로 해석한다. 지속 nextAllowedAt과 원 지시·기준시각/신뢰 근거는 재시작 후에도 보존한다. 실행 중 벽시계가 변해도 이미 정한 단조 대기/마감은 늘이거나 단축하지 않는다. 재시작에는 신뢰된 UTC가 nextAllowedAt을 지났는지 확인하고 새 단조 대기로 대응한다. 보정/절전/시각 신뢰를 입증하지 못하면 신규 요청/게시를 보류하며 임의로 대기 완료 처리하지 않는다. 실제 공급자 헤더 해석/시계 신뢰 프로필은 후속 적격 조건이다.

대기+다음 작업이 [U2-P02](performance-design.md#u2-p02)의 정리 여유/cutoff를 만족하지 못하면 nextAllowedAt·미완료 사유를 commit하고 이번 실행을 종료한다. 같은 예약의 여러 DB 접근/소켓/자식 timeout을 새600초로 해석하지 않는다. 전송 직전에는 [U2-SEC03](security-design.md#u2-sec03)·[U2-SEC04](security-design.md#u2-sec04)의 현재 권한/정책/승인/안전을 다시 검사한다.

검증 설계: U2-S07·U2-S39·U2-S41·U2-S47·U2-S59·U2-S61·U2-S62에 1/2/3회 실패·영구 오류·미확인 과금·예약/전송 직후 중단·두 목적 예산 경쟁·Retry-After가 남은 시간보다 짧음/같음/김·벽시계 앞뒤 보정을 주입한다. 4번째 전송/조기 전송/기간 예산 초기화/미확인 반환0건과600초 종료를 요구한다. 실제 쿼터/가격/시계 대응·지터 구현은 미검증이다.

<a id="u2-r05"></a>
## U2-R05 — 수집 커서·분할 완결성

대응: NFR5.5·NFR5.6. 소유: ActivityCollection(원천), AnalysisPublication(분석/게시). 규칙: BR2.2·BR2.9·BR4.3·BR4.4·BR4.9·BR10.1·BR10.2.

원천 목록 전체 종료와 각 상세 확정을 분리한다. 유효 활동은 확정하고 실패 상세/목록 범위는 CollectionIssue·pendingRanges로 보존한다. 부분 페이지/시간·호출 소진이면 완료 cursor를 전진하지 않는다. 정상 전체 목록0건만 EMPTY 후보다. Garmin P05 종료/수정/커서 상세 계약이 없으므로 실제 수집은 계속 차단하고 임의 endpoint/종료 조건을 발명하지 않는다.

C03 INLINE은 activities 전체와 Detail 없음, PARTITIONED는 루트 activities=[]와 등록 Detail만 허용한다. 유한 묶음으로 만들되 전체 snapshotId/sourceSnapshotRef/subjectRef/projection·기간·N/연속index·참조/활동ID 유일성·선언 개수·정렬·정확 합계를 대조한다. 정렬은 UTC 순간/활동ID Unicode 코드 포인트 순서이고 원 오프셋을 보존한다. 조각 기간 겹침은 허용하되 같은 활동 중복은 금지다. Detail 선확정/선게시→고정 버전 재읽기/해시 확인→루트 마지막 게시를 수행한다. 다중 파일 원자성은 가정하지 않는다.

누락/읽기 실패/해시·버전 불명 조각은 사용하지 않고 SOURCE_INCOMPLETE·별도 effective PARTIAL/실패 조각을 남긴다. 중복/index·개수/범위/계보/Schema·합계 오류는 DATA_INVALID로 관련 채택을 보류한다. 생산자의 completeness를 덮어쓰지 않는다. PARTIAL은 전부 도착해도 COMPLETE로 승격하지 않으며 COMPLETE는 sourceCollectedAt·누락 없음·전체 유효 도착/합계 일치가 필요하다. NEVER_COLLECTED는 sourceCollectedAt=null·missingPeriods=[period], 정상 EMPTY는 성공0건·누락 없음이다. generatedAt·sourceCollectedAt·lastSuccess를 혼용하지 않는다. withheld 자체는 수집/전달 누락이 아니다.

검증 설계: U2-S06·U2-S08·U2-S09·U2-S11·U2-S17~U2-S21·U2-S62와 계약S06~S16·S19~S20. 마지막 페이지 전 중단·Detail 실패/혼합/중복/합계 오류에서 허위 COMPLETE/커서 전진0건·정상 기대 일치를 확인한다. 실제 수집/파일/원격 전달은 미실행이다.

<a id="u2-r06"></a>
## U2-R06 — 정확 십진·기간·일정 시각

대응: NFR5.7·NFR6.1·NFR6.2. 소유: AnalysisPublication(계산/기간), CalendarDelivery(일정 시각), U1(고정 수치 규범), 후속 U2 개발/품질 담당(도구 부합). 규칙: BR2.7·BR2.9·BR4.2·BR4.6~BR4.8·BR9.2·BR9.3·BR9.5·BR10.1·BR10.2.

계산은 [GTA-NUMERIC-1](../../../inception/contract-design/contract-summary.md#numeric-profile-v1)을 그대로 구현한다. bigdecimal0.4.11 후보는 부동소수점 경유 없는 정확 입력·유한 합계에만 사용하고, 무제한 나눗셈이나 기본 정밀도에 파생값 결정을 맡기지 않는다. 원천 문자열/원 단위는 별도 원천 기록으로 보존한다. 입력과 정확 합계의 정수부 최대30자리·소수부 최대18자리를 검사하며 초과는 DATA_INVALID다. 합계는 6자리로 반올림하지 않는다. 일반 parser1024자리 상한은 이 더 엄격한 의미 범위를 넓히지 않는다.

파생 계산은 입력을 정수 계수/10의 거듭제곱으로 바꿔 약분한 정확 유리수로 수행한다. 각 연산 전 분자/분모 각각 최대256자리 경계를 검사하고 초과는 RESOURCE_LIMIT로 보류한다. 속도=거리(m)/시간(s), 페이스=시간(s)×1000/거리(m)이며 반올림된 속도를 페이스 입력으로 쓰지 않는다. 최종 정확 유리수에만 한 번 10^6을 곱한 정수 몫q/나머지r을 구해 2r과 분모를 비교하고, 같으면 q 또는 q+1 중 짝수를 택하는 ROUND_HALF_EVEN을 적용한다. 이 정수 연산도 같은 자원 경계/실행 deadline을 지키며 검사를 큰 중간값 할당 뒤로 미루지 않는다. 정확 정수 연산 수단의 구현/부합은 후속 검증 대상이며 새 라이브러리는 선정하지 않는다.

computed wire는 선행0·소수부 후행0·불필요한 소수점을 제거하되 1미만 정수부0을 유지하고 0은 "0"으로 만든다. 지수·음수0·NaN/Infinity를 금지하며 최종 정수부30자리 초과 또는 정확 양수가 최종6자리에서0으로 소실되면 DATA_INVALID다. 분모0은 not_applicable+quantity=null이며 observed/computed/estimated/missing/not_collected/not_applicable/withheld의7상태를 보존한다. 단위 불일치/미지원 수식·근거 누락도 DATA_INVALID다. calculationBasis에 프로필·수식·허용 원천 참조/개정·입력 단위·정확 합계/최종6자리 구분을 연결하고 숨긴 원천은 복사하지 않는다. 수신 수치와 단위는 허용 원천에서 재계산한 정규형 wire와 정확히 같아야 한다. 허용 오차0이며 수학적 반올림 오차 상한0.0000005를 수신 허용 오차로 쓰지 않는다. 사람용 half-even2자리/분:초 표시는 wire·digest·승인 내용을 바꾸지 않는다.

chrono+chrono-tz0.10.4 후보와 실제 IANA_TZDB_VERSION·chrono 선택 버전/빌드를 manifest에 고정한다. 활동 원 오프셋·UTC 순간·사용자 IANA 날짜를 구별하고 최근7/28/90일은 기준 현지 날짜D의[D-(N-1),D+1), ISO 월요일 주·달력 월/연도는 시작 포함/끝 제외다. 미래/부분 당일/미수집을 표시하며 날짜 계산이 완전 수집 증거가 되지 않는다.

Calendar는 승인 C05/C04와 현재 설정의 timingPolicy/tzdb를 대조한다. 세션 localTime 우선, null일 때 승인 내용에 결합한 기본 시각을 사용한다. 현지 시각이 단일 실제 순간이어야 하며 DST ambiguous/none·시각 불신은 BLOCKED다. 종료는 시작+expectedDuration의 경과 초이며 자동 시각 보정/이동을 하지 않는다. 신규 CREATE는 신뢰 현재 시각보다 엄격한 미래만 후보이고, 이전 미확인 효과의 대조는 U2-R03이 먼저다. 처분은 승인된 미래 영향만 처리한다.

검증 설계: U2-S10·U2-S12~U2-S16·U2-S49~U2-S56·U2-S72와 고정 NUM-01~NUM-16을 대조한다. 반복소수/절반 양방향 HALF_EVEN·정확 합계·분모0·양수 소실·원천 재계산과 잘못된 wire/단위·근거 필수 항목별 누락/원천 개정 변경을 포함한다. 정수부30/31자리·소수부18/19자리·중간 분자/분모256/257자리 경계를 각각 검사해 DATA_INVALID/RESOURCE_LIMIT를 구별한다. 자정/윤일/연말·DST/시각 경과도 기존대로 확인한다. 고정 수치/오류·시간 기대 전수 일치와 미검증 도구/시각의 적격 표시0건을 요구한다. 근거: [bigdecimal](https://docs.rs/bigdecimal/0.4.11/bigdecimal/), [chrono-tz](https://docs.rs/chrono-tz/0.10.4/chrono_tz/). 수치 규범은 확정되었으며 실제 계산 도구/tzdb/상호운용은 미검증이다.

<a id="u2-r07"></a>
## U2-R07 — 확인된 평가 실패의 제한된 복귀

대응: NFR9.3. 소유: PlanEvaluation(평가 사실), CalendarDelivery(근거 전달), PlanAdmission(새 최종 판정). 규칙: BR6.5·BR8.5·BR8.6.

평가 결과는 VALID/CALL_FAILED/INVALID/OUTCOME_UNKNOWN/BLOCKED를 원 요청/digest에 불변 연결한다. 늦은 응답은 새 결과/대조로 남기고 기존 실패나 현재 계획을 덮지 않는다. CalendarDelivery는 결과/실패 근거를 PlanAdmission에 전달한다. 확인된 CALL_FAILED에 한해 변경 없는 정확한 승인/형식/안전 통과 스냅샷·현재 정책/계보/철회/권한·미해소 경고 없음의 전체 조건을 새로 검사한다. 모두 적격일 때만 실패 고지와 새 ELIGIBLE_WITH_EVALUATION_FAILURE 판정으로 원 내용 게시 후보가 될 수 있다.

INVALID/미확인을 CALL_FAILED로 바꾸거나 오류 평가의 제안·안전 경고를 무시하지 않는다. 조건 하나라도 미해소면 BLOCKED이며 실제 승인/안전 프로필 부재는 계속 차단한다. 자동 공급자/모델 fallback·새 계획 승인 질문을 도입하지 않는다. 게시 후보는 Calendar 실제 성공이 아니며 U2-R03/직전 권한·예산 검사를 다시 거친다.

검증 설계: U2-S40·U2-S44~U2-S47·U2-S60의 확인 실패와 INVALID/미확인·안전/승인 실패를 비교한다. 허용 대역에서 필수 새 판정/고지, 음성에서 우회 효과0건을 확인한다. 실제 승인·안전·외부 평가/게시 적격성은 미해소다.
