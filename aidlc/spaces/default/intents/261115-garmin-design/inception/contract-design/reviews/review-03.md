## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-11-18T01:14:33Z
**Iteration:** 1
**Verdict Dictated:** no

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Major | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > C04 grants.allowedFieldPaths 및 C03 activities.metrics / Common.Metric | 서비스별 일부 지표만 공유할 때 사용할 교환 표현이 닫히지 않았다. 날짜·종목·거리만 허용한 C04는 스키마를 통과하지만 C03의 운동은 duration·pace·speed·heartRate까지 필수다. 비허용 duration을 생략하면 required 오류이며, Metric.state에는 정책상 비공개를 나타낼 값도 없다. 실제 수집한 값을 missing/not_collected로 바꾸면 수집 사실과 공유 제한이 섞인다. 또한 activity.intensity·summary.totals 같은 정책 이름을 실제 JSON 필드에 매핑하는 규칙이 없어 U2와 U3가 서로 다른 공유 범위를 적용할 수 있다. CR07의 확인 불가 시 보류는 안전하지만, 정상적으로 일부 필드만 허용한 사용자의 자료 전달은 구현자가 규칙을 추가해야 한다. | 정책 이름과 실제 교환 필드의 대응표, 필수 식별/메타데이터의 전송 조건, 비허용 지표의 생략 또는 비공개 표현을 공통 명세에 정의한다. 거리만 허용하고 시간·심박은 실제 수집된 합성 사례로 생산자와 소비자가 같은 표현·차단 결과를 얻는지 확인한다. | Resolved (reviewer) |
| R-02 | Major | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > C03 detailArtifacts 및 CR03 출처/완전성 | 상세 자료와 기간별 탐색의 참조 대상 본문이 정의되지 않았다. detailArtifacts의 원소는 위치·버전·digest만 가진 ArtifactRef이며, 대상이 C03인지 별도 형식인지, 어떤 기간/운동 범위를 담당하는지, 분할 시 중복·누락·순환과 완결을 어떻게 판별하는지 정해져 있지 않다. 합성 ANALYSIS도 detailArtifacts가 빈 경우만 보여 준다. CR03은 상세 참조와 완전성 대조를 요구하지만 소비자가 검증할 대상을 명세하지 않아, FR4.1~4.4의 상세·기간별 자료 탐색을 두 단위가 독립 구현하기 어렵다. | 상세 파일이 따를 등록 스키마와 참조 관계를 고정하고, 범위·분할·완결·중복 처리 규칙을 정의한다. 상세 참조가 있는 정상 사례와 참조 유실·누락·중복 사례를 추가하고 요약/상세의 집계 일치 및 PARTIAL 판정 조건을 명시한다. | Resolved (reviewer) |
| R-03 | Minor | aidlc/spaces/default/intents/261115-garmin-design/inception/contract-design/contract-summary.md > C04 공유 투영과 필드 대응 > 생산자와 소비자 적용 순서 2·5 | 2번은 projection.allowedFieldPaths가 해당 grant의 분석 필드 전체와 정확히 같아야 한다고 정하지만, 5번은 경로별 허용 범위의 교집합으로 새 투영을 만드는 분기를 허용한다. Drive는 거리·시간, ChatGPT는 거리만 허용한 합성 정책에서 교집합 투영은 스키마를 통과하지만 Drive grant와의 동일성 검사에서 PERMISSION_DENIED가 된다. 전송 보류라는 대안은 유효하므로 금지 자료 전송으로 이어지지는 않지만, 명시한 교집합 생성 분기의 판정이 일치하지 않는다. | 교집합 투영을 사용할 때의 경로별 대조 규칙을 명시한다. 각 grant의 허용 범위 안에 있는 공통 공개 집합을 검사하도록 규칙을 맞추거나, 현재 버전에서는 허용 집합이 다르면 보류한다고 통일하고 Drive/ChatGPT 허용 범위가 다른 합성 사례를 추가한다. | Resolved (reviewer) |

> R-03 Reviewer note: contract-summary.md의 C03 공유 투영과 필드 대응 > 생산자와 소비자 적용 순서 2·5가 모두 grant의 분석용 9개 이름을 추출한 집합과 최종 projection의 정확한 동일성을 요구한다. 한 경로라도 더 넓거나 좁으면 교집합 생성 없이 전체 신규 전송을 PERMISSION_DENIED로 보류한다. S21의 동일 집합은 COMPLETE, S22·S23의 더 넓거나 좁은 집합은 PERMISSION_DENIED임을 실행 확인했다. 실제 경로는 신뢰된 설정·실제 연결에서 결정하고 정책 자동 변경도 금지하므로 기존 모순이 해소됐다.

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| python3 aidlc/spaces/default/intents/261115-garmin-design/.aidlc-engine/checks/check_contract.py | PASS, 종료 코드 0. 스키마 12개·참조 146개·구조 사례 54개·의미 사례 23개·엄격 파싱 사례 7개·프로필 5개. hashes 및 collected_vs_withheld_projection 통과. | S21~S23을 포함한 합성 문서 정합성을 확인했다. real_api_or_consent_qualification=false이며 실제 승인·정책 현재성·외부 API 적격성을 증명하지 않는다. |
| 읽기 전용 독립 추가 반례 5개, 동일 검사 함수에 메모리 내 합성 입력 적용 | PASS. 분석 집합이 같고 비분석 goal.target만 추가된 경로는 COMPLETE. Drive grant 누락·동일 튜플 중복·대상 불일치·두 번째 경로의 더 넓은 분석 집합은 각각 PERMISSION_DENIED. | 분석용 이름만 추출하는 규칙과 정확한 경로별 grant 선택이 맞물린다. 이 추가 실행도 제품 구현이나 실제 동의 검증이 아니다. |
| 지정 상류 문서와 변경 규범 대조 | 변경 범위에서 새로운 불일치 없음. | U1 명세 소유, U2 원 정책 소유, U3의 확인 불가 시 신규 전송 보류, 독립 자체 검증 경계를 유지한다. |

### Summary

R-03은 수정됐으며 이번 사용자 요청 변경 범위에서 새 finding은 확인되지 않았다. Ollama 제외·원격 OpenAI 초기 대상·로컬/사설 대체 제공자 미정 및 기존 승인·정책 최신성·외부 연동 차단 조건을 유지한 문서 설계에 대한 판단이며, 실제 제품 활성화나 연동 성공의 판정은 아니다.
