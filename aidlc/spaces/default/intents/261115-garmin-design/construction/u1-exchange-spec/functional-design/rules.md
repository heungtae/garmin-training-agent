# U1 공통 교환 명세 — 업무 규칙

- 단위: `u1-exchange-spec`, 기준 계약: [Common·C01~C08 1.0.0](../../../inception/contract-design/contract-summary.md).
- 이 YAML이 U1의 의미 규칙 기준이다. 구조는 등록 Schema, 순서·상태 전이는 [functional-spec.md](functional-spec.md)가 기준이다. source의 FR은 U1에 배정된 **명세 부분**이며, 실제 적용은 U2/U3의 원 소유자가 수행한다.
- `violation`의 오류는 소비자가 표현해야 할 결과다. U1이 원격 작업을 수행하거나 제품 승인 결과를 발급한다는 뜻이 아니다.

## Business Rules

```yaml
rule_set: U1-EXCHANGE-1.0.0
rules:
  - id: BR1.1
    statement: "검증된 고정 명세와 사례만 선택한다."
    category: validation
    applies_to: [SpecificationRelease, ContractDefinition, ConsumerBinding, C01, C02]
    trigger: "배포 묶음 선택 또는 소비자 부합 검사"
    logic: "IF Common과 C01/C02 bootstrap의 신뢰된 고정값 및 C03~C08 각각 한 번의 schemaId/schemaDigest/fixturesDigest가 실제 산출물과 모두 일치 THEN 선택한다. 입력이 지정한 원격 registry는 읽지 않는다."
    violation: "VERSION_UNSUPPORTED 또는 CONTENT_MISMATCH/DATA_INVALID; 선택·활성화 보류"
    source: [FR4.3, FR4.5, FR5.11, FR7.3]
  - id: BR1.2
    statement: "전체 JSON 내용과 버전을 불변으로 결합한다."
    category: constraint
    applies_to: [C01, C02, C03, C05, C06, C07, ArtifactRef]
    trigger: "해시 생성·대조 또는 명세/계획 개정"
    logic: "IF 전체 payload의 RFC 8785 JCS UTF-8 SHA-256이 참조 digest와 일치 THEN 동일 내용 후보로 본다. 설명·extensions도 포함한다. 승인 선언 자체·Markdown·파일명·헤더는 C05 해시에 섞지 않는다. 배포한 버전의 내용은 교체하지 않는다."
    violation: "CONTENT_MISMATCH; 같은 ID/버전의 다른 내용을 병합·덮어쓰기하지 않음"
    source: [FR6.10, FR6.12, FR7.3, FR7.7]
  - id: BR1.3
    statement: "파싱 전부터 유한 한도를 적용하고 엄격한 JSON만 허용한다."
    category: validation
    applies_to: [C01, C02, C03, C04, C05, C06, C07, C08]
    trigger: "입력 바이트 수신 및 출력 준비"
    logic: "IF 허용 루트/대상·MIME·실행 한도·바이트/깊이 제한이 확인되고 UTF-8 객체 하나를 엄격 파싱할 수 있고 고정 Schema에 부합 THEN 의미 검사를 진행한다. 선두 단일 BOM·바깥 공백/CRLF만 허용하고 문자열은 보존한다. 중복 키·잘림·후행 문서·NaN/Infinity·잘못된 UTF-8·루트 비객체·알 수 없는 필수/권한 필드는 거절한다."
    violation: "DATA_INVALID/VERSION_UNSUPPORTED/RESOURCE_LIMIT; 프로필/한도 미설정도 보류, 입력 자동 복구 금지"
    source: [FR4.3, FR6.12, FR7.4, FR7.9, NFR5]
  - id: BR1.4
    statement: "ID와 외부 버전은 불투명 문자열로 대조한다."
    category: constraint
    applies_to: [ArtifactRef, C03, C05, C07, C08]
    trigger: "객체·버전·세션 식별 또는 반복 처리"
    logic: "IF ID는 1~1024자로 원문이 같고 정확한 소유 대상/버전/digest가 같음 THEN 같은 대상을 참조한다. 선행 0·대소문자·Unicode를 보존하며 이름·날짜·원격 수정 시각만으로 동일성/최신성을 정하지 않는다."
    violation: "DATA_INVALID/CONTENT_MISMATCH/REMOTE_CONFLICT; 다른 객체를 대체하거나 긴 ID를 잘라 재사용하지 않음"
    source: [FR3.6, FR7.3, FR7.7]
  - id: BR2.1
    statement: "7개 Metric 상태와 실제 0을 구별한다."
    category: validation
    applies_to: [Metric, C03]
    trigger: "측정 필드 교환 및 재계산"
    logic: "IF state가 observed/computed/estimated THEN quantity가 필요하고 그 외는 null이다. observed는 sourceRef 필수·calculationBasis=null, computed는 sourceRef와 계산 근거 필수, estimated는 추정 근거 필수다. withheld는 quantity/sourceRef/calculationBasis 모두 null이다. 실제 0은 수치 0이며 누락/미수집/해당 없음/비공개를 0으로 만들지 않는다."
    violation: "DATA_INVALID; 미제공 값 임의 생성 금지; 미허용 값의 상태 노출은 BR4.4 적용"
    source: [FR2.7, FR2.9, FR4.6]
  - id: BR2.2
    statement: "수치·단위·결정적 계산과 추정을 대조한다."
    category: calculation
    applies_to: [Quantity, Metric, C03, C05]
    trigger: "수치/강도/기간 합계의 의미 검사"
    logic: "IF 십진 문자열이 음수가 아니고 거리 m·시간 s·페이스 s/km·속도 m/s·심박 bpm 등 해당 필드 단위가 일치 THEN 계산한다. 결정적 페이스=시간(s)×1000/거리(m), 속도=거리(m)/시간(s); 분모 0은 not_applicable이다. 표현상 반올림/변환은 식별한 계산 근거와 허용 프로필에 결합하며 근거·정밀도 미해소를 observed로 승격하지 않는다."
    violation: "DATA_INVALID; NaN·무한대 금지, 비현실성/안전의 적격 기준 미해소는 SAFETY_BLOCKED로 연결"
    source: [FR2.7, FR2.9, FR4.3, FR4.6, FR6.6]
  - id: BR2.3
    statement: "기간·원천 시각·시간대 정책을 구분한다."
    category: validation
    applies_to: [Period, TimingPolicy, C03, C05, C07]
    trigger: "일자 포함 여부 및 세션 시각 해석"
    logic: "IF 실제 IANA 시간대와 적격 tzdbVersion에서 시작<끝인 시작 포함·끝 제외 기간이고 원천 오프셋을 보존하며 UTC 생성/수집 시각과 구별 THEN 범위를 대조한다. localTime=null이면 C05에 결합한 기본 시각만 사용한다. DST 중복/누락 시각을 자동 이동하지 않는다."
    violation: "DATA_INVALID/DEPENDENCY_UNQUALIFIED; 시각·정책·대상 변경은 기존 승인 전용 금지"
    source: [FR4.5, FR6.2, FR6.10, FR9.5, NFR6]
  - id: BR2.4
    statement: "종목을 보존하고 종목별로 집계한다."
    category: constraint
    applies_to: [C03, Metric]
    trigger: "종목 교환 및 summaryBySport 대조"
    logic: "IF running/swimming/cycling/strength/other/unknown 등록값 THEN 그대로 유지하고 종목별 유일 운동으로 집계한다. unknown을 running으로 바꾸거나 이종 종목 페이스/강도를 단일 성과로 합치지 않는다."
    violation: "DATA_INVALID; 미상/미지원은 명시하며 새 종목별 계획 기능을 자동 추가하지 않음"
    source: [FR4.7, FR2.7, FR4.3]
  - id: BR2.5
    statement: "원천·수집·생성·게시 시각과 계산 근거를 구별한다."
    category: constraint
    applies_to: [C03, C05, C08, ArtifactRef]
    trigger: "자료 출처/최신성/변경 상태 안내"
    logic: "IF sourceSnapshotRef·sourceRevision·sourceCollectedAt·generatedAt와 게시 결과의 observedAt/lastSuccessfulAt가 각각 유지됨 THEN 해당 범위만 안내한다. 변환/추정의 근거와 허용된 sourceRef를 연결하고 다른 시각/버전을 하나의 최신 값으로 대체하지 않는다."
    violation: "DATA_INVALID 또는 SOURCE_INCOMPLETE; 이전 유효본과 갱신 필요/실패 상태를 별도로 보존"
    source: [FR2.7, FR3.9, FR4.4, FR4.5, FR4.9]
  - id: BR3.1
    statement: "C03의 INLINE과 PARTITIONED를 혼합하지 않는다."
    category: validation
    applies_to: [C03, ArtifactRef]
    trigger: "분석 manifest 구성/검사"
    logic: "IF INLINE THEN detailArtifacts=[]·expectedPartCount=0·expectedActivityCount=activities 길이다. IF PARTITIONED THEN activities=[]·N>=1·총 운동>=1이며 등록 C03 Detail만 참조한다. 상세와 루트의 snapshotId/sourceSnapshotRef/subjectRef/projection/rootPeriod·partCount가 일치한다. Detail 하위 참조/순환은 허용하지 않는다."
    violation: "DATA_INVALID; 계보/정책/원천 혼합 자료의 분석·계획 근거 채택 보류"
    source: [FR4.1, FR4.3, FR4.4, FR6.12]
  - id: BR3.2
    statement: "분할 번호·참조·개수·기간을 대조한다."
    category: validation
    applies_to: [C03]
    trigger: "descriptor 및 도착한 Detail 대조"
    logic: "IF N개 descriptor의 partIndex가 0..N-1 각각 한 번이고 오름차순이며 동일 store/object/version 중복이 없고 activityCount>=1의 합이 expectedActivityCount와 같으며 본문 개수도 일치 THEN 분할 구조가 맞다. Detail.period=descriptor.period이고 동일 시간대의 rootPeriod 안에 포함되어야 한다. 운동 현지 일자도 양쪽 기간 안이어야 한다. 조각 기간 겹침 자체는 허용한다."
    violation: "중복·범위 밖 index·개수/기간 불일치 DATA_INVALID; 유효 descriptor 자체의 누락은 BR3.3의 PARTIAL"
    source: [FR4.3, FR4.4, FR4.5, FR4.9]
  - id: BR3.3
    statement: "상세 읽기 누락과 무효 내용을 다른 결과로 기록한다."
    category: validation
    applies_to: [C03, ArtifactRef, ConformanceAssessment]
    trigger: "고정 Detail 확보 및 검증"
    logic: "IF 등록 저장소 별칭의 정확한 objectId/versionRef 본문을 엄격 파싱하고 JCS digest를 대조한 뒤 등록 Detail 구조/의미를 통과 THEN 해당 조각만 사용한다. 유효 범위의 descriptor/상세 없음·읽기 실패·버전 미확인·해시 불일치는 조각 미사용과 SOURCE_INCOMPLETE/PARTIAL이다. 구조 오류·계보 혼합·중복·개수/집계 불일치는 DATA_INVALID다."
    violation: "누락은 failedParts와 effectiveCompleteness=PARTIAL; 무효 스냅샷은 분석/계획 근거 채택 보류. 실패를 0건으로 표시하지 않음"
    source: [FR4.1, FR4.3, FR4.4, FR4.9]
  - id: BR3.4
    statement: "전체 운동을 고유 ID와 안정적인 순서로 연결한다."
    category: constraint
    applies_to: [C03]
    trigger: "INLINE 목록 및 모든 상세 연결 결과 검사"
    logic: "IF 각 조각과 전체 연결 결과가 startedAt의 UTC 순간·동률 시 activityId Unicode 코드 포인트 순이고 activityId가 전체에서 유일 THEN 유지한다. 원 오프셋은 보존한다. 같은 ID의 다른 sourceRevision도 중복이며 동일 내용 중복도 자동 무시·합산하지 않는다."
    violation: "DATA_INVALID; 이름/시각이 같은 다른 ID 운동을 합치지 않음"
    source: [FR3.6, FR4.3, FR4.7]
  - id: BR3.5
    statement: "원천 completeness와 수신 effectiveCompleteness를 분리한다."
    category: calculation
    applies_to: [C03, ConformanceAssessment]
    trigger: "분석 자료의 유효 완전성 판정"
    logic: "IF COMPLETE 선언에 sourceCollectedAt 존재·missingPeriods=[]·전달 성공·합계 일치 THEN 유지한다. PARTIAL은 누락 기간(불명이면 전체 period)을 유지하며 상세 도착만으로 COMPLETE로 승격하지 않는다. EMPTY는 성공 수집·INLINE·정상 0건·빈 요약·누락 없음, NEVER_COLLECTED는 sourceCollectedAt=null·INLINE·0건·빈 요약·missingPeriods=[period]다. 전달 누락은 선언을 바꾸지 않고 유효 결과 PARTIAL로 남긴다."
    violation: "DATA_INVALID 또는 SOURCE_INCOMPLETE; 수집 미완료를 미운동으로 단정하지 않음. withheld 자체는 수집/전달 누락 아님"
    source: [FR2.9, FR4.1, FR4.6, FR4.9]
  - id: BR3.6
    statement: "허용된 종목별 합계를 정확한 Decimal과 상태 우선순위로 대조한다."
    category: calculation
    applies_to: [C03, Metric]
    trigger: "모든 게시 활동의 요약 검증"
    logic: "IF summary.totals 허용 THEN 존재 종목별 한 행·유일 운동 수·거리 m/시간 s 정확한 십진 합을 대조한다. 비공개 입력은 합계도 withheld, 공개 입력은 missing 우선·그다음 not_collected·나머지 not_applicable 제외(전부면 not_applicable)·수치 중 estimated 존재 시 estimated·그 외 computed와 근거다. totals 미허용은 summaryBySport=[]다. 모든 상세 확보 전 요약을 검증 완료로 표시하지 않는다."
    violation: "DATA_INVALID 또는 PERMISSION_DENIED; 부분 합을 전체 합으로 표시하거나 비공개를 0으로 계산하지 않음"
    source: [FR4.3, FR4.6, FR4.7, FR4.9, FR4.10]
  - id: BR3.7
    statement: "탐색 안내는 검증 가능한 범위와 실패 상태를 함께 전달한다."
    category: policy
    applies_to: [C03, C08]
    trigger: "최신 요약·상세/기간 탐색 자료 작성 또는 소비"
    logic: "IF 확인한 snapshot/period/ArtifactRef 및 원천/전달 완전성·시각·스키마 버전이 연결됨 THEN 해당 자료를 안내한다. 접근 실패·연결 단절·자료 없음·오래됨·미동기화는 각 사유와 다음 확인 경로를 표시한다. 임의 URL이나 새 탐색 API를 추가하지 않는다."
    violation: "SOURCE_INCOMPLETE/OUTCOME_UNKNOWN; 빈 자료를 정상 최신 보고서로 안내하지 않음"
    source: [FR4.1, FR4.4, FR4.5, FR4.9, FR3.9]
  - id: BR4.1
    statement: "정책 표현과 실제 현재 동의/권한을 구분한다."
    category: authorization
    applies_to: [C04, C05, C06, C07, C08]
    trigger: "각 신규 전송 직전 및 승인/정책 철회 확인"
    logic: "IF 원 사용자·원 정책·현재 버전·철회·목적/서비스/대상·실제 권한을 독립 검증하고 정책 전체 digest가 일치 THEN 해당 필드 범위만 허용한다. ACTIVE/consentRecordRef/verificationRecordRef나 오래된 사본은 증명이 아니다. C05~C08의 필수 업무 메타데이터도 명시적 동의가 필요하다."
    violation: "POLICY_UNVERIFIED/POLICY_STALE/PERMISSION_DENIED; 신규 전송 보류. 기존 외부 사본의 회수/삭제 성공을 주장하지 않음"
    source: [FR4.10, FR5.8, FR7.9, FR8.7, NFR2, NFR3]
  - id: BR4.2
    statement: "C03 최소 메타데이터 4개를 명시적으로 허용받는다."
    category: authorization
    applies_to: [C03, C04]
    trigger: "C03/Detail 투영 준비 및 재검사"
    logic: "IF analysis.metadata·summary.period·activity.date·activity.sport 모두 명시 허용 THEN 고정 슬롯/계보·시각·기간·운동/조각 개수까지 공개되는 범위로 검사한다. activity.date는 오프셋 포함 시각이다. 필수 스키마 필드라는 이유로 동의를 자동 추가하지 않는다."
    violation: "PERMISSION_DENIED; 네 항목 중 하나라도 없으면 C03 전체 신규 전송 보류"
    source: [FR4.10, FR4.5, FR8.7, NFR3]
  - id: BR4.3
    statement: "모든 실제 분석 경로의 허용 집합은 정확히 같아야 한다."
    category: authorization
    applies_to: [C03, C04, AnalysisProjection]
    trigger: "저장소/최종 독자가 포함된 실제 전송 경로 검사"
    logic: "IF 신뢰된 설정과 실제 연결로 정한 모든 경로에서 (service,purpose=ANALYSIS,targetAlias) grant가 정확히 하나이고 분석용 9개 이름을 추린 ASCII 정렬 집합이 projection.allowedFieldPaths와 정확히 같음 THEN 다음 검사로 진행한다. 다른 목적/대상/서비스 grant를 합치지 않는다."
    violation: "PERMISSION_DENIED; 더 넓거나 좁은 경로 하나라도 있으면 전체 신규 전송 보류. 자동 교집합/합집합 금지; 명시적 정책 변경 후 새 digest·projection·snapshotId/digest로 재검사"
    source: [FR4.10, FR8.7, NFR3, NFR4]
  - id: BR4.4
    statement: "미허용 지표를 withheld로 고정하고 역산/우회 공개를 막는다."
    category: policy
    applies_to: [C03, C04, Metric]
    trigger: "필드 투영·요약·계산 근거·수신 자료 검사"
    logic: "IF 지표 미허용 THEN 존재 여부와 관계없이 고정 슬롯에 withheld 및 quantity/sourceRef/calculationBasis=null을 쓴다. pace/speed는 intensity와 distance와 duration이 모두 허용돼야 공개한다. heartRate는 별도 허용이다. 비공개 값을 missing 등으로 위장하거나 합계·설명·extensions·sourceRef로 옮기지 않는다."
    violation: "PERMISSION_DENIED; 전체 관련 전송 보류 및 새 정책/투영 재검사"
    source: [FR2.9, FR4.6, FR4.10, FR8.7, NFR3, NFR4]
  - id: BR4.5
    statement: "비밀·기본 제외 자료와 미정의 민감 필드를 교환하지 않는다."
    category: policy
    applies_to: [C03, C04, C05, C06, C07, C08, SyntheticFixture]
    trigger: "모든 문서/오류/자유 서술/시험 자료 생성 및 전송"
    logic: "IF 인증정보·보호 보관 참조·직접 개인 식별자 또는 금지 자료가 있음 THEN 전송하지 않는다. GPS/FIT·수면/HRV·통증은 기본 제외이며 별도 동의만으로 미등록 필드를 extensions에 추가할 수 없다. constraints/설명/오류도 검사하고 구조 필터만으로 민감성 완전 검증을 자칭하지 않는다."
    violation: "PERMISSION_DENIED/DATA_INVALID; 안전한 최소 자료가 불가하면 보류. 승인 내용 자동 삭제/가림 후 같은 승인 재사용 금지"
    source: [FR4.10, FR7.9, FR8.7, NFR1, NFR3, NFR4]
  - id: BR5.1
    statement: "목표·가능 시간·고정 운동·제약을 완전하게 교환한다."
    category: validation
    applies_to: [C05]
    trigger: "목표 작성/수신 의미 검사"
    logic: "IF running 목표의 ID/개정·objective/targetDate·선택 거리/시간(m/s)·가능 요일/시간·양의 weeklyFrequency·고정 운동/제약이 구조에 있고 가능한 시간은 from<to이며 고정 운동의 일자/요일/시간을 일관되게 해석할 수 있음 THEN 검토한다. 미지정 목표량은 null로 남기며 모순/필수 미정을 임의 확정하지 않는다."
    violation: "DATA_INVALID; 추가 확인 필요를 표현하고 계획 전체 게시 보류"
    source: [FR5.4, FR6.2, FR7.4]
  - id: BR5.2
    statement: "계획 전체의 주차·세션·휴식·기간 일관성을 검사한다."
    category: validation
    applies_to: [C05]
    trigger: "완전본 작성/수신 판별"
    logic: "IF 목표일까지의 적용 범위·주차 목표·날짜별 running 세션·양수 s 예상시간·선택 m 거리·강도·준비/본/정리 수행 내용·휴식일이 완전하고 sessionId/sessionVersionId가 각각 유일하며 세션/휴식 날짜가 기간 안이고 서로 모순되지 않음 THEN 구조/의미 후보를 인정한다. 고정 운동·가능 시간과 충돌하면 확인한다."
    violation: "DATA_INVALID; 필수 누락·음수·기간 밖·중복·부분 작성은 계획 전체 보류, 다른 버전/유효 세션만 골라 자동 게시 금지"
    source: [FR6.2, FR6.12, FR7.4]
  - id: BR5.3
    statement: "강도 기준·단위·상하한과 미측정 사실을 보존한다."
    category: validation
    applies_to: [C05, Quantity]
    trigger: "세션 intensity 검사"
    logic: "IF heart_rate=bpm·pace=s/km·speed=m/s·rpe=rpe의 수치 상하한이 단위와 순서에 부합하고 rpe는 등록 scaleRef가 있으며 qualitative는 비수치 안내로 해석됨 THEN 표현을 인정한다. 수치 없는 기준은 임의 측정값으로 채우지 않는다. 척도/적용 기준을 확인할 수 없으면 보류한다."
    violation: "DATA_INVALID/DEPENDENCY_UNQUALIFIED; 생리적 안전 한계·의학적 보장을 새로 발명하지 않음"
    source: [FR6.6, FR6.2, FR2.9]
  - id: BR5.4
    statement: "개정·동시 변경은 새 내용과 새 승인으로 결합한다."
    category: constraint
    applies_to: [C05, C06, C07, ArtifactRef]
    trigger: "개정·재수신·검사 후 변경 감지"
    logic: "IF 새 versionId·previousPlanDigest·변경 사유·변경 항목 비교가 현재 확정 계보와 일치하고 새 전체 내용/정책/시각/행위에 새 승인이 있음 THEN 후속 수신 검증 후보가 된다. 같은 부모의 동시 승인 분기·초기 최신 계보 불명·과거 자료 재업로드·검사 후 원격 변경은 자동 병합/되돌리기하지 않는다."
    violation: "REMOTE_CONFLICT/CONTENT_MISMATCH/APPROVAL_UNVERIFIED; 이전 유효본 보존·재검증, 실제 운동 수정 금지"
    source: [FR6.10, FR6.12, FR7.3, FR7.7, FR9.5]
  - id: BR5.5
    statement: "완전본 저장/수동 전달은 직접 실행 명령 없이 동일 조건을 만족한다."
    category: constraint
    applies_to: [C05, C06, C07, C08]
    trigger: "Drive 저장 및 허용 수동 전달 정의"
    logic: "IF 버전별 JSON 전체와 승인 근거 연결을 지속 보관하고 실제 읽기 재확인으로 위치/버전/내용을 대조 THEN STORE 확인 후보가 된다. 수동 대안도 완전성·승인 신뢰를 동일하게 요구한다. Markdown 수정이나 저장 성공이 승인/수신/게시를 대신하지 않는다. 로컬 직접 호출·상시 서버·명령 payload는 요구하지 않는다."
    violation: "OUTCOME_UNKNOWN/DATA_INVALID/DEPENDENCY_UNQUALIFIED; 실제 미지원/미확인 경로는 보류, 성공 안내 금지"
    source: [FR5.9, FR5.10, FR5.11, FR7.1, FR6.12]
  - id: BR6.1
    statement: "C06 선언은 정확한 전체 대상과 단일 행위에 연결한다."
    category: authorization
    applies_to: [C05, C06, C07]
    trigger: "승인 선언의 구조/내용/행위 대조"
    logic: "IF PLAN이면 PUBLISH_PLAN 하나, DISPOSITION이면 C07 action에 대응하는 REPLACE_PLAN/WITHDRAW_PLAN/CANCEL_PUBLICATION 하나이고 targetDigest·policyDigest·subject·원 ArtifactRef가 모두 일치 THEN 독립 신뢰 검증의 후보로만 본다. profileId/recordId/claimedSubjectRef는 불신 지시자다."
    violation: "DATA_INVALID/CONTENT_MISMATCH/APPROVAL_UNVERIFIED; 선언·approved·해시·파일 소유·LLM 답변을 승인으로 취급하지 않음"
    source: [FR5.8, FR6.10, FR7.4, FR7.9]
  - id: BR6.2
    statement: "적격 독립 검증기와 현재 인간 승인 근거가 없으면 게시 권한이 없다."
    category: authorization
    applies_to: [C04, C06, C07, C08]
    trigger: "실제 승인 적격성 확인으로 넘길 때"
    logic: "IF 등록된 적격 검증기가 실제 사용자·전체 내용·행위·정책·현재 계보/철회와 명시적 인간 의도를 모두 독립 확인 THEN U2 내부 VerificationResult만 산출 가능하다. 외부가 보낸 VERIFIED는 인정하지 않는다. 현행 적격 프로필은 없으므로 U1 합성 적합성으로 이를 만들지 않는다. 추가 PC 승인을 몰래 기본 정책으로 도입하지 않는다."
    violation: "APPROVAL_PROFILE_UNQUALIFIED/APPROVAL_UNVERIFIED; 자동 게시·변경·취소 보류"
    source: [FR5.8, FR7.4, FR7.9, NFR2, NFR10]
  - id: BR6.3
    statement: "폐기·교체·취소는 승인된 미래 영향 범위에 한정한다."
    category: authorization
    applies_to: [C07, C06, C05]
    trigger: "처분 요청/새 계획/세션 영향 대조"
    logic: "IF expectedVersionId/expectedPlanDigest가 현재 대상이고 C07 전체 digest의 DISPOSITION 승인이 있고 영향 범위가 확인됨 THEN 미래 세션만 후보로 삼는다. SELECTED_FUTURE는 해당 sessionIds, ALL_FUTURE는 빈 sessionIds로 대상 계획의 미래 범위를 뜻한다. REPLACE는 replacementPlan의 새 PUBLISH_PLAN 승인도 필요하며 나머지는 replacementPlan=null이다."
    violation: "DATA_INVALID/APPROVAL_UNVERIFIED/REMOTE_CONFLICT; 완료 실제 운동·변경 없는 세션·다른 계획/일정 보존, 부분 실패는 C08로 분리"
    source: [FR7.8, FR9.5, FR6.10]
  - id: BR6.4
    statement: "명세 적합성·평가 결과·실제 게시 적격성은 별개다."
    category: policy
    applies_to: [ConformanceAssessment, C05, C08]
    trigger: "평가/게시 상태 표현과 U2 인계"
    logic: "IF U2가 사용자 승인·형식·안전 검증을 통과한 변경 없는 정확한 계획 digest를 확인하고 평가 호출 실패를 명시적으로 확인/고지함 THEN 기존 승인 버전 게시 예외를 검토할 수 있다. 오류 결과·미승인 조정안·미해소 안전 경고·정책 불명을 반영하지 않는다. 최종 판정은 U2 PlanAdmission이며 U1은 근거/차단 표현만 정의한다."
    violation: "SAFETY_BLOCKED/APPROVAL_UNVERIFIED/DEPENDENCY_UNQUALIFIED; 실제 Garmin·모델/비용·로컬 처리·자원 한도 미해소도 해당 실행 차단 유지"
    source: [FR6.8, FR7.4, FR7.9, FR8.7]
  - id: BR7.1
    statement: "작성·승인·저장·수신·검증·평가·게시의 소유/결과를 분리한다."
    category: constraint
    applies_to: [C05, C06, C08]
    trigger: "상태 생산/수신 및 설명"
    logic: "IF U3 생산자 THEN STORE만, U2는 해당 결과 소유자가 RECEIVE/VALIDATE/EVALUATE/CALENDAR 등을 실제 결과로 생산한다. C05 PROPOSAL과 C06 선언은 C08 SUCCESS로 자동 전환되지 않는다. 각 workId/subject/targetDigest/session을 연결하고 다른 단계의 성공을 추정하지 않는다."
    violation: "DATA_INVALID; 권위/최신성 미확인 U2 결과를 U3가 성공으로 자칭하지 않음"
    source: [FR3.9, FR5.10, FR6.8, FR7.9, NFR7, NFR10]
  - id: BR7.2
    statement: "성공은 그 단계의 실제 확인 범위에만 붙인다."
    category: validation
    applies_to: [C08]
    trigger: "저장/수신/게시 결과 판독"
    logic: "IF SUCCESS THEN errors=[]이며 생산자의 실제 대상/내용 확인이 필요하다. FAILED/BLOCKED/CONFLICT/OUTCOME_UNKNOWN은 오류 1개 이상이다. Calendar 전 대상 세션 성공만 전체 SUCCESS, 일부 성공은 PARTIAL이며 실패/미확인/대기를 세션별로 남긴다. observedAt과 lastSuccessfulAt을 구분한다."
    violation: "DATA_INVALID/OUTCOME_UNKNOWN; 응답 유실·부분 저장·잘못된 위치·미확인을 성공으로 표시하지 않음"
    source: [FR3.9, FR5.10, FR6.8, FR7.8, FR9.5, NFR7, NFR10]
  - id: BR7.3
    statement: "재처리는 원 대상/버전/내용/효과 대조 뒤에만 수행한다."
    category: constraint
    applies_to: [ArtifactRef, C07, C08]
    trigger: "중복 조회·응답 유실·취소 부분 실패의 표현"
    logic: "IF 같은 원 의도·소유 대상·버전/digest·세션/원격 연결을 확인 THEN 이미 성공한 결과에 연결한다. 원격 반영 불명은 OUTCOME_UNKNOWN과 대조 조치로 표현하고 확인 전 새 객체 생성/덮어쓰기하지 않는다. 성공한 타 대상/세션은 보존한다."
    violation: "OUTCOME_UNKNOWN/REMOTE_CONFLICT; 실행/복구는 U2/U3 담당, 불신 suggestedAction/파일명/본문을 명령으로 실행하지 않음"
    source: [FR3.6, FR5.10, FR7.8, FR7.9, FR9.5, NFR5]
  - id: BR7.4
    statement: "합성 예상 판정·실행 증거·제품 권한을 분리한다."
    category: policy
    applies_to: [SyntheticFixture, ConformanceCase, ConformanceAssessment, ConsumerBinding]
    trigger: "사례 작성·부합 검사·결과 보고"
    logic: "IF 고정 입력/치환/조건/대응 BR와 구조·의미 기대값·외부 차단을 분리하고 실제 수행 scope의 증거가 있음 THEN 해당 범위의 기대 일치만 MATCHED로 기록한다. 미수행은 PLANNED/NOT_RUN이다. U1은 U2 전용 LLM 스키마나 U3 전용 자료에 역의존하지 않는다."
    violation: "부합 판단 MISMATCHED 또는 NOT_RUN; 일반 JCS Unicode/수치·실제 외부 권한/지원/안전/실행을 한정 합성 결과로 확대하지 않음"
    source: [FR4.3, FR5.8, FR5.11, FR7.4, FR7.9, NFR1, NFR10]
```

## 규칙 요약

| 그룹 | 규칙 | 명세 책임과 실패 경계 |
|---|---|---|
| 등록/동일성 | BR1.1~BR1.4 | 고정 registry·전체 JCS·엄격 파싱·불투명 ID; 실패 입력 자동 보정 금지 |
| 값/출처 | BR2.1~BR2.5 | 7상태·0·십진 단위·기간/시간대·종목·원천/게시 시각 분리 |
| 분석 자료 | BR3.1~BR3.7 | 등록 Detail·분할·범위·정렬/중복·원천/전달 완전성·정확한 집계·탐색 |
| 공유 정책 | BR4.1~BR4.5 | 현재 동의·최소 4필드·모든 경로 동일 집합·withheld·비밀/민감자료 제외 |
| 목표/계획 | BR5.1~BR5.5 | 완전본·강도·개정 계보/동시 변경·명령 없는 Drive 전달 |
| 권한/처분 | BR6.1~BR6.4 | 불신 선언·독립 승인·미래 영향·게시/평가 분리와 미해소 차단 |
| 결과/검증 | BR7.1~BR7.4 | 단계/생산자별 실제 결과·미확인 대조·합성 적합성의 한계 |

34개 규칙은 상류 CR01~CR12를 U1 책임 범위에서 구체화한다. U2의 수집·계산 구현·승인 검증기·안전 프로필·저장/전송/Calendar 실행과 U3의 실제 읽기/승인 의사/저장 성공은 각 단위의 독립 검증 및 전체 실제 인수로 확인해야 한다.
