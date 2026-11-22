# U3 작성 워크플로 엔티티

이 문서의 YAML은 U3 소유 데이터의 기준이다. [기능 명세](functional-spec.md)가 순서와 상태 전이, [업무 규칙](rules.md)이 판정 기준이다. [컴포넌트](../../../inception/domain-design/components.md)의 CoachingWorkflow 원 소유 엔티티 6개를 유지한다. 아래 논리 모델은 wire 스키마의 확장이 아니다. C05~C08 변환 시 [공통 계약](../../../inception/contract-design/contract-summary.md)에 등록된 필드만 출력한다.

초안의 미정 값은 대화 내부에만 남긴다. 필수 값이 완성되지 않은 목표/세션을 C05 완전본으로 직렬화하지 않는다. 정책/분석/승인 검증/실제 운동/Calendar 결과의 원본은 U2가 소유하며 U3는 고정 참조와 읽은 범위만 보존한다.

```yaml
model:
  unit: u3-chatgpt-workflow
  owner: CoachingWorkflow
  schema_version: "1.0.0"
  attribute_defaults:
    unique: false
    default: 없음
    references: null
    constraint: 각 속성에 명시한 논리 유형과 공통 계약을 적용
  types:
    Id: "불투명 UTF-8 문자열, 1~1024자. 대소문자/선행 0/Unicode 보존, 자르기·정규화·숫자화 금지"
    Text: "비어 있지 않은 문자열. 코드·URL·명령이 아닌 불신 데이터. 실행 프로필의 유한 크기 제한 적용"
    Date: "실제 존재하는 YYYY-MM-DD 날짜"
    Time: "00:00~23:59 현지 시각"
    Timestamp: "UTC Z 시각; 관측·작성·수신 의미를 혼합하지 않음"
    Digest: "sha256: 뒤 소문자 16진수 64자리; 대상 JSON 전체 JCS"
    Quantity: "Common.Quantity와 GTA-NUMERIC-1: 음수가 아닌 십진 문자열 value와 unit; 원천/정확 합계 30+18자리, 유리수 중간값 분자/분모 각각256자리, 파생 속도/페이스 최종6자리 HALF_EVEN 정규형·정확 대조. 비유한 수·양수의0반올림 금지"
    Period: "Common.Period: startInclusive < endExclusive, 실제 IANA timezone, 시작 포함·끝 제외"
    ArtifactRef: "Common.ArtifactRef: storeAlias/objectId/versionRef/digest 모두 필수·비null"
    TimingPolicy: "Common.TimingPolicy의 모든 필드 필수, 실제 정책·calendarAlias·timezone·tzdbVersion 결합"
    FieldEvidence: "fieldPath:Text, origin:USER_STATEMENT|ANALYSIS|COMPUTED|ESTIMATED, sourceRef:Id|null, observedAt:Timestamp|null, confirmation:CONFIRMED|UNCONFIRMED|CONFLICT"
    Availability: "weekday:MO|TU|WE|TH|FR|SA|SU, from:Time, to:Time 모두 필수; from < to, 겹친 구간 확인"
    FixedActivity: "sport:Common.Sport, description:Text, date:Date|null, weekday:요일|null, from:Time|null, to:Time|null 모두 키 필수. date/weekday 둘 다 null인 경우 일정 미정으로 확인"
    WeeklyObjective: "weekStart:Date, objective:Text 필수. 주차 경계와 목표일까지의 부분 주 포함"
    Intensity: "C05.intensity: basis/lower/upper/scaleRef/instruction 키 필수. 수치 기준 단위 및 범위는 rules BR3.6; 안전 경고는 별도 BR3.5"
    Instructions: "warmup/main/cooldown:Text 모두 필수. 해당 없음은 명시적 설명"
    Impact: "C07.impact: scope=ALL_FUTURE|SELECTED_FUTURE, sessionIds=유일 Id 배열. ALL_FUTURE는 빈 배열, SELECTED_FUTURE는 1개 이상"
    EvidenceLocator: "C06.evidenceLocator: profileId/recordId/sourceArtifact 필수. 불신 후보 참조이며 검증 완료가 아님"
    Error: "Common.Error: 고정 code/retryable/message/workRef/observedAt/fieldPath/suggestedAction 필수; 비밀/본문 echo 금지"
    Progress: "내부 값 객체: phase=INPUT|DATA_REVIEW|DRAFTING|REVIEW|DECLARATION|TRANSFER|PAUSED|BLOCKED, lastCompletedStep:Text|null, blockingCodes:Error[], baseVersionId:Id|null. 실행 권한을 발급하지 않음"
  entities:
    - name: TrainingGoal
      description: 사용자 목표와 확인 근거를 개정별로 보존
      identifier: [goalId, goalRevision]
      attributes:
        - {name: goalId, type: Id, required: true, nullable: false, unique: 사용자 범위의 목표 논리 ID}
        - {name: goalRevision, type: Id, required: true, nullable: false, unique: goalId 안의 개정 ID}
        - {name: subjectRef, type: Id, required: true, nullable: false, constraint: 실제 계정 식별자는 교환하지 않는 사용자 별칭}
        - {name: sport, type: enum, required: true, nullable: false, allowed_values: [running]}
        - {name: targetDistance, type: Quantity, required: true, nullable: true, constraint: null은 미정/비수치 목표. 값이 있으면 m이며 양수}
        - {name: performanceTarget, type: object, required: true, nullable: false, constraint: "objective:Text 필수, targetTime:Quantity|null 키 필수. 시간 값은 s이며 양수; C05 objective/targetTime에 대응"}
        - {name: targetDate, type: Date, required: true, nullable: true, constraint: 내부 초안만 null 가능. C05 출력 전 필수 확정}
        - {name: availability, type: "Availability[]", required: true, nullable: false, constraint: 입력 중 빈 배열 가능. C05는 1개 이상·각 시간 범위 유효}
        - {name: weeklyFrequency, type: integer, required: true, nullable: true, constraint: C05 출력은 1~9007199254740991. 실제 가능한 시간/세션 수와 대조하고 불가능한 빈도는 확인}
        - {name: fixedActivities, type: "FixedActivity[]", required: true, nullable: false, constraint: 빈 배열은 확인한 없음. 미확인은 fieldEvidence에 표시}
        - {name: constraints, type: "Text[]", required: true, nullable: false, constraint: 빈 배열은 확인한 없음. 민감 원천은 별도 동의/등록 범위 없이 전송 금지}
        - {name: fieldEvidence, type: "FieldEvidence[]", required: true, nullable: false, constraint: 동일 fieldPath별 근거/상충을 보존. 추정을 사용자 진술로 승격 금지}
        - {name: goalConfirmation, type: enum, required: true, nullable: false, allowed_values: [INCOMPLETE, NEEDS_CONFIRMATION, CONFIRMED], default: INCOMPLETE}
      constraints:
        - goalId와 subjectRef는 개정 계보에서 변경하지 않는다. 수정된 내용은 새 goalRevision으로 보존한다.
        - CONFIRMED는 해당 개정 요약의 사용자 확인이며 계획 게시 승인이 아니다.
        - 필수 목표일·실행 가능한 시간·빈도가 미정/상충이면 계획 확정과 C05 완전본 출력 보류.
    - name: AuthoredPlanVersion
      description: 특정 목표 개정과 근거를 결합한 불변 C05 작성 버전
      identifier: [authoredPlanVersionId]
      attributes:
        - {name: authoredPlanVersionId, type: Id, required: true, nullable: false, unique: 사용자 범위의 작성 버전 ID, wire: C05.versionId}
        - {name: planId, type: Id, required: true, nullable: false, constraint: 같은 계획 개정 계보에서 유지}
        - {name: subjectRef, type: Id, required: true, nullable: false}
        - {name: goalId, type: Id, required: true, nullable: false, references: TrainingGoal.goalId}
        - {name: goalRevision, type: Id, required: true, nullable: false, references: TrainingGoal.goalRevision, constraint: goalId와 복합 참조·정확한 목표 스냅샷}
        - {name: previousVersionId, type: Id, required: true, nullable: true, references: AuthoredPlanVersion.authoredPlanVersionId, constraint: 최초만 null. 다른 planId/사용자 부모·순환 금지}
        - {name: previousPlanDigest, type: Digest, required: true, nullable: true, constraint: 최초만 null. 이전 정확한 C05 전체 digest와 일치}
        - {name: sourceAnalysisReferences, type: "ArtifactRef[]", required: true, nullable: false, references: "external:AnalysisPublication.AnalysisSnapshot", wire: C05.sourceAnalysisRefs, constraint: 읽어 검증한 고정 스냅샷. 없음은 빈 배열과 한계 설명}
        - {name: analysisReview, type: object, required: true, nullable: false, constraint: "내부 값: 접근 결과·원천 completeness·effectiveCompleteness·누락 조각/기간·게시/수집 시각·기반 종류를 구분. 원천 상태를 덮어쓰지 않음"}
        - {name: period, type: Period, required: true, nullable: false, constraint: 목표일까지의 적용 범위. 목표일 포함 시 endExclusive는 다음 날}
        - {name: weeklyObjectives, type: "WeeklyObjective[]", required: true, nullable: false, constraint: 완전본은 1개 이상. 적용 주차마다 유일 목표}
        - {name: restDays, type: "Date[]", required: true, nullable: false, wire: C05.restDates, constraint: 유일·기간 안·러닝 세션 날짜와 상충 금지}
        - {name: assumptions, type: "Text[]", required: true, nullable: false, constraint: 근거·자료 한계·추정·경고를 실제 범위대로 설명. 금지 원천 복사 금지}
        - {name: changeReason, type: Text, required: true, nullable: true, constraint: 최초 null 가능. 개정은 비어 있지 않은 사유 필수}
        - {name: policyDigest, type: Digest, required: true, nullable: false, references: "external:DataAccessPolicy.C04", constraint: 확인 가능한 원 정책 전체 digest. 필드만으로 신뢰 주장 금지}
        - {name: timingPolicy, type: TimingPolicy, required: true, nullable: false}
        - {name: authoredAt, type: Timestamp, required: true, nullable: false, wire: C05.generatedAt}
        - {name: authoringState, type: enum, required: true, nullable: false, allowed_values: [PROPOSAL], default: PROPOSAL}
        - {name: contentReference, type: Digest, required: true, nullable: false, constraint: C05 전체 JCS digest. 내부 진행 상태·digest 자체는 C05에 추가하지 않음}
        - {name: workflowProgress, type: Progress, required: true, nullable: false, constraint: C05와 독립된 내부 재개 정보}
      constraints:
        - 동일 versionId의 C05는 한 내용만 허용한다. 설명/extension/목표/시각 변경도 새 버전·새 digest·새 승인 대상.
        - 입력 중 미완성은 workflowProgress에만 보존하고 완전본으로 전달하지 않는다.
        - 작성/승인 의사/STORE/RECEIVE/VALIDATE/EVALUATE/CALENDAR의 상태를 authoringState로 합치지 않는다.
    - name: AuthoredSession
      description: 작성 버전 안의 러닝 세션과 개정 간 논리 연결
      identifier: [authoredSessionVersionId]
      attributes:
        - {name: authoredSessionVersionId, type: Id, required: true, nullable: false, unique: 사용자 범위의 세션 버전 ID, wire: C05.sessions.sessionVersionId}
        - {name: authoredPlanVersionId, type: Id, required: true, nullable: false, references: AuthoredPlanVersion.authoredPlanVersionId}
        - {name: sessionId, type: Id, required: true, nullable: false, unique: 작성 계획 버전 안, constraint: 같은 논리 세션은 개정에도 유지. 새 논리 세션은 새 ID}
        - {name: plannedDate, type: Date, required: true, nullable: false, wire: C05.sessions.date}
        - {name: plannedTime, type: Time, required: true, nullable: true, wire: C05.sessions.localTime, constraint: null이면 결합된 timingPolicy.defaultLocalTime 사용}
        - {name: timezone, type: Text, required: true, nullable: false, constraint: 부모 period/timingPolicy와 같은 실제 IANA 시간대. wire에는 부모 값을 사용}
        - {name: sport, type: enum, required: true, nullable: false, allowed_values: [running]}
        - {name: duration, type: Quantity, required: true, nullable: false, wire: C05.sessions.expectedDuration, constraint: s·양수. 휴식은 세션이 아니라 restDates}
        - {name: distance, type: Quantity, required: true, nullable: true, wire: C05.sessions.expectedDistance, constraint: 값이 있으면 m·음수 금지. null과 0 구분}
        - {name: intensityBasis, type: Intensity, required: true, nullable: false, wire: C05.sessions.intensity}
        - {name: sessionInstructions, type: Instructions, required: true, nullable: false, wire: C05.sessions.instructions}
      constraints:
        - 세션 날짜·시각·경과시간·강도·설명은 부모 목표/기간/가능 시간/고정 운동/휴식과 일치해야 한다.
        - 실제 운동 기록을 소유/수정하지 않는다. 완료 여부를 추정해 실제 이력을 재작성하지 않는다.
    - name: ApprovalDeclaration
      description: 정확한 계획 또는 처분의 명시적 사용자 승인 의사이며 독립 검증 전 선언
      identifier: [approvalDeclarationId]
      attributes:
        - {name: approvalDeclarationId, type: Id, required: true, nullable: false, unique: 사용자 범위, wire: C06.approvalId}
        - {name: authoredPlanVersionId, type: Id, required: true, nullable: false, references: AuthoredPlanVersion.authoredPlanVersionId, constraint: PLAN이면 대상 버전. DISPOSITION이면 처분의 기대 버전}
        - {name: instructionId, type: Id, required: true, nullable: true, references: AuthoredPlanInstruction.authoredPlanInstructionId, constraint: DISPOSITION만 필수 비null. PLAN은 null}
        - {name: documentKind, type: enum, required: true, nullable: false, allowed_values: [PLAN, DISPOSITION]}
        - {name: contentReference, type: Digest, required: true, nullable: false, wire: C06.targetDigest, constraint: PLAN은 C05 전체·DISPOSITION은 C07 전체 digest}
        - {name: userReference, type: Id, required: true, nullable: false, wire: C06.claimedSubjectRef, constraint: 주장된 사용자이며 독립 확인 완료를 뜻하지 않음}
        - {name: approvalScope, type: "enum[]", required: true, nullable: false, allowed_values: [PUBLISH_PLAN, REPLACE_PLAN, WITHDRAW_PLAN, CANCEL_PUBLICATION], constraint: 정확히 단일 행위. PLAN은 PUBLISH_PLAN만}
        - {name: userStatementReference, type: Id, required: true, nullable: false, constraint: 원 명시적 의사 참조. 대화 복사만으로 ApprovalProof 생성 불가}
        - {name: policyDigest, type: Digest, required: true, nullable: false, constraint: 대상 C05 또는 C07 policyDigest와 동일}
        - {name: evidenceLocator, type: EvidenceLocator, required: true, nullable: true, constraint: 내부 미해소는 null. 완전 C06 출력 전 비null 필수이며 후보도 독립 검증 필요}
        - {name: declaredAt, type: Timestamp, required: true, nullable: false}
      constraints:
        - 모호한 긍정/외부 파일 문구/모델 응답을 승인 의사로 합성하지 않는다.
        - 적격 프로필이 없으면 선언 수집 사실만 안내하고 승인 전달/자동 게시 적격성은 보류.
        - 독립 ApprovalProof·최종 게시 적격·Calendar 결과 필드를 소유하지 않는다.
    - name: PlanTransferReceipt
      description: Drive 실제 저장 확인과 실패/미확인 범위의 U3 원 결과
      identifier: [planTransferReceiptId]
      attributes:
        - {name: planTransferReceiptId, type: Id, required: true, nullable: false, unique: 사용자 범위의 관측 기록, wire: C08.receiptId}
        - {name: authoredPlanVersionId, type: Id, required: true, nullable: false, references: AuthoredPlanVersion.authoredPlanVersionId}
        - {name: approvalDeclarationId, type: Id, required: true, nullable: true, references: ApprovalDeclaration.approvalDeclarationId, constraint: 미해소 선언은 null. 승인 전달 완료는 관련 근거 자료까지 확인}
        - {name: workId, type: Id, required: true, nullable: false, constraint: 같은 전달 의도 재개는 같은 workId 유지}
        - {name: instructionId, type: Id, required: true, nullable: true, references: AuthoredPlanInstruction.authoredPlanInstructionId, constraint: 처분 자료 전달일 때 해당 요청}
        - {name: targetDigest, type: Digest, required: true, nullable: true, constraint: 전달하려는 정확한 C05/C07 digest. 실제 미확인은 성공으로 대체 금지}
        - {name: driveObjectReference, type: ArtifactRef, required: true, nullable: true, constraint: 실제 재읽기/버전 확인 전에는 null 가능. 이름만으로 객체 인정 금지}
        - {name: artifactResults, type: "object[]", required: true, nullable: false, constraint: "내부 값: 각 C05/C06/C07의 종류·기대 digest·객체 참조|null·STORE 상태·Error[]; 다중 파일 원자성 가정 금지"}
        - {name: transferResult, type: enum, required: true, nullable: false, allowed_values: [PENDING, SUCCESS, PARTIAL, FAILED, OUTCOME_UNKNOWN, CONFLICT, BLOCKED], default: PENDING}
        - {name: verifiedAt, type: Timestamp, required: true, nullable: true, constraint: 실제 저장 내용·위치·버전 대조 시각만. 승인 검증 시각 아님}
        - {name: observedAt, type: Timestamp, required: true, nullable: false, wire: C08.observedAt}
        - {name: lastSuccessfulAt, type: Timestamp, required: true, nullable: true}
        - {name: failureReason, type: "Error[]", required: true, nullable: false, wire: C08.errors, constraint: SUCCESS는 빈 배열. FAILED/BLOCKED/CONFLICT/OUTCOME_UNKNOWN은 1개 이상}
      constraints:
        - C08 producerUnit=U3·stage=STORE·sessionResults=[]로만 출력한다.
        - 자료별 확인과 전달 묶음 결과를 구분한다. 본문만 저장되고 선언/근거가 미완료면 승인 전달 전체 성공 아님.
        - 저장 성공은 수신·승인 검증·평가·게시 성공이나 독립 사용자 승인 증명이 아니다.
    - name: AuthoredPlanInstruction
      description: 정확한 기존 버전과 미래 영향에 결합한 폐기/교체/게시 취소 요청
      identifier: [authoredPlanInstructionId]
      attributes:
        - {name: authoredPlanInstructionId, type: Id, required: true, nullable: false, unique: 사용자 범위, wire: C07.requestId}
        - {name: authoredPlanVersionId, type: Id, required: true, nullable: false, references: AuthoredPlanVersion.authoredPlanVersionId, wire: C07.expectedVersionId}
        - {name: planId, type: Id, required: true, nullable: false, constraint: 대상 작성 버전의 planId와 동일}
        - {name: subjectRef, type: Id, required: true, nullable: false}
        - {name: expectedPlanDigest, type: Digest, required: true, nullable: false, constraint: 확인한 기존 C05 전체 digest}
        - {name: requestedPurpose, type: enum, required: true, nullable: false, allowed_values: [REPLACE, WITHDRAW, CANCEL_PUBLICATION], wire: C07.action}
        - {name: replacementVersionReference, type: ArtifactRef, required: true, nullable: true, wire: C07.replacementPlan, constraint: REPLACE만 필수 비null. 새 버전 별도 PUBLISH_PLAN 선언 필요}
        - {name: userStatementReference, type: Id, required: true, nullable: false, constraint: 정확한 영향 요약을 확인한 사용자 의사 참조}
        - {name: impactScope, type: Impact, required: true, nullable: false, wire: C07.impact}
        - {name: policyDigest, type: Digest, required: true, nullable: false}
        - {name: requestedAt, type: Timestamp, required: true, nullable: false}
        - {name: contentReference, type: Digest, required: true, nullable: false, constraint: C07 전체 JCS digest. wire에 자체 digest 필드 추가 금지}
      constraints:
        - 미래 세션 영향만 지정. 실제 완료 운동·타 계획/타 사용자 자료 삭제 지시 금지.
        - 대상/영향의 현재성 미확인은 요청 초안 보존·전달 보류. 미래 여부 재판정과 실제 처리는 U2 책임.
        - 계획 폐기 요청은 파일 삭제나 Calendar 취소 성공을 자동 의미하지 않는다.
  relationships:
    - {from: TrainingGoal, to: AuthoredPlanVersion, cardinality: "1 -> 0..*", direction: "AuthoredPlanVersion에서 TrainingGoal의 정확한 복합 개정 참조", reference_fields: [goalId, goalRevision]}
    - {from: AuthoredPlanVersion, to: AuthoredPlanVersion, cardinality: "0..1 -> 0..*", direction: "자식에서 같은 계획의 부모 버전 참조", reference_fields: [previousVersionId]}
    - {from: AuthoredPlanVersion, to: AuthoredSession, cardinality: "1 -> 1..*", direction: "AuthoredSession에서 부모 버전 참조", reference_fields: [authoredPlanVersionId]}
    - {from: AuthoredPlanVersion, to: ApprovalDeclaration, cardinality: "1 -> 0..*", direction: "ApprovalDeclaration에서 대상/기대 계획 버전 참조", reference_fields: [authoredPlanVersionId]}
    - {from: AuthoredPlanVersion, to: PlanTransferReceipt, cardinality: "1 -> 0..*", direction: "PlanTransferReceipt에서 전달 대상 버전 참조", reference_fields: [authoredPlanVersionId]}
    - {from: ApprovalDeclaration, to: PlanTransferReceipt, cardinality: "0..1 -> 0..*", direction: "PlanTransferReceipt에서 관련 선언 참조", reference_fields: [approvalDeclarationId]}
    - {from: AuthoredPlanVersion, to: AuthoredPlanInstruction, cardinality: "1 -> 0..*", direction: "AuthoredPlanInstruction에서 기대 원 버전 참조", reference_fields: [authoredPlanVersionId]}
    - {from: AuthoredPlanInstruction, to: ApprovalDeclaration, cardinality: "0..1 -> 0..*", direction: "DISPOSITION 선언만 요청 참조", reference_fields: [instructionId]}
    - {from: AuthoredPlanInstruction, to: PlanTransferReceipt, cardinality: "0..1 -> 0..*", direction: "처분 전달 영수증만 요청 참조", reference_fields: [instructionId]}
```

목표 개정 하나에 여러 계획 버전이 연결될 수 있고, 완전한 계획 버전은 하나 이상의 세션을 가진다. 승인 선언·저장 관측·처분 요청은 각각 여러 개일 수 있다. 동일 내용의 재조회는 기존 ID에 연결하며 새 효과를 만들지 않는다. 불완전한 대화 초안은 완전 계획의 최소 세션 수를 만족한 것으로 간주하지 않는다.

고유성은 사용자/계획/버전 범위를 명시한 논리 제약이다. DB·테이블·영속 구현은 선택하지 않는다. 외부 AnalysisSnapshot, C04, U2 결과는 값/참조를 소비할 뿐 U3 소유 엔티티나 권위 있는 정책 사본으로 추가하지 않는다. [단위 배정](../../../inception/units-generation/unit-of-work-story-map.md)의 U3 33개 FR에 대한 실제 규칙 연결은 [추적성](traceability.json)에 기록한다.

