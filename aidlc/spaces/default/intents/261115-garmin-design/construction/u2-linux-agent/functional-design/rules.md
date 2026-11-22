# U2 Linux 에이전트 업무 규칙

근거: [요구사항](../../../inception/requirements-analysis/requirements.md), [기능 배정](../../../inception/units-generation/unit-of-work-story-map.md), [공유 계약](../../../inception/contract-design/contract-summary.md), [확인 답변](functional-design-questions.md). [entities.md](entities.md)의 이름과 [functional-spec.md](functional-spec.md)의 흐름/전이를 사용한다.

아래 YAML이 판단 규칙의 기준이다. IF/THEN 설명은 논리 명세이며 구현 코드가 아니다. 안전 규칙의 실제 근거/한계와 외부 적격성을 발명하지 않고 미설정 차단으로 표현한다.

```yaml
unit: u2-linux-agent
rules:
  - id: BR1.1
    statement: "설치/초기화/제거는 데이터 삭제와 분리한다"
    category: "policy"
    applies_to: ["RuntimeConfiguration","ScheduleRegistration","MaintenanceRequest"]
    trigger: "CLI 설치·제거"
    logic: "IF Ubuntu 24.04 이상 및 필요한 실행 권한/의존성이 확인되면 초기화 후보를 검증하고 예약 등록 상태를 확인한다. IF 지원 밖/권한 부족이면 원인·조치를 표시한다. IF 제거면 등록 실행을 중단하고 확인된 제거 범위만 처리하며 데이터 삭제는 별도 영향 확인을 요구한다."
    violation: "지원 밖/불충분 권한은 실패; 기존 유효 설정/자료 보존"
    source: ["FR1.1"]
  - id: BR1.2
    statement: "설정 후보 전체 검증 후 유효본을 교체한다"
    category: "validation"
    applies_to: ["RuntimeConfiguration","ServiceConnection","SharingConsent","RetentionPolicy"]
    trigger: "CLI 초기 설정·수정"
    logic: "IF 최초 기간·수집 범위·선택 대상·독립 주기·IANA 시간대·인증 참조·보존 선택의 검증을 통과하고 기대 configurationRevision이 현재와 같으면 새 개정으로 확정한다. ELSE 필드별 오류/누락 및 수정 방법을 안내하고 기존 설정을 유지한다. 비밀 값은 조회 결과에 포함하지 않는다."
    violation: "무효/동시 변경은 설정 교체 금지; 미선택 보존 기간은 자동 삭제 금지"
    source: ["FR1.2"]
  - id: BR1.3
    statement: "예약 등록 완료와 실제 로그아웃 실행 검증은 구별한다"
    category: "policy"
    applies_to: ["ScheduleRegistration","ExecutionRecord"]
    trigger: "설정 확정 후 등록"
    logic: "IF 유효 설정을 확정하면 두 jobPurpose를 별도 등록하고 실제 등록 상태를 관측한다. 로그인/로그아웃 각각의 실행 증거가 없으면 예약 지원 실측 완료를 표시하지 않는다. 종료/절전 중 실행은 보장하지 않고 복귀 시 누락을 재검사한다."
    violation: "등록 실패는 FAILED; 다음 예정 시각/실행 성공 추정 금지"
    source: ["FR1.3"]
  - id: BR1.4
    statement: "수집/동기화와 계획 확인 주기는 독립 관리한다"
    category: "constraint"
    applies_to: ["RuntimeConfiguration","ScheduleRegistration"]
    trigger: "주기 조회·변경·중단·재개"
    logic: "IF 주기가 양수이며 유한 실행 프로필이 지원하면 해당 목적의 주기만 변경한다. 기본은 collectionInterval=PT1H, planCheckInterval=PT15M이다. IF PAUSED면 새 예약 실행을 시작하지 않으며 진행 중 외부 효과는 결과를 보존·대조한다. 재개는 유효 설정과 등록 결과를 확인한다."
    violation: "0/음수/지원 불가 주기 거절, 기존 값 유지"
    source: ["FR1.4"]
  - id: BR1.5
    statement: "즉시 실행도 동일 중복/현재성 조건을 따른다"
    category: "policy"
    applies_to: ["ScheduleRegistration","ExecutionRecord"]
    trigger: "즉시 실행·상태 조회"
    logic: "IF 즉시 실행 요청이면 현재 설정과 목적별 workKey를 확인해 일반 실행 흐름을 사용한다. 상태는 마지막 실행/결과·다음 예정·미완료·마지막 성공을 구분한다. 최초/비활성은 null과 사유로 표시한다."
    violation: "미실행/비활성을 SUCCESS 또는 예정 시각으로 표시 금지"
    source: ["FR1.5"]
  - id: BR1.6
    statement: "중복 실행 배제와 도메인 멱등성을 함께 유지한다"
    category: "constraint"
    applies_to: ["ExecutionRecord","CollectionCursor","RepositoryPublication","PublicationIntent"]
    trigger: "같은 PC 중복 예약/즉시 실행"
    logic: "IF 같은 사용자/PC/jobPurpose가 진행 중이면 새 실행은 DUPLICATE_SUPPRESSED 또는 대기로 남기며 중복 효과를 만들지 않는다. 충돌하는 같은 원천/대상/세션의 변경은 소유 모듈이 기대 개정을 검사한다. 중단된 실행은 완료로 추정하지 않고 영속 작업 상태를 조회한다."
    violation: "단일 실행권 확보 불가 시 새 작업 중단; 기존 작업 보존"
    source: ["FR1.6"]
  - id: BR1.7
    statement: "복귀는 마지막 확정 지점과 미완료를 재검사한다"
    category: "policy"
    applies_to: ["CollectionCursor","ExecutionRecord","DeliveryAttempt"]
    trigger: "종료·절전·오프라인 후 실행"
    logic: "IF 미완료/누락 가능 범위가 있으면 마지막 로컬 확정 지점 이후 목록/상세·늦은 수정·게시/평가/Calendar 상태를 소유자에게 재검사 요청한다. 성공하지 않은 범위를 완료 커서로 넘기지 않는다. OUTCOME_UNKNOWN은 효과 재요청보다 대조가 우선이다."
    violation: "재검사 실패를 빈 정상 결과나 완료로 변환 금지"
    source: ["FR1.7"]
  - id: BR1.8
    statement: "CLI는 한국어 텍스트·결과·복구 조치를 제공한다"
    category: "policy"
    applies_to: ["ExecutionRecord","CollectionIssue","MaintenanceRequest"]
    trigger: "모든 CLI 결과"
    logic: "IF 작업이 종료/보류되면 대상·단계·오류 유형·마지막 성공·재시도 가능성·사용자 조치를 한국어로 표시하고 성공/부분/실패/보류를 종료 결과로 구별한다. 경로/도구/설정 누락은 해당 필드를 지목한다. 제어문자/마크업은 비실행 텍스트로 표현한다."
    violation: "원문/비밀/개인/건강 수치가 진단으로 유출되면 출력 차단"
    source: ["FR1.8"]
  - id: BR2.1
    statement: "Garmin 상세 계약/권한 확인 전 수집을 활성화하지 않는다"
    category: "authorization"
    applies_to: ["ServiceConnection","CredentialReference"]
    trigger: "Garmin 등록·연결 시험"
    logic: "IF P05 공식 상세 계약·인증/갱신·목록/상세/지표/페이지/기간/수정/한도 및 실제 권한이 확인되면 보호된 GARMIN_API_KEY 참조를 이용해 시험한다. 이름만으로 헤더/엔드포인트를 추측하지 않는다."
    violation: "미설정/거절/만료/미적격을 구별; DEPENDENCY_UNQUALIFIED 또는 PERMISSION_DENIED"
    source: ["FR2.1"]
  - id: BR2.2
    statement: "전체 목록 페이지와 각 상세의 확정 범위를 분리한다"
    category: "validation"
    applies_to: ["ActivityRecord","CollectionCursor","CollectionIssue"]
    trigger: "수집 실행"
    logic: "IF 적격 원천 목록을 읽으면 공식 페이지 종료 조건까지 진행하고 각 유효 상세를 로컬 확정한다. 일부 상세 실패는 ID와 pendingRanges를 보존한다. 목록 실패는 전체 요청 범위 미완료로 남긴다. 마지막 빈 페이지는 적격 계약의 종료 조건일 때만 종료로 인정한다."
    violation: "상세/목록 오류를 0건으로 확정 금지; 유효 다른 운동 보존"
    source: ["FR2.2"]
  - id: BR2.3
    statement: "최초/신규/수정/늦은 수정의 근거를 보존한다"
    category: "validation"
    applies_to: ["CollectionCursor","ActivityRecord"]
    trigger: "최초 수집·증분·복귀"
    logic: "IF 최초면 요청 기간 시작 포함/끝 제외를 검사한다. IF 신규/수정이면 원천 공식 수정 근거와 현재 개정을 대조한다. 늦은 수정 재검사 범위/방법은 P05 근거가 있어야 하며 판별 불가면 한계를 표시한다."
    violation: "미확보 커서/수정 계약 발명 금지; 불명 범위 완료 표시 금지"
    source: ["FR2.3"]
  - id: BR2.4
    statement: "원천 연결과 불투명 ID로 유일 운동을 유지한다"
    category: "constraint"
    applies_to: ["ActivityRecord"]
    trigger: "운동 반복 수신"
    logic: "IF (sourceConnectionId,sourceActivityId)가 같으면 단일 활동을 대조하고 같은 내용은 무변경 처리한다. 다른 ID는 이름/날짜가 같아도 병합하지 않는다. Unicode·대소문자·선행 0을 보존한다."
    violation: "충돌 내용의 무근거 덮어쓰기/이중 합산 금지"
    source: ["FR2.4"]
  - id: BR2.5
    statement: "확인 원천 수정과 게시 사본 충돌을 분리한다"
    category: "policy"
    applies_to: ["ActivityRecord","AnalysisSnapshot","RepositoryConflict"]
    trigger: "수정 확인"
    logic: "IF 원천 수정이 확인되면 새 로컬 개정을 확정한 후 영향 기간/종목 분석을 새 스냅샷으로 생성한다. 재계산 실패는 이전 유효본과 갱신 필요 상태를 보존한다. 게시 사본 수정/삭제는 RepositoryConflict로 처리한다."
    violation: "원격 게시 삭제를 원천 운동 삭제로 전파 금지"
    source: ["FR2.5"]
  - id: BR2.6
    statement: "지원 종목/지표와 미상 상태를 유지한다"
    category: "validation"
    applies_to: ["ActivityRecord"]
    trigger: "정규화"
    logic: "IF 원천이 지원하는 운동/지표면 해당 종목과 단위를 보존한다. ELSE other/unknown/미지원 사유를 명시하고 running으로 치환하지 않는다. 종목별 계산 정의가 없는 지표는 유효 통계에서 제외하고 범위를 표시한다."
    violation: "미지원 지표/종목 발명 금지"
    source: ["FR2.6"]
  - id: BR2.7
    statement: "측정값·단위·원천·수집시각 및 변환 근거를 보존한다"
    category: "validation"
    applies_to: ["ActivityRecord","AnalysisSnapshot"]
    trigger: "수집·변환"
    logic: "IF observed면 실제 sourceRef와 단위/수집시각이 필요하다. IF computed면 정확한 원천과 계산 정의가 필요하며 원값·변환 결과를 구별한다. 비현실적/단위 없는 값은 유효값과 분리하고 도메인 근거 없이 자동 보정하지 않는다."
    violation: "DATA_INVALID 또는 부분 수집; 이전 유효 자료 보존"
    source: ["FR2.7"]
  - id: BR2.8
    statement: "외부/항목 오류는 한정 복구한다"
    category: "policy"
    applies_to: ["CollectionIssue","CollectionCursor"]
    trigger: "인증·제한·응답·통신 오류"
    logic: "IF 만료/권한 오류면 재인증 전 반복 효과 요청을 중단한다. IF 429/일시 장애면 공급자 대기 지시와 유한 예산 내 재시도한다. IF 대기 지시가 실행 한도를 넘으면 다음 작업으로 남긴다. 유효 운동과 미완료 수·범위를 각각 보존한다."
    violation: "무한 대기/재시도 금지; 고정 한도/백오프는 NFR 선정"
    source: ["FR2.8"]
  - id: BR2.9
    statement: "미제공/미수집/해당 없음/실제 0/추정을 혼동하지 않는다"
    category: "validation"
    applies_to: ["ActivityRecord","AnalysisSnapshot"]
    trigger: "측정값 수신·집계"
    logic: "IF 값이 미제공이면 missing, 수집 전이면 not_collected, 정의상 해당 없으면 not_applicable이다. 실제 수치 0은 observed/computed 값 0이다. estimated는 근거와 추정 상태를 유지한다. not_collected를 미운동으로 판단하지 않는다."
    violation: "값·원천 사실 임의 생성 금지"
    source: ["FR2.9"]
  - id: BR3.1
    statement: "GitHub와 Drive 연결/권한 시험을 독립한다"
    category: "authorization"
    applies_to: ["ServiceConnection"]
    trigger: "저장소 등록·시험"
    logic: "IF 한 대상 연결 실패면 해당 연결 상태와 조치를 기록하며 다른 연결과 로컬 자료를 유지한다. P01/P02 실제 쓰기/재읽기·비공개/권한 증거 전 지원 성공을 주장하지 않는다."
    violation: "미적격 대상 신규 게시 보류"
    source: ["FR3.1"]
  - id: BR3.2
    statement: "활성 분석 대상만 전송한다"
    category: "authorization"
    applies_to: ["RuntimeConfiguration","RepositoryPublication"]
    trigger: "대상 선택·게시"
    logic: "IF 대상이 RuntimeConfiguration.analysisTargets에 명시 선택되어 있고 storage/모든 finalReaderConnectionIds가 등록·역할·현재 동의/권한 검사를 통과하면 해당 분석만 게시 후보로 삼는다. connectionIds는 등록 목록이며 동의는 전송 허가이므로 활성 선택을 대신하지 않는다. 하나/양쪽/0개 선택을 지원하고 0개면 로컬 보존·외부 미게시다. 계획 확인은 별도 planInboxConnectionId만 사용한다. 대상 비활성화 직후 미전송/재시도 쓰기를 중단하고 이전 미확인 효과는 허용된 읽기 대조만 하며 임의 삭제하지 않는다. 변경은 기대 설정 개정으로 확정·조회·재시작 복원한다."
    violation: "비활성/미허용 대상 전송 금지"
    source: ["FR3.2"]
  - id: BR3.3
    statement: "외부 효과 전 로컬 유효본과 의도를 확정한다"
    category: "constraint"
    applies_to: ["ActivityRecord","AnalysisSnapshot","RepositoryPublication"]
    trigger: "수집/생성/게시"
    logic: "IF 새 자료·의도의 로컬 확정이 성공한 경우에만 외부 요청을 허용한다. 디스크 부족/읽기 전용/중단이면 이전 유효본을 유지하고 새 저장/게시 성공을 주장하지 않는다. 허용 데이터 루트 이탈/순환 접근을 거절한다."
    violation: "로컬 확정 실패 시 신규 외부 효과 0건"
    source: ["FR3.3"]
  - id: BR3.4
    statement: "대상별 성공·실패·대기·미확인을 집계한다"
    category: "policy"
    applies_to: ["RepositoryPublication","ExecutionRecord"]
    trigger: "게시 결과"
    logic: "IF 둘 중 한 대상만 성공하면 전체는 PARTIAL이며 대상별 결과와 마지막 성공을 표시한다. SUCCESS는 해당 대상의 실제 내용/버전 확인 후만 인정한다."
    violation: "한 대상 성공을 전체 동기화 성공으로 표시 금지"
    source: ["FR3.4"]
  - id: BR3.5
    statement: "실패 대상만 복구하고 타 대상 성공을 유지한다"
    category: "policy"
    applies_to: ["RepositoryPublication"]
    trigger: "게시 재시도"
    logic: "IF 한 대상이 실패/대기면 해당 대상 의도만 현재 동의/권한/내용 재확인 후 재시도한다. 다른 대상 SUCCESS는 되돌리거나 재생성하지 않는다. 미확인은 대조 후 판단한다."
    violation: "부분 실패를 이유로 성공 자료 삭제 금지"
    source: ["FR3.5"]
  - id: BR3.6
    statement: "응답 유실은 고정 대상/내용 대조가 먼저다"
    category: "constraint"
    applies_to: ["RepositoryPublication","RepositoryConflict"]
    trigger: "쓰기 응답 유실·중단"
    logic: "IF OUTCOME_UNKNOWN이면 원 의도·고정 경로/객체·기대 digest·원격 버전을 조회한다. 일치하면 SUCCESS, 다르면 CONFLICT, 실제 미생성이 확인되면 동일 의도를 재시도하고 조회 불가는 계속 미확인으로 둔다."
    violation: "불명확한 상태에서 새 경로/객체 생성·무조건 덮어쓰기 금지"
    source: ["FR3.6"]
  - id: BR3.7
    statement: "원격 사본 충돌·보존·삭제 영향은 명시 확인한다"
    category: "policy"
    applies_to: ["RepositoryConflict","RetentionPolicy","MaintenanceRequest"]
    trigger: "원격 변경·삭제·정리"
    logic: "IF 원격 사용자 변경/삭제면 충돌을 기록해 자동 덮어쓰기/로컬 전파를 금지한다. IF 보존 기간 미설정이면 자동 삭제하지 않는다. IF 삭제 요청이면 로컬/원격/일정 범위와 복구 한계를 표시하고 같은 범위의 사용자 확인 후 소유자별 처리한다. 미해소 효과의 대조 근거는 삭제하지 않는다."
    violation: "무단 삭제/복구 보장 금지"
    source: ["FR3.7"]
  - id: BR3.8
    statement: "비공개/허용 대상 확인 후 게시한다"
    category: "authorization"
    applies_to: ["ServiceConnection","SharingConsent","RepositoryPublication"]
    trigger: "각 신규 전송 직전"
    logic: "IF 현재 목적·서비스·대상 권한/명시 동의·비공개 상태가 확인돼야 전송한다. 공개/허용 안 된 폴더/불명 권한은 보류한다. 실제 권한·현재성과 적격 프로필 문서의 존재를 구별한다."
    violation: "PERMISSION_DENIED/POLICY_UNVERIFIED/POLICY_STALE"
    source: ["FR3.8"]
  - id: BR3.9
    statement: "생성·원천 수집·갱신·마지막 성공 게시 시각을 구별한다"
    category: "policy"
    applies_to: ["AnalysisSnapshot","RepositoryPublication"]
    trigger: "자료/상태 생성"
    logic: "IF 상태를 표시하면 generatedAt/collectedAt/updatedAt/lastConfirmedAt을 별도 인용하고 현재 실패와 마지막 성공을 함께 표시한다. 미실행/null을 최신 성공으로 대체하지 않는다."
    violation: "오인 최신/성공 표시 금지"
    source: ["FR3.9"]
  - id: BR4.1
    statement: "최신 상태/상세/기간 탐색을 허용 고정 참조로 제공한다"
    category: "validation"
    applies_to: ["AnalysisSnapshot","RepositoryPublication"]
    trigger: "분석 산출물 생성"
    logic: "IF 로컬 확정 자료가 있으면 최신 스냅샷과 기간/상세의 탐색 참조를 생성하되 대상별 동의 투영을 적용한다. 자료 없음·접근 실패는 이유/재확인 경로를 표시하며 파일명만으로 최신을 추정하지 않는다."
    violation: "빈/접근 실패 보고서를 정상 최신으로 표시 금지"
    source: ["FR4.1"]
  - id: BR4.2
    statement: "기간은 시간대의 시작 포함·끝 제외로 계산한다"
    category: "calculation"
    applies_to: ["AnalysisSnapshot"]
    trigger: "최근/주/월/연 분석"
    logic: "IF 기준 현지 날짜 D의 최근 N일이면 [D-(N-1),D+1), N=7/28/90으로 고정하고 기준시각과 부분 당일을 표시한다. 주는 ISO 월요일~다음 월요일, 월/연은 달력 경계이며 아직 오지 않은 범위를 완전 수집으로 표시하지 않는다. startedAt을 해당 IANA 시간대로 변환한 날짜로 배정한다."
    violation: "시각/시간대 미신뢰 시 집계 보류; DST/윤일/연말 중복 금지"
    source: ["FR4.2"]
  - id: BR4.3
    statement: "구조화 상세와 계산 정의로 재계산 가능하게 한다"
    category: "validation"
    applies_to: ["AnalysisSnapshot"]
    trigger: "분석 생성·전달"
    logic: "IF 요약을 게시하면 등록 C03 Activity/Detail과 정확한 단위·원천 개정·계산 정의를 제공한다. 한도로 분할할 때 등록 Detail만 쓰며 원자적 다중 파일 게시를 가정하지 않는다. 제외/실패 범위를 명시한다."
    violation: "크기 초과를 조용히 잘라 완전 분석으로 표시 금지"
    source: ["FR4.3"]
  - id: BR4.4
    statement: "상세 개정과 영향 요약의 계보를 고정한다"
    category: "constraint"
    applies_to: ["AnalysisSnapshot","ActivityRecord"]
    trigger: "원천 수정·탐색"
    logic: "IF 상세 개정이 바뀌면 영향을 받는 모든 기간/종목 파생본은 새 입력 집합으로 생성한다. 연결 소실은 불일치로 보존하며 원천 삭제/다른 버전 혼합으로 해결하지 않는다."
    violation: "정합한 이전 스냅샷 보존; 갱신 필요 표시"
    source: ["FR4.4"]
  - id: BR4.5
    statement: "범위·시각·단위·출처·명세를 함께 식별한다"
    category: "validation"
    applies_to: ["AnalysisSnapshot"]
    trigger: "자료 생성"
    logic: "IF 분석 생성이면 period/timezone/generatedAt/sourceCollectedAt/schemaVersion·입력 개정/계산 정의를 포함한다. 서로 다른 수집/생성/게시 버전을 단일 최신으로 합치지 않는다."
    violation: "필수 메타데이터 누락 시 게시 보류"
    source: ["FR4.5"]
  - id: BR4.6
    statement: "분모 0과 비수치 상태는 유효 성과가 아니다"
    category: "calculation"
    applies_to: ["AnalysisSnapshot"]
    trigger: "계산·표시"
    logic: "IF distance=0이면 pace=not_applicable, IF duration=0이면 speed=not_applicable로 수치 null을 사용한다. 누락/미수집 입력은 0 대체 없이 해당 상태를 전파한다. estimated는 근거를 유지하고 미허용은 withheld로 처리한다. NaN/Infinity는 거절한다."
    violation: "허위 평균/성과 및 0 치환 금지"
    source: ["FR4.6"]
  - id: BR4.7
    statement: "종목별 유일 집합으로 계산한다"
    category: "calculation"
    applies_to: ["AnalysisSnapshot","ActivityRecord"]
    trigger: "집계"
    logic: "IF sport가 같고 ID가 유일한 집합만 해당 종목 합계로 계산한다. unknown/other를 running으로 합치지 않는다. 서로 다른 종목의 페이스/강도를 합산하지 않는다. 중복 ID는 C03 채택을 보류한다."
    violation: "중복/혼합 종목 합계 DATA_INVALID"
    source: ["FR4.7"]
  - id: BR4.8
    statement: "정확 계산 뒤 표시 반올림과 차이를 설명한다"
    category: "calculation"
    applies_to: ["AnalysisSnapshot"]
    trigger: "수치/요약 생성"
    logic: "IF 허용된 원천/단위를 계산하면 공통 GTA-NUMERIC-1을 적용한다. 원천과 같은 단위 합계는 정수부30/소수부18자리 이내 정확 십진으로 보존하고, 분자/분모 각각256자리 이내 유리수 중간값에서 속도/페이스만 마지막 소수부6자리 HALF_EVEN으로 wire 정규화한다. 양수의0반올림·결과 한도 초과는 DATA_INVALID, 중간값 한도 초과는 RESOURCE_LIMIT다. calculationBasis에 프로필/수식/허용 원천 개정/단위/정확 합계 또는 최종 반올림을 기록한다. 같은 입력 재계산의 정규형·단위를 오차0으로 대조한다. 사람용2자리 표시는 별도이며 반올림된 속도로 페이스를 재계산하지 않는다."
    violation: "동일 스냅샷 중 숫자/설명 불일치는 생성 보류"
    source: ["FR4.8"]
  - id: BR4.9
    statement: "원천 완전성과 전달 완전성/최신성을 분리한다"
    category: "validation"
    applies_to: ["AnalysisSnapshot","CollectionCursor","RepositoryPublication"]
    trigger: "자료 완전성 판정"
    logic: "IF source COMPLETE라도 Detail 미도착/미확인이면 effectiveCompleteness=PARTIAL이다. 원천 PARTIAL은 전달 성공으로 COMPLETE 승격하지 않는다. EMPTY는 성공 0건, NEVER_COLLECTED는 미수집이다. 누락기간·실패 조각·마지막 성공 게시를 표시한다."
    violation: "부분 자료를 완전/최신으로 오인시키지 않음"
    source: ["FR4.9"]
  - id: BR4.10
    statement: "모든 실제 전송 경로를 같은 현재 정책으로 검사한다"
    category: "authorization"
    applies_to: ["SharingConsent","AnalysisSnapshot","EvaluationRequest","PublicationIntent"]
    trigger: "저장소/ChatGPT/LLM/Calendar 전송 직전"
    logic: "IF 신뢰된 analysisTargets의 저장 연결과 실제 finalReader 연결 각각의 SharingConsent를 찾아 connection.serviceName/purpose/targetReference를 C04 service/purpose/targetAlias로 대응하고 현재 주체/개정/digest/철회·권한 검증을 통과하면 해당 범위만 전송한다. 실제 도구 경로와 설정 경로가 다르거나 chatgpt를 drive/openai로 위장하면 보류한다. 각 grant는 유일해야 하며 C03 모든 실제 ANALYSIS 경로의 정렬된 분석 필드 집합은 projection과 정확히 같아야 한다. 넓거나 좁아도 교집합 자동 생성 없이 전체 신규 전송을 보류한다. 최소 네 필드 명시 동의가 필요하며 자유 서술/요약/계산/오류도 금지 자료를 우회 전송하지 못한다."
    violation: "PERMISSION_DENIED/POLICY_UNVERIFIED/POLICY_STALE; 동의 자동 확대/축소 금지"
    source: ["FR4.10"]
  - id: BR5.8
    statement: "외부 승인 선언은 독립 검증 전 권한이 아니다"
    category: "authorization"
    applies_to: ["ApprovalProof","AdmissionAssessment"]
    trigger: "C06 수신·게시 직전"
    logic: "IF 등록 적격 검증기가 실제 사용자·C05/C07 전체 digest·정책 digest·행위·명시적 인간 의도·현재성/철회 CLEAR를 모두 확인해야 검증 근거를 인정한다. approved/파일 소유/OAuth/hash/LLM/외부 VERIFIED는 부족하다. 추가 PC 승인으로 기존 정책을 몰래 바꾸지 않는다."
    violation: "APPROVAL_PROFILE_UNQUALIFIED/APPROVAL_UNVERIFIED; 자동 게시 보류"
    source: ["FR5.8"]
  - id: BR5.11
    statement: "Drive 주기 수신은 로컬 직접 호출 없이 수행한다"
    category: "policy"
    applies_to: ["ReceivedPlanArtifact","ScheduleRegistration"]
    trigger: "PLAN_CHECK 실행"
    logic: "IF 적격 Drive 읽기 경로면 등록된 storeAlias/허용 범위에서 C05/C06/C07을 조회한다. ChatGPT→PC 명령·상시 서버/MCP를 정상 경로 필수로 추가하지 않는다."
    violation: "읽기/권한 미확인은 보류; 명령 지시 실행 금지"
    source: ["FR5.11"]
  - id: BR6.2
    statement: "필수 계획/세션이 모두 유효해야 전체를 채택한다"
    category: "validation"
    applies_to: ["ReceivedPlanArtifact","AdmissionAssessment"]
    trigger: "계획 형식/의미 검사"
    logic: "IF C05 goal/period/weeklyObjectives/sessions/restDates/강도·수행내용·단위가 완전하고 기간/목표일·가능 시간/고정 운동·휴식과 일치하며 세션/버전 ID가 유일하면 다음 검증으로 진행한다. 예상 duration>0 s, distance>=0 m, lower<=upper 및 기준별 단위/RPE scaleRef를 확인한다."
    violation: "누락/중복/음수/기간 밖/모순은 DATA_INVALID; 계획 전체 보류"
    source: ["FR6.2"]
  - id: BR6.5
    statement: "안전 근거·적용조건·한계가 미해소면 적격 판정을 내리지 않는다"
    category: "policy"
    applies_to: ["AdmissionAssessment","EvaluationResult"]
    trigger: "안전 검사·최종 판정"
    logic: "IF 규칙집이 훈련량/강도 변화·휴식/회복 및 명시 제약의 근거/버전/적용 조건/비교 단위/허용 한계/부족 자료 처리를 갖추고 현재 입력으로 판정 가능해야 안전 통과한다. 단위별 양/강도 비교·동일 기간 변화·고정 운동/가용 시간 중복·휴식 충돌을 검사한다. 보편 의료 임계값을 발명하지 않으며 미설정/비교 불가/미해소 경고는 차단한다."
    violation: "SAFETY_BLOCKED; LLM 실패로 경고/차단 우회 금지"
    source: ["FR6.5"]
  - id: BR6.8
    statement: "작성·승인·저장·수신·평가·게시 결과를 분리한다"
    category: "policy"
    applies_to: ["ReceivedPlanArtifact","AdmissionAssessment","EvaluationResult","PublicationIntent"]
    trigger: "상태 조회/결과 생성"
    logic: "IF 각 단계 결과를 표시하면 원 소유자의 실제 결과와 버전/digest를 연결한다. 스냅샷 보존/평가 성공/Drive 저장 성공을 Calendar SUCCESS로 사용하지 않는다. 부분/skip/미확인은 전체 게시 성공이 아니다."
    violation: "허위 전체 성공 금지"
    source: ["FR6.8"]
  - id: BR6.10
    statement: "새 내용과 개정은 새 승인 및 확정 계보를 요구한다"
    category: "authorization"
    applies_to: ["AdmittedPlanSnapshot","ApprovalProof","AdmissionAssessment"]
    trigger: "새 계획/늦은 응답"
    logic: "IF C05 전체 내용/정책/시각/설명/extension이 바뀌면 새 versionId/digest와 새 C06 근거가 필요하다. previousPlanDigest를 현재 계보와 비교하고 동일 부모의 동시 승인 분기/구버전/현재 계보 불명은 보류한다. 파일명/수정시각만으로 최신을 정하지 않는다."
    violation: "CONTENT_MISMATCH/REMOTE_CONFLICT/APPROVAL_UNVERIFIED"
    source: ["FR6.10"]
  - id: BR6.11
    statement: "계획 개정/취소가 실제 운동을 변경하지 않는다"
    category: "constraint"
    applies_to: ["ActivityRecord","AdmittedPlanDisposition","CalendarBinding"]
    trigger: "개정·취소·연결 소실"
    logic: "IF 승인 미래 세션을 갱신/취소해도 실제 ActivityRecord 및 과거 일정/다른 일정을 보존한다. 연결 소실을 원천 삭제로 해석하지 않는다."
    violation: "실적 덮어쓰기/삭제 금지"
    source: ["FR6.11"]
  - id: BR6.12
    statement: "완전한 같은 버전만 검증한다"
    category: "validation"
    applies_to: ["ReceivedPlanArtifact","AdmittedPlanSnapshot"]
    trigger: "부분 파일·혼합 버전 수신"
    logic: "IF 엄격 파싱/완전성·원격 전후 버전·참조/전체 digest가 모두 일치해야 검증 사본을 만든다. 잘림/부분 작성/동시 변경은 전체 보류하고 완전본을 다시 수신·검증한다. 일부 유효 세션을 떼어 새 계획으로 만들지 않는다."
    violation: "SOURCE_INCOMPLETE/DATA_INVALID/REMOTE_CONFLICT"
    source: ["FR6.12"]
  - id: BR7.2
    statement: "계획 확인 실패를 최신 확인으로 처리하지 않는다"
    category: "validation"
    applies_to: ["ScheduleRegistration","ReceivedPlanArtifact"]
    trigger: "설정 주기 PLAN_CHECK"
    logic: "IF 신뢰 가능한 원격 계보/버전을 확인하면 고정 자료를 수신하고 대조한다. ELSE 마지막 성공과 현재 실패를 남기고 기존 사본을 보존하며 그 사본을 현재 최신으로 추정하지 않는다."
    violation: "최신 여부 불명 상태의 신규 게시 보류"
    source: ["FR7.2"]
  - id: BR7.3
    statement: "내용·계보·ID와 원격 저장 위치를 각각 대조한다"
    category: "constraint"
    applies_to: ["ReceivedPlanArtifact","AdmittedPlanSnapshot","PublicationIntent"]
    trigger: "수신/중복 대조"
    logic: "IF 같은 subject/plan/version인데 digest가 다르면 충돌이다. 이름 변경/이동돼도 같은 ID/내용이면 동일 원본으로 연결하고 동명 다른 ID는 병합하지 않는다. 앱 versionId·원격 versionRef·snapshotId는 다른 식별자다."
    violation: "CONTENT_MISMATCH/REMOTE_CONFLICT"
    source: ["FR7.3"]
  - id: BR7.4
    statement: "형식·참조·허용 행위·승인·현재성을 모두 검사한다"
    category: "authorization"
    applies_to: ["ApprovalProof","AdmissionAssessment"]
    trigger: "수신 검증·최종 게시"
    logic: "IF 지원 registry의 Common/C01~C08 버전·schema/digest, 계획/승인/정책 참조·행위가 정확히 일치하고 적격 검증이 통과해야 다음 상태로 진행한다. C06 PLAN은 PUBLISH_PLAN만, DISPOSITION은 대응 단일 행위만 허용한다."
    violation: "잘못된 형식/미승인/참조 누락/미지원은 전체 보류"
    source: ["FR7.4"]
  - id: BR7.5
    statement: "반복 조회/재개는 영속 결과를 재사용한다"
    category: "constraint"
    applies_to: ["ReceivedPlanArtifact","PublicationIntent","CalendarBinding"]
    trigger: "중복 수신·재시작"
    logic: "IF 같은 버전/내용이면 기존 검증·의도·연결을 조회하고 완료 효과를 재생성하지 않는다. 다만 현재 승인/정책/안전 확인은 다시 수행한다. 미해소 외부 결과는 조회 대조하고 구버전 응답으로 새 버전을 되돌리지 않는다."
    violation: "중복 효과/구버전 덮어쓰기 금지"
    source: ["FR7.5"]
  - id: BR7.6
    statement: "계획별 단계와 세션별 결과를 보존한다"
    category: "policy"
    applies_to: ["ExecutionRecord","AdmissionAssessment","DeliveryAttempt"]
    trigger: "상태/오류 집계"
    logic: "IF 결과를 생성하면 수신/검증/평가/Calendar 단계·정확한 digest·대상 세션별 대기/성공/실패/부분/충돌/미확인을 연결한다. 현재 오류와 마지막 성공·다음 조치를 구별한다."
    violation: "조회 불가/미확인을 완료로 표시 금지"
    source: ["FR7.6"]
  - id: BR7.7
    statement: "검사 후 변경과 동시 수정은 재검증/보류한다"
    category: "validation"
    applies_to: ["ReceivedPlanArtifact","AdmissionAssessment","CalendarBinding"]
    trigger: "수신 전후·외부 효과 직전"
    logic: "IF Drive 전후 버전/digest 또는 승인/정책/원천/계보가 달라지면 기존 판정을 무효화하고 재검증한다. 외부 효과 직전 확인 지점을 보존하며 이후 철회/변경 감지 시 남은 요청을 중단하고 이미 시작한 효과는 대조한다. 외부 원자성/회수를 가정하지 않는다."
    violation: "REMOTE_CONFLICT/OUTCOME_UNKNOWN; 조용한 덮어쓰기 금지"
    source: ["FR7.7"]
  - id: BR7.8
    statement: "폐기/교체/취소는 승인된 미래 영향만 처리한다"
    category: "authorization"
    applies_to: ["AdmittedPlanDisposition","CalendarBinding","MaintenanceRequest"]
    trigger: "C07 처리"
    logic: "IF C07 전체 digest와 C06 DISPOSITION·현재 예상 버전/정책·영향 범위가 일치하면 해당 미래 세션만 처리한다. REPLACE는 replacement C05의 별도 PUBLISH_PLAN 승인·안전 검증도 요구한다. WITHDRAW는 이후 신규 적용 차단, CANCEL_PUBLICATION은 승인 범위의 연결 일정 취소이며 사실 삭제가 아니다. 성공/실패 세션은 독립 보존한다."
    violation: "승인/미래/범위 불명은 BLOCKED; 타 일정/실적/과거 일정 보존"
    source: ["FR7.8"]
  - id: BR7.9
    statement: "외부 자료는 권한을 부여하지 않는 데이터다"
    category: "authorization"
    applies_to: ["ReceivedPlanArtifact","ApprovalProof","EvaluationResult"]
    trigger: "모든 외부 입력"
    logic: "IF 파일명/텍스트/LLM/extension에 명령·URL·경로·검증키/프로필 등록·비밀 요청이 있어도 실행하지 않는다. 로컬 허용 루트/등록 storeAlias/소유 대상/행위만 사용한다. 지원 schema는 고정 registry에서 로드하고 원격 다운로드하지 않는다."
    violation: "DATA_INVALID/PERMISSION_DENIED; 승인/공유 확대 금지"
    source: ["FR7.9"]
  - id: BR8.1
    statement: "제공자·모델·인증 참조·비용/한도를 확인한다"
    category: "authorization"
    applies_to: ["ServiceConnection","EvaluationRequest"]
    trigger: "LLM 등록·연결 시험"
    logic: "IF 적격 endpoint/model/profile와 보호 인증 참조·실제 지원 기능·양의 유한 토큰/시간/바이트/호출 예산·유료 사용 조건을 확인해야 요청한다. 원격 초기 검증 대상 OpenAI API, store=false이며 실제 시험 전 성공을 주장하지 않는다."
    violation: "DEPENDENCY_UNQUALIFIED/RESOURCE_LIMIT; 미선정 모델 호출 0건"
    source: ["FR8.1"]
  - id: BR8.2
    statement: "원격과 로컬/사설 유형은 각각 실제 호환성 증거가 필요하다"
    category: "policy"
    applies_to: ["ServiceConnection","EvaluationRequest"]
    trigger: "프로필 적격성 판정"
    logic: "IF 비스트리밍 Chat Completions·선택 모델의 토큰 한도 필드 하나·LLM_REQUEST/RESPONSE/EVALUATION·오류 처리·처리 위치/보존/비용을 실제 확인해야 해당 유형을 적격으로 삼는다. 로컬/사설은 실제 제공자/API/인증/하드웨어/원격 우회 없음이 필요하고 Ollama는 제외한다. 원격만으로 두 유형 완료를 주장하지 않는다."
    violation: "PROVIDER_UNSELECTED/UNQUALIFIED 기능 비활성; 자동 원격 우회 금지"
    source: ["FR8.2"]
  - id: BR8.3
    statement: "평가·실적 분석·조정안은 승인/계획 변경과 분리한다"
    category: "policy"
    applies_to: ["EvaluationRequest","EvaluationResult"]
    trigger: "평가 요청/응답"
    logic: "IF 평가를 수행하면 같은 검증 계획/허용 분석 자료/기간·출처를 요청과 결합한다. 적정성·진행 실적 해석·조정안은 findings/proposedAdjustments에 보존하며 새 승인 없이 계획·일정에 적용하지 않는다."
    violation: "결과를 자동 승인/계획 개정으로 적용 금지"
    source: ["FR8.3"]
  - id: BR8.4
    statement: "모델 결과의 구조·digest·근거·수치를 다시 검사한다"
    category: "validation"
    applies_to: ["EvaluationResult"]
    trigger: "LLM 응답 수신"
    logic: "IF finish_reason=stop, refusal 없음, tool_calls 비어 있음, content 엄격 JSON 및 EVALUATION schema 통과, evaluatedDigest 일치, evidenceRefs가 허용 입력에 존재하고 수치/주장이 원천·계산 정의와 일치해야 VALID다. 자료 부족은 한계로 표시하고 진단/근거 없는 심박·기록·확률을 채택하지 않는다."
    violation: "LLM_INVALID; 불신 내용/명령 실행 및 사실 승격 금지"
    source: ["FR8.4"]
  - id: BR8.5
    statement: "평가 실패 예외는 변경 없는 기존 검증 스냅샷에만 적용한다"
    category: "policy"
    applies_to: ["EvaluationResult","AdmissionAssessment","PublicationIntent"]
    trigger: "평가 호출 실패 후 게시 판단"
    logic: "IF 명시적으로 확인된 CALL_FAILED이고 해당 정확한 digest에 현재 사용자 승인·형식·안전·정책·계보 검증이 모두 통과하며 미해소 경고가 없으면 PlanAdmission이 실패 고지와 ELIGIBLE_WITH_EVALUATION_FAILURE를 새로 판정할 수 있다. 오류 결과/INVALID/미확인을 CALL_FAILED로 위장하지 않고 오류 평가 내용/제안을 반영하지 않는다."
    violation: "승인/안전 실패·미승인 수정/새 모델 우회는 BLOCKED; 실패를 평가 성공으로 표시 금지"
    source: ["FR8.5"]
  - id: BR8.6
    statement: "실패·늦은 평가 응답은 원본과 현재 계획을 보존한다"
    category: "policy"
    applies_to: ["EvaluationRequest","EvaluationResult","AdmittedPlanSnapshot"]
    trigger: "타임아웃·429·오프라인·늦은 응답"
    logic: "IF 평가 실패/미완료면 원 계획·분석과 요청 계보를 유지하고 유한 예산 안에서 동일 제공자 재시도한다. 사용량/응답 불명은 OUTCOME_UNKNOWN으로 비용/결과 대조 후 결정한다. 늦은 응답은 원 요청에만 연결하고 현재 버전을 자동 변경하지 않는다."
    violation: "무한/중복 호출·예약 재개로 예산 초기화·제공자 자동 변경 금지"
    source: ["FR8.6"]
  - id: BR8.7
    statement: "제공자별 허용 입력과 문맥 한도를 적용한다"
    category: "authorization"
    applies_to: ["SharingConsent","EvaluationRequest"]
    trigger: "LLM 요청 생성"
    logic: "IF PLAN_EVALUATION 목적의 현재 동의와 분석 자료에 필요한 모든 실제 경로 grant가 확인돼야 입력을 만든다. 비밀/민감/숨긴 원천 수치는 설명/근거에도 포함하지 않는다. 문맥 초과는 허용 분할 및 불완전성 명시 또는 명시 실패이며 조용한 잘림/대체 제공자 전송은 금지한다."
    violation: "PERMISSION_DENIED/RESOURCE_LIMIT; 미동의 대체 제공자 0건"
    source: ["FR8.7"]
  - id: BR9.1
    statement: "선택 캘린더 권한을 각 요청 전 확인한다"
    category: "authorization"
    applies_to: ["ServiceConnection","PublicationIntent"]
    trigger: "연결·게시/복구"
    logic: "IF 계정/대상·필요 최소 권한·철회/현재성이 확인돼야 효과 요청한다. 잘못된 대상/거절/철회면 새 효과를 중단하고 승인 원본·시도를 보존한다. 다른 생활 일정 읽기를 초기 필수 권한으로 요구하지 않는다."
    violation: "PERMISSION_DENIED/DEPENDENCY_UNQUALIFIED"
    source: ["FR9.1"]
  - id: BR9.2
    statement: "시각 정책과 미래 여부를 검증한 세션만 신규 생성한다"
    category: "policy"
    applies_to: ["PublicationIntent","AdmissionAssessment"]
    trigger: "승인 계획 주기 게시"
    logic: "IF 현재 승인 C05/C04와 timingPolicy가 같고 localTime이 있으면 우선 적용, null이면 결합된 defaultLocalTime을 쓴다. IANA/tzdb에서 단일 시작 순간을 해석하고 신뢰된 현재 시각보다 엄격히 미래일 때만 CREATE 후보로 삼는다. 시작<=현재인 실제 미생성 세션은 SKIPPED_PAST이며 시각 이동 없이 사유/범위를 남긴다. 미확인 외부 효과는 먼저 대조한다."
    violation: "시각/현재성 불명이면 BLOCKED; 과거 생성/자동 재배치 금지"
    source: ["FR9.2"]
  - id: BR9.3
    statement: "일정은 승인 세션과 허용 투영에 일치해야 한다"
    category: "validation"
    applies_to: ["PublicationIntent","CalendarBinding"]
    trigger: "이벤트 투영"
    logic: "IF 종목·현지 시각/시간대·예상 시간·목적·거리/시간·강도·준비/본/정리 내용이 승인 원본과 일치하고 목적별 필수 업무 묶음 공유가 허용돼야 이벤트를 만든다. 종료는 예상 duration의 실제 경과 초를 시작 순간에 더한다. reminders.useDefault=true이며 참석자/GPS/FIT/건강 원천/비밀은 넣지 않는다. DST 중복/부재는 자동 추정하지 않는다."
    violation: "DATA_INVALID/PERMISSION_DENIED; 승인 내용 임의 가림으로 같은 승인 사용 금지"
    source: ["FR9.3"]
  - id: BR9.4
    statement: "고정 이벤트 ID·원 의도·연결로 중복/응답 유실을 대조한다"
    category: "constraint"
    applies_to: ["PublicationIntent","CalendarBinding","DeliveryAttempt"]
    trigger: "CREATE/재시도/409"
    logic: "IF subjectRef/calendarAlias/planId/sessionId에 P03 고정 eventId를 계산해 로컬 의도/연결/기대 내용을 먼저 확정한다. 응답 유실·409는 같은 ID GET 후 원 의도와 기대 내용/소유 계보 대조를 수행한다. 일치만 성공, 다른 내용은 충돌, 조회 실패는 미확인이다. 실제 미존재 확인 후에만 현재 미래 정책으로 CREATE를 재판정한다."
    violation: "불명 결과를 미게시/미존재로 단정해 새 ID 생성 금지"
    source: ["FR9.4"]
  - id: BR9.5
    statement: "승인된 미래 일정 영향만 조건부 변경/취소한다"
    category: "authorization"
    applies_to: ["AdmittedPlanDisposition","PublicationIntent","CalendarBinding"]
    trigger: "개정/취소 처리"
    logic: "IF 검증 처분과 정확한 현재 계보가 확인되고 해당 연결 세션/이벤트가 신뢰된 현재 시각보다 미래이며 확인된 영향 범위에 포함되면 GET/If-Match로 UPDATE/CANCEL한다. 변경 없는 세션은 유지하고 과거 이벤트/완료 실적/다른 일정을 보존한다."
    violation: "범위/미래/권한 불명·시각 경과는 보류/범위 제외 명시; 무단 삭제 금지"
    source: ["FR9.5"]
  - id: BR9.6
    statement: "사용자 수정/조건부 충돌은 덮어쓰지 않는다"
    category: "validation"
    applies_to: ["CalendarConflict","CalendarBinding","DeliveryAttempt"]
    trigger: "GET 대조·412·원격 삭제"
    logic: "IF 마지막 확정 내용/개정과 최신 이벤트가 다르거나 GET/소유 연결을 신뢰할 수 없으면 CONFLICT 또는 OUTCOME_UNKNOWN으로 보류한다. 최신 etag를 받아 무조건 재시도하지 않으며 양쪽 변경/삭제 상태를 보존하고 해결 확인을 요구한다."
    violation: "REMOTE_CONFLICT/OUTCOME_UNKNOWN; 이름/marker만으로 소유 추정 금지"
    source: ["FR9.6"]
  - id: BR9.7
    statement: "부분 성공·미확인·과거 건너뜀을 성공과 구별한다"
    category: "policy"
    applies_to: ["DeliveryAttempt","PublicationIntent","ExecutionRecord"]
    trigger: "세션별 결과/복구"
    logic: "IF 일부 성공하고 다른 세션 실패/보류/skip/미확인이면 전체 요청 범위는 PARTIAL이다. 성공이 하나도 없고 skip만이면 C08 BLOCKED와 DATA_INVALID·고정 한국어 정책 사유를 사용하며 wire SKIPPED를 추가하지 않는다. 원 요청 효과 대상이 1개 이상이고 모든 대상 세션이 실제 확인 성공일 때만 전체 SUCCESS다. 효과 대상 0개는 BLOCKED와 적용 가능한 미래 세션 없음의 사유를 남긴다. 세션별 성공 유지·실패만 복구하며 미확인은 먼저 대조한다."
    violation: "과거 제외 범위를 조용히 성공 분모에서 제거 금지; 원본 계획 보존"
    source: ["FR9.7"]
  - id: BR10.1
    statement: "C03 분할은 등록 Detail·계보·개수·범위를 검증한다"
    category: "validation"
    applies_to: ["AnalysisSnapshot","RepositoryPublication"]
    trigger: "PARTITIONED 생성·대조"
    logic: "IF PARTITIONED면 activities=[]이고 N>=1, partIndex=0..N-1 각 1회, descriptor 정렬/참조 유일, partCount=N, 각 본문/descriptor 개수 일치 및 합=expectedActivityCount다. 모든 루트/Detail의 snapshotId/sourceSnapshotRef/subjectRef/projection/rootPeriod를 대조한다. 각 기간은 root 내, 같은 시간대이며 운동 날짜가 포함돼야 한다. Detail 하위/임의 URL 참조를 금지하고 Detail 선게시/재읽기 후 루트를 마지막 게시한다."
    violation: "계보/중복/범위/합 불일치는 DATA_INVALID; 미도착/읽기 실패/digest 불명은 SOURCE_INCOMPLETE/PARTIAL"
    source: ["FR4.3","FR4.4","FR4.9"]
  - id: BR10.2
    statement: "C03 요약 상태와 정렬은 공통 의미 규칙을 따른다"
    category: "calculation"
    applies_to: ["AnalysisSnapshot"]
    trigger: "manifest/detail 생성·검사"
    logic: "IF 활동이면 (startedAt UTC 순간,activityId Unicode code point) 정렬하고 스냅샷 전체 activityId 유일을 요구한다. summary.totals 허용 시 종목별 활동 수를 대조하고 m/s Decimal 합계를 계산한다. 비공개는 withheld, 공개 입력 missing 우선, 그 외 not_collected, not_applicable 제외/전부 해당 없음, 수치에 estimated 있으면 estimated, 그 외 computed 순서를 따른다. 상세 전부 확인 전 합계 확정 금지."
    violation: "NaN/이중 합산/부분을 전체로 표시 금지"
    source: ["FR4.6","FR4.7","FR4.8"]
  - id: BR10.3
    statement: "기본 메타데이터 묶음과 파생 유출을 확인한다"
    category: "authorization"
    applies_to: ["SharingConsent","AnalysisSnapshot"]
    trigger: "C03 투영/동의 설정"
    logic: "IF analysis.metadata/summary.period/activity.date/activity.sport 중 하나라도 미허용이면 전체 C03 신규 전송을 보류한다. 개수/불투명 계보/정확 시각 공개를 동의 시 알린다. 미허용 metric은 state=withheld 및 quantity/sourceRef/calculationBasis=null이고 고정 슬롯을 생략하지 않는다. pace/speed는 intensity+distance+duration 모두 허용, heartRate는 별도 허용이 필요하다. summary.totals만으로 개별 값 권한을 확대하지 않는다. 미등록 민감 필드는 별도 동의가 있어도 extensions로 전송하지 않는다."
    violation: "PERMISSION_DENIED; 숨긴 값/원천을 요약/설명/오류에 옮기지 않음"
    source: ["FR4.10","FR8.7"]
  - id: BR10.4
    statement: "엄격 파싱과 고정 명세 전체 digest를 적용한다"
    category: "validation"
    applies_to: ["ReceivedPlanArtifact","AnalysisSnapshot","EvaluationResult"]
    trigger: "모든 경계 JSON"
    logic: "IF UTF-8 선두 단일 BOM/바깥 공백·CRLF면 파싱 허용하되 문자열 의미는 보존한다. 중복 키/잘림/후행 문서/NaN/Infinity/잘못된 UTF-8/루트 비객체는 거절한다. registry 1.0.0/전체 JCS·schema/fixtures digest를 대조한다. 알 수 없는 필수/권한 필드는 거절하고 등록 extension은 권한에 사용하지 않되 digest에 포함한다."
    violation: "DATA_INVALID/VERSION_UNSUPPORTED/CONTENT_MISMATCH/RESOURCE_LIMIT"
    source: ["FR7.4","FR7.9","FR4.5"]
```

## 규칙 요약

| 규칙 | 기능 | 적용 |
|---|---|---|
| BR1.1 | 설치/초기화/제거는 데이터 삭제와 분리한다 | FR1.1 |
| BR1.2 | 설정 후보 전체 검증 후 유효본을 교체한다 | FR1.2 |
| BR1.3 | 예약 등록 완료와 실제 로그아웃 실행 검증은 구별한다 | FR1.3 |
| BR1.4 | 수집/동기화와 계획 확인 주기는 독립 관리한다 | FR1.4 |
| BR1.5 | 즉시 실행도 동일 중복/현재성 조건을 따른다 | FR1.5 |
| BR1.6 | 중복 실행 배제와 도메인 멱등성을 함께 유지한다 | FR1.6 |
| BR1.7 | 복귀는 마지막 확정 지점과 미완료를 재검사한다 | FR1.7 |
| BR1.8 | CLI는 한국어 텍스트·결과·복구 조치를 제공한다 | FR1.8 |
| BR2.1 | Garmin 상세 계약/권한 확인 전 수집을 활성화하지 않는다 | FR2.1 |
| BR2.2 | 전체 목록 페이지와 각 상세의 확정 범위를 분리한다 | FR2.2 |
| BR2.3 | 최초/신규/수정/늦은 수정의 근거를 보존한다 | FR2.3 |
| BR2.4 | 원천 연결과 불투명 ID로 유일 운동을 유지한다 | FR2.4 |
| BR2.5 | 확인 원천 수정과 게시 사본 충돌을 분리한다 | FR2.5 |
| BR2.6 | 지원 종목/지표와 미상 상태를 유지한다 | FR2.6 |
| BR2.7 | 측정값·단위·원천·수집시각 및 변환 근거를 보존한다 | FR2.7 |
| BR2.8 | 외부/항목 오류는 한정 복구한다 | FR2.8 |
| BR2.9 | 미제공/미수집/해당 없음/실제 0/추정을 혼동하지 않는다 | FR2.9 |
| BR3.1 | GitHub와 Drive 연결/권한 시험을 독립한다 | FR3.1 |
| BR3.2 | 활성 분석 대상만 전송한다 | FR3.2 |
| BR3.3 | 외부 효과 전 로컬 유효본과 의도를 확정한다 | FR3.3 |
| BR3.4 | 대상별 성공·실패·대기·미확인을 집계한다 | FR3.4 |
| BR3.5 | 실패 대상만 복구하고 타 대상 성공을 유지한다 | FR3.5 |
| BR3.6 | 응답 유실은 고정 대상/내용 대조가 먼저다 | FR3.6 |
| BR3.7 | 원격 사본 충돌·보존·삭제 영향은 명시 확인한다 | FR3.7 |
| BR3.8 | 비공개/허용 대상 확인 후 게시한다 | FR3.8 |
| BR3.9 | 생성·원천 수집·갱신·마지막 성공 게시 시각을 구별한다 | FR3.9 |
| BR4.1 | 최신 상태/상세/기간 탐색을 허용 고정 참조로 제공한다 | FR4.1 |
| BR4.2 | 기간은 시간대의 시작 포함·끝 제외로 계산한다 | FR4.2 |
| BR4.3 | 구조화 상세와 계산 정의로 재계산 가능하게 한다 | FR4.3 |
| BR4.4 | 상세 개정과 영향 요약의 계보를 고정한다 | FR4.4 |
| BR4.5 | 범위·시각·단위·출처·명세를 함께 식별한다 | FR4.5 |
| BR4.6 | 분모 0과 비수치 상태는 유효 성과가 아니다 | FR4.6 |
| BR4.7 | 종목별 유일 집합으로 계산한다 | FR4.7 |
| BR4.8 | 정확 계산 뒤 표시 반올림과 차이를 설명한다 | FR4.8 |
| BR4.9 | 원천 완전성과 전달 완전성/최신성을 분리한다 | FR4.9 |
| BR4.10 | 모든 실제 전송 경로를 같은 현재 정책으로 검사한다 | FR4.10 |
| BR5.8 | 외부 승인 선언은 독립 검증 전 권한이 아니다 | FR5.8 |
| BR5.11 | Drive 주기 수신은 로컬 직접 호출 없이 수행한다 | FR5.11 |
| BR6.2 | 필수 계획/세션이 모두 유효해야 전체를 채택한다 | FR6.2 |
| BR6.5 | 안전 근거·적용조건·한계가 미해소면 적격 판정을 내리지 않는다 | FR6.5 |
| BR6.8 | 작성·승인·저장·수신·평가·게시 결과를 분리한다 | FR6.8 |
| BR6.10 | 새 내용과 개정은 새 승인 및 확정 계보를 요구한다 | FR6.10 |
| BR6.11 | 계획 개정/취소가 실제 운동을 변경하지 않는다 | FR6.11 |
| BR6.12 | 완전한 같은 버전만 검증한다 | FR6.12 |
| BR7.2 | 계획 확인 실패를 최신 확인으로 처리하지 않는다 | FR7.2 |
| BR7.3 | 내용·계보·ID와 원격 저장 위치를 각각 대조한다 | FR7.3 |
| BR7.4 | 형식·참조·허용 행위·승인·현재성을 모두 검사한다 | FR7.4 |
| BR7.5 | 반복 조회/재개는 영속 결과를 재사용한다 | FR7.5 |
| BR7.6 | 계획별 단계와 세션별 결과를 보존한다 | FR7.6 |
| BR7.7 | 검사 후 변경과 동시 수정은 재검증/보류한다 | FR7.7 |
| BR7.8 | 폐기/교체/취소는 승인된 미래 영향만 처리한다 | FR7.8 |
| BR7.9 | 외부 자료는 권한을 부여하지 않는 데이터다 | FR7.9 |
| BR8.1 | 제공자·모델·인증 참조·비용/한도를 확인한다 | FR8.1 |
| BR8.2 | 원격과 로컬/사설 유형은 각각 실제 호환성 증거가 필요하다 | FR8.2 |
| BR8.3 | 평가·실적 분석·조정안은 승인/계획 변경과 분리한다 | FR8.3 |
| BR8.4 | 모델 결과의 구조·digest·근거·수치를 다시 검사한다 | FR8.4 |
| BR8.5 | 평가 실패 예외는 변경 없는 기존 검증 스냅샷에만 적용한다 | FR8.5 |
| BR8.6 | 실패·늦은 평가 응답은 원본과 현재 계획을 보존한다 | FR8.6 |
| BR8.7 | 제공자별 허용 입력과 문맥 한도를 적용한다 | FR8.7 |
| BR9.1 | 선택 캘린더 권한을 각 요청 전 확인한다 | FR9.1 |
| BR9.2 | 시각 정책과 미래 여부를 검증한 세션만 신규 생성한다 | FR9.2 |
| BR9.3 | 일정은 승인 세션과 허용 투영에 일치해야 한다 | FR9.3 |
| BR9.4 | 고정 이벤트 ID·원 의도·연결로 중복/응답 유실을 대조한다 | FR9.4 |
| BR9.5 | 승인된 미래 일정 영향만 조건부 변경/취소한다 | FR9.5 |
| BR9.6 | 사용자 수정/조건부 충돌은 덮어쓰지 않는다 | FR9.6 |
| BR9.7 | 부분 성공·미확인·과거 건너뜀을 성공과 구별한다 | FR9.7 |
| BR10.1 | C03 분할은 등록 Detail·계보·개수·범위를 검증한다 | FR4.3·FR4.4·FR4.9 |
| BR10.2 | C03 요약 상태와 정렬은 공통 의미 규칙을 따른다 | FR4.6·FR4.7·FR4.8 |
| BR10.3 | 기본 메타데이터 묶음과 파생 유출을 확인한다 | FR4.10·FR8.7 |
| BR10.4 | 엄격 파싱과 고정 명세 전체 digest를 적용한다 | FR7.4·FR7.9·FR4.5 |

FR별 U2의 실행 책임을 모두 연결한다. 공유 FR에서 U1은 교환 규범, U3는 작성·승인 의사/저장 경험을 소유하며 이 규칙이 상대 단위의 실제 완료를 대신하지 않는다. NFR1~NFR11의 비밀·권한·동의·무결성·시각·오류·복구·비진단·추적·증거 구분을 공통 적용한다. 상세 기술/수치 목표는 후속 NFR 설계의 책임이다.

