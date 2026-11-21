## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-11-18T01:04:54Z
**Iteration:** 1
**Verdict Dictated:** no

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Major | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > C04 grants.allowedFieldPaths 및 C03 activities.metrics / Common.Metric | 서비스별 일부 지표만 공유할 때 사용할 교환 표현이 닫히지 않았다. 날짜·종목·거리만 허용한 C04는 스키마를 통과하지만 C03의 운동은 duration·pace·speed·heartRate까지 필수다. 비허용 duration을 생략하면 required 오류이며, Metric.state에는 정책상 비공개를 나타낼 값도 없다. 실제 수집한 값을 missing/not_collected로 바꾸면 수집 사실과 공유 제한이 섞인다. 또한 activity.intensity·summary.totals 같은 정책 이름을 실제 JSON 필드에 매핑하는 규칙이 없어 U2와 U3가 서로 다른 공유 범위를 적용할 수 있다. CR07의 확인 불가 시 보류는 안전하지만, 정상적으로 일부 필드만 허용한 사용자의 자료 전달은 구현자가 규칙을 추가해야 한다. | 정책 이름과 실제 교환 필드의 대응표, 필수 식별/메타데이터의 전송 조건, 비허용 지표의 생략 또는 비공개 표현을 공통 명세에 정의한다. 거리만 허용하고 시간·심박은 실제 수집된 합성 사례로 생산자와 소비자가 같은 표현·차단 결과를 얻는지 확인한다. | Resolved (reviewer) |
| R-02 | Major | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > C03 detailArtifacts 및 CR03 출처/완전성 | 상세 자료와 기간별 탐색의 참조 대상 본문이 정의되지 않았다. detailArtifacts의 원소는 위치·버전·digest만 가진 ArtifactRef이며, 대상이 C03인지 별도 형식인지, 어떤 기간/운동 범위를 담당하는지, 분할 시 중복·누락·순환과 완결을 어떻게 판별하는지 정해져 있지 않다. 합성 ANALYSIS도 detailArtifacts가 빈 경우만 보여 준다. CR03은 상세 참조와 완전성 대조를 요구하지만 소비자가 검증할 대상을 명세하지 않아, FR4.1~4.4의 상세·기간별 자료 탐색을 두 단위가 독립 구현하기 어렵다. | 상세 파일이 따를 등록 스키마와 참조 관계를 고정하고, 범위·분할·완결·중복 처리 규칙을 정의한다. 상세 참조가 있는 정상 사례와 참조 유실·누락·중복 사례를 추가하고 요약/상세의 집계 일치 및 PARTIAL 판정 조건을 명시한다. | Resolved (reviewer) |
| R-03 | Minor | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > C04 공유 투영과 필드 대응 > 생산자와 소비자 적용 순서 2·5 | 2번은 projection.allowedFieldPaths가 해당 grant의 분석 필드 전체와 정확히 같아야 한다고 정하지만, 5번은 경로별 허용 범위의 교집합으로 새 투영을 만드는 분기를 허용한다. Drive는 거리·시간, ChatGPT는 거리만 허용한 합성 정책에서 교집합 투영은 스키마를 통과하지만 Drive grant와의 동일성 검사에서 PERMISSION_DENIED가 된다. 전송 보류라는 대안은 유효하므로 금지 자료 전송으로 이어지지는 않지만, 명시한 교집합 생성 분기의 판정이 일치하지 않는다. | 교집합 투영을 사용할 때의 경로별 대조 규칙을 명시한다. 각 grant의 허용 범위 안에 있는 공통 공개 집합을 검사하도록 규칙을 맞추거나, 현재 버전에서는 허용 집합이 다르면 보류한다고 통일하고 Drive/ChatGPT 허용 범위가 다른 합성 사례를 추가한다. | New |

> R-01 Reviewer note: Common.Metric의 withheld는 quantity·sourceRef·calculationBasis를 모두 null로 고정한다. C04의 공유 투영 표는 정책 이름과 실제 JSON 필드, pace/speed의 거리·시간 의존성, 심박 별도 허용을 정의한다. analysis.metadata·summary.period·activity.date·activity.sport의 명시적 동의를 최소 조건으로 두며 미충족 시 전체 전송을 보류한다. 합성 원천에 시간 1200s·심박 145bpm이 존재하는 경우에도 거리만 허용한 투영에서 해당 값과 출처·근거가 제거되는 검사를 통과했다.

> R-02 Reviewer note: C03의 등록 Detail 스키마와 DetailRef가 본문·계보·기간·조각 번호·개수를 고정한다. 상세 파일·분할·완결 규칙은 고정 버전/digest, 중첩 참조 금지, 전체 운동 ID 유일성, 정렬, 범위, 누락 시 PARTIAL, 오류 시 채택 보류, 원천/수신 완전성 분리와 종목별 합계 대조를 명세한다. 정상 두 조각 및 누락·중복·해시·합계·계보·범위 오류를 포함하는 합성 의미 검사가 통과했다.

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| python3 aidlc/spaces/default/intents/261115-garmin-design/.aidlc-engine/checks/check_contract.py | PASS: schema_roots=12, resolved_refs=146, structural_cases=54, semantic_cases=20, strict_parse_cases=7, profiles=5, hashes=pass, collected_vs_withheld_projection=pass | 등록 스키마·참조·합성 자료·정책 투영·상세 분할의 문서 정합성을 확인했다. real_api_or_consent_qualification=false다. |
| 독립 합성 반례: 읽기 전용 runpy 실행 후 메모리 안에서 Drive grant에 activity.duration을 추가하고 ChatGPT grant는 거리만 유지 | schemaValid=true, 교집합 투영의 의미 검사 결과 PERMISSION_DENIED | Drive 대상 projection에 더 좁은 공통 집합을 적용하면 정확한 집합 동일성 조건에서 거절됨을 확인했다. 신규 Minor finding의 재현이며 실제 전송은 수행하지 않았다. |
| 상류 문서 및 계약 수동 대조 | U1 명세 소유·U2/U3 소비 경계, 3개 단위, 승인/정책 신뢰 차단, 원격 OpenAI 초기 대상·Ollama 제외·로컬/사설 대체 제공자 미정 유지 | 기존 책임과 P0 검증 조건의 축소 또는 새 실행 권한 부여를 발견하지 않았다. |

### 검증 한계

이 검토는 지정 산출물·Q&A·단계 정의와 전달된 상류 입력에 대한 단일 자문 검토다. 제품 구현, 실제 Garmin/Drive/GitHub/Calendar/OpenAI 호출, ChatGPT 지원 환경, 승인 발급·검증, 정책 현재성·철회와 의학적 적격성은 검증하지 않았다. 산출물은 이 항목들을 미해소 차단 조건으로 유지한다. 합성 검사기는 제한된 fixture 영역의 digest와 의미 규칙을 검사하며 범용 JCS 구현 또는 제품 검증기를 인증하지 않는다.

### Summary

부분 공유의 교환 표현과 상세 자료의 검증 대상이 정의되어 두 기존 Major finding은 해결되었다. 경로별 허용 집합이 다른 경우의 교집합 규칙에는 경미한 정리가 필요하지만 보류 동작이 명시되어 있으며, 문서 설계를 이어 갈 수 있는 상태다.
