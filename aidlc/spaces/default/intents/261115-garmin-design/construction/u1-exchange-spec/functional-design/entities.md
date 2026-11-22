# U1 공통 교환 명세 — 논리 모델

- 단위: `u1-exchange-spec` (`spec`), 설계 기준일: 2026-11-18.
- 근거: [확인한 입력](functional-design-questions.md), [단위와 소유권](../../../inception/units-generation/unit-of-work.md), [공통 계약 1.0.0](../../../inception/contract-design/contract-summary.md), [컴포넌트](../../../inception/domain-design/components.md).
- 이 문서의 YAML은 U1 **명세 관리 모델**의 기준이다. 전송 payload의 필드·필수성·열거값은 공통 계약의 등록 JSON Schema를 참조한다. 제품 엔티티를 재소유하거나 제품 DB를 정의하지 않는다. 흐름과 전이는 [functional-spec.md](functional-spec.md), 판정은 [rules.md](rules.md)가 기준이다.

## Entity Model

`attribute_defaults`는 아래 속성에서 생략된 제약의 명시적 기본값이다. `required: true`여도 `type`에 null이 있으면 속성 존재는 필수이고 값은 null일 수 있다. 명세 관리 식별자는 전송 Common.Id의 제한을 공유하며, 제품 ID를 새로 발급하거나 바꾸지 않는다.

```yaml
model_version: "1.0.0"
owner: U1
kind: specification_model
attribute_defaults:
  required: true
  unique: false
  default: none
  min: none
  max: none
  references: none
types:
  Id: {logical_type: opaque_string, min: 1, max: 1024, constraints: "선행 0·대소문자·Unicode 원문 보존"}
  Digest: {logical_type: string, constraints: "sha256: 다음 소문자 16진수 64자리; 전체 JSON의 JCS UTF-8 digest"}
  Timestamp: {logical_type: utc_instant, constraints: "유효한 date-time, UTC Z"}
  RuleId: {logical_type: string, constraints: "rules.md에 존재하는 BR{group}.{seq}"}
entities:
  - name: SpecificationRelease
    description: "Common과 C01~C08 및 합성 교환 사례를 고정하는 명세 배포 묶음; 제품 승인과 무관"
    identifier: releaseId
    attributes:
      - {name: releaseId, type: Id, unique: true}
      - {name: schemaVersion, type: string, allowed_values: ["1.0.0"]}
      - {name: createdAt, type: Timestamp}
      - {name: commonDigest, type: Digest}
      - {name: contracts, type: "list<ReleaseContractEntry>", min: 6, max: 6}
    constraints:
      - "C03~C08이 각각 정확히 한 번; C01/C02 bootstrap은 소비자의 검증된 설치 경로에서 별도 고정"
      - "Common의 digest, 각 schemaDigest, fixturesDigest를 실제 고정 산출물과 대조"
      - "배포된 버전은 불변; 자기 선언만으로 신뢰하지 않으며 제품 활성화를 뜻하지 않음"
    relationships:
      - {to: ContractDefinition, cardinality: "1 -> 9", direction: "release -> definition", meaning: "Common 및 C01~C08의 고정 정의를 참조; contracts 배열에는 C03~C08만 존재"}
      - {to: SyntheticFixture, cardinality: "1 -> 12", direction: "release -> fixture", meaning: "현재 기준의 RELEASE와 11개 교환 fixture; digest 대상에서 RELEASE 제외"}
  - name: ContractDefinition
    description: "고정 registry의 U1 정의·하위 fragment·의미 규칙 연결"
    identifier: schemaId
    attributes:
      - {name: schemaId, type: Id, unique: true}
      - {name: definitionKey, type: string, allowed_values: [Common, C01, C02, C03, C04, C05, C06, C07, C08]}
      - {name: schemaDigest, type: Digest}
      - {name: sourceAnchor, type: string, constraints: "승인된 contract-summary.md의 해당 절"}
      - {name: fragmentRefs, type: "set<Id>", min: 0, constraints: "고정 registry 안에서만 해석; C03 Detail은 루트 digest에 결합"}
      - {name: ruleIds, type: "set<RuleId>", min: 1}
    constraints:
      - "U2 전용 EVALUATION·LLM_REQUEST·LLM_RESPONSE와 외부 P01~P05 어댑터를 소유/배포 의존에 넣지 않음"
      - "입력 URI를 원격 다운로드·코드 실행·새 검증기 등록 근거로 사용하지 않음"
    relationships:
      - {to: ContractDefinition, cardinality: "0..* -> 0..*", direction: "definition -> referenced definition", meaning: "C02에서 C01, C03~C08에서 Common 등의 명시적 고정 참조"}
  - name: SyntheticFixture
    description: "실제 사용자·계정·건강 기록·비밀을 포함하지 않는 불변 합성 입력"
    identifier: fixtureKey
    attributes:
      - {name: fixtureKey, type: Id, unique: true, constraints: "release 안에서 이름 유일; 버전 간 전체 식별은 releaseId와 결합"}
      - {name: releaseId, type: Id, references: SpecificationRelease.releaseId}
      - {name: schemaId, type: "Id|null", references: ContractDefinition.schemaId, constraints: "원시 바이트 파싱 음성 자료이면 null 가능"}
      - {name: inputForm, type: string, allowed_values: [JSON_VALUE, RAW_UTF8_BYTES]}
      - {name: content, type: "synthetic_json_value|synthetic_bytes", constraints: "문자·바이트 원문 보존; 음성 자료를 자동 수정하지 않음"}
      - {name: privacyClass, type: string, allowed_values: [SYNTHETIC_ONLY]}
    constraints:
      - "fixtureKey 유일성은 release 범위; 서로 다른 내용에 같은 releaseId/fixtureKey 재사용 금지"
      - "현행 U1 교환 fixture는 ANALYSIS, POLICY, PLAN, DECLARATION, DISPOSITION, RECEIPT, POLICY_DISTANCE_ONLY, ANALYSIS_DISTANCE_ONLY, ANALYSIS_PARTITIONED, DETAIL_0, DETAIL_1"
      - "RELEASE를 제외한 위 11개 이름→내용 객체 전체의 digest를 fixturesDigest로 사용; U2 fixture 제외"
    relationships: []
  - name: ConformanceCase
    description: "입력·합성 조건·예상 구조/의미/외부 차단을 서로 분리한 적합성 사례 정의"
    identifier: caseId
    attributes:
      - {name: caseId, type: Id, unique: true, constraints: "release 범위 유일; 기존 V/N/B/T/S ID와 신규 FD ID 구별"}
      - {name: releaseId, type: Id, references: SpecificationRelease.releaseId}
      - {name: fixtureKeys, type: "list<Id>", min: 1, references: SyntheticFixture.fixtureKey}
      - {name: ruleIds, type: "set<RuleId>", min: 1}
      - {name: setup, type: synthetic_conditions, constraints: "고정 입력 치환·읽기 실패·신뢰된 실제 경로 목록의 모의 설정; 실행 명령 아님"}
      - {name: expectedParse, type: "boolean|null", constraints: "검사하지 않는 층은 null"}
      - {name: expectedStructure, type: "boolean|null"}
      - {name: expectedSemantic, type: "string|null", constraints: "COMPLETE/PARTIAL/EMPTY/NEVER_COLLECTED 또는 Common.Error.code 등 검사 범위의 기대값"}
      - {name: requiredExternalGate, type: string, constraints: "실제 승인/정책/권한/실행 검증의 미해소 상태를 예상 적합성과 분리"}
    constraints:
      - "expected는 실행 증거가 아니며 rebindPolicy/rebindDetails는 합성 구성에서만 사용"
      - "문자열·바이트 경계와 의미 실패를 구조 검사 하나로 합격 처리하지 않음"
    relationships:
      - {to: SyntheticFixture, cardinality: "0..* -> 1..*", direction: "case -> fixture", meaning: "사례가 동일 release의 입력을 참조"}
  - name: ConformanceAssessment
    description: "한 고정 사례에 대해 실제 수행한 한정 적합성 검사의 결과; 제품 권한 검증 결과가 아님"
    identifier: assessmentId
    attributes:
      - {name: assessmentId, type: Id, unique: true}
      - {name: caseId, type: Id, references: ConformanceCase.caseId}
      - {name: releaseId, type: Id, references: SpecificationRelease.releaseId}
      - {name: inputDigest, type: "Digest|null", constraints: "파싱 불가 바이트에는 JSON digest를 자칭하지 않음"}
      - {name: scope, type: "set<string>", allowed_values: [PARSING, STRUCTURE, SEMANTICS, DOCUMENT_CONSISTENCY], min: 1}
      - {name: outcome, type: string, allowed_values: [PLANNED, MATCHED, MISMATCHED, NOT_RUN]}
      - {name: observedAt, type: "Timestamp|null", constraints: "실제 검사 전 null"}
      - {name: observedResults, type: "list<logical_result>", min: 0}
      - {name: evidenceRefs, type: "list<string>", min: 0}
      - {name: effectiveCompleteness, type: "string|null", allowed_values: [COMPLETE, PARTIAL, EMPTY, NEVER_COLLECTED, null]}
      - {name: failedParts, type: "list<logical_part_failure>", min: 0}
      - {name: externalAuthority, type: string, allowed_values: [NOT_ESTABLISHED], default: NOT_ESTABLISHED}
    constraints:
      - "MATCHED는 수행 scope의 기대 일치만 뜻함; VERIFIED·사용자 승인·게시 성공으로 승격 금지"
      - "원천 completeness를 변경하지 않음; 무효 입력은 effectiveCompleteness가 있어도 채택 불가"
      - "이번 기능 설계 문서는 신규 사례의 MATCHED 실행 기록을 만들지 않음"
    relationships:
      - {to: ConformanceCase, cardinality: "0..* -> 1", direction: "assessment -> case", meaning: "동일 사례의 여러 소비자/검사 결과를 별도로 연결"}
  - name: ConsumerBinding
    description: "U2/U3가 독립적으로 고정할 명세와 자체 부합 범위의 논리 연결; 제품 연결 설정이 아님"
    identifier: bindingId
    attributes:
      - {name: bindingId, type: Id, unique: true}
      - {name: consumerUnit, type: string, allowed_values: [U2, U3]}
      - {name: releaseId, type: Id, references: SpecificationRelease.releaseId}
      - {name: bindingState, type: string, allowed_values: [UNASSESSED, CONFORMANT, NONCONFORMANT]}
      - {name: assessmentRefs, type: "list<Id>", min: 0, references: ConformanceAssessment.assessmentId}
      - {name: limitations, type: "list<string>", min: 1, constraints: "외부 지원·신뢰·전체 인수의 미검증 범위 명시"}
    constraints:
      - "U2/U3 각자의 자료로 같은 U1 버전에 부합; 상대 실행 파일·DB·전용 시험 자료를 필수로 참조하지 않음"
      - "CONFORMANT는 고정 명세의 검증 범위만 의미; 외부 기능 활성화 권한 아님"
    relationships:
      - {to: SpecificationRelease, cardinality: "0..* -> 1", direction: "binding -> release", meaning: "소비자별 명시적으로 고정한 버전"}
      - {to: ConformanceAssessment, cardinality: "0..* -> 0..*", direction: "binding -> assessment", meaning: "소비자가 실제 확인한 결과만 참조"}
value_objects:
  - name: ReleaseContractEntry
    attributes: [contractId, schemaId, schemaDigest, fixturesDigest]
    constraints: "C01의 정확한 필드·유형; C03~C08 각각 한 번"
  - name: Quantity
    attributes: [value, unit]
    constraints: "Common.Quantity와 GTA-NUMERIC-1; value는 0 이상 십진 문자열, 원천/정확 합계 정수부 30자리·소수부 18자리, 파생 속도/페이스는 최종 소수부 6자리 HALF_EVEN 정규형. 단위는 [m, s, m/s, s/km, bpm, rpe, ratio, count] 중 하나; 값의 정밀도와 실제 도구 적격성을 구별"
  - name: Metric
    attributes: [state, quantity, sourceRef, calculationBasis]
    constraints: "Common.Metric; observed/computed/estimated/missing/not_collected/not_applicable/withheld의 7상태; rules.md BR2.1~2.2"
  - name: Period
    attributes: [startInclusive, endExclusive, timezone]
    constraints: "유효 일자·실제 IANA 시간대; 시작<끝; 시작 포함·끝 제외"
  - name: ArtifactRef
    attributes: [storeAlias, objectId, versionRef, digest]
    constraints: "등록 별칭·불투명 고정 버전·실제 전체 내용 digest; 임의 URL 탐색 불가"
  - name: TimingPolicy
    attributes: [policyId, policyRevision, calendarAlias, timezone, defaultLocalTime, tzdbVersion]
    constraints: "Common.TimingPolicy; C05 전체 digest와 결합; 변경 시 새 승인"
  - name: AnalysisProjection
    attributes: [service, purpose, targetAlias, policyDigest, allowedFieldPaths]
    constraints: "Common.AnalysisProjection; ANALYSIS 목적; 등록된 분석용 9개 필드 이름의 정렬 집합"
  - name: Error
    attributes: [code, retryable, message, workRef, observedAt, fieldPath, suggestedAction]
    constraints: "Common.Error; 고정 코드/안내·비밀 제외; suggestedAction은 실행 명령 아님"
```

U1 모델 엔티티 6개와 값 객체 8개다. 릴리스는 9개 정의를 고정하며 배포 문서의 contracts는 C03~C08 6개만 담는다. SyntheticFixture와 ConformanceCase의 식별자는 release 범위다. ConformanceAssessment는 실제로 수행한 한정 검사와 미수행을 구분하는 명세 모델이며, 이번 문서가 합성 의미 검증기의 구현을 추가하지 않는다.

## 교환 표현과 원 소유자

아래는 새 도메인 엔티티가 아닌 기존 소유 자료의 논리적 읽기/쓰기 표현이다. 등록 Schema의 모든 `required`·null 허용·`additionalProperties`·`allOf` 조건을 그대로 적용한다. 별도 필드 사본을 정의하지 않아 상류와의 이중 기준을 피한다.

| 표현 | 논리 필드와 관계 | 원 소유·제약 |
|---|---|---|
| C03 manifest | snapshotId/sourceSnapshotRef/subjectRef, generatedAt/sourceCollectedAt, period/completeness/missingPeriods, projection, delivery, summaryBySport, activities, detailArtifacts, schemaVersion/documentType, 선택 extensions | U2 AnalysisPublication. sourceSnapshotRef 1개에서 대상별 snapshotId/digest가 여러 개일 수 있음. extensions로 초기 C03 자유 자료를 전송하지 않음 |
| C03 Activity | activityId/sourceRevision/sport/startedAt, 고정 distance/duration/pace/speed/heartRate Metric | 원천 U2 ActivityCollection, 게시 표현 U2 AnalysisPublication. 전체 스냅샷의 activityId 유일, 서로 다른 sourceRevision 중복도 금지 |
| C03 DetailRef/Detail | ArtifactRef·partIndex·period·activityCount / schemaVersion/documentType·snapshotId/sourceSnapshotRef/subjectRef·projection·rootPeriod·partIndex/partCount·period·activities | 등록 fragment `urn:gta:contract:C03:1.0.0#/$defs/Detail`. 루트 1→N 상세, 상세의 하위 참조 없음; descriptor와 실제 내용 대조 |
| C04 | policyId/policyRevision/subjectRef/issuedAt/state, timingPolicy/verificationRecordRef, grants(service,purpose,targetAlias,allowedFieldPaths,sensitiveFieldPaths,consentRecordRef), 선택 extensions | U2 DataAccessPolicy의 SharingConsent·ServiceConnection·RuntimeConfiguration 참조 표현. U3는 원 정책의 권위 있는 사본을 생성하지 않음. 인증 참조/보호 저장 위치 제외 |
| C05 goal | goalId/goalRevision/sport, targetDistance/targetTime/objective/targetDate, availability/weeklyFrequency/fixedActivities/constraints | U3 TrainingGoal. running 고정; 거리는 m·목표 시간 s, null은 미지정; 목표 수행 objective는 필수 |
| C05 plan | subjectRef/planId/versionId/previousPlanDigest/generatedAt/authoringState, goal/period/policyDigest/timingPolicy, sourceAnalysisRefs/weeklyObjectives/sessions/restDates/assumptions/changeReason, 선택 extensions | U3 AuthoredPlanVersion. authoringState=PROPOSAL, 이전 digest는 초기 null 또는 확정 계보 참조. goal 스냅샷 1개와 세션 1개 이상을 전체 결합 |
| C05 session | sessionId/sessionVersionId/date/localTime/sport, expectedDuration/expectedDistance, intensity(basis,lower,upper,scaleRef,instruction), instructions(warmup,main,cooldown) | U3 AuthoredSession. running, expectedDuration 양수 s·expectedDistance null 또는 m. localTime null이면 결합한 기본 시각. ID·세션 버전 각각 계획 안 유일 |
| C06 | approvalId/claimedSubjectRef/documentKind/targetDigest/policyDigest/authorizedActions/declaredAt, evidenceLocator(profileId,recordId,sourceArtifact), 선택 extensions | U3 ApprovalDeclaration의 불신 선언. U2 ApprovalProof ID를 외부에서 지정하지 않음. Common.VerificationResult는 적격 U2 검증기의 내부 산출이며 외부 선언이 아님 |
| C07 | requestId/subjectRef/planId/expectedVersionId/expectedPlanDigest/action/replacementPlan/impact(scope,sessionIds)/policyDigest/requestedAt, 선택 extensions | U3 AuthoredPlanInstruction. 검증 후 U2 AdmittedPlanDisposition과 계보 연결; REPLACE에는 새 C05 ArtifactRef, 나머지는 null |
| C08 | receiptId/producerUnit/subjectRef/workId/stage/state/targetDigest/observedAt/lastSuccessfulAt, sessionResults(sessionId,state,remoteReference)/errors, 선택 extensions | U3는 PlanTransferReceipt의 STORE만, U2는 각 처리 소유자의 결과. 외부 status를 받아 소유자의 사실로 자동 채택하지 않음 |

제품의 31개 엔티티는 [원래 배치 표](../../../inception/units-generation/unit-of-work.md)의 U2 25개·U3 6개 소유를 유지한다. U1 명세 객체를 소유한다는 사실은 실제 수집·승인·Calendar 상태를 생성/변경할 권한을 부여하지 않는다. 제품의 작성본→검증 사본은 같은 가변 객체가 아니며 versionId·내용 digest·원 계보로 연결한다.
