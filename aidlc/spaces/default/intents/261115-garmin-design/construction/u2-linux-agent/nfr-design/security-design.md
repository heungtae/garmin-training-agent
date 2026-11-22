# U2 Linux 에이전트 보안 설계

## Sources

[보안 요구사항](../nfr-requirements/security-requirements.md)의 NFR1.1~NFR5.1·NFR9.1~NFR9.2, [기술 결정](../nfr-requirements/tech-stack-decisions.md)의 U2-TSD-03·04·08·10·12, [기능 명세](../functional-design/functional-spec.md)의 F01·F06~F10 및 [공유 계약](../../../inception/contract-design/contract-summary.md)의 C01·C03~C08·CR01~CR09·P01~P05를 따른다. 구체 기술 후보와 관리 권한의 원본은 [설계 Q&A](nfr-design-questions.md)다. 문서/해시·OAuth 보유·파일 소유·외부 VERIFIED·LLM 결과를 실제 권한으로 인정하지 않는다.

<a id="u2-sec01"></a>
## U2-SEC01 — 비밀 저장과 관리자 권한 제한

대응: NFR1.1·NFR2.1. 소유: DataAccessPolicy(비밀 참조/연결), OperationControl(OS 관리), 각 소비자(메모리 사용). 규칙: BR1.2·BR1.8·BR4.10.

설치에서 확인한 비-root 일반 사용자 UID/GID를 시스템 oneshot 서비스에 고정한다. 관리자 인증은 설치/제거·고정 서비스/타이머 등록·변경·중단/재개·암호화 비밀 등록/갱신 등 필요한 OS 작업에만 쓴다. 일반 상태/설정 읽기와 업무 계산은 비특권이다. 자동 수집/분석/평가/게시마다 sudo 질문이나 추가 계획 승인 단계를 넣지 않는다. CLI 즉시 실행의 비밀 사용 경로도 관리된 같은 서비스 경로이며 CLI가 복호화한 비밀을 argv/환경으로 넘기지 않는다. 필요한 서비스 활성화 권한이 없으면 안전하게 조치를 안내하고 우회하지 않는다.

비밀은 systemd255 계열의 시스템 관리자 `systemd-creds`·`LoadCredentialEncrypted`를 이용한 호스트 키 기반 암호화 credential 저장으로 설계한다. 관리자는 허용 등록 절차에서 비밀을 입력하며 서비스에는 읽기 전용 자격자료가 전달된다. 앱은 필요한 시간 동안만 메모리에서 읽고 도메인 DB에는 CredentialReference의 내부 참조만 둔다. 비밀값과 보호 보관 참조는 CLI/교환/Markdown/로그/진단에 싣지 않는다. GARMIN_API_KEY는 기존 참조 이름이며 인증 헤더/갱신 규약은 P05 확인 전 추측하지 않는다.

고정 데이터 루트 후보 `/var/lib/garmin-training-agent/`는 설치 때 로그아웃 후 접근 가능한 실제 로컬 마운트/소유권을 확인한다. 디렉터리0700·파일0600·UMask0077, 경로/소유/심볼릭 링크 검사, NoNewPrivileges, 허용 데이터 경로 외 쓰기 제한, core dump 금지를 적용한다. credential 원본/호스트 키는 관리자 보호 경로에 둔다. 제약이 합법적 TLS·타이머·DB 동작을 막지 않는지 실제 설치 시험 전 지원을 주장하지 않는다.

TPM을 새 필수 장치로 만들지 않으며 최신 사용자별 암호화 기능이255에 있다고 추정하지 않는다. GUI 키링 해제/사용자 로그인 세션을 비밀 접근의 숨은 전제로 삼지 않는다. 키/credential/마운트/서비스 접근 미적격이면 관련 기능을 보류하고 평문 설정으로 fallback하지 않는다. 호스트/root 또는 소유 계정 침해·메모리/절전 이미지·호스트 키와 자료가 함께 있는 디스크 반출을 완전 방어한다고 주장하지 않는다. 건강 DB 저장 시 암호화/전체 디스크 암호화를 제공한다는 주장도 하지 않는다.

관리 기능은 고정 unit/설치 경로와 검증한 구조화 값만 받으며 임의 root 명령·외부 문자열 실행·상시 비밀 브로커·범용 Polkit/sudo 우회를 허용하지 않는다. 갱신은 새 암호화 credential을 검증/교체한 뒤 해당 연결의 접근/적격성을 재검사한다. 실패한 갱신을 ACTIVE로 표시하지 않고 기존 유효본/철회 상태를 보존한다.

검증 설계: U2-S01·U2-S02·U2-S41·U2-S48·U2-S63에서 합성 비밀을 정상/실패/재시도/core/진단 경계에 주입해 출력0건·필수 한국어 조치 존재를 확인한다. 관리자 경계·로그아웃 접근·갱신 실패·경로 권한은 실제 Ubuntu에서 별도 검사한다. 근거: [systemd255 exec](https://www.freedesktop.org/software/systemd/man/255/systemd.exec.html), [creds](https://www.freedesktop.org/software/systemd/man/255/systemd-creds.html). Q&A가 확인한 설계 근거이며 이 단계 설치/지원 시험은 미실행이다.

<a id="u2-sec02"></a>
## U2-SEC02 — 불신 입력과 엄격 검사 경계

대응: NFR1.2·NFR5.1. 소유: PlanAdmission(수신), AnalysisPublication(교환), PlanEvaluation(content), 각 수신 모듈. 규칙: BR6.12·BR7.9·BR10.4.

입력은 파일/HTTP 원시 바이트부터 [U2-C01](scalability-design.md#u2-c01)의 원시/해제 후 크기·깊이·누적 예산을 적용한다. UTF-8 유효성→허용된 단일 선두 BOM/바깥 공백→중복 키를 잃기 전 탐지→단일 루트 객체/후행 문서 검사→고정 registry Draft2020-12 구조/format 검사→전체 JCS digest→독립 의미/정책/승인/안전 검사 순서다. NaN/Infinity·잘림·잘못된 Unicode를 거절하고 문자열을 자동 수선/정규화하지 않는다. serde_json1.0.154 후보의 String 경로와 중복 키 사전 검사를 설계하며 Value에 덮어쓴 뒤 중복을 찾는 방식을 쓰지 않는다.

jsonschema0.62.0 후보는 설치본에 고정한 registry1.0.0과 등록 참조만 해석한다. remote/file retriever를 비활성화하고 date/date-time 등 계약 format을 명시적으로 검사한다. payload의 URI·profileId·검증기 이름으로 네트워크/schema/code를 로드하지 않는다. Common/C03~C08 및 schema/fixture 실제 digest를 C01 고정 기대값과 대조한다. serde_jcs0.3.0·SHA-256 후보는 문서 전체(extension 포함)의 RFC8785 UTF-8을 사용한다. UTF-16 속성 정렬·숫자·Unicode·고정 기대digest의 적합성 시험 전 라이브러리 이름만으로 일반 JCS 적격을 주장하지 않는다.

외부 instruction/파일명/오류·LLM content는 데이터다. 구조화 허용 별칭과 고정 objectId/versionRef만 따라가며 셸·임의 URL·로컬 파일·임의 코드·비밀 조회를 실행하지 않는다. 허용 루트 이탈·순환 링크·제어문자·한글/공백 경로를 명시 검사하고 안전한 텍스트로 취급한다. 상세는 등록 Detail만 읽고 중첩 참조를 허용하지 않는다. 검사 실패는 DATA_INVALID/CONTENT_MISMATCH/RESOURCE_LIMIT 등 기존 code와 필드 경로를 반환하고 이전 유효본을 유지한다. 구조 통과는 의미·승인 통과가 아니다.

검증 설계: U2-S20·U2-S34~U2-S38·U2-S64, 공통T01~T07·고정 release 변형, 정상 BOM/CRLF/인용/한글과 오류 입력을 함께 검사한다. 지정 음성의 잘못 허용/부수 효과0건과 정상 기대 전부 일치가 필요하다. 실제 구현/라이브러리 상호운용은 미검증이다. 근거: [serde_json](https://docs.rs/serde_json/1.0.154/serde_json/de/struct.Deserializer.html), [jsonschema](https://docs.rs/jsonschema/0.62.0/jsonschema/), [serde_jcs](https://docs.rs/serde_jcs/0.3.0/serde_jcs/).

<a id="u2-sec03"></a>
## U2-SEC03 — 각 요청의 현재 권한·동의·투영 검사

대응: NFR2.1·NFR3.1·NFR3.2·NFR3.3·NFR4.1. 소유: DataAccessPolicy(원 정책), 각 전송 소유자(직전 검사), AnalysisPublication(투영). 규칙: BR3.1·BR3.8·BR4.10·BR8.7·BR9.1·BR10.3.

요청 직전 신뢰한 현재 설정에서 실제 서비스/목적/대상 경로를 구하고 연결의 최소 권한·비공개·활성 대상·현재 사용자/원 정책 digest·동의/철회를 검증한다. connectionIds는 등록 목록이며 전송 동의/활성 선택이 아니다. analysisTargets가 선택한 저장소 DIRECT_SERVICE와 모든 chatgpt FINAL_READER의 실제 경로를 검사한다. 빈 선택은 로컬 보존·분석 외부 미게시이며 선택 경로 오류를 빈 선택으로 숨기지 않는다. planInboxConnectionId는 별도 drive DIRECT_SERVICE 계획 수신 선택이고 null이면 수신 보류다. Drive 분석 비활성화/분석0개가 이 선택을 해제하지 않는다. 이 확인은 최초/재시도/대조/LLM/Calendar 모두에 적용한다. payload가 주장한 경로 목록을 검사 범위로 삼지 않는다. 불명/거절/만료/철회/공개 대상은 신규 효과를 막고 조치를 반환한다. 진행 중 전송의 결과는 미확인/대조로 보존하며 외부 사본 회수 성공으로 표현하지 않는다.

chatgpt FINAL_READER는 credentialReferenceId/endpointReference/modelReference=null이며 Linux 호출 어댑터·비밀 등록·직접 실행 권한을 만들지 않는다. 실제 독자 계정/도구 경로·주체 대응·현재성 증거 없으면 UNQUALIFIED다. SharingConsent.connectionId에서 C04(serviceName→service,purpose,targetReference→targetAlias)의 유일 grant로 대응하고 주체·원 개정·현재성/철회·전체 정책 digest를 확인한다. Drive와 ChatGPT의 원 동의는 독립적이며 저장소 허용을 최종 독자 허용으로 승격하지 않는다. 계정/대상 혼동·다른 서비스 위장·독자 누락·중복 매핑은 차단한다.

C03 실제 ANALYSIS 경로마다 유일한 grant의 분석용9개 필드 집합을 ASCII 정렬하여 projection과 정확히 비교한다. 넓거나 좁음·중복 grant·경로 누락이면 전체 신규 분석 전송을 보류한다. grant를 합치거나 교집합을 자동 생성하지 않는다. 최소 analysis.metadata/summary.period/activity.date/activity.sport 중 하나라도 미허용이면 C03 전체 보류다. 실제 시각/오프셋·계보/개수까지 공개됨을 동의 설명에 유지한다.

미허용 지표는 고정 metrics 슬롯의 withheld와 quantity/sourceRef/calculationBasis=null을 유지한다. pace/speed는 intensity+distance+duration 모두 필요하며 heartRate는 독립 허용이다. summary.totals는 개별 비공개 지표를 공개할 권한이 아니다. 자유 서술/오류/근거/extension에 숨긴 수치·출처를 우회시키지 않는다. 기본 GPS/FIT/수면/HRV/통증·민감 원천/비밀은 전송하지 않으며 미등록 필드를 별도 동의만으로 추가하지 않는다.

C05~C08/LLM/Calendar도 업무 목적의 필수 묶음과 정확한 허용 입력을 검사한다. 안전한 최소 자료가 불가하면 보류한다. 동일 승인 payload를 임의 가려 재전송하지 않는다. 정책 변경이면 새 전체 정책 digest·투영·snapshotId로 다시 검사한다. 권한·현재성·승인 캐시의 통과로 직전 검사를 생략하지 않는다. 예산 예약 후 검사 조건이 바뀌면 전송하지 않고 예약 결과는 [U2-R04](reliability-design.md#u2-r04)로 처리한다.

검증 설계: U2-S07·U2-S22~U2-S26·U2-S31·U2-S39·U2-S48·U2-S61·U2-S63·U2-S65~U2-S71·U2-S73 및 계약S02~S05·S17~S18·S21~S23. 허용 정상과 더 넓음/좁음/누락/중복·검사 후 철회, 등록/목적별 선택의 저장·재시작, 분석0개·Drive 분석 중단/계획 수신 유지를 비교한다. 잘못 허용/금지 전송0건·필수 판정 일치를 요구한다. 모델 표현은 확정되었으며 구현 매핑/실제 경로·권한·정책 현재성 검증 전 관련 전송 보류는 [U2-O04](observability-design.md#u2-o04)를 따른다.

<a id="u2-sec04"></a>
## U2-SEC04 — 독립 승인·안전·LLM 근거 판정

대응: NFR2.2·NFR9.1·NFR9.2. 소유: PlanAdmission(승인/안전/최종 판정), PlanEvaluation(평가), CalendarDelivery(직전 효과). 규칙: BR5.8·BR6.5·BR6.10·BR7.4·BR7.7·BR8.2~BR8.5·BR9.5.

수신 C05/C07 전체의 정확한 내용/digest·사용자·행위·정책·명시적 인간 의도·현재 승인 계보/철회 CLEAR를 등록된 독립 적격 검증기로 확인해야 한다. 외부 approved/VERIFIED·정상 해시·임의 profileId는 ApprovalProof가 아니다. REPLACE는 C07 처분 승인과 새 C05 PUBLISH_PLAN의 두 근거를 각각 검증한다. 버전 혼합/같은 버전 다른 내용/동시 분기·검사 후 변경은 전체 보류하며 새 내용은 새 승인이다. 추가 PC 승인을 정책 대체로 넣지 않는다.

안전 검사는 근거/버전·대상·기간/단위·비교 방법·허용 한계·부족 자료 처리의 적격성을 요구한다. 자료 부족/비교 불가·양/강도·회복 경고·미해소 안전은 SAFETY_BLOCKED다. 근거 없는 의료 임계값·진단·수치 보장·자동 승인을 추가하지 않는다. 경고/불확실성·비진단 고지·확인/조정 안내를 보존한다. 형식/승인/안전을 통과해도 스냅샷은 ADMITTED_FOR_EVALUATION이며 최종 ELIGIBLE이 아니다. 최종 효과 전 PlanAdmission이 현재 근거로 새 불변 AdmissionAssessment를 만든다.

PlanEvaluation은 적격 제공자/모델/처리 위치·비용/기간 예산과 허용 분석을 고정한 후만 요청한다. 초기 원격 프로필은 비스트리밍 OpenAI Chat Completions·tools 없음·store=false·실제 모델 지원 토큰 한도 필드 하나다. 응답 finish_reason/refusal/tool_calls/content를 검사하고 content를 U2-SEC02로 다시 파싱한다. 같은 evaluatedDigest·허용 evidenceRefs와 실제 수치만 VALID 후보다. length/거절/형식/허위 근거는 INVALID이며 제안은 별도 보존하고 새 승인 전 적용하지 않는다. CALL_FAILED/OUTCOME_UNKNOWN 구분과 예외는 [U2-R07](reliability-design.md#u2-r07)에만 정의한다.

검증 설계: U2-S33·U2-S37~U2-S48·U2-S55~U2-S56의 정상 대역과 위조/분기/변경/허위 수치·안전 경고를 비교한다. 유한 사례의 잘못 허용0건·필수 경고/판정 전부 일치를 요구한다. 실제 C06·현재성·안전 근거·모델/비용/로컬 제공자·의학 타당성은 미해소이며 Ollama 제외를 유지한다.

<a id="u2-sec05"></a>
## U2-SEC05 — HTTP 경계와 정보 노출 억제

대응: NFR1.1·NFR1.2·NFR2.1·NFR8.5. 소유: 각 외부 어댑터 및 DataAccessPolicy.

허용 프로필의 고정 endpoint·TLS 인증서/호스트 검증을 유지한다. reqwest 후보에서 자동 proxy/redirect를 기본 허용하지 않으며 필요한 경우에만 실제 공급자 endpoint/인증 전달/처리 위치·권한/동의/예산을 별도 적격화한다. 본문의 URL·Location·schema 지시가 새 endpoint 선택권을 주지 않는다. deadline/취소는 [U2-P02](performance-design.md#u2-p02), 바이트/압축 해제는 [U2-C01](scalability-design.md#u2-c01), 오류/진단은 [U2-O01](observability-design.md#u2-o01)의 단일 정의를 따른다. 공개 HTTP 서버를 만들지 않으므로 브라우저 보안 헤더/CSRF 세션 기능을 새로 추가하지 않는다.

실패는 고정 code/허용 fieldPath/workRef/한국어 suggestedAction으로 바꾸고 원격 본문·인증 헤더·토큰·건강 수치·보호 참조를 출력하지 않는다. 원문을 로그에 먼저 쓰고 나중에 필터링하는 경로는 허용하지 않는다. U2-S47·U2-S48·U2-S63·U2-S64와 인증서 오류/redirect/proxy/과대 본문 대역에서 실제 부수 효과와 출력 건수를 확인해야 한다. 근거: [reqwest0.13.5](https://docs.rs/reqwest/0.13.5/reqwest/struct.ClientBuilder.html), [Tokio timeout](https://docs.rs/tokio/1.54.1/tokio/time/fn.timeout.html). 실제 TLS/클라이언트 feature·외부 프로필은 미검증이다.
