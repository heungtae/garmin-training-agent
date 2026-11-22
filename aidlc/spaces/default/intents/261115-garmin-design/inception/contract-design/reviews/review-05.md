## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-11-21T21:31:08Z
**Iteration:** 1
**Verdict Dictated:** no

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Major | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > C04 grants.allowedFieldPaths 및 C03 activities.metrics / Common.Metric | 서비스별 일부 지표만 공유할 때 사용할 교환 표현이 닫히지 않았다. 날짜·종목·거리만 허용한 C04는 스키마를 통과하지만 C03의 운동은 duration·pace·speed·heartRate까지 필수다. 비허용 duration을 생략하면 required 오류이며, Metric.state에는 정책상 비공개를 나타낼 값도 없다. 실제 수집한 값을 missing/not_collected로 바꾸면 수집 사실과 공유 제한이 섞인다. 또한 activity.intensity·summary.totals 같은 정책 이름을 실제 JSON 필드에 매핑하는 규칙이 없어 U2와 U3가 서로 다른 공유 범위를 적용할 수 있다. CR07의 확인 불가 시 보류는 안전하지만, 정상적으로 일부 필드만 허용한 사용자의 자료 전달은 구현자가 규칙을 추가해야 한다. | 정책 이름과 실제 교환 필드의 대응표, 필수 식별/메타데이터의 전송 조건, 비허용 지표의 생략 또는 비공개 표현을 공통 명세에 정의한다. 거리만 허용하고 시간·심박은 실제 수집된 합성 사례로 생산자와 소비자가 같은 표현·차단 결과를 얻는지 확인한다. | Resolved (reviewer) |
| R-02 | Major | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > C03 detailArtifacts 및 CR03 출처/완전성 | 상세 자료와 기간별 탐색의 참조 대상 본문이 정의되지 않았다. detailArtifacts의 원소는 위치·버전·digest만 가진 ArtifactRef이며, 대상이 C03인지 별도 형식인지, 어떤 기간/운동 범위를 담당하는지, 분할 시 중복·누락·순환과 완결을 어떻게 판별하는지 정해져 있지 않다. 합성 ANALYSIS도 detailArtifacts가 빈 경우만 보여 준다. CR03은 상세 참조와 완전성 대조를 요구하지만 소비자가 검증할 대상을 명세하지 않아, FR4.1~4.4의 상세·기간별 자료 탐색을 두 단위가 독립 구현하기 어렵다. | 상세 파일이 따를 등록 스키마와 참조 관계를 고정하고, 범위·분할·완결·중복 처리 규칙을 정의한다. 상세 참조가 있는 정상 사례와 참조 유실·누락·중복 사례를 추가하고 요약/상세의 집계 일치 및 PARTIAL 판정 조건을 명시한다. | Resolved (reviewer) |
| R-03 | Minor | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > C04 공유 투영과 필드 대응 > 생산자와 소비자 적용 순서 2·5 | 2번은 projection.allowedFieldPaths가 해당 grant의 분석 필드 전체와 정확히 같아야 한다고 정하지만, 5번은 경로별 허용 범위의 교집합으로 새 투영을 만드는 분기를 허용한다. Drive는 거리·시간, ChatGPT는 거리만 허용한 합성 정책에서 교집합 투영은 스키마를 통과하지만 Drive grant와의 동일성 검사에서 PERMISSION_DENIED가 된다. 전송 보류라는 대안은 유효하므로 금지 자료 전송으로 이어지지는 않지만, 명시한 교집합 생성 분기의 판정이 일치하지 않는다. | 교집합 투영을 사용할 때의 경로별 대조 규칙을 명시한다. 각 grant의 허용 범위 안에 있는 공통 공개 집합을 검사하도록 규칙을 맞추거나, 현재 버전에서는 허용 집합이 다르면 보류한다고 통일하고 Drive/ChatGPT 허용 범위가 다른 합성 사례를 추가한다. | Resolved (reviewer) |
| R-04 | Minor | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > 합성 적합성 사례와 검증 한계 > fixtures의 ANALYSIS·ANALYSIS_DISTANCE_ONLY·ANALYSIS_PARTITIONED·DETAIL_0·DETAIL_1 | 계산값 8개의 calculationBasis가 새 GTA-NUMERIC-1의 필수 근거 규칙을 아직 반영하지 않는다. 예를 들어 페이스는 `1200s / 2km`, 합계는 `합성 원천 합계`만 기록하여 프로필 식별자·원천 개정·정확 합계 또는 최종 반올림 구분이 빠져 있다. 값과 구조는 맞지만 이 자료를 전체 수치 부합의 정상 입력으로 재사용하면 새 규범과 충돌한다. | 최초 고정 릴리스 전에 이 문서의 계산값 근거를 새 규칙에 맞추고 연쇄 참조 digest를 갱신한다. 수치 부합 검사에서 정상 fixture의 근거도 확인하고, 근거 누락 음성 사례를 추가한다. | New |

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| Python Fraction 기반 NUM-01~16 독립 재계산 | PASS: 16/16 | 정확한 유리수 연산으로 반복소수·양방향 HALF_EVEN·분모 0·30자리 경계·양수의 0 반올림 거절·18자리 정확 합계·원천에서 페이스 재계산의 문서 기대값을 확인했다. 제품 구현 실행은 아니다. |
| Python jsonschema Draft202012Validator 및 referencing | PASS: 메타스키마 12개, 참조 146개, 구조 사례 54/54 | 고정 registry에서 참조를 해결하고 형식 검사와 사례별 치환 후 expectedSchema를 대조했다. expectedGate와 23개 semanticCases의 제품 실행 결과는 검증하지 않았다. |
| 읽기 전용 문서 링크·계산 근거 검사 | 상대 문서 링크 PASS; 계산값 근거 8/8에 프로필 식별자 누락 | 링크 대상은 존재한다. 근거 누락은 위 Minor finding의 증거이며 JSON Schema 구조 통과와 의미 부합은 구별된다. |
| 상류 요구사항 및 단위 경계 대조 | PASS: 검토 범위 내 모순 없음 | FR2.7·FR2.9·FR4.3·FR4.6~8의 원천 보존·재현성·비수치 상태 구분과 부합하며 U1 소유 및 U2/U3 독립 부합 경계를 유지한다. 단계가 지정한 별도 검증 명령은 없다. |

### Summary

정확 원천·합계와 유리수 중간값을 유지하고 파생값에만 최종 6자리 HALF_EVEN을 적용하는 규칙 및 NUM-01~16의 기대값은 일관된다. 합성 자료의 근거 표기를 보완할 경미한 항목이 있으며, 후속 설계 동기화·실제 Rust/ChatGPT 계산 도구 부합·외부 연동 적격성은 완료된 것으로 판단하지 않았다.
