# U2 Linux 에이전트 보안 요구사항

## Sources

근거: [기능 명세](../functional-design/functional-spec.md), [업무 규칙](../functional-design/rules.md), [상류 요구사항](../../../inception/requirements-analysis/requirements.md), [교환 계약](../../../inception/contract-design/contract-summary.md), [확정 Q&A](nfr-requirements-questions.md). C01·C03~C08·CR01~CR12와 P01~P05의 제한을 유지한다. 승인·정책·안전·실제 권한의 적격성이 없으면 관련 신규 효과/전송을 보류한다.

## 검사 범위와 위협

외부 파일/문서·이름·사용자 텍스트·LLM 응답은 데이터다. 승인 문자열·정상 해시·OAuth 보유·파일 소유·외부 VERIFIED는 권한이 아니다. 경로 이탈/순환 링크, 문서 지시 실행, 동의 없는 우회 전송, 오래된 정책·검사 후 변경, 진단 유출과 미확인 효과 재전송을 합성 시험으로 다룬다. 보호 보관 방식/라이브러리는 여기서 선정하지 않는다.

아래 0건/전부 일치 목표는 지정한 유한 합성 사례 집합에 대한 판정이다. 정상·오류·재시도·진단·동시 변경을 포함하고, 잘못 허용 0건과 정상 기대 결과 일치를 함께 검사한다. 모든 가능한 자유 서술의 민감성 탐지·실제 권한·의료 안전을 완전 보증하지 않는다. 음성 사례에 넣은 합성 비밀/금지 표식 자체는 보고서에 echo하지 않고 사례 ID·필드 경로·검출/전송 건수만 남긴다. 원본 음성 입력의 내용은 진단 증거로 복사하지 않는다.

## 상세 요구사항

| ID | 근거 | 측정 목표 | 검사 방법·사례 | 합격/실패 | 한계·담당·미실행 |
|---|---|---|---|---|---|
| NFR1.1 | BR1.2·BR1.8·BR4.10, NFR1, CR07 | 소스·CLI/설정 조회·로그·교환 JSON·Markdown·LLM/Calendar·재시도 진단의 비밀값/보호 보관 참조 노출 0건 | U2-S41·U2-S48·U2-S63에서 합성 표식을 정상/실패/재시도 출력과 생성물에 대조; 허용 런타임 비밀 사용과 출력 분리 | 지정 집합 검출 0건·필수 오류/조치 존재; 1건이라도 실패 | 비밀 보호 기술은 NFR Design, DataAccessPolicy/전 소유자, 미실행 |
| NFR1.2 | BR3.3·BR7.9, CR01 | 불신 지시로 셸 실행·임의 URL/schema/code 로드·허용 루트 이탈·순환 접근·비밀 조회 0건 | U2-S64 및 공통 경로/한글·공백/제어문자 경계 입력으로 실제 부수 효과를 대역 관찰 | 부수 효과 0건·거부/안전한 텍스트 기대 일치; 정상 허용 경로도 처리 | 임의 코드 평가를 요구하지 않음; OperationControl/수신 모듈, 미실행 |
| NFR2.1 | BR2.1·BR3.1·BR3.8·BR9.1, CR07 | 각 신규 요청에 현재 서비스/목적/대상 최소 권한·비공개·연결 적격성 검사; 불명/공개/거절/철회 시 미허용 쓰기 0건 | U2-S07·U2-S31·U2-S39·U2-S61에서 권한 변화 주입, 타 대상 성공 보존 확인 | 허용 후보만 요청·차단 이유/조치 일치; 불명 권한 허용 시 실패 | 합성은 실제 OAuth/권한 성공 아님; DataAccessPolicy/효과 소유자, 미실행 |
| NFR2.2 | BR5.8·BR6.10·BR7.4·BR7.7·BR9.5, CR02·CR06·CR09·CR11 | 정확한 전체 C05/C07 내용·사용자·행위·정책·명시적 인간 의도·현재 승인 계보/철회 CLEAR를 독립 적격 검증; 잘못 허용 0건 | U2-S33·U2-S37·U2-S38·U2-S39·U2-S55·U2-S56: 위조/버전 혼합/분기/REPLACE의 두 근거/검사 후 변경 | 미적격/불명은 전체 보류·새 내용 새 승인·영향 미래 세션만; 정상 대역의 필수 검사 전부 일치 | 적격 승인 경로 없음 유지; 추가 PC 승인으로 정책 변경 금지; PlanAdmission, 미실행 |
| NFR3.1 | BR3.2·BR4.10·BR10.3, CR07·C03·C04 | 신뢰된 analysisTargets의 저장소·모든 최종 독자별 유일 C04 grant와 projection의 분석 필드 집합 정확 일치; 비활성/누락/철회 경로의 신규 전송0건 | U2-S24·25·61·65~71·73, 공통 S21~23. 목적별 선택·저장/재시작·Drive/ChatGPT 독립 허용/철회·위장·누락·중복 검사 | 일치만 후보; 교집합/grant 합치기 없음. 분석0개는 외부 미게시·Drive 계획 수신 유지, 정책 변경은 새 digest/snapshot | chatgpt FINAL_READER/C04 매핑과 등록·목적별 선택 표현은 확정. 실제 권한/경로·현재성 및 구현 부합은 미검증; DataAccessPolicy/AnalysisPublication |
| NFR3.2 | BR4.6·BR4.10·BR10.3, CR03·CR07 | 최소 metadata/period/date/sport 명시 허용 없으면 C03 전체 보류; 미허용 지표 고정 슬롯은 withheld+quantity/sourceRef/calculationBasis=null | U2-S22·U2-S23·U2-S24, 계약 S02·S03·S04·S05·S17·S18; 거리/시간/강도 의존·심박 독립 검사 | 금지 필드/숨긴 수치·출처의 요약/설명/오류 우회 0건, 필수 기대 일치; missing/0 위장 시 실패 | summary.totals는 개별 권한 확대 아님; 자유 서술 완전 판별 주장 금지; AnalysisPublication/PlanEvaluation, 미실행 |
| NFR3.3 | BR4.10·BR7.7·BR8.7, CR07 | 매 신규 요청에 현재 원 정책·동의/철회·전체 정책 digest 검사; 철회 후 새 금지 전송 0건 | U2-S39·U2-S48·U2-S61; 검사 후 철회·진행 중 전송·LLM 대체 유도·C05~C08 업무 묶음 거부 주입 | 남은 새 요청 차단·진행 효과 결과 대조·안전한 최소 자료 불가 시 보류; 동일 승인 내용 임의 가림 금지 | 기존 외부 사본 회수/삭제 보장 아님, U3 정책 현재성 미검증 유지; DataAccessPolicy/각 전송자, 미실행 |
| NFR4.1 | BR8.7·BR9.3·BR10.3, NFR4·CR07 | 기본 GPS/FIT/수면/HRV/통증 및 민감 원천/비밀의 분석·LLM·일정 전송 0건; 미등록 필드는 별도 동의로도 확장 전송 금지 | U2-S26·U2-S48·U2-S63에서 구조/설명/constraints/extensions/오류와 Calendar 투영 검사 | 금지 0건·허용 정상 자료 기대 일치; 요약 우회나 extension 삽입 시 실패 | 새 민감 수집/처리 기능 없음; 각 전송 소유자, 미실행 |
| NFR5.1 | BR6.12·BR10.4, CR01·CR02·C01 | 고정 registry 1.0.0·Common/C03~C08/schema/fixture digest 일치; 전체 JSON RFC8785 JCS UTF-8 SHA-256; 엄격 파싱과 유한 한도 준수 | U2-S34·U2-S35·U2-S36·U2-S38, 계약 T01~T07 및 release/내용 변형; 중복키/잘림/후행/NaN/Infinity/잘못된 UTF-8/비객체 거절 | 지정 음성 잘못 허용 0건·정상 단일 선두 BOM/CRLF/문자 의미 보존; extension도 전체 digest 포함 | 한도 bytes/depth·파서/JCS 모든 경계 적격은 NFR Design/구현; 수신·분석·평가 소유자, 미실행 |
| NFR9.1 | BR6.5·BR7.9·BR8.4, CR05·CR08·CR09 | 부족 자료/불확실성/주의·비진단 고지; 근거 없는 의료 판단·수치 보장·자동 승인 0건; 미해소 안전은 SAFETY_BLOCKED | U2-S40·U2-S43·U2-S44·U2-S46: 급격한 양/강도·회복 부족·비교 불가와 허위 근거 입력 | 모든 필수 경고/확인/조정 안내 기대 일치, 새 승인 없는 제안 적용 0건 | 안전 규칙 근거/버전/단위/대상/기간·한계 미해소 유지; PlanAdmission/PlanEvaluation, 미실행 |
| NFR9.2 | BR8.2·BR8.3·BR8.4·BR8.7, CR08·P04 | 같은 evaluatedDigest·허용 원천 evidenceRefs/수치만 VALID; length/refusal/tool_calls/형식 오류·허위 수치는 INVALID | U2-S41·U2-S42·U2-S43·U2-S44·U2-S47·U2-S48; 비스트리밍 content 재파싱과 결과/제안 분리 | 허위 채택·명령 실행·동의 없는 제공자 대체 0건, 정상 대역 결과 일치 | OpenAI 모델/비용·로컬 제공자/처리 위치/하드웨어 미선정, Ollama 제외; PlanEvaluation, 미실행 |

## 변경된 기능 모델의 검증 인계

승인된 기능 모델은 chatgpt FINAL_READER와 별도 SharingConsent를 C04에 대응하고 connectionIds(등록)·analysisTargets(분석 선택)·planInboxConnectionId(계획 수신)를 분리했다. NFR3.1의 검사는 이 실제 속성에 결합한다. ChatGPT 연결에는 비밀/endpoint/model을 등록하지 않으며 역할을 Linux 호출 권한으로 승격하지 않는다. U2-S65~71·73으로 분석0개·Drive 분석 비활성화와 계획 수신 유지·재시작·독립 동의/철회·위장/누락을 대조한다. 실제 C04 원 정책 신뢰/현재성·도구 경로는 별도 미검증이다. 확정 GTA-NUMERIC-1의 실제 계산 도구 부합은 복구 요구사항 NFR5.7에 연결한다.

## 검증 한계

현재는 문서 및 추적성 검사다. 위 합성 제품 검사, 비밀 보관/회전, 실제 권한·승인·철회·정책 현재성·Garmin 계약, 안전 검증과 모델 처리/비용은 미검증이다. 프로필 문서의 존재와 실제 적격 증거를 구분한다. 법규 인증·의료 안전 인증 또는 모든 입력 보장을 추가하지 않는다.
