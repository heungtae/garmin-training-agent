# U2 Linux 에이전트 데이터 모델

근거: [단위](../../../inception/units-generation/unit-of-work.md), [배정](../../../inception/units-generation/unit-of-work-story-map.md), [요구사항](../../../inception/requirements-analysis/requirements.md), [소유 컴포넌트](../../../inception/domain-design/components.md), [공유 계약](../../../inception/contract-design/contract-summary.md), [확인 답변](functional-design-questions.md).

아래 YAML이 논리 데이터 형식·소유·제약·관계의 기준이다. 흐름과 전이는 [functional-spec.md](functional-spec.md), 판단 규칙은 [rules.md](rules.md)를 따른다. 원 소유 엔티티 25개를 유지하며 값 객체는 새 소유 엔티티가 아니다. 물리 DB·저장 형식·보호 기술은 선정하지 않는다.

```yaml
unit: u2-linux-agent
schema_version: '1.0.0'
attribute_convention: '모든 열거 속성은 존재해야 한다. nullable=true만 null 허용. unique=false는 별도 유일성 없음. Set은 중복 금지, List는 순서 보존, 두 컬렉션은 별도 최소 조건이 없으면 빈 값 허용. 참조는 식별자/정확한 개정 참조이고 소유권 이전·연쇄 삭제가 아니다.'
value_types:
  Id: "공통 Id: 1~1024자 불투명 문자열; 원천 ID는 자르거나 대소문자/선행 0/Unicode 정규화하지 않음"
  Timestamp: "UTC Z의 유효 date-time; 미실행/미확정은 명시 null"
  OffsetTimestamp: "유효 오프셋 포함 원천 date-time; 원문 보존 및 UTC 순간 대조"
  Timezone: "실제 IANA 시간대; tzdbVersion을 TimingPolicy/검증 문맥과 결합"
  Duration: "양수 논리 기간; 미정 값으로 무한 실행/삭제 금지; 지원 범위는 NFR 프로필"
  Digest: "sha256: 및 소문자 64자리; 전체 JSON RFC8785 JCS"
  Period: "Common.Period: startInclusive/endExclusive/timezone; 시작<끝"
  Metric: "Common.Metric: state=observed/computed/estimated/missing/not_collected/not_applicable/withheld; quantity는 값 상태에만; observed는 sourceRef, computed는 sourceRef+calculationBasis, estimated는 calculationBasis; withheld는 세 필드 모두 null"
  Quantity: "음수 아닌 십진 문자열+등록 단위 m, s, m/s, s/km, bpm, rpe, ratio, count; GTA-NUMERIC-1의 원천/정확 합계 30+18자리·유리수 중간값 256자리·속도/페이스 최종 6자리 HALF_EVEN·wire 정규형과 정확 대조; NaN/Infinity 금지"
  AnalysisTargetSelection: "{storageConnectionId:Id, finalReaderConnectionIds:Set<Id>}; storage는 등록된 github/drive DIRECT_SERVICE 하나, reader는 등록된 chatgpt FINAL_READER 1개 이상. 모든 참조는 RuntimeConfiguration.connectionIds 안에 존재하며 실제 허용 도구 경로의 독자를 빠짐없이 표현한다. storageConnectionId별 유일하며 연결 존재/동의만으로 선택을 생성하지 않음"
  TimingPolicy: "Common.TimingPolicy 전체: policyId/policyRevision/calendarAlias/timezone/defaultLocalTime/tzdbVersion; 시간대·시각·대상 변경은 승인 영향 재검증"
  ArtifactRef: "Common.ArtifactRef 전체: storeAlias/objectId/versionRef/digest; 허용 별칭만, raw URL/경로 추적 금지"
  ActivityRevisionRef: "activityId+sourceRevision의 필수 쌍; 정확한 과거 개정까지 조회 가능. 단일 ID가 현재 개정으로 바뀌어도 참조 근거 불변"
  PlanVersionRef: "subjectRef/planId/versionId/digest, exact C05 연결; 외부 작성 엔티티는 U3 소유"
  SessionRef: "PlanVersionRef+sessionId/sessionVersionId; 세션 ID는 해당 계획 내 유일"
  PlanPayload: "등록 C05 1.0.0 전체; goalSnapshot/sessionSnapshots와 정확히 일치하며 변경 불가"
  GoalSnapshot: "C05 goal 전체. targetDistance는 m, targetTime은 s 또는 null; goalId/goalRevision/objective/targetDate/availability/weeklyFrequency/fixedActivities/constraints 필수"
  SessionSnapshot: "C05 session 전체. date/localTime(nullable)/sport=running/expectedDuration>0 s/expectedDistance>=0 m 또는 null/intensity/instructions 필수"
  Impact: "대상 계획/버전/digest·소유자·로컬/원격 효과·세션 집합·행위·사용자 확인 근거; C07 scope+sessionIds 의미 유지"
  VerificationResult: "Common 내부 전용 형식 전체; VERIFIED/UNQUALIFIED/REJECTED/UNAVAILABLE; VERIFIED의 사용자/내용/정책/행위/issuer/record/currentness/humanIntentBound/revocation=CLEAR 필수"
  VerificationEvidence: "적격 검증 프로필+검증 레코드·실제 사용자/내용/목적/대상/현재성/철회"
  QualificationEvidence: "프로필/버전/관측시각·합성 또는 실제 증거 유형·지원/차단 범위; 실제 권한과 명세 적격 구별"
  PermissionEvidence: "요청 권한/확인 권한·targetPrivate=true/false/UNKNOWN·관측시각·철회/현재성"
  ProtectedReference: "비밀 자체가 아닌 내부 보호 참조; 로컬 루트·소유자 검사, 외부 교환/진단 금지"
  WorkRef: "owner/workId/objectId/versionRef/state/observedAt/lastSuccessfulAt/errorRef; 다른 owner 결과를 대리 발급 금지"
  PendingRange: "period/activityRef/stage/reason; 성공하지 않은 항목/범위는 보존"
  CursorPosition: "공식 원천 페이지/변경 커서+로컬 확정 참조; P05 미해소 시 값/알고리즘 발명 금지"
  SportSummary: "C03 SummaryBySport: sport/activityCount/distance/duration; 유일 운동 집합·단위·상태 일치"
  AnalysisData: "C03 registry의 Activity/Detail/DetailRef와 manifest; 전송/원천 완전성 구별"
  SourceMetadata: "원천 연결/개정·수집시각·기준시각·누락기간·계산/반올림 정의·schemaVersion"
  AnalysisProjection: "Common.AnalysisProjection 전체; service/purpose=ANALYSIS/targetAlias/policyDigest/정렬 allowedFieldPaths"
  ValidationPolicyRef: "규칙집 ID/버전/digest·각 규칙의 근거/적용조건/단위/한계·미설정 차단; 의학적 수치를 발명하지 않음"
  CheckContext: "검증 프로필/사용자·전체 내용/승인/계보/철회·정책·Drive 개정·원천 개정·trustedNow·안전·평가 근거와 확인 시각; 외부 원자성 아님"
  EvaluationContext: "snapshot digest/analysis 개정·model/profile·consent/policyDigest·Limits 및 비용 예산·실제 처리 위치 증거"
  EffectContext: "snapshot/session/effect/target·expectedDigest·trustedNow+시각 증거·interpretedStart/end·최종 assessment·권한/정책 확인·처분 참조·skipReason/skipScope(nullable)"
  Finding: "EVALUATION.findings: severity INFO/WARNING/BLOCKER, ruleRef nullable, evidenceRefs[], explanation; evidence는 허용 입력과 일치"
  Error: "Common.Error 전체 고정 code/retryable/message/workRef/observedAt/fieldPath/suggestedAction; 오류 원문/비밀/건강 수치 echo 금지"
  FieldPath: "C04 allowedFieldPaths/sensitiveFieldPaths 등록 enum만; 미등록 민감 자료 전송 없음"
  MetricName: "원천 계약에서 등록된 종목별 이름; C03은 distance/duration/pace/speed/heartRate 고정 슬롯"
  Action: "PUBLISH_PLAN|REPLACE_PLAN|WITHDRAW_PLAN|CANCEL_PUBLICATION|SHARE_DATA"
  Text: "한국어 자유 서술; 비밀/민감자료 제외·터미널 제어/명령 실행 금지; 유한 길이는 NFR 한도"
  Enum: "각 속성 allowed_values 또는 명시 제약의 닫힌 집합; 문서/로컬 값과 wire enum을 구별"
entities:
  - name: RuntimeConfiguration
    owner: OperationControl
    description: "검증된 유효 운영 설정"
    identifier: configurationId
    attributes:
      - {"name":"configurationId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"timezone","type":"Timezone","required":true,"nullable":false,"unique":false,"references":null,"constraints":"실제 IANA 식별자"}
      - {"name":"collectionScope","type":"Set<Id>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용 종목/지표만; 비지원은 수집 설정 활성화 불가"}
      - {"name":"initialCollectionPeriod","type":"Period","required":true,"nullable":false,"unique":false,"references":null,"constraints":"startInclusive < endExclusive"}
      - {"name":"collectionInterval","type":"Duration","required":true,"nullable":false,"unique":false,"references":null,"constraints":"양수; 기본 PT1H; NFR 실행 프로필 지원 범위"}
      - {"name":"planCheckInterval","type":"Duration","required":true,"nullable":false,"unique":false,"references":null,"constraints":"양수; 기본 PT15M; 독립 변경"}
      - {"name":"connectionIds","type":"Set<Id>","required":true,"nullable":false,"unique":false,"references":"ServiceConnection","constraints":"등록 연결 목록이며 목적별 활성 선택/전송 동의를 뜻하지 않음; 삭제 연쇄 없음"}
      - {"name":"analysisTargets","type":"Set<AnalysisTargetSelection>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"목적=ANALYSIS의 명시적 활성 선택. 빈 집합은 로컬 보존·분석 외부 미게시. 저장소별 유일, 미등록/역할 불일치/독자 누락은 설정 거절"}
      - {"name":"planInboxConnectionId","type":"Id","required":true,"nullable":true,"unique":false,"references":"ServiceConnection","constraints":"계획 수신 전용 drive DIRECT_SERVICE 선택. null이면 PLAN_CHECK 수신 보류; analysisTargets 변경으로 자동 해제/선택하지 않음"}
      - {"name":"calendarDefaults","type":"TimingPolicy","required":true,"nullable":false,"unique":false,"references":null,"constraints":"승인 C05 및 현재 C04와 동일; 기본 시각 미설정 시 게시 보류"}
      - {"name":"configurationRevision","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"검증된 변경마다 새 개정; 동시 갱신은 기대 개정 대조"}
      - {"name":"installationState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"설치 상태는 예약/외부 성공을 의미하지 않음","allowed_values":["INITIALIZED","READY","REMOVING","REMOVED"]}
    constraints: ["한 사용자/한 PC의 활성 설정은 하나","무효 후보는 유효본을 대체하지 않음"]
    relationships:
      - {"field":"connectionIds","target":"ServiceConnection","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..*","kind":"many_to_many"}
      - {"field":"analysisTargets","target":"ServiceConnection","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..*","kind":"many_to_many"}
      - {"field":"planInboxConnectionId","target":"ServiceConnection","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
  - name: ScheduleRegistration
    owner: OperationControl
    description: "목적별 예약 등록과 독립 중단/재개"
    identifier: scheduleId
    attributes:
      - {"name":"scheduleId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"configurationId","type":"Id","required":true,"nullable":false,"unique":false,"references":"RuntimeConfiguration","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"jobPurpose","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["COLLECTION_SYNC","PLAN_CHECK"]}
      - {"name":"registeredAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"lastTriggeredAt","type":"Timestamp","required":true,"nullable":true,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"nextPlannedAt","type":"Timestamp","required":true,"nullable":true,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"scheduleState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["PENDING","ACTIVE","PAUSED","FAILED","REMOVED"]}
      - {"name":"configurationRevision","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"등록에 적용된 유효 설정 개정"}
    constraints: ["configurationId+jobPurpose별 활성 등록 최대 하나","PAUSED/REMOVED는 nextPlannedAt=null; 미등록은 실행 성공 아님"]
    relationships:
      - {"field":"configurationId","target":"RuntimeConfiguration","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: ExecutionRecord
    owner: OperationControl
    description: "예약·즉시·복구 실행 및 소유자별 결과 집계"
    identifier: executionId
    attributes:
      - {"name":"executionId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"scheduleId","type":"Id","required":true,"nullable":true,"unique":false,"references":"ScheduleRegistration","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"triggerSource","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["SCHEDULED","IMMEDIATE","RECOVERY","MAINTENANCE"]}
      - {"name":"startedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"finishedAt","type":"Timestamp","required":true,"nullable":true,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"childWorkRefs","type":"List<WorkRef>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"소유 컴포넌트·작업/버전·현재 결과·마지막 성공·오류 참조"}
      - {"name":"executionOutcome","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["RUNNING","SUCCESS","PARTIAL","FAILED","BLOCKED","OUTCOME_UNKNOWN","DUPLICATE_SUPPRESSED","INTERRUPTED"]}
      - {"name":"recoveryHint","type":"Text","required":true,"nullable":true,"unique":false,"references":null,"constraints":"미완료 작업·원인·다음 조치; 비밀/원문 없음"}
      - {"name":"workKey","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"사용자+PC+jobPurpose의 중복 실행 배제 범위"}
    constraints: ["finishedAt은 종료 결과 때만 값","하위 일부 실패/미확인을 전체 SUCCESS로 집계 금지"]
    relationships:
      - {"field":"scheduleId","target":"ScheduleRegistration","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
  - name: MaintenanceRequest
    owner: OperationControl
    description: "제거·삭제·보존 정리의 확인된 영향 요청"
    identifier: maintenanceRequestId
    attributes:
      - {"name":"maintenanceRequestId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"requestedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"requestPurpose","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["UNINSTALL","DELETE_DATA","RETENTION_CLEANUP","PLAN_DISPOSITION"]}
      - {"name":"affectedObjectRefs","type":"Set<WorkRef>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"소유자와 로컬/원격/일정 범위 구별"}
      - {"name":"confirmedImpact","type":"Impact","required":true,"nullable":true,"unique":false,"references":null,"constraints":"동일 범위에 사용자 확인 근거; 미확인은 null"}
      - {"name":"ownerOutcomes","type":"List<WorkRef>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"소유자별 대기/성공/실패/미확인; 제거와 데이터 삭제 구별"}
    constraints: ["영향 확대 시 기존 확인 재사용 금지; 각 소유자만 자료 변경"]
    relationships: []
  - name: ServiceConnection
    owner: DataAccessPolicy
    description: "서비스·계정·대상별 연결과 실제 권한/적격 증거"
    identifier: connectionId
    attributes:
      - {"name":"connectionId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"serviceName","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"C04 service와 같은 이름으로 대응; chatgpt는 최종 독자 경로만 표현","allowed_values":["garmin","github","drive","chatgpt","calendar","openai","local_private"]}
      - {"name":"connectionRole","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"chatgpt는 FINAL_READER만, 다른 서비스는 DIRECT_SERVICE만. FINAL_READER는 Linux 호출 어댑터/실행 권한이 아님","allowed_values":["DIRECT_SERVICE","FINAL_READER"]}
      - {"name":"accountReference","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"로컬의 불투명 계정 별칭; 직접 식별정보 전송 금지"}
      - {"name":"targetReference","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"선택 저장소/폴더/캘린더 또는 API 대상 별칭"}
      - {"name":"credentialReferenceId","type":"Id","required":true,"nullable":true,"unique":false,"references":"CredentialReference","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"permissionSummary","type":"PermissionEvidence","required":true,"nullable":false,"unique":false,"references":null,"constraints":"요청 권한·관측 권한·비공개 여부·증거 시각·철회/현재성; 미확인은 UNKNOWN"}
      - {"name":"connectionState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["UNCONFIGURED","UNQUALIFIED","READY","DENIED","EXPIRED","REVOKED","UNAVAILABLE"]}
      - {"name":"checkedAt","type":"Timestamp","required":true,"nullable":true,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"endpointReference","type":"Id","required":true,"nullable":true,"unique":false,"references":null,"constraints":"등록된 신뢰 프로필 별칭; 원격 문서가 주소/검증기를 등록하지 못함"}
      - {"name":"modelReference","type":"Id","required":true,"nullable":true,"unique":false,"references":null,"constraints":"LLM에만 필요; 실제 지원 모델은 적격 확인 후 설정"}
      - {"name":"qualificationEvidence","type":"QualificationEvidence","required":true,"nullable":false,"unique":false,"references":null,"constraints":"실제 검증 범위/프로필/버전·처리 위치·비용/한도 참조; 합성 결과와 분리"}
    constraints: ["serviceName+accountReference+targetReference는 유일","활성 설정 안에서 같은 serviceName+targetReference가 다른 계정을 모호하게 가리키면 거절","chatgpt FINAL_READER는 credentialReferenceId/endpointReference/modelReference=null; 실제 독자 계정/도구 경로·주체 대응·현재성 증거 없으면 UNQUALIFIED","READY는 현재 권한과 목적별 적격성 재확인을 생략하지 않음"]
    relationships:
      - {"field":"credentialReferenceId","target":"CredentialReference","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
  - name: CredentialReference
    owner: DataAccessPolicy
    description: "비밀 값이 아닌 보호 보관 참조"
    identifier: credentialReferenceId
    attributes:
      - {"name":"credentialReferenceId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"protectedStoreReference","type":"ProtectedReference","required":true,"nullable":false,"unique":false,"references":null,"constraints":"로컬 내부 전용; C03~C08·로그·상태 출력에 금지"}
      - {"name":"serviceName","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["garmin","github","drive","calendar","openai","local_private"]}
      - {"name":"registeredAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"rotationState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["ACTIVE","ROTATION_REQUIRED","UNAVAILABLE","REVOKED"]}
    constraints: ["값/토큰은 모델 속성이 아님; 보호 기술은 NFR 선정","GARMIN_API_KEY는 참조 이름만 의미"]
    relationships: []
  - name: SharingConsent
    owner: DataAccessPolicy
    description: "서비스·목적·대상별 원 동의와 개정"
    identifier: consentId
    attributes:
      - {"name":"consentId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"connectionId","type":"Id","required":true,"nullable":false,"unique":false,"references":"ServiceConnection","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"purpose","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["ANALYSIS","PLAN_STORAGE","PLAN_EVALUATION","CALENDAR_PUBLICATION"]}
      - {"name":"allowedFields","type":"Set<FieldPath>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"C04 등록 필드만; 민감 별도 명시 동의는 민감 필드 집합으로 구분"}
      - {"name":"excludedFields","type":"Set<FieldPath>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용과 교집합 없음; 비밀은 영구 금지"}
      - {"name":"consentRevision","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"새 동의/철회에 새 개정"}
      - {"name":"confirmedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"withdrawnAt","type":"Timestamp","required":true,"nullable":true,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"policyDigest","type":"Digest","required":true,"nullable":false,"unique":false,"references":null,"constraints":"C04 전체 JCS와 결합"}
      - {"name":"verificationEvidence","type":"VerificationEvidence","required":true,"nullable":false,"unique":false,"references":null,"constraints":"사용자·목적·대상·현재성·철회 검증; 외부 ACTIVE 문자열 불충분"}
    constraints: ["connectionId+purpose별 현재 동의 최대 하나; 연결의 serviceName/purpose/targetReference를 C04 service/purpose/targetAlias로 그대로 대응하고 주체·원 개정·policyDigest를 결합","C04 튜플 grant 유일; Drive 동의와 ChatGPT 최종 독자 동의는 별도 행이며 합치거나 대체하지 않음","철회는 신규 전송 차단이며 기존 복사본 회수 보장 아님"]
    relationships:
      - {"field":"connectionId","target":"ServiceConnection","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: RetentionPolicy
    owner: DataAccessPolicy
    description: "데이터 범위별 보존 및 실제 복구 한계"
    identifier: retentionPolicyId
    attributes:
      - {"name":"retentionPolicyId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"dataScope","type":"Set<WorkRef>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"활동·분석·수신/계획·결과·로컬/원격 구별"}
      - {"name":"retentionPeriod","type":"Duration","required":true,"nullable":true,"unique":false,"references":null,"constraints":"양수 또는 명시적 보존; null은 미설정·자동 삭제 금지"}
      - {"name":"configuredAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"deletionImpactPolicy","type":"Text","required":true,"nullable":false,"unique":false,"references":null,"constraints":"삭제 범위 사전 확인·관계 보존; 미해소 원격 효과 자료 삭제 금지"}
      - {"name":"remoteRecoveryLimit","type":"Text","required":true,"nullable":false,"unique":false,"references":null,"constraints":"검증된 범위 또는 미검증 표시; 복구 가능 보장 금지"}
    constraints: ["dataScope별 활성 정책 유일; 첫 설정에 기간 선택 요구, 미선택 시 자동 삭제 없음"]
    relationships: []
  - name: ActivityRecord
    owner: ActivityCollection
    description: "원천 운동 사실의 유일한 로컬 기록"
    identifier: activityId
    attributes:
      - {"name":"activityId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"sourceActivityId","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"대소문자·선행 0·Unicode 보존"}
      - {"name":"sourceConnectionId","type":"Id","required":true,"nullable":false,"unique":false,"references":"ServiceConnection","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"sport","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["running","swimming","cycling","strength","other","unknown"]}
      - {"name":"startedAt","type":"OffsetTimestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"원 오프셋 보존; 파싱 불가 시 유효 집계에서 제외"}
      - {"name":"sourceTimezone","type":"Timezone","required":true,"nullable":true,"unique":false,"references":null,"constraints":"미제공은 null; 사용자 시간대로 원천 시간대 발명 금지"}
      - {"name":"measurements","type":"Map<MetricName,Metric>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"등록 종목별 지표·단위·출처·원값/변환 근거"}
      - {"name":"sourceRevision","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"확인된 원천 개정; 미지원이면 로컬 내용 개정과 판별 한계 표시"}
      - {"name":"collectedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"completeness","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["COMPLETE","PARTIAL"]}
      - {"name":"sourceRevisionEvidence","type":"Text","required":true,"nullable":false,"unique":false,"references":null,"constraints":"공식 수정 판별 근거 또는 지원 불가 한계"}
    constraints: ["sourceConnectionId+sourceActivityId 유일","원천 확인 수정만 새 개정 반영; 게시 사본 수정/삭제와 구별","분석/승인/미해소 효과가 참조한 과거 개정은 불변 이력으로 보존; 현재 sourceRevision 변경으로 고정 근거를 소실하지 않음"]
    relationships:
      - {"field":"sourceConnectionId","target":"ServiceConnection","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: CollectionCursor
    owner: ActivityCollection
    description: "확정 범위와 미완료/늦은 수정 재검사"
    identifier: collectionCursorId
    attributes:
      - {"name":"collectionCursorId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"sourceConnectionId","type":"Id","required":true,"nullable":false,"unique":false,"references":"ServiceConnection","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"requestedPeriod","type":"Period","required":true,"nullable":false,"unique":false,"references":null,"constraints":"시작 포함/끝 제외"}
      - {"name":"confirmedPosition","type":"CursorPosition","required":true,"nullable":true,"unique":false,"references":null,"constraints":"공식 페이지/수정 판별 계약에 의해 검증된 로컬 확정 지점; 미확정 null"}
      - {"name":"pendingRanges","type":"List<PendingRange>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"기간 또는 활동 ID·단계·사유; 전체 실패면 요청 전체 유지"}
      - {"name":"lastSuccessfulAt","type":"Timestamp","required":true,"nullable":true,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"cursorState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["NEVER_COLLECTED","RUNNING","COMPLETE","PARTIAL","BLOCKED"]}
    constraints: ["성공한 페이지/항목을 로컬 확정한 후만 진행","늦은 수정 확인 범위는 원천 계약 미해소 시 완료 주장 금지"]
    relationships:
      - {"field":"sourceConnectionId","target":"ServiceConnection","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: CollectionIssue
    owner: ActivityCollection
    description: "수집 항목·범위별 오류와 재개"
    identifier: collectionIssueId
    attributes:
      - {"name":"collectionIssueId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"collectionCursorId","type":"Id","required":true,"nullable":false,"unique":false,"references":"CollectionCursor","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"sourceActivityReference","type":"Id","required":true,"nullable":true,"unique":false,"references":null,"constraints":"목록 단계 실패는 null"}
      - {"name":"issueCategory","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["AUTH","PERMISSION","RATE_LIMIT","NETWORK","INVALID_RESPONSE","UNSUPPORTED","INCOMPLETE","LOCAL_STORAGE"]}
      - {"name":"observedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"retryState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["WAITING","READY","REQUIRES_ACTION","EXHAUSTED","RESOLVED"]}
      - {"name":"userAction","type":"Text","required":true,"nullable":false,"unique":false,"references":null,"constraints":"한국어 원인·조치; 본문/비밀 없음"}
    constraints: ["오류는 성공 0건과 구별; 유효 다른 운동은 보존"]
    relationships:
      - {"field":"collectionCursorId","target":"CollectionCursor","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: AnalysisSnapshot
    owner: AnalysisPublication
    description: "한 입력 개정 집합의 불변 분석과 대상별 투영"
    identifier: analysisSnapshotId
    attributes:
      - {"name":"analysisSnapshotId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"activityRevisionReferences","type":"Set<ActivityRevisionRef>","required":true,"nullable":false,"unique":false,"references":"ActivityRecord","constraints":"활동 ID+sourceRevision 집합; 정확한 참조 수치 재계산 근거"}
      - {"name":"period","type":"Period","required":true,"nullable":false,"unique":false,"references":null,"constraints":"최근 7/28/90일 및 주/월/연 범위; 경계 기준시각 포함"}
      - {"name":"timezone","type":"Timezone","required":true,"nullable":false,"unique":false,"references":null,"constraints":"period.timezone과 일치"}
      - {"name":"sportSummaries","type":"List<SportSummary>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"종목별 유일; Decimal 합계·상태 우선순위 적용"}
      - {"name":"structuredData","type":"AnalysisData","required":true,"nullable":false,"unique":false,"references":null,"constraints":"C03 Activity/Detail·manifest; INLINE/PARTITIONED 배타"}
      - {"name":"sourceMetadata","type":"SourceMetadata","required":true,"nullable":false,"unique":false,"references":null,"constraints":"출처·원천 개정·누락·변환/반올림·기준 시각·등록 명세 digest"}
      - {"name":"schemaVersion","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"고정 1.0.0"}
      - {"name":"generatedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"completeness","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["COMPLETE","PARTIAL","EMPTY","NEVER_COLLECTED"]}
      - {"name":"projection","type":"AnalysisProjection","required":true,"nullable":true,"unique":false,"references":null,"constraints":"게시형에만 값; C04 및 모든 실제 경로와 동일"}
      - {"name":"sourceSnapshotRef","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"대상별 투영의 원 분석 계보; 원본은 자기 ID"}
      - {"name":"contentDigest","type":"Digest","required":true,"nullable":false,"unique":false,"references":null,"constraints":"실제 전체 JSON JCS"}
    constraints: ["동일 ID에 다른 내용 금지; 투영 내용/대상/정책 변경은 새 ID/digest","source completeness와 전달 effectiveCompleteness 구별"]
    relationships:
      - {"field":"activityRevisionReferences","target":"ActivityRecord","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..*","kind":"many_to_many"}
  - name: RepositoryPublication
    owner: AnalysisPublication
    description: "대상별 독립 게시 의도와 확인 결과"
    identifier: repositoryPublicationId
    attributes:
      - {"name":"repositoryPublicationId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"analysisSnapshotId","type":"Id","required":true,"nullable":false,"unique":false,"references":"AnalysisSnapshot","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"connectionId","type":"Id","required":true,"nullable":false,"unique":false,"references":"ServiceConnection","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"consentRevision","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"전송에 적용된 SharingConsent의 정확한 개정"}
      - {"name":"remoteObjectReferences","type":"List<ArtifactRef>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"고정 경로/객체/버전/digest; Detail 선확인 후 manifest"}
      - {"name":"publicationState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["LOCAL_COMMITTED","PENDING","IN_PROGRESS","SUCCESS","FAILED","OUTCOME_UNKNOWN","CONFLICT","BLOCKED","PARTIAL"]}
      - {"name":"createdAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"updatedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"lastConfirmedAt","type":"Timestamp","required":true,"nullable":true,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"expectedContentReference","type":"Digest","required":true,"nullable":false,"unique":false,"references":null,"constraints":"전송 전 로컬 확정 기대 내용"}
      - {"name":"effectiveCompleteness","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"COMPLETE|PARTIAL|EMPTY|NEVER_COLLECTED; 원 선언과 별도"}
    constraints: ["analysisSnapshotId+connectionId 유일","대상별 성공 독립; 응답 유실은 재조회 전 새 객체 금지"]
    relationships:
      - {"field":"analysisSnapshotId","target":"AnalysisSnapshot","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"connectionId","target":"ServiceConnection","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: RepositoryConflict
    owner: AnalysisPublication
    description: "게시 사본의 사용자 수정/삭제 충돌"
    identifier: repositoryConflictId
    attributes:
      - {"name":"repositoryConflictId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"repositoryPublicationId","type":"Id","required":true,"nullable":false,"unique":false,"references":"RepositoryPublication","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"localRevision","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"로컬 기대 개정"}
      - {"name":"remoteRevision","type":"Id","required":true,"nullable":true,"unique":false,"references":null,"constraints":"실제 버전; 삭제/조회 불명은 null"}
      - {"name":"remoteChangeSummary","type":"Text","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용된 필드의 변경/삭제 여부; 민감 원문 없음"}
      - {"name":"detectedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"resolutionRequest","type":"Id","required":true,"nullable":true,"unique":false,"references":"MaintenanceRequest","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
    constraints: ["자동 로컬 삭제/원격 덮어쓰기 없음; 해결 요청 범위 재검증"]
    relationships:
      - {"field":"repositoryPublicationId","target":"RepositoryPublication","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"resolutionRequest","target":"MaintenanceRequest","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
  - name: ReceivedPlanArtifact
    owner: PlanAdmission
    description: "불신 Drive 파일의 고정 수신 기록"
    identifier: receivedPlanArtifactId
    attributes:
      - {"name":"receivedPlanArtifactId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"remoteObjectReference","type":"ArtifactRef","required":true,"nullable":false,"unique":false,"references":null,"constraints":"등록 storeAlias·객체·버전·digest"}
      - {"name":"remoteRevision","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"Drive 실제 원격 버전; 앱 versionId와 별도"}
      - {"name":"receivedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"rawContentReference","type":"ProtectedReference","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용 로컬 루트의 불변 원문; 명령/경로로 실행 금지"}
      - {"name":"sourceVersionReference","type":"PlanVersionRef","required":true,"nullable":true,"unique":false,"references":null,"constraints":"subjectRef+planId+versionId+digest; 파싱 불가 null"}
      - {"name":"completeness","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["COMPLETE","PARTIAL","INVALID","UNKNOWN"]}
      - {"name":"conflictSummary","type":"Text","required":true,"nullable":true,"unique":false,"references":null,"constraints":"수신 전후 변경·동일 버전 다른 내용·분기"}
      - {"name":"sourceInstructionReference","type":"ArtifactRef","required":true,"nullable":true,"unique":false,"references":null,"constraints":"C07의 정확한 수신 요청; 계획이면 null"}
      - {"name":"receptionState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["RECEIVED","VALIDATING","VALIDATED","BLOCKED","CONFLICT"]}
    constraints: ["storeAlias+objectId+versionRef+digest별 동일 수신 재사용","metadata-before/blob/metadata-after 불일치면 채택 금지"]
    relationships: []
  - name: ApprovalProof
    owner: PlanAdmission
    description: "등록 적격 검증기의 독립 승인 검증 근거"
    identifier: approvalProofId
    attributes:
      - {"name":"approvalProofId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"receivedPlanArtifactId","type":"Id","required":true,"nullable":false,"unique":false,"references":"ReceivedPlanArtifact","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"sourceDeclarationReference","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"외부 ApprovalDeclaration/C06 approvalId의 출처; 로컬 권한 아님"}
      - {"name":"verifiedUserReference","type":"Id","required":true,"nullable":true,"unique":false,"references":null,"constraints":"검증된 실제 사용자 대응; 실패 시 null"}
      - {"name":"verifiedContentReference","type":"Digest","required":true,"nullable":true,"unique":false,"references":null,"constraints":"C05 또는 C07 전체 digest; 검증 불가 null"}
      - {"name":"approvalScope","type":"Set<Action>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"PUBLISH_PLAN 또는 C07 대응 단일 행위"}
      - {"name":"verificationBasis","type":"VerificationResult","required":true,"nullable":false,"unique":false,"references":null,"constraints":"Common 내부 검증 형식; 적격 검증기/명시적 인간 의도/정책/최신성/철회 모두 필요"}
      - {"name":"verifiedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
    constraints: ["외부가 로컬 proof ID/VERIFIED를 발급하지 못함","미해소 적격 프로필이면 UNQUALIFIED; 스냅샷 자동 게시 불가"]
    relationships:
      - {"field":"receivedPlanArtifactId","target":"ReceivedPlanArtifact","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: AdmittedPlanSnapshot
    owner: PlanAdmission
    description: "형식·승인·안전 검증 후 보존하는 정확한 불변 사본"
    identifier: admittedPlanSnapshotId
    attributes:
      - {"name":"admittedPlanSnapshotId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"sourcePlanVersionReference","type":"PlanVersionRef","required":true,"nullable":false,"unique":false,"references":null,"constraints":"외부 AuthoredPlanVersion의 subjectRef+planId+versionId+digest"}
      - {"name":"contentReference","type":"Digest","required":true,"nullable":false,"unique":false,"references":null,"constraints":"C05 전체 JCS; 필드 삭제/가림 금지"}
      - {"name":"approvalProofId","type":"Id","required":true,"nullable":false,"unique":false,"references":"ApprovalProof","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"goalSnapshot","type":"GoalSnapshot","required":true,"nullable":false,"unique":false,"references":null,"constraints":"C05 goal의 정확한 사본"}
      - {"name":"sessionSnapshots","type":"List<SessionSnapshot>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"C05 sessions의 정확한 사본; 논리 세션/버전 ID 유일"}
      - {"name":"sourceDataReferences","type":"Set<ActivityRevisionRef>","required":true,"nullable":false,"unique":false,"references":"ActivityRecord","constraints":"정확한 개정·허용 수집 근거"}
      - {"name":"admittedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"planPayload","type":"PlanPayload","required":true,"nullable":false,"unique":false,"references":null,"constraints":"goal/session 외 주차·휴식·가정·설명·정책·계보를 포함한 C05 전체"}
      - {"name":"previousPlanDigest","type":"Digest","required":true,"nullable":true,"unique":false,"references":null,"constraints":"최초 계획만 null; 기존 확정 계보와 일치"}
    constraints: ["subjectRef+planId+versionId별 유일 내용","수신 스냅샷 보존은 게시 직전 적격성 보장이 아님; 기존 버전 보존"]
    relationships:
      - {"field":"approvalProofId","target":"ApprovalProof","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"sourceDataReferences","target":"ActivityRecord","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..*","kind":"many_to_many"}
  - name: AdmissionAssessment
    owner: PlanAdmission
    description: "시점별 검증/최종 게시 적격 판정"
    identifier: admissionAssessmentId
    attributes:
      - {"name":"admissionAssessmentId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"admittedPlanSnapshotId","type":"Id","required":true,"nullable":true,"unique":false,"references":"AdmittedPlanSnapshot","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"receivedPlanArtifactId","type":"Id","required":true,"nullable":false,"unique":false,"references":"ReceivedPlanArtifact","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"validationPolicyReference","type":"ValidationPolicyRef","required":true,"nullable":false,"unique":false,"references":null,"constraints":"안전 규칙집 버전·근거·적용 조건·한계 및 정책 digest"}
      - {"name":"sourceDataRevisionReferences","type":"Set<ActivityRevisionRef>","required":true,"nullable":false,"unique":false,"references":"ActivityRecord","constraints":"검증에 사용한 정확한 원천 개정"}
      - {"name":"assessmentOutcome","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["BLOCKED","CONFLICT","ADMITTED_FOR_EVALUATION","ELIGIBLE","ELIGIBLE_WITH_EVALUATION_FAILURE","SUPERSEDED"]}
      - {"name":"blockingReasons","type":"List<Error>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"미해소 승인/정책/안전·부족 자료·계보·시각 오류; 오류 없으면 []"}
      - {"name":"assessedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"evaluationEvidenceReference","type":"Id","required":true,"nullable":true,"unique":false,"references":"EvaluationResult","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"checkContext","type":"CheckContext","required":true,"nullable":false,"unique":false,"references":null,"constraints":"승인/철회·정책·원격 원본·원천 개정·시각·적격 프로필 확인 지점"}
    constraints: ["평가 전 판정과 최종 적격 분리","근거 변화/현재성 불명이면 최종 판정 재사용 금지; 평가 역호출 없음"]
    relationships:
      - {"field":"admittedPlanSnapshotId","target":"AdmittedPlanSnapshot","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
      - {"field":"receivedPlanArtifactId","target":"ReceivedPlanArtifact","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"sourceDataRevisionReferences","target":"ActivityRecord","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..*","kind":"many_to_many"}
      - {"field":"evaluationEvidenceReference","target":"EvaluationResult","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
  - name: AdmittedPlanDisposition
    owner: PlanAdmission
    description: "승인된 폐기/교체/취소 영향과 판정"
    identifier: admittedPlanDispositionId
    attributes:
      - {"name":"admittedPlanDispositionId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"affectedPlanSnapshotReference","type":"Id","required":true,"nullable":false,"unique":false,"references":"AdmittedPlanSnapshot","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"replacementSnapshotReference","type":"Id","required":true,"nullable":true,"unique":false,"references":"AdmittedPlanSnapshot","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"sourceRequestReference","type":"ArtifactRef","required":true,"nullable":false,"unique":false,"references":null,"constraints":"외부 원문이 아닌 C07 정확한 고정 참조"}
      - {"name":"verifiedApprovalReference","type":"Id","required":true,"nullable":false,"unique":false,"references":"ApprovalProof","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"confirmedImpact","type":"Impact","required":true,"nullable":false,"unique":false,"references":null,"constraints":"ALL_FUTURE 또는 SELECTED_FUTURE; 대상 버전/digest/세션과 사용자 승인"}
      - {"name":"dispositionAssessment","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["BLOCKED","VERIFIED","PARTIAL","APPLIED","CONFLICT","OUTCOME_UNKNOWN"]}
      - {"name":"assessedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
    constraints: ["C07 action에 정확한 C06 단일 행위; REPLACE는 새 계획 PUBLISH_PLAN 별도 근거 필요","과거 일정/실제 활동/다른 세션 보존"]
    relationships:
      - {"field":"affectedPlanSnapshotReference","target":"AdmittedPlanSnapshot","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"replacementSnapshotReference","target":"AdmittedPlanSnapshot","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
      - {"field":"verifiedApprovalReference","target":"ApprovalProof","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: EvaluationRequest
    owner: PlanEvaluation
    description: "정확한 계획·분석·모델·동의의 평가 요청"
    identifier: evaluationRequestId
    attributes:
      - {"name":"evaluationRequestId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"admittedPlanSnapshotId","type":"Id","required":true,"nullable":false,"unique":false,"references":"AdmittedPlanSnapshot","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"analysisSnapshotReferences","type":"Set<Id>","required":true,"nullable":false,"unique":false,"references":"AnalysisSnapshot","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"connectionId","type":"Id","required":true,"nullable":false,"unique":false,"references":"ServiceConnection","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"modelReference","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"적격 프로필이 지정한 모델"}
      - {"name":"consentRevision","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"동의 개정; 동일 서비스/목적/대상"}
      - {"name":"requestInputReference","type":"ProtectedReference","required":true,"nullable":false,"unique":false,"references":null,"constraints":"로컬 보존 허용 요청; 비밀 헤더 제외"}
      - {"name":"requestedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"requestContext","type":"EvaluationContext","required":true,"nullable":false,"unique":false,"references":null,"constraints":"계획 digest·분석 개정·프로필/모델·정책 digest·유한 자원/비용 예산·처리 위치"}
      - {"name":"requestState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["PREPARED","IN_PROGRESS","COMPLETED","FAILED","OUTCOME_UNKNOWN","BLOCKED"]}
    constraints: ["미선정 프로필/한도/비용/동의면 외부 호출 0건","재시도는 새 시도와 같은 입력 계보를 연결; 제공자 자동 변경 없음"]
    relationships:
      - {"field":"admittedPlanSnapshotId","target":"AdmittedPlanSnapshot","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"analysisSnapshotReferences","target":"AnalysisSnapshot","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..*","kind":"many_to_many"}
      - {"field":"connectionId","target":"ServiceConnection","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: EvaluationResult
    owner: PlanEvaluation
    description: "평가·미승인 제안·오류를 분리 보존"
    identifier: evaluationResultId
    attributes:
      - {"name":"evaluationResultId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"evaluationRequestId","type":"Id","required":true,"nullable":false,"unique":false,"references":"EvaluationRequest","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"evaluatedContentReference","type":"Digest","required":true,"nullable":false,"unique":false,"references":null,"constraints":"요청한 C05 전체 digest"}
      - {"name":"evaluationOutcome","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["VALID","CALL_FAILED","INVALID","OUTCOME_UNKNOWN","BLOCKED"]}
      - {"name":"findings","type":"List<Finding>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"INFO/WARNING/BLOCKER 및 실제 근거; 오류 결과를 유효 소견으로 승격 금지"}
      - {"name":"proposedAdjustments","type":"List<Text>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"새 승인 전 제안만; 계획 사본 갱신 금지"}
      - {"name":"evidenceReferences","type":"Set<Id>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용 입력의 실제 존재 근거만"}
      - {"name":"assumptions","type":"List<Text>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"비진단·자료 부족 구별"}
      - {"name":"limitations","type":"List<Text>","required":true,"nullable":false,"unique":false,"references":null,"constraints":"자료·모델·검증 한계; 정상 무소견도 검증 전제 표시"}
      - {"name":"completedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"failureReason","type":"Error","required":true,"nullable":true,"unique":false,"references":null,"constraints":"성공은 null; 비정상/불명은 필수"}
      - {"name":"assessment","type":"Enum","required":true,"nullable":true,"unique":false,"references":null,"constraints":"VALID 결과일 때만 EVALUATION 값","allowed_values":["NO_FINDINGS","CAUTION","UNSUITABLE","INSUFFICIENT_DATA"]}
    constraints: ["동일 request의 늦은 응답은 현재 계획 변경 권한 없음","CALL_FAILED와 INVALID/미확인 구별; 유효 평가도 승인 아님"]
    relationships:
      - {"field":"evaluationRequestId","target":"EvaluationRequest","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: PublicationIntent
    owner: CalendarDelivery
    description: "외부 효과 전 영속 보존한 세션 의도"
    identifier: publicationIntentId
    attributes:
      - {"name":"publicationIntentId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"admittedPlanSnapshotId","type":"Id","required":true,"nullable":false,"unique":false,"references":"AdmittedPlanSnapshot","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"sourceSessionReference","type":"SessionRef","required":true,"nullable":false,"unique":false,"references":null,"constraints":"planId/sessionId/sessionVersionId/digest"}
      - {"name":"calendarConnectionId","type":"Id","required":true,"nullable":false,"unique":false,"references":"ServiceConnection","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"admissionAssessmentReference","type":"Id","required":true,"nullable":true,"unique":false,"references":"AdmissionAssessment","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"evaluationResultReference","type":"Id","required":true,"nullable":true,"unique":false,"references":"EvaluationResult","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"requestedEffect","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["CREATE","UPDATE","CANCEL"]}
      - {"name":"confirmedImpact","type":"Impact","required":true,"nullable":false,"unique":false,"references":null,"constraints":"정확한 대상/미래 세션 범위; UPDATE/CANCEL은 검증된 처분 참조"}
      - {"name":"intentState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["PREPARED","BLOCKED","READY","IN_PROGRESS","CONFIRMED","FAILED","OUTCOME_UNKNOWN","CONFLICT","SKIPPED_PAST"]}
      - {"name":"fixedEventId","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"P03의 gta+SHA-256 JCS tuple 소문자 base32hex; 55자"}
      - {"name":"expectedContentReference","type":"Digest","required":true,"nullable":false,"unique":false,"references":null,"constraints":"현재 의도의 승인된 이벤트 투영 전체"}
      - {"name":"effectContext","type":"EffectContext","required":true,"nullable":false,"unique":false,"references":null,"constraints":"현재 시각 근거·해석 시작/종료·적격 판정/권한 확인·정책/시각 개정·처분·과거 건너뜀 사유/범위"}
    constraints: ["동일 논리 세션/대상 고정 ID 유지; 버전별 효과 의도는 구별","SKIPPED_PAST는 생성이 없다고 확인된 CREATE에만 허용","admittedPlanSnapshotId+sourceSessionReference+calendarConnectionId+requestedEffect+expectedContentReference별 의도 유일; 같은 논리 세션의 외부 효과 직렬화"]
    relationships:
      - {"field":"admittedPlanSnapshotId","target":"AdmittedPlanSnapshot","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"calendarConnectionId","target":"ServiceConnection","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"admissionAssessmentReference","target":"AdmissionAssessment","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
      - {"field":"evaluationResultReference","target":"EvaluationResult","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
  - name: CalendarBinding
    owner: CalendarDelivery
    description: "논리 세션과 고정 원격 이벤트의 연결"
    identifier: calendarBindingId
    attributes:
      - {"name":"calendarBindingId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"publicationIntentId","type":"Id","required":true,"nullable":false,"unique":false,"references":"PublicationIntent","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"sourcePlanReference","type":"PlanVersionRef","required":true,"nullable":false,"unique":false,"references":null,"constraints":"현재 확인된 계획 계보"}
      - {"name":"sourceSessionReference","type":"SessionRef","required":true,"nullable":false,"unique":false,"references":null,"constraints":"논리 sessionId 유지"}
      - {"name":"remoteEventReference","type":"Id","required":true,"nullable":false,"unique":false,"references":null,"constraints":"의도와 동일 fixedEventId; 생성 전에도 고정 ID 예약"}
      - {"name":"lastConfirmedRemoteRevision","type":"Id","required":true,"nullable":true,"unique":false,"references":null,"constraints":"실제 GET/확인 etag; 미확정 null"}
      - {"name":"lastAppliedContentReference","type":"Digest","required":true,"nullable":true,"unique":false,"references":null,"constraints":"마지막 확인한 이벤트 내용; 미확정 null"}
      - {"name":"bindingState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["RESERVED","ACTIVE","CANCELLED","OUTCOME_UNKNOWN","CONFLICT"]}
      - {"name":"intentHistory","type":"Set<Id>","required":true,"nullable":false,"unique":false,"references":"PublicationIntent","constraints":"개정 의도 이력; publicationIntentId는 마지막 관련 의도"}
    constraints: ["subjectRef+calendarAlias+planId+sessionId 유일; target+eventId 유일","원격 marker만으로 소유 인정 금지","한 PublicationIntent는 최대 한 CalendarBinding에 연결; intentHistory는 해당 논리 세션/대상의 의도만 포함"]
    relationships:
      - {"field":"publicationIntentId","target":"PublicationIntent","direction":"source_to_target","source_cardinality":"0..1","target_cardinality":"1","kind":"one_to_one"}
      - {"field":"intentHistory","target":"PublicationIntent","direction":"source_to_target","source_cardinality":"0..1","target_cardinality":"0..*","kind":"one_to_many"}
  - name: DeliveryAttempt
    owner: CalendarDelivery
    description: "세션 의도별 효과/대조 시도와 결과"
    identifier: deliveryAttemptId
    attributes:
      - {"name":"deliveryAttemptId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"publicationIntentId","type":"Id","required":true,"nullable":false,"unique":false,"references":"PublicationIntent","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"calendarBindingId","type":"Id","required":true,"nullable":false,"unique":false,"references":"CalendarBinding","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"startedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"finishedAt","type":"Timestamp","required":true,"nullable":true,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"remoteOutcome","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["NOT_SENT","SUCCESS","FAILED","OUTCOME_UNKNOWN","CONFLICT"]}
      - {"name":"retryState","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["NONE","RECONCILE_FIRST","READY","REQUIRES_ACTION","EXHAUSTED","DONE"]}
      - {"name":"failureReason","type":"Error","required":true,"nullable":true,"unique":false,"references":null,"constraints":"비정상 결과 필수; 성공/진행 중은 null"}
      - {"name":"attemptKind","type":"Enum","required":true,"nullable":false,"unique":false,"references":null,"constraints":"허용값 이외 거절","allowed_values":["LOOKUP","CREATE","UPDATE","CANCEL"]}
      - {"name":"expectedRemoteRevision","type":"Id","required":true,"nullable":true,"unique":false,"references":null,"constraints":"UPDATE/CANCEL 조건부 etag; CREATE/초기 LOOKUP null"}
    constraints: ["시도 시작을 로컬 확정하지 못하면 효과 요청 금지","OUTCOME_UNKNOWN이면 RECONCILE_FIRST; 조회 불능을 미존재로 변환 금지"]
    relationships:
      - {"field":"publicationIntentId","target":"PublicationIntent","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"calendarBindingId","target":"CalendarBinding","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
  - name: CalendarConflict
    owner: CalendarDelivery
    description: "사용자 수정/식별 불일치/조건부 충돌 근거"
    identifier: calendarConflictId
    attributes:
      - {"name":"calendarConflictId","type":"Id","required":true,"nullable":false,"unique":"해당 엔티티 전체","references":null,"constraints":"원 소유 컴포넌트가 발급하며 수명 동안 불변"}
      - {"name":"calendarBindingId","type":"Id","required":true,"nullable":false,"unique":false,"references":"CalendarBinding","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
      - {"name":"expectedContentReference","type":"Digest","required":true,"nullable":false,"unique":false,"references":null,"constraints":"마지막 확인 내용/현재 의도를 구별"}
      - {"name":"observedRemoteRevision","type":"Id","required":true,"nullable":true,"unique":false,"references":null,"constraints":"조회 불가/삭제 불명 null"}
      - {"name":"userChangeSummary","type":"Text","required":true,"nullable":false,"unique":false,"references":null,"constraints":"양쪽 차이·원인; 허용 최소 안내"}
      - {"name":"detectedAt","type":"Timestamp","required":true,"nullable":false,"unique":false,"references":null,"constraints":"UTC Z; 원천 활동 시각은 OffsetTimestamp 사용"}
      - {"name":"resolutionRequest","type":"Id","required":true,"nullable":true,"unique":false,"references":"MaintenanceRequest","constraints":"삭제 연쇄 없음; 정확한 식별자만 참조"}
    constraints: ["자동 최신 etag 재덮어쓰기 금지; 이름만 같은 타 이벤트 조작 금지"]
    relationships:
      - {"field":"calendarBindingId","target":"CalendarBinding","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"1","kind":"many_to_one"}
      - {"field":"resolutionRequest","target":"MaintenanceRequest","direction":"source_to_target","source_cardinality":"0..*","target_cardinality":"0..1","kind":"many_to_one"}
```

## 소유와 관계 요약

| 컴포넌트 | 엔티티 수 | 책임 |
|---|---:|---|
| OperationControl | 4 | 유효 설정·예약·실행 집계·유지보수 요청 |
| DataAccessPolicy | 4 | 연결·비밀 참조·동의·보존 |
| ActivityCollection | 3 | 유일 원천 운동·커서·미완료 오류 |
| AnalysisPublication | 3 | 불변 분석·대상별 게시·사본 충돌 |
| PlanAdmission | 5 | 불신 수신·검증 근거·불변 사본·시점별 적격성·처분 |
| PlanEvaluation | 2 | 정확한 입력 요청·검증 결과/제안/실패 |
| CalendarDelivery | 4 | 의도·세션 연결·시도·충돌 |

관계의 source_cardinality는 한 대상이 가질 수 있는 원본 수, target_cardinality는 한 원본이 참조하는 대상 수다. many_to_many는 양쪽 0..*이며 Set의 각 참조는 정확한 ID/개정 한 개를 식별한다. CalendarBinding의 현재 의도는 1개이고 의도 하나는 최대 연결 한 개에 속한다. intentHistory는 한 연결에서 0..* 의도를 참조하며 의도별 연결은 최대 1개다. 외부 AuthoredPlanVersion·ApprovalDeclaration·AuthoredPlanInstruction은 출처 지시자이며 U3 소유를 유지한다. U1은 Common/C01~C08 명세만 소유한다.

로컬 상태는 C08 wire 상태와 별개다. SKIPPED_PAST를 wire에 추가하거나 Calendar 성공으로 바꾸지 않는다. 실제 계정·건강 자료·비밀 값은 모델 예시에 사용하지 않는다.

