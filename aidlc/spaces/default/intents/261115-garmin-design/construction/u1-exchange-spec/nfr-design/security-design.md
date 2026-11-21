# U1 공통 교환 명세 — 보안·품질 설계

- 단위: U1 `u1-exchange-spec` (`spec`), Standard 깊이/검증 전략.
- 대상: 승인된 상세 NFR 22개를 구현자가 적용할 수 있는 14개 해법과 검사·증거 인계로 연결한다. U1은 명세·공통 합성 사례의 소유자이며 제품 검증기나 외부 실행 권한의 발급자가 아니다.
- 이 문서는 기존 Common·C01~C08/기능 모델의 필드·규칙·기대값을 참조한다. 실제 검증 도구·실행 한도 값·정밀도·tzdb 선정과 구현은 U2/U3에 남는다.

## Sources

| 입력 | 이 설계에 적용한 내용 |
|---|---|
| [확인한 NFR Design 답변](nfr-design-questions.md) | ARTIFACT-ONLY 입력, 판정 단계 분리·범위·미해소 조건 유지 |
| [security-requirements.md](../nfr-requirements/security-requirements.md) | 상세 NFR 22개, 필수 유한 검사 집합·0건/전수 일치 목표와 실제 책임 |
| [tech-stack-decisions.md](../nfr-requirements/tech-stack-decisions.md) | U1-TD-001~006: UTF-8 JSON·고정 Schema·전체 JCS·독립 부합·도구 적격성 |
| [functional-spec.md](../functional-design/functional-spec.md) | WF1~WF7의 선행조건/상태 전이, FD01~FD26의 하위 경계 조건 |
| [contract-summary.md](../../../inception/contract-design/contract-summary.md) | Common·C01~C08, CR01~CR12, U1 fixture와 V/N/B/T/S의 기존 기대값 |
| [rules.md](../functional-design/rules.md)·[entities.md](../functional-design/entities.md) | BR1.1~BR7.4, ConformanceAssessment·ConsumerBinding 등 기존 모델 |
| [components.md](../../../inception/domain-design/components.md) | 원 정책·작성·승인/평가·Calendar·결과 생산자의 소유 경계 |

## 신뢰 경계와 설계 결정

| 경계 | 신뢰 가능한 기준과 불신 자료 | 통제·출력과 책임 |
|---|---|---|
| 설치/배포 → 명세 선택 | 소비자가 검증한 bootstrap/registry 고정값만 기준. 수신 RELEASE의 자기 digest·URL은 증명 아님 | U1-SD-01. U1은 불변 정의/사례, U2/U3는 실제 배포 신뢰와 독립 고정/검사 소유 |
| 수신 바이트 → 구조/내용/의미 | 파일명·본문·마크업·수식·URL·LLM 지시·extensions·profileId는 데이터 | U1-SD-02~03·08~10. 등록 기준으로만 검사하며 데이터로 검증기·명령·권한을 바꾸지 않음 |
| 교환 정책/승인 → 실제 동의/인간 의도 | C04 ACTIVE·C06·VERIFIED·해시·파일 소유는 불신 선언 | U1-SD-04~07·11. 실제 권위는 U2/U3의 독립 적격 확인만으로 성립. 미해소면 전송/효과 보류 |
| 외부 효과 → 결과/안내 | 응답 ID·과거 receipt·다른 생산자 성공은 현재 효과의 증명 아님 | U1-SD-12~13. 원 실행 소유자가 대상/버전/세션별 실제 결과를 확인하고 U3는 적격 읽기 전 성공 안내 보류 |
| 합성 검사 → 소비자 부합 | 기대값과 실제 관찰, 문서 정합과 제품 의미/실행은 서로 다름 | U1-SD-14. 고정 릴리스/수행 범위만 인용하며 externalAuthority=NOT_ESTABLISHED 유지 |

선택 이유는 검증 기준의 입력 오염과 단계 간 권한 승격을 동시에 막기 위해서다. 전체 내용 결합·고정 registry·실패 시 보류를 적용하며, 원격 최신 명세 자동 채택·느슨한 필드 무시·선택 필드 해시·자동 교집합·한 성공 상태로의 통합을 채택하지 않는다. 그 결과 미적격 도구/외부 경로는 계속 차단되며 소비자별 실제 검증 비용이 남는다. 기존 U1-TD-001~006과 CD-ADR-001~003을 구체화하는 선택이며 새 제품/인프라 기술 결정은 아니다.

## 검사 의존성과 오류 우선순위

아래 순서는 WF1/WF2와 CR01~CR12의 **선행조건**이다. 전역 오류 코드 순위를 새로 만들지 않는다. 앞 단계가 실패/미해소이면 의존하는 뒤 단계는 수행 완료로 표시하지 않는다. 검사 보고에서 미수행 scope는 NOT_RUN, 증거가 없는 바인딩은 UNASSESSED로 남긴다. 독립적으로 관찰한 여러 차단은 각 사유를 보존하며 대표 코드 하나가 나머지 차단을 해소하지 않는다.

| 순서·선행조건 | 처리·해법 | 통과가 뜻하는 범위 / 실패 처리 |
|---|---|---|
| 0. 신뢰된 설치 기준 존재 | U1-SD-01: bootstrap/registry·RELEASE·실제 정의/fixture 대조 | 명세 선택 후보만 생성. VERSION_UNSUPPORTED·CONTENT_MISMATCH·DATA_INVALID 또는 도구 미적격은 선택 보류 |
| 1. 실제 대상/루트·권한·MIME·유한 프로필 확인 | U1-SD-02: 바이트/깊이 한도 적용과 엄격 파싱 | 단일 JSON 객체 확보만 의미. DATA_INVALID·RESOURCE_LIMIT·DEPENDENCY_UNQUALIFIED이면 자동 복구 없이 중단 |
| 2. 등록 버전/종류만 선택 | U1-SD-01~02: 등록 Schema와 로컬 참조·필수/null/조건 검사 | 구조만 적합. 미지 버전은 VERSION_UNSUPPORTED, 구조 오류는 DATA_INVALID |
| 3. 전체 JSON/고정 참조 확보 | U1-SD-03: JCS/SHA-256·ArtifactRef·내용/계보 대조 | 동일 내용 후보만 생성. CONTENT_MISMATCH/REMOTE_CONFLICT를 의미/승인 통과로 완화하지 않음 |
| 4. 구조/내용 선행조건 충족 | U1-SD-08~11: 수치·시간·분할·전체 계획·선언 대응의 의미 검사 | 값/범위 적합만 의미. C03 Detail 처리의 아래 특칙과 계획 전체 보류를 적용 |
| 5. 각 신규 전송/효과 직전 | U1-SD-04~07·11: 현재 원 정책·전체 실제 경로·출력·정확한 승인/안전 독립 확인 | 정책/승인 적격성 미해소는 관련 전송/게시/변경/취소 보류. 합성 조건으로 충족 처리 금지 |
| 6. 적격 실행 소유자의 실제 효과 후 | U1-SD-12~13: 원 의도/대상 대조·독립 결과/오류 | 실제 확인한 생산자/단계/세션만 표현. 응답 유실 OUTCOME_UNKNOWN, 일부 성공 PARTIAL |
| 7. 각 검사/결과의 안전한 증거 확보 | U1-SD-14: 범위별 기대/관찰·한계 인계 | 수행 범위의 부합만 인용. 입력/정책/릴리스/소비자/검사 범위 변경은 기존 증거 보존 후 새 검사 |

생산 시에는 현재 동의와 실제 경로 확인(U1-SD-04~05) 뒤 허용 투영(U1-SD-06)을 만들고 수치/분할 자료를 구성한다. 수신자는 등록 구조·고정 내용부터 검사한 뒤 같은 의미/정책 규칙을 다시 적용한다. 실제 신규 전송/효과 직전에는 다시 현재성·철회·계보·안전을 확인한다. 검사 당시의 합격을 다음 요청의 상시 권한으로 저장하지 않는다.

C03 Detail은 WF3/BR3.3의 특칙을 적용한다. 등록 fragment 대상으로 고정 object/version을 확보하고 엄격 파싱·JCS digest 대조·Detail 구조/의미를 검사한다. 유효 descriptor/상세 누락·읽기 실패·버전 미확인·digest 실패는 조각 미사용과 SOURCE_INCOMPLETE/PARTIAL이다. 읽은 본문의 구조/계보/중복/범위/집계 모순이 확인되면 DATA_INVALID로 스냅샷 채택을 보류한다. 무효를 PARTIAL로 낮추지 않으며 전체 대상 C05/C07의 CONTENT_MISMATCH와 이 조각 전달 실패를 혼동하지 않는다.

## U1-SD-01 — 불변 명세 묶음 선택

연결: NFR5.1; BR1.1·BR7.4; CR01; WF1; U1-TD-002·004·006.

**입력/선행조건:** 소비자의 검증된 설치/배포 경로에서 고정한 Common·C01/C02 bootstrap·registry와 후보 RELEASE. 선택한 도구가 Draft 2020-12와 등록 참조를 지원해야 한다.

**처리/출력:** Common·C01~C08의 정의 9개와 C03 Detail fragment를 고정 로컬 registry에서 해석한다. C02의 C01 참조 등 모든 등록 참조가 해석되어야 한다. RELEASE의 schemaVersion/commonDigest와 C03~C08 각각 한 번의 schemaId/schemaDigest를 실제 정의와 대조한다. fixturesDigest는 ANALYSIS·POLICY·PLAN·DECLARATION·DISPOSITION·RECEIPT·POLICY_DISTANCE_ONLY·ANALYSIS_DISTANCE_ONLY·ANALYSIS_PARTITIONED·DETAIL_0·DETAIL_1의 **이름→전체 내용 객체 11개**에 대해 대조한다. RELEASE는 별도 C01/C02 구조 fixture이며 이 digest에서 제외한다. 출력은 고정 릴리스와 선택된 정의에 대한 부합 후보이고 제품 활성화 허가가 아니다.

**실패/차단:** 미등록 버전은 VERSION_UNSUPPORTED, 모순된 계약 목록은 DATA_INVALID, 실제 내용 digest 불일치는 CONTENT_MISMATCH다. 참조/도구 미적격은 DEPENDENCY_UNQUALIFIED로 관련 검사를 보류한다. 원격 URL 다운로드·새 버전 자동 활성화·같은 배포 버전 덮어쓰기는 하지 않는다. 허용 필드/권한·행위·단위·ID·의미·필수 구조 변경은 기존 호환 파괴 검토·새 주요 버전·소비자 합의에 연결하고 공유 확대는 별도 동의를 요구한다.

**필수 검사/확인 지점:** V01~V02·N01·N11·FD01, schema/common/11개 fixture의 각각 변경·누락·중복 변형. 선택한 releaseId/정의/digest 대조 결과와 미해석 참조의 안전한 경로만 인계한다. U1은 고정 기준/기대값, U2/U3는 각각 실제 신뢰 고정·독립 검사·도구 프로필을 소유한다. 소비자 개정 식별의 한계는 U1-SD-14에 남는다.

## U1-SD-02 — 유한 엄격 파싱과 불신 지시 격리

연결: NFR1.2·NFR5.3; BR1.1·BR1.3~BR1.4·BR4.5·BR7.3; CR01; WF2; U1-TD-001·002·005.

**입력/선행조건:** 허용 루트·실제 대상/권한·MIME와 소비자가 선정한 유한 입출력/실행 프로필. 바이트/깊이 한도는 읽기/파싱 전부터 도중까지 적용하고 한도 확인 자체가 실패해도 보류한다. U1은 운영 기본 숫자를 제시하지 않는다.

**처리/출력:** 엄격 UTF-8로 단일 객체 하나만 파싱하며 중복 키를 소실시키기 전에 탐지한다. 선두 단일 BOM·바깥 공백/CRLF만 허용하고 문자열·한국어·인용부호·줄바꿈·불투명 ID는 원문 보존한다. 등록 Schema의 required/null·enum·additionalProperties·allOf/조건·참조를 검사하고 format 검사 지원 여부를 소비자 프로필에 명시한다. 날짜/시간 의미는 U1-SD-09에서 별도 확인한다. 모르는 `extensions.x_*`는 등록 문자열/null 형식만 구조상 허용하며 권한/행동에는 사용하지 않는다. 초기 C03/Detail 자유 확장 전송은 허용하지 않는다.

파일명/본문/URL/마크업/수식·PLAN 설명·오류의 suggestedAction·LLM 응답은 검사 자료로만 취급한다. 등록 별칭과 정확한 objectId/versionRef 외 경로를 탐색하거나 profileId/recordId로 검증 서버·키·명령을 등록하지 않는다. 사람이 읽는 렌더링도 데이터로 이스케이프하며 실제 명령/경로 격리는 소비자 검증 대상이다.

**실패/차단:** 중복 키·잘림·후행 문서·NaN/Infinity·잘못된 UTF-8·루트 비객체·두 BOM은 DATA_INVALID. 한도 초과/미설정은 RESOURCE_LIMIT, 한도 적용/파서 지원 미적격은 DEPENDENCY_UNQUALIFIED로 보류한다. 자동 절단·키 덮어쓰기·수선 뒤 통과시키지 않는다. 파싱 불가 입력은 JSON JCS digest 없이 원시 합성 자료 식별/조건과 기대 거절을 기록한다.

**필수 검사/확인 지점:** T01~T07·N22·B02·FD03~FD04와 잘못된 UTF-8/두 BOM·바이트/깊이 경계/한도 없음·지원 불가, 설명/extension/오류의 불신 지시 변형. 파싱 결과와 구조 결과를 따로 남기고 원문 echo 없이 실패 fieldPath·프로필/사례 참조를 인계한다. U1은 규범/기대값, U2/U3는 실제 파서·한도·경로/명령/출력 격리 소유다. 실제 OS/파일 I/O 검증은 미수행이다.

## U1-SD-03 — 전체 내용 결합과 계보 충돌 보존

연결: NFR5.2·NFR5.4; BR1.2·BR1.4·BR3.4·BR5.2·BR5.4·BR6.3·BR7.3; CR02·CR10·CR11; WF2·WF5~WF6; U1-TD-003.

**입력/처리/출력:** 구조 적합 객체 전체를 RFC8785 JCS로 정규화한 UTF-8 바이트의 SHA-256으로 결합한다. 형식은 `sha256:` 뒤 소문자 64자리 16진수다. 설명·가정·extensions·시각/정책도 포함하며 C06 자체·Markdown·헤더·파일명·원격 수정 시각은 C05 해시에 섞지 않는다. ArtifactRef의 storeAlias/objectId/versionRef/digest와 실제 내용은 각각 대조한다. ID는 1~1024자 불투명 원문으로 유지하고 선행 0·대소문자·Unicode를 정규화/절단하지 않는다.

계획은 previousPlanDigest를 수신자의 현재 확정 계보와 대조한다. 검사 전후 원격 버전/내용 변화, 같은 논리 버전의 다른 내용, 형제 승인 분기·초기 최신 계보 불명·과거 재업로드는 자동 병합/최신 추정 없이 보류한다. 반복 조회는 같은 원 대상/의도/내용의 기존 결과에 연결한다. 유효 세션만 다른 문서/버전에서 추출해 합치지 않는다. 출력은 정확한 내용/계보 후보이며 승인/인증 결과가 아니다.

**실패/차단:** 내용 불일치는 CONTENT_MISMATCH, 동시 변경/현재 계보 충돌은 REMOTE_CONFLICT, ID/중복 구조는 DATA_INVALID다. 이전 유효본/미확인 결과를 보존하고 재처리 전에 원 의도/고정 대상부터 대조한다. 변경한 내용·정책·시각은 새 버전/digest/승인으로 U1-SD-11에 연결한다.

**필수 검사/확인 지점:** B02·N15·N19~N22·FD02·FD04~FD05·FD11·FD13·FD21·FD23·FD25~FD26. 전체 필드 변경/원 ArtifactRef/검사 전후 차이의 안전한 참조를 남긴다. U1은 규약/기대값, U2/U3는 일반 JCS Unicode/수치·잘못된 Unicode 적격성 및 실제 원자 확정/버전 감지를 소유한다. 한정 ASCII·유한 정수·십진 문자열 사례 결과로 일반 JCS 합격이나 강제 종료/원격 손실 방지를 주장하지 않는다.

## U1-SD-04 — 현재 정책과 요청 직전 동의 재확인

연결: NFR2.1·NFR3.3; BR4.1·BR4.3·BR4.5·BR5.4; CR07; WF4.

**입력/처리/출력:** 원 정책 소유자 DataAccessPolicy의 실제 사용자·정책 버전/전체 digest·철회/동의·권한·비공개 대상 및 해당 서비스/목적/대상을 독립 확인한 근거와 C04를 대조한다. C04 ACTIVE/consentRecordRef/verificationRecordRef나 오래된 사본만으로 허용하지 않는다. 이 확인을 매 신규 요청 직전에 수행하고 승인/안전·원 계보 확인과 함께 남은 실행 요청의 선행조건으로 둔다. 출력은 그 요청의 정확한 허용 범위 후보 또는 보류 사유다.

C05~C08도 목적별 필수 업무 묶음/메타데이터의 명시적 동의가 있어야 한다. 필수 필드라는 이유로 자동 동의하거나 문서를 임의 가림/삭제 후 같은 승인을 재사용하지 않는다. 정책 변경은 새 policyDigest·투영·snapshotId/digest 및 관련 새 내용/승인을 거쳐 처음부터 재검사한다. 철회를 발견하면 남은 신규 요청을 중단하고 이미 진행 중/외부 반영/실패/대기를 구분한다.

**실패/차단:** 현재성/신뢰 불명은 POLICY_UNVERIFIED, 오래됨/철회는 POLICY_STALE, 공개/불명 대상·서비스/목적/대상·권한 범위 불일치는 해당 CR07 기대에 따라 PERMISSION_DENIED 등으로 보류한다. 이미 전송 중인 요청 취소나 외부 사본 회수/삭제 성공을 추정하지 않는다.

**필수 검사/확인 지점:** N07·FD02·FD17·FD24와 공개/불명 대상·동의 전/거부/철회·현재성 불명·다른 서비스/목적/대상·C05~C08 업무 grant 누락·신규 요청 직전 정책 변경 변형. 원 정책 확인 시점/대상/digest의 안전한 근거와 차단 범위만 인계한다. U1은 계약/기대값, U2는 원 정책·실제 최소 권한/대상, U3는 해당 환경의 독립 확인을 소유한다. C04 확인 경로 미해소로 U3 관련 실제 신규 전송은 계속 보류다.

## U1-SD-05 — 모든 실제 분석 경로의 동일 허용 집합

연결: NFR3.1; BR4.1~BR4.3; CR07; WF4.

**입력/처리/출력:** 검사할 경로 목록은 신뢰된 전송 설정과 실제 소비 연결로 정하며 저장소와 최종 독자를 모두 포함한다. payload가 제공한 경로 생략 목록을 사용하지 않는다. 각 경로의 정확한 `(service,purpose=ANALYSIS,targetAlias)`에 grant가 하나만 있어야 한다. 그 grant에서 분석용 9개 이름인 analysis.metadata·summary.period·activity.date·activity.sport·activity.distance·activity.duration·activity.intensity·activity.heartRate·summary.totals만 추려 ASCII 정렬한 집합을 projection.allowedFieldPaths와 대조한다. **모든 경로에서 정확히 같은 집합**이어야 다음 투영 검사로 진행한다.

analysis.metadata·summary.period·activity.date·activity.sport 네 항목은 각각 명시 허용이어야 한다. 이 범위가 오프셋 포함 시각·불투명 계보·참조·운동/조각 개수도 공개함을 동의 범위에 포함한다. 더 넓거나 더 좁은 한 경로라도 자동 교집합/합집합을 만들지 않는다. 다른 목적/서비스/대상 grant를 합쳐 대체하지 않는다.

**실패/차단:** grant 누락/중복·최소 네 항목 중 하나 누락·집합 불일치는 PERMISSION_DENIED로 전체 신규 전송 보류다. 경로별 차이를 값/비밀 없이 안내하고 명시적 정책 변경 후 U1-SD-04부터 새 자료로 검사한다.

**필수 검사/확인 지점:** S05·S21~S23·FD17, 최소 네 항목 각각 하나 제거·경로 하나 생략·중복 grant·다른 서비스/목적/대상 변형. 검사한 실제 경로 목록의 안전한 참조와 각 정렬 집합 비교/누락 경로를 인계한다. U1은 집합 규범, U2/U3는 실제 경로 발견·정책/권한 확인을 소유한다. 합성 transportGrants는 실제 연결 증명이 아니다.

## U1-SD-06 — 고정 withheld와 파생 공개 차단

연결: NFR3.2; BR2.1·BR3.6·BR4.4; CR03·CR07; WF3~WF4.

**입력/처리/출력:** 현재 허용 집합이 확인된 후 생산자는 미허용 지표를 수집 유무에 관계없이 고정 슬롯의 withheld로 투영하고 quantity/sourceRef/calculationBasis를 모두 null로 만든다. 수신자도 같은 규칙으로 검사한다. missing/not_collected 등으로 바꾸어 숨긴 값의 수집 여부를 노출하지 않는다. pace/speed는 intensity+distance+duration의 세 허용이 모두 있어야 하며 heartRate는 별도로 확인한다. summary.totals는 독립 동의이고 미허용이면 summaryBySport=[]다. totals 허용이 개별 지표 동의를 추가하지 않는다.

계산 근거·sourceRef·합계·설명·extensions까지 검사하여 숨긴 수치/원천 식별자와 역산 가능한 파생값을 다른 위치로 옮기지 않게 한다. 허용된 메타데이터·계보·시각·개수 자체는 U1-SD-05의 명시 동의 범위로 관리한다.

**실패/차단:** 미허용 슬롯/파생/합계의 노출은 PERMISSION_DENIED. 비공개를 실제 0이나 누락 상태로 치환하여 통과시키지 않는다. 출력 수정으로 승인 대상 내용이 바뀌면 기존 승인 재사용 없이 U1-SD-03·11로 돌아간다.

**필수 검사/확인 지점:** S01~S04·S17~S18·N33·FD18~FD19. 같은 정책 아래 숨긴 원 수치 유무만 다른 두 합성 원천을 비교하여 미허용 슬롯·파생값·설명이 동일한지 확인한다. 원 수치를 보고에 복사하지 않고 비교 대상 경로·차이 건수·기대 판정만 인계한다. U1은 투영 규범, U2/U3는 실제 생성/전송 전체 검사 소유다.

## U1-SD-07 — 허용 출력과 민감성 불명 보류

연결: NFR1.1·NFR4.1·NFR4.2; BR4.4~BR4.5·BR7.4; CR07·CR12; WF2·WF4·WF7.

**입력/처리/출력:** 출력 후보는 등록 Schema 허용 필드와 목적별 동의 범위로만 구성한다. 인증정보/토큰·보호 보관 위치/참조·직접 개인 식별자·GPS/위치 원본/FIT·수면/HRV·통증 자료를 정상 생성물/전송 후보·오류·진단·요약·결과 보고에 넣지 않는다. 별도 동의가 있어도 현재 미등록 민감 필드/기능을 만들지 않는다. constraints·instructions·계산 근거·sourceRef·설명·extensions도 별도 목적/서술 검사 대상으로 삼는다.

구조 필터를 통과해도 금지 자료 포함 여부가 불명확하면 안전한 최소 자료를 확인할 때까지 전송을 보류한다. 승인된 내용을 임의 삭제/가림해서 같은 승인으로 보내지 않는다. 오류는 U1-SD-13의 고정 코드/한국어 안내와 안전한 참조만 생성하고 원 본문·헤더·의심 값을 보간하지 않는다. fieldPath는 검증된 등록 경로 또는 null로 제한하여 공격자가 만든 키 이름의 echo도 피한다. 증거 참조는 합성 사례/안전한 작업·근거 위치만 사용하며 비밀 보관 참조를 사용하지 않는다.

**실패/차단:** 미등록 구조는 DATA_INVALID, 금지 공개는 PERMISSION_DENIED로 해당 출력/전송을 보류한다. 민감성 불명은 안전 확인 완료로 표시하지 않고 같은 보호 경계의 보류 사유/다음 조치를 남긴다. 한정 표식 탐지 통과는 모든 자연어의 민감성 판별이나 의료 안전 보증이 아니다.

**필수 검사/확인 지점:** N05·FD20, POLICY/PLAN/RECEIPT 및 C03/Detail의 필드·자유 서술·extension에 합성 비밀/금지 자료/모호 표현을 넣는 변형. 합성 표식은 **선언된 음성 입력에만** 두고 정상/거절/오류/재처리/보고 경로 전체의 출력 탐지 건수를 확인한다. 보고에는 사례 ID·안전한 경로·건수만 남기고 표식 원문을 복사하지 않는다. U1은 제외/기대값, U2/U3는 실제 목적별 서술 검사·이스케이프·안전 출력 검사를 소유한다. 실제 비밀 저장/암호화 방식은 이 단위에서 선정하지 않는다.

## U1-SD-08 — 상태를 보존하는 정확한 십진/계획 검사

연결: NFR5.6; BR2.1~BR2.2·BR2.4·BR3.6·BR5.1~BR5.3; CR03·CR05; WF3·WF5.

| 입력/상태 | 검사 방식과 출력 |
|---|---|
| observed/computed/estimated | quantity 필수. observed는 sourceRef 필수·calculationBasis=null, computed는 sourceRef와 계산 근거, estimated는 추정 근거 필요. 근거 없는 측정값 생성/승격 금지 |
| missing/not_collected/not_applicable/withheld | quantity=null. withheld는 sourceRef/calculationBasis도 null. 실제 0은 수치 0으로 보존하고 비수치를 0으로 합산하지 않음 |
| 양과 파생값 | 음수 아닌 십진 문자열·필드별 단위 m/s/s/km/m/s/bpm 등을 대조한다. 페이스=시간(s)×1000/거리(m), 속도=거리(m)/시간(s). 해당 분모0은 not_applicable, NaN/Infinity는 거절 |
| 종목별 합계 | 전체 유일 운동을 종목별로 대조. running/swimming/cycling/strength/other/unknown을 유지하고 unknown을 running으로 대체하거나 이종 성과를 합치지 않음. 거리 m/시간 s는 정확 Decimal 합산 |
| 합계 상태 | 비공개 입력은 withheld가 우선. 공개 입력은 missing → not_collected → not_applicable 제외(전부면 not_applicable) → 수치 중 estimated 존재 시 estimated → 나머지 computed와 근거. totals 미허용은 빈 요약 |
| C05 전체 계획 | 필수 목표/기간/주차 목표/휴식/가능 시간/고정 운동·세션 수행 내용과 ID/세션 버전 유일성·양수 예상시간 s·선택 거리 m·강도 단위/상하한·RPE scaleRef를 교차 대조. 미지정 목표량 null 보존 |

**선행조건/실패:** 정책에 의해 공개 가능한 값만 U1-SD-06 이후 계산한다. 모든 상세를 확인하기 전 루트 요약을 전체 검증 완료로 표시하지 않는다. 단위·근거·합계·필수/세션 모순은 DATA_INVALID이며 계획은 **전체** 보류한다. 무한소수·반올림/정밀도·척도 적격성이 미해소이면 관련 검증 완료를 선언하지 않고 DEPENDENCY_UNQUALIFIED 등 기존 차단에 연결한다. 생리적 임계값/안전 판단은 별도 SAFETY_BLOCKED 조건을 유지한다.

**필수 검사/확인 지점:** B01·N02~N04·N08~N10·FD06~FD08·FD11·FD16·FD21~FD22. 상태/단위/수식·적용한 계산 프로필·정확 합계 비교 범위만 인계한다. U1은 규범/기대값, U2/U3는 실제 Decimal·정밀도/반올림/척도 도구 선정과 적격 실행 소유다. 이 단계는 허용 정밀도나 의학적 타당성을 선정하지 않는다.

## U1-SD-09 — 기간/DST와 출처별 시각 분리

연결: NFR6.1·NFR6.2; BR2.3·BR2.5·BR3.2·BR5.1~BR5.4·BR7.2; CR02·CR04·CR12; WF3·WF5·WF7.

**입력/처리/출력:** 유효 일자·실제 IANA 시간대/적격 tzdbVersion에서 시작<끝인 시작 포함·끝 제외 기간을 대조한다. startedAt의 원 오프셋 문자열을 보존하고 현지 일자를 루트/Detail 기간과 대조하며 정렬은 UTC 순간을 사용한다. 세션 localTime이 있으면 우선하고 null이면 C05 전체에 결합된 기본 시각만 사용한다. 단일 현지 시각으로 해석 가능한지를 검사하여 DST 중복/누락 시각을 자동 이동/오프셋 추정하지 않는다.

원천 시각·sourceCollectedAt·generatedAt·observedAt·lastSuccessfulAt은 각 출처/버전과 별도로 유지한다. 이번 실패와 이전 성공, 미수집과 미운동을 함께 표현하며 가장 큰 timestamp 하나로 최신/성공을 결정하지 않는다. timingPolicy·timezone/tzdbVersion/calendarAlias·기본/세션 시각 변경은 전체 내용 변경이므로 새 승인/검증에 연결한다.

**실패/차단:** 무효 일자/기간·단일 시각 불명은 DATA_INVALID, 적격 tzdb/지원 근거 없음은 DEPENDENCY_UNQUALIFIED로 보류한다. timestamp 문자열이 실제 원 정책/외부 효과의 현재성을 증명하지 않는다.

**필수 검사/확인 지점:** N10·N13~N14·S19~S20·FD09~FD10·FD14~FD15·FD23·FD26와 timingPolicy 변경. 자정·월말·윤일·연말·서로 다른 오프셋·DST 모호/누락·미확인 tzdb를 포함한다. 기간 해석/원 오프셋·시각별 출처/버전·프로필/미수행 범위만 인계한다. U1은 경계/표현, U2/U3는 적격 시간대 자료와 실제 집계/Calendar·시계/단조 경과시간 검증 소유다.

## U1-SD-10 — 분할 전달의 누락·무효·원천 완전성 분리

연결: NFR5.5; BR3.1~BR3.7; CR03; WF3.

**입력/처리:** INLINE은 전체 activities·detailArtifacts=[]·expectedPartCount=0·목록 길이=expectedActivityCount다. PARTITIONED는 activities=[]·N>=1·전체 운동 수>=1이며 C03 등록 Detail만 사용한다. 생산자는 불변 상세를 먼저 저장하고 실제 digest를 결합한 루트를 마지막에 게시한다. 여러 파일 원자성은 가정하지 않는다.

소비자는 등록 별칭의 고정 objectId/versionRef만 읽고 U1-SD-02~03의 Detail 특칙을 적용한다. 정상 descriptor의 partIndex는 0..N−1 각각 한 번·오름차순, store/object/version은 중복 없이 activityCount>=1이고 모두 존재할 때 합이 expectedActivityCount와 같아야 한다. Detail의 snapshotId/sourceSnapshotRef/subjectRef/projection/rootPeriod·partCount는 루트와 같고 Detail.period=descriptor.period이며 동일 시간대의 루트 안에 있어야 한다. 하위 Detail/순환 참조는 탐색하지 않는다.

각 조각과 전체 연결 결과는 `(startedAt UTC 순간, activityId Unicode 코드 포인트 순)`으로 검사한다. activityId는 전체에서 유일해야 하며 같은 내용/다른 sourceRevision 중복도 거절한다. 기간 겹침은 허용하되 운동 현지 일자·본문 개수·정확 종목별 합계를 검사한다. 조각 기간의 합집합으로 수집 완료를 추정하지 않는다.

| 조건 | 출력/우선 처리 |
|---|---|
| 구조/계보/중복/범위 밖 index/존재한 선언 개수/집계 모순 | DATA_INVALID로 스냅샷 분석/계획 근거 채택 보류. 누락도 있더라도 무효를 PARTIAL로 완화하지 않음 |
| 유효 descriptor/Detail 누락·읽기/버전/digest 실패 | 조각 미사용·failedParts와 SOURCE_INCOMPLETE/effectiveCompleteness=PARTIAL. 실패를 정상 0건으로 바꾸지 않음 |
| 원천 COMPLETE·sourceCollectedAt 존재·missingPeriods=[]·전달/합계 확인 | 확인한 범위에서만 effectiveCompleteness=COMPLETE |
| 원천 PARTIAL | 전달 전부 도착해도 PARTIAL 유지. 알려진 누락 기간, 불명이면 전체 period 유지 |
| 성공 수집·INLINE·0건·빈 요약·missingPeriods=[] | EMPTY. 수집 실패/미수집을 이 상태로 치환 금지 |
| sourceCollectedAt=null·INLINE·0건·빈 요약·missingPeriods=[period] | NEVER_COLLECTED. 미운동 단정 금지 |
| 정책 withheld 존재 | 그 사실만으로 수집/전달 완전성을 낮추지 않음. 수치 재계산 한계는 별도 |

**필수 검사/확인 지점:** S06~S20·N34·FD12~FD16. descriptor/실제 상세의 고정 참조와 실패 조각·원천 completeness/유효 결과·전체 요약 검증 수행 여부를 분리 인계한다. manifest/기간/ArtifactRef 및 해당 생산자의 C08만 탐색 근거로 사용하고 끊김/오래됨/미동기화를 명시한다. U1은 규범/사례, U2/U3는 실제 저장/읽기/집계·원천 범위 확인 소유다. 새 탐색 서버나 다중 파일 원자성 보장은 도입하지 않는다.

## U1-SD-11 — 전체 계획/단일 행위 선언과 독립 승인 경계

연결: NFR2.2; BR5.4·BR6.1~BR6.4; CR06·CR09·CR11; WF5~WF6.

**입력/처리/출력:** 전체 계획 의미 검사를 통과한 C05 또는 정확한 대상 버전/digest/미래 영향의 C07에 C06 선언을 대조한다. claimedSubjectRef·전체 targetDigest·policyDigest·원 ArtifactRef·documentKind·행위가 모두 대응해야 한다. PLAN은 PUBLISH_PLAN 하나, DISPOSITION은 C07 action에 대응하는 REPLACE_PLAN/WITHDRAW_PLAN/CANCEL_PUBLICATION 중 정확한 하나다. 출력은 독립 신뢰 검증의 **후보**이며 ApprovalProof가 아니다.

SELECTED_FUTURE는 해당 sessionIds, ALL_FUTURE는 빈 목록으로 그 계획의 미래 범위만 나타낸다. REPLACE는 replacementPlan의 새 완전본과 **별도 유효 PUBLISH_PLAN 승인**도 필요하다. WITHDRAW/CANCEL_PUBLICATION의 replacementPlan은 null이다. 원 실행 소유자가 현재 계보·미래 여부·실제 소유 연결을 확인하여 완료 실제 운동·변경 없는 세션·타 계획/사용자 일정을 보존한다. 원격 이벤트 이름/marker는 소유 증명으로 쓰지 않는다.

U2의 등록된 적격 검증기만 실제 사용자·정확한 전체 내용/행위·정책·현재 유효성/철회·명시적 인간 의도를 독립 확인하고 내부 VerificationResult/ApprovalProof를 만들 수 있다. profileId/recordId는 후보 참조이며 외부 서버/키 등록 권한이 없다. OAuth 보유·작성자·자체 서명·대화 복사·hash·approved/VERIFIED·LLM 답변을 이 근거로 대신하지 않는다. 추가 PC 승인 정책을 도입하지 않는다.

**실패/차단:** 구조/행위 모순 DATA_INVALID, 대상 내용 불일치 CONTENT_MISMATCH, 사용자/행위/현재성 미확인은 APPROVAL_UNVERIFIED, 적격 프로필 없음은 APPROVAL_PROFILE_UNQUALIFIED, 현재 계보 충돌은 REMOTE_CONFLICT로 보류한다. 현재 적격 승인 프로필은 없으며 자동 게시/변경/취소는 차단된다. U2 PlanAdmission의 게시 직전 최신 승인·안전·정책 확인을 생략하지 않는다. 평가 호출 실패 예외도 정확히 같은 변경 없는 계획 digest의 기존 승인/형식/안전 검증과 명시적 실패 고지가 있어야 U2가 검토할 수 있다. 오류 결과·미승인 조정안·미해소 안전 경고를 적용하지 않는다.

**필수 검사/확인 지점:** V05~V07·N12·N16~N21·FD02·FD23~FD25. 대상/정책/사용자/단일 행위·두 승인 분리·확정 계보·미래 영향 및 미해소 외부 차단을 안전한 참조로 인계한다. U1은 표현/대조 기대값, U3는 실제 인간 의도 전달, U2 PlanAdmission은 독립 승인·철회/계보/안전·최종 적격 판정 소유다. 합성 승인 근거로 외부 권위를 발급하지 않는다.

## U1-SD-12 — 생산자/단계/세션별 결과와 미확인 복구

연결: NFR7.1·NFR10.2; BR5.5·BR6.4·BR7.1~BR7.3; CR02·CR06·CR10~CR12; WF5~WF7.

**입력/처리/출력:** C08의 receiptId/producerUnit/subjectRef/workId/stage/targetDigest/observedAt와 해당 sessionResults로 원 의도·사용자·고정 버전/내용·단계·대상 세션을 대조한다. U3는 STORE만 생산한다. U2의 RECEIVE/VALIDATE/EVALUATE/CALENDAR는 실제 소유자가 생산하고 U3는 위치/권한/최신성·읽기 신뢰를 확인하기 전 자칭하지 않는다. C05 PROPOSAL·C06 선언·저장·수신·검증·평가·Calendar 성공을 각각 유지한다.

STORE는 버전별 JSON 완전본/근거가 지속 저장되고 실제 재읽기에서 위치/버전/전체 digest가 확인된 범위만 SUCCESS다. 수동 대안도 같은 조건이며 업로드 응답 ID·Markdown 수정만으로 확정하지 않는다. SUCCESS는 errors=[], FAILED/BLOCKED/CONFLICT/OUTCOME_UNKNOWN은 오류 1개 이상이다. Calendar는 대상 세션 **전부** 실제 확인한 경우만 전체 SUCCESS, 일부 성공은 PARTIAL이며 PENDING/FAILED/OUTCOME_UNKNOWN/CONFLICT/BLOCKED를 세션별 보존한다. observedAt과 lastSuccessfulAt을 분리하여 현재 실패를 과거 성공으로 덮지 않는다.

외부 효과는 원 실행 소유자가 원 의도/대상/기대 내용·digest 보존 → 현재 권한/원격 상태 대조 → 효과 요청 → 실제 확인/결과 보존 순서로 책임진다. 쓰기 응답 유실은 OUTCOME_UNKNOWN이고 원 의도·고정 대상·버전/digest·원격 내용 대조 전 새 객체 생성/덮어쓰기/재생성으로 해소하지 않는다. 원격 사용자 수정은 CONFLICT/REMOTE_CONFLICT로 보존한다. 재처리는 실패/미확인 범위만 현재 승인·정책을 다시 확인하며 성공한 다른 대상/세션은 유지한다.

**실패/차단:** 잘못된 생산자/단계·대상/오류 모순은 DATA_INVALID, 효과/접근/현재성 불명은 OUTCOME_UNKNOWN 또는 해당 차단 상태다. 일부 성공을 전체 성공으로 올리지 않는다. 한 단계의 확인이 다른 단계 권한을 해소하지 않는다.

**필수 검사/확인 지점:** V08·V12·N23~N25·FD02·FD23~FD26. C05/C06/C07/C08·ArtifactRef의 안전한 연결과 실패 원인/다음 대조·대상 세션·현재 오류/이전 성공을 인계한다. U1은 표현/연결, U2/U3 원 소유자는 실제 영속 증거·중복/충돌/부분 복구와 실제 읽기를 소유한다. 실제 로그 보존 기간·DB·트랜잭션·서비스 간 원자성을 이 설계에서 정하지 않는다.

## U1-SD-13 — 고정 오류 분류와 안전한 한국어 조치

연결: NFR7.2; BR2.5·BR3.7·BR7.2~BR7.3; Common.Error; CR12; WF7.

**입력/처리/출력:** 원 처리 단계의 검증된 오류 유형/작업/관찰 시각만 받아 Common.Error의 code·retryable·message·workRef·observedAt·fieldPath·suggestedAction을 모두 만든다. message는 사유/차단 범위를 한국어 텍스트로 설명하고 색상 없이 상태를 알 수 있어야 한다. fieldPath는 안전한 등록 경로/null, workRef는 비밀 아닌 허용 불투명 작업 참조다. 원 값/요청 본문/헤더를 문구에 echo하지 않는다. suggestedAction은 아래 고정 안내이며 실행 명령·승인·자동 재시도 권한이 아니다.

| 오류 분류/예 | 안내 연결과 제한 |
|---|---|
| 자료/버전/내용 DATA_INVALID·VERSION_UNSUPPORTED·CONTENT_MISMATCH·SOURCE_INCOMPLETE | CORRECT_DATA 또는 QUALIFY_DEPENDENCY/RECONCILE_REMOTE 등 실제 원인에 맞는 등록 안내. 누락/미확인을 원본 자동 수선으로 덮지 않음 |
| 권한/정책 PERMISSION_DENIED·POLICY_UNVERIFIED·POLICY_STALE | REAUTHENTICATE 또는 QUALIFY_DEPENDENCY 등 실제 원인에 맞는 조치. 동의/정책 변경 없이 반복 요청하지 않음 |
| 승인/안전 APPROVAL_UNVERIFIED·APPROVAL_PROFILE_UNQUALIFIED·SAFETY_BLOCKED | RECONFIRM_APPROVAL 또는 QUALIFY_DEPENDENCY 등 근거 해소 안내. 안내 문자열로 미적격 경로/안전 경고를 우회하지 않음 |
| 충돌/미확인 REMOTE_CONFLICT·OUTCOME_UNKNOWN | REVIEW_CONFLICT/RECONCILE_REMOTE. 원 사용자 수정/고정 대상을 대조하기 전 새 쓰기 금지 |
| 자원/일시 오류 RESOURCE_LIMIT·DEPENDENCY_UNQUALIFIED·RATE_LIMITED·TIMEOUT | QUALIFY_DEPENDENCY/RETRY_LATER 등 실제 원인과 남은 유한 예산에 맞는 안내. 실제 시간/호출/비용 수치와 재시도 수행은 소비자 책임 |
| 평가 LLM_INVALID | 잘못된 결과를 계획에 적용하지 않고 해당 소유자의 수정/의존 적격화 조치 안내. U1 검사에 U2 전용 LLM 자료를 추가하지 않음 |

표는 기존 code/action 열거값 안의 안내 설계이며 새로운 필수 일대일 매핑/실행 정책은 아니다. 영구 입력/권한 오류와 일시 오류를 구별하고 retryable=true라도 현재 동의/승인·기간별 호출/비용 예산·재대조 조건을 다시 만족해야 한다. 유한 한도 만료 뒤 남은 상태/조치를 보존하며 예약 실행으로 예산을 초기화/우회하지 않는다.

**실패/필수 검사/확인 지점:** V12·N24~N25·FD26 및 인증/정책/자료/충돌/자원/안전/평가 오류의 합성 분류 변형. 필수 필드/한국어 사유/등록 조치·현재 오류/마지막 성공 분리와 U1-SD-07의 출력 0건 검사를 병행한다. 출력 누출/필수 누락/잘못된 성공 승격은 검사 실패다. U1은 형식/기대 안내, U2/U3는 실제 CLI/대화·종료 결과·유한 재시도 소유다. 운영 로그 수집/대시보드 설계는 포함하지 않는다.

## U1-SD-14 — 독립 부합 증거와 재현 범위 제한

연결: NFR10.1·NFR10.3; BR1.1·BR7.4; CR12; WF1; U1-TD-004~006.

**입력/처리/출력:** U1 고정 릴리스/실제 입력·치환·합성 환경 조건, 해당 BR/상세 NFR/해법, 검사 scope, 사용 가능한 실제 도구/버전/설정/유한 프로필, 기대/관찰/판정, 안전한 evidenceRefs와 미해소 외부 차단을 연결한다. 이들은 검사 보고의 정보이며 새 wire/모델 필드 추가가 아니다. 파싱 불가 바이트는 ConformanceAssessment.inputDigest=null로 두고 원시 합성 입력 식별/조건을 연결한다.

PARSING·STRUCTURE·SEMANTICS·DOCUMENT_CONSISTENCY를 나누고 실제 수행한 scope의 기대 일치만 MATCHED, 불일치는 MISMATCHED로 기록한다. 정의만 한 사례는 PLANNED, 미수행/환경·도구 미확보는 NOT_RUN이다. externalAuthority=NOT_ESTABLISHED는 모든 부합 검사에서 유지한다. 기대 거절/보류가 맞으면 그 검사의 기대 일치이며 제품 SUCCESS가 아니다. 릴리스/입력/범위/프로필·소비자가 바뀌면 기존 기록을 보존한 새 검사로 연결한다.

ConsumerBinding은 U2/U3가 각자 같은 고정 릴리스의 실제 assessmentRefs와 limitations를 인용한다. 필수 불일치가 있으면 NONCONFORMANT, 미수행만 있으면 UNASSESSED이며 필요한 검사를 독립 수행하여 모두 기대 일치한 범위만 CONFORMANT 후보가 된다. **기존 ConsumerBinding에는 소비자 구현/워크플로 개정 식별이 부족한 승인된 위험이 남는다.** 사용 가능한 검사 프로필/한계의 보고는 모델 보완/위험 해소나 개정별 완전 재현성 확보가 아니다. 고정 releaseId/assessmentRefs만으로 임의 소비자 개정 전체/제품 권한을 주장하지 않는다.

**실패/필수 검사/확인 지점:** 아래 필수 집합/변형과 각 해법 연결이 빠지거나 미수행을 합격 분모에서 빼어 전수 성공으로 표시하면 증거 검사는 실패다. 입력/릴리스/scope/프로필 변화와 기존 증거의 다른 내용/행위/세션 재사용 거절을 대조한다. U1은 사례/연결 규범과 문서 정합, U2/U3는 실제 독립 부합 실행·도구 적격성·소비자 인수를 소유한다. 이 문서는 제품 의미 검증기를 실행한 MATCHED 기록을 만들지 않는다.

## 필수 유한 검사 집합과 인계 기준

아래 집합 전체와 각 해법의 변형이 필수다. 기존 [원 계약](../../../inception/contract-design/contract-summary.md)과 [FD 사례](../functional-design/functional-spec.md)의 기대값을 변경하지 않는다. 논리 ID 하나의 모든 하위 조건을 포함하며 ID 개수를 assertion 수/제품 커버리지로 표현하지 않는다.

| 집합 | 필수 범위 | 대조/증거 확인 지점 |
|---|---|---|
| U1 구조/교환 43개 ID | V01~V08·V12~V17, N01~N25·N33~N34, B01~B02 | expectedSchema와 expectedGate를 별도 대조. 정상 구조에도 남는 승인/정책/읽기 차단 보존 |
| 엄격 수신 | T01~T07, FD03의 UTF-8/두 BOM/바이트·깊이 경계·한도 없음/미지원 | 원시 입력/프로필 참조·파싱/구조의 수행 여부 분리. 파싱 불가 바이트를 JSON digest로 표시 금지 |
| 투영/분할 | S01~S23 | COMPLETE/PARTIAL/DATA_INVALID/PERMISSION_DENIED 층별 기대. source completeness·failedParts/유효 결과·정책 경로 비교 분리 |
| 기능 경계 | FD01~FD26의 모든 하위 조건 | 각 연결 해법/BR·상세 NFR/기대 관찰 확인. FD05 일반 JCS·FD08 정밀도·FD10 tzdb는 적격 도구/근거 전 NOT_RUN/미해소 |
| 보호/권한 변형 | 합성 비밀/금지 자료·불신 지시·공개/불명 대상·최소 네 항목 각각 누락·잘못된 서비스/목적/대상·동의 전/거부/철회·현재성 불명·자유 서술 불명·C05~C08 동의 누락 | 원 fixture/치환/합성 조건·기대 거절/보류·출력 경로/건수와 미해소 외부 차단 확인. 음성 표식 원문 보고 금지 |

필수 집합에서 비밀/금지 자료 출력 0건, 거절/보류 대상의 잘못된 허용 0건, 등록 참조/digest 및 기대 판정 전수 일치가 합격 기준이다. 하나라도 위반하면 관련 요구행 실패이며 미실행/미적격은 별도 NOT_RUN/미해소로 노출한다. 이는 유한 검사 집합의 목표이며 보편 비밀 탐지/외부 권한/의료 안전 보증이 아니다.

U1 자체 검사는 U1 고정 명세·12개 기준 fixture(RELEASE+11개 교환 fixture)만 의존한다. U2 전용 V09~V11·N26~N32·B03 및 EVALUATION/LLM_REQUEST/LLM_RESPONSE Schema/fixture, U2 실행 파일/DB나 U3 construction 자료를 필수 의존으로 넣지 않는다. 합성 transportGrants/rebindPolicy/rebindDetails는 시험 구성일 뿐 실제 권한/소비자의 자동 재서명·승인 기능이 아니다.

## 상세 추적과 검증 한계

[traceability.json](traceability.json)의 upstream_ids는 공식 seed의 22개를 그대로 보존한다. 아래 연결과 OK는 **실제 설계 해법의 존재/책임 추적**이며 구현/제품 시험 통과를 뜻하지 않는다.

| 상세 NFR | 설계 해법 | 필수 확인/실제 인계 |
|---|---|---|
| NFR1.1 | U1-SD-07 | 생성/오류/진단/요약/보고 출력 0건 → U2/U3 실제 검사 |
| NFR1.2 | U1-SD-02 | 불신 지시의 데이터 격리 → 실제 경로/명령/렌더링 격리 |
| NFR2.1 | U1-SD-04 | 현재 정책/비공개 대상/권한 불명 보류 → 실제 원 권위 확인 |
| NFR2.2 | U1-SD-11 | 정확한 전체 내용/단일 행위 선언과 독립 승인 → U2/U3 적격성 |
| NFR3.1 | U1-SD-05 | 전체 실제 경로/정확 집합/최소 네 항목 → 실제 연결 대조 |
| NFR3.2 | U1-SD-06 | withheld/파생/합계 쌍 비교 → 실제 전송/생성 검사 |
| NFR3.3 | U1-SD-04 | 요청 직전 동의/철회·내용 변경 새 검사 → 남은 요청 중단 |
| NFR4.1 | U1-SD-07 | 기본 제외/미등록 민감 자료 → 구조/서술/실제 출력 검사 |
| NFR4.2 | U1-SD-07 | 자유 서술/민감성 불명 보류 → 목적별 최소 자료 확인 |
| NFR5.1 | U1-SD-01 | 9개 정의/6개 계약/11개 전체 fixture digest → 소비자 독립 고정 |
| NFR5.2 | U1-SD-03 | 전체 JSON/정책/대상 결합 → 일반 JCS 적격 실행 |
| NFR5.3 | U1-SD-02 | 엄격 파싱/유한 한도 → 실제 파서·한도 경계 증거 |
| NFR5.4 | U1-SD-03 | 불투명 ID/계보/충돌/미확인 보존 → 실제 원자 확정·재대조 |
| NFR5.5 | U1-SD-10 | INLINE/분할·누락/무효·원천/전달 완전성 → 실제 읽기/집계 |
| NFR5.6 | U1-SD-08 | 7상태/정확 Decimal/전체 계획 → 정밀도/척도 적격성 |
| NFR6.1 | U1-SD-09 | 기간/DST/원 오프셋 → 적격 tzdb/실제 Calendar 시각 |
| NFR6.2 | U1-SD-09 | 출처별 시각/정책 변경 새 승인 → 원천/현재성 확인 |
| NFR7.1 | U1-SD-12 | 생산자/단계/세션·현재 결과 → 실제 독립 결과/읽기 신뢰 |
| NFR7.2 | U1-SD-13 | 필수 오류/한국어 사유/안내 → 실제 CLI/대화/종료 결과 |
| NFR10.1 | U1-SD-14 | 전체 필수 집합/scope/기대 관찰/미수행 → 독립 부합 실행 |
| NFR10.2 | U1-SD-12 | 의도/사용자/버전/세션/원인·결과 연결 → 실제 보존/복구 |
| NFR10.3 | U1-SD-14 | 고정 범위의 증거/개정 식별 한계 → 소비자별 적격성과 제한 고지 |

## Assumptions & Open Questions

새 사용자 정책/외부 성공을 가정하지 않았다. 아래는 기존 미해소 조건의 인계이며 이 설계가 해소/활성화를 선언하지 않는다.

| 미해소 조건 | 차단/소유자와 필요한 해소 증거 |
|---|---|
| C06/C07 인간 의도·정확한 내용/행위·현재 계보/철회 | 적격 승인 프로필 없음. U2 PlanAdmission/U3 승인 전달의 독립 실제 근거 전 자동 게시/변경/취소 보류 |
| C04 원 정책 신뢰·최신성/철회 | U2 DataAccessPolicy/U3의 실제 확인 경로 검증 전 관련 신규 전송 보류 |
| ChatGPT 개인 계정 웹/모바일 JSON 읽기/쓰기·지속 저장·수동 대안 | U3 환경별 지원/권한/완전본 재읽기 실제 증거 전 저장/전달 성공 미검증 |
| P01~P03 Drive/GitHub/Calendar 권한/비공개·중복/충돌/유실, C08 위치/권한/최신성 | 해당 소유자의 실제 결과/대조·복구/읽기 신뢰 전 UNQUALIFIED 유지. U3의 U2 결과 성공 자칭 금지 |
| P05 Garmin 공식 상세 계약 | U2 공식 인증·지표·페이지/수정·기간·오류/한도 근거 확보 전 BLOCKED_CONTRACT_UNAVAILABLE 유지 |
| P04 원격 OpenAI 모델/호환·응답 품질·예산/비용 | 초기 원격 대상 선정만 유지. 실제 모델/비용/유한 조건 적격성 전 활성화 보류 |
| 로컬/사설 제공자/API·모델·처리 위치·하드웨어 | Ollama 제외. 대체 조건 미정 유지, 원격 유형만으로 로컬/사설 P0 완료 불가 |
| 시간/입출력 바이트·깊이/호출/비용·실제 자원/정밀도·반올림/척도/tzdb | U2/U3 실제 값/도구/버전 선정·측정·경계 검증 전 관련 처리 보류. U1 임의 운영 기본값 없음 |
| 안전 규칙 근거/임계값·미해소 경고 | U2 안전 게시 차단/U3 경고 검증 유지. 구조/수치 합격은 의료 안전이나 생리적 타당성의 증명 아님 |
| ConsumerBinding 소비자 구현/워크플로 개정 식별 부족 | 승인된 미해결 위험 유지. 고정 release/수행 프로필 범위만 인용하며 모델 보완/개정별 완전 재현성 해소 선언 금지 |

U1 직접 배정이 아닌 NFR8·NFR9·NFR11의 실제 유한 재개·안전·환경별 지원 검증은 U2/U3에 남는다. 서버/DB/클라우드·HTTP/암호화/비밀 보관 구현·성능/가용성 SLA·운영 관제/회로 차단기 수치는 이 단위에서 도입하지 않는다.

이번 산출물의 검증은 ID·상류/해법·로컬 링크·표·UTF-8/공백·추적성의 문서 정합 범위다. 제품 의미 검증기·일반 JCS/Decimal/tzdb 적격성·실제 OS/파일 I/O·외부 권위/효과·안전·과금·소비자 인수 시험은 미수행/미검증이다. 그 범위는 NOT_RUN·externalAuthority=NOT_ESTABLISHED 및 각 기존 차단으로 유지한다.
