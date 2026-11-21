# 요구사항별 구현 단위 배정

- 작성일: 2026-11-17
- 근거: [상세 요구사항](../requirements-analysis/requirements.md), [컴포넌트 목록](../domain-design/components.md), [도메인 ADR](../domain-design/decisions.md), [단위 정의](unit-of-work.md), [의존 DAG](unit-of-work-dependency.md), [확인 답변](units-generation-questions.md).
- User Stories 단계는 이 작업 계획에서 생략되어 승인된 하위 FR ID를 사용한다. 상위 FR는 하위 ID를 통해 연결한다. 원문 ID는 근거로 함께 유지한다.
- 여러 Unit ID와 Directory는 같은 순서이며 세미콜론으로 구분한다. 한 요구사항이 여러 단위에 걸치면 각 단위가 실제로 맡은 부분만 마지막 열에 지정한다.

## 기능 요구사항 매핑

| Requirement | Unit ID | Directory | 원문 ID | 단위별 구현 부분 |
|---|---|---|---|---|
| FR1.1 | U2 | u2-linux-agent | INS-001 | U2: Rust 프로그램 설치·초기화·실행·제거 |
| FR1.2 | U2 | u2-linux-agent | INS-002 | U2: CLI 초기 설정·검증·기존 설정 보존 |
| FR1.3 | U2 | u2-linux-agent | INS-003 | U2: 로그아웃 중 예약 등록·실행 검증 |
| FR1.4 | U2 | u2-linux-agent | INS-004 | U2: 두 주기의 독립 조회·변경·중단·재개 |
| FR1.5 | U2 | u2-linux-agent | INS-005 | U2: 즉시 실행·마지막/다음 실행 상태 |
| FR1.6 | U2 | u2-linux-agent | INS-006 | U2: 같은 PC 중복 작업 제어와 중복 결과 방지 |
| FR1.7 | U2 | u2-linux-agent | INS-007 | U2: 복귀 후 누락 기간·미완료 작업 재검사 |
| FR1.8 | U2 | u2-linux-agent | INS-008 | U2: 한국어 CLI·오류 원인·조치·종료 결과 |
| FR2.1 | U2 | u2-linux-agent | GAR-001 | U2: Garmin 인증 참조 등록·실제 연결 시험 |
| FR2.2 | U2 | u2-linux-agent | GAR-002 | U2: 목록 페이지·상세 수집과 부분 실패 보존 |
| FR2.3 | U2 | u2-linux-agent | GAR-003 | U2: 최초 기간·신규/수정·늦은 수정 처리 |
| FR2.4 | U2 | u2-linux-agent | GAR-004 | U2: 불투명 ID로 유일 운동·집계 유지 |
| FR2.5 | U2 | u2-linux-agent | GAR-005 | U2: 원천 수정과 영향 요약 갱신·게시 사본 충돌 구별 |
| FR2.6 | U2 | u2-linux-agent | GAR-006 | U2: 제공 종목·지표 수집·미지원 표시 |
| FR2.7 | U1; U2 | u1-exchange-spec; u2-linux-agent | GAR-007 | U1: 측정 필드·단위·원천·시각 교환 표현; U2: 측정값·단위·원천·수집 시각 보존 |
| FR2.8 | U2 | u2-linux-agent | GAR-010 | U2: 만료·제한·누락·응답 오류와 재시도 |
| FR2.9 | U1; U2 | u1-exchange-spec; u2-linux-agent | GAR-011 | U1: 미수집·미제공·추정과 실제 값의 표현; U2: 미제공 값 임의 생성 금지와 누락 보존 |
| FR3.1 | U2 | u2-linux-agent | STO-001 | U2: GitHub·Drive 각각의 인증·권한 시험 |
| FR3.2 | U2 | u2-linux-agent | STO-002 | U2: 단독/병행 저장소 선택·비활성 대상 전송 금지 |
| FR3.3 | U2 | u2-linux-agent | STO-003 | U2: 외부 게시 전 로컬 확정·디스크 실패 보존 |
| FR3.4 | U2 | u2-linux-agent | STO-004 | U2: 저장소별 독립 성공·실패·대기 |
| FR3.5 | U2 | u2-linux-agent | STO-005 | U2: 실패 대상만 재시도·타 대상 성공 보존 |
| FR3.6 | U1; U2 | u1-exchange-spec; u2-linux-agent | STO-006 | U1: 외부 객체·운동·계획 식별과 재처리 기준의 명세; U2: 원격 결과 대조·유일 게시·미확인 보류 |
| FR3.7 | U2 | u2-linux-agent | STO-007 | U2: 원격 충돌·보존 기간·삭제 영향 확인·복구 한계 |
| FR3.8 | U2 | u2-linux-agent | STO-008 | U2: 비공개/허용 대상 확인과 공유 차단 |
| FR3.9 | U1; U2 | u1-exchange-spec; u2-linux-agent | STO-009 | U1: 산출물 생성·갱신·동기화 상태 표현; U2: 게시 상태·생성/갱신·마지막 성공 표시 |
| FR4.1 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | DAT-001 | U1: 최신 요약·탐색 안내의 교환 구조; U2: 로컬 요약·탐색 자료 생성·허용 게시; U3: 최신 요약/탐색 자료를 읽는 안내 |
| FR4.2 | U2 | u2-linux-agent | DAT-002 | U2: 7/28/90일·주/월/연 기간 집계 |
| FR4.3 | U1; U2 | u1-exchange-spec; u2-linux-agent | DAT-003 | U1: 재계산 가능한 구조화 분석 자료 계약; U2: 구조화 자료 생성·재계산 가능 범위 제공 |
| FR4.4 | U1; U2 | u1-exchange-spec; u2-linux-agent | DAT-004 | U1: 운동 상세와 기간 요약의 연결 표현; U2: 상세·요약 구분·원천 변경 갱신 |
| FR4.5 | U1; U2 | u1-exchange-spec; u2-linux-agent | DAT-005 | U1: 범위·시각·시간대·단위·출처·버전 메타데이터; U2: 자료 메타데이터 생성·보존 |
| FR4.6 | U1; U2 | u1-exchange-spec; u2-linux-agent | DAT-006 | U1: 누락·미수집·0·추정·해당 없음의 표현; U2: 누락/0·추정과 분모 0 처리 |
| FR4.7 | U1; U2 | u1-exchange-spec; u2-linux-agent | DAT-007 | U1: 종목 식별과 종목별 지표 교환 표현; U2: 종목별 계산·중복/미상 구분 |
| FR4.8 | U2 | u2-linux-agent | DAT-008 | U2: 원천·요약 수치/반올림 일관성 |
| FR4.9 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | DAT-009 | U1: 불완전·미동기화·최신성 상태 표현; U2: 완전성·미포함 기간·마지막 성공 게시; U3: 최신성·불완전 상태를 확인하고 한계 고지 |
| FR4.10 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | DAT-012 | U1: 서비스별 허용 필드·동의와 금지 자료 교환 규약; U2: 게시/평가/Calendar 전송에 허용 필드 적용; U3: ChatGPT 자료/저장 동의와 금지 필드 준수 |
| FR5.1 | U3 | u3-chatgpt-workflow | CHP-001 | U3: 자연어 요청별 흐름과 미지원 안내 |
| FR5.2 | U3 | u3-chatgpt-workflow | CHP-002 | U3: 입력→기록→제안→수정→승인→저장 확인 흐름 |
| FR5.3 | U3 | u3-chatgpt-workflow | CHP-003 | U3: 신뢰 가능한 기존 입력 재사용·상충 확인 |
| FR5.4 | U1; U3 | u1-exchange-spec; u3-chatgpt-workflow | CHP-004 | U1: 목표·가능 시간·기존 운동·제약의 교환 표현; U3: 목표/가능 시간/빈도/제약의 입력 안내 |
| FR5.5 | U3 | u3-chatgpt-workflow | CHP-005 | U3: 부족한 필수값 확인·중요 값 임의 확정 금지 |
| FR5.6 | U3 | u3-chatgpt-workflow | CHP-006 | U3: 구조화 목표 요약·수정 기회 |
| FR5.7 | U3 | u3-chatgpt-workflow | CHP-007 | U3: 자료 접근 실패·추정 기반 구별 |
| FR5.8 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | CHP-008 | U1: 정확한 버전·승인 의사·증명 대상과 행위 범위의 계약; U2: 수신한 승인 근거를 사용자·정확한 버전과 검증; U3: 정확한 버전의 사용자 승인 의사 수집·보존 |
| FR5.9 | U1; U3 | u1-exchange-spec; u3-chatgpt-workflow | CHP-009 | U1: 저장/수동 전달 산출물의 완전성·버전 계약; U3: Drive 저장·허용된 수동 대안·미지원 보류 |
| FR5.10 | U1; U3 | u1-exchange-spec; u3-chatgpt-workflow | CHP-010 | U1: 저장 성공·실패·미확인 결과 표현; U3: 실제 저장 확인 전 성공 응답 금지 |
| FR5.11 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | CHP-011 | U1: 직접 실행 명령 없는 저장 자료 전달 계약; U2: 로컬 직접 호출을 요구하지 않는 주기 수신; U3: Drive 매개 전달·PC 직접 실행 비필수 |
| FR5.12 | U3 | u3-chatgpt-workflow | CHP-013 | U3: 웹/모바일별 실제 지원·제한·대안 안내 |
| FR6.1 | U3 | u3-chatgpt-workflow | PLN-001 | U3: 목표일까지 러닝 계획·자료 부족 한계 |
| FR6.2 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | PLN-002 | U1: 목표·기간·주차·세션·휴식과 불완전 입력 사례; U2: 필수 계획 필드·기간·ID·수치 검사와 전체 보류; U3: 목표·주차·세션·휴식의 완전한 작성 |
| FR6.3 | U3 | u3-chatgpt-workflow | PLN-003 | U3: 사용자 가능 시간·고정 운동·회복 고려 |
| FR6.4 | U3 | u3-chatgpt-workflow | PLN-004 | U3: 능력 차이·근거·불확실성 설명 |
| FR6.5 | U2; U3 | u2-linux-agent; u3-chatgpt-workflow | PLN-005 | U2: 수신 계획의 근거 있는 안전 검증과 미해소 경고 보류; U3: 과도한 양/강도·회복 부족 경고와 미승인 조정안 |
| FR6.6 | U1; U3 | u1-exchange-spec; u3-chatgpt-workflow | PLN-006 | U1: 강도 기준과 단위의 교환 표현; U3: 강도 기준·단위 명시 |
| FR6.7 | U3 | u3-chatgpt-workflow | PLN-007 | U3: 준비/본/정리 등 수행 내용 작성 |
| FR6.8 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | PLN-008 | U1: 작성·승인·저장·수신·평가·게시 상태 구별; U2: 승인 검증·수신·평가·부분 게시 상태 보존; U3: 작성/승인/개정/취소 표시·게시 성공 구별 |
| FR6.9 | U3 | u3-chatgpt-workflow | PLN-009 | U3: 전체/주/세션 수정 요청·새 승인 전 제안 |
| FR6.10 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | PLN-010 | U1: 개정 계보·변경 근거·새 승인 결합 계약; U2: 새 버전의 새 승인·구버전 반영 차단; U3: 개정 차이·사유·새 승인 의사 수집 |
| FR6.11 | U2; U3 | u2-linux-agent; u3-chatgpt-workflow | PLN-011 | U2: 계획 개정과 실제 운동 데이터 분리·보존; U3: 실제 완료 운동을 변경하지 않는 개정 |
| FR6.12 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | PLN-012 | U1: 완전본 판별·버전 결합과 부분 작성 음성 사례; U2: 부분 작성/혼합 버전 차단·완전본 재검증; U3: 완전한 저장·잘림/혼합 버전 피하기 |
| FR7.1 | U1; U3 | u1-exchange-spec; u3-chatgpt-workflow | CMD-001 | U1: 지속 보관할 목표·계획 교환 산출물 명세; U3: 승인 목표·계획의 지속 Drive 보관/확인 |
| FR7.2 | U2 | u2-linux-agent | CMD-002 | U2: 설정 주기의 Drive 최신 계획 확인 |
| FR7.3 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | CMD-003 | U1: 목표·계획·세션·개정의 고유 식별과 버전 계약; U2: 수신 버전·스냅샷·세션 식별 대조; U3: 작성 목표·계획·세션·개정 식별자 제공 |
| FR7.4 | U1; U2 | u1-exchange-spec; u2-linux-agent | CMD-004 | U1: 미승인·형식 오류·부분 입력 음성 사례와 오류 표현; U2: 승인·형식·완전성·허용 행위 검증 |
| FR7.5 | U2 | u2-linux-agent | CMD-005 | U2: 중복 조회·중단 재개 시 중복 적용 차단 |
| FR7.6 | U2 | u2-linux-agent | CMD-006 | U2: 수신/검증/세션별 게시 상태와 오류 집계 |
| FR7.7 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | CMD-007 | U1: 동시 수정/검사 후 변경과 원 버전 표현; U2: 동시 수정·검사 후 변경 감지·보류; U3: 원 버전·완전 저장·동시 수정 한계 안내 |
| FR7.8 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | CMD-008 | U1: 폐기·교체·취소의 대상·승인 범위 표현; U2: 요청 승인 검증·영향 확인·미래 세션 처분; U3: 폐기·교체·게시 취소 요청과 영향 확인 |
| FR7.9 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | CMD-009 | U1: 허용 데이터·행위 범위와 불신 입력 경계 계약; U2: 불신 자료의 명령 실행/경로/권한 확대 차단; U3: 외부 자료 지시로 승인/공유/실행 권한 확대 금지 |
| FR8.1 | U2 | u2-linux-agent | LLM-001 | U2: LLM 제공자·모델·인증 참조 등록/연결 확인 |
| FR8.2 | U2 | u2-linux-agent | LLM-002 | U2: 원격 및 로컬/사설 실제 호환성 검증 |
| FR8.3 | U2 | u2-linux-agent | LLM-003 | U2: 평가·적정성·실적 분석·미승인 조정안 분리 |
| FR8.4 | U2 | u2-linux-agent | LLM-004 | U2: 형식·근거·불확실성·허위 수치 검증 |
| FR8.5 | U2 | u2-linux-agent | LLM-005 | U2: 오류 결과 반영 금지·검증 통과 동일 버전 예외 |
| FR8.6 | U2 | u2-linux-agent | LLM-006 | U2: 평가 실패·재시도·늦은 결과와 원본 보존 |
| FR8.7 | U1; U2 | u1-exchange-spec; u2-linux-agent | LLM-007 | U1: LLM 공유 범위·금지 필드와 동의 자료 계약; U2: 제공자별 허용 입력·금지 필드 차단 |
| FR9.1 | U2 | u2-linux-agent | CAL-001 | U2: 계정·캘린더 선택·권한 거절/철회 대응 |
| FR9.2 | U2 | u2-linux-agent | CAL-002 | U2: 시간 설정·승인 세션의 주기 게시 |
| FR9.3 | U2 | u2-linux-agent | CAL-003 | U2: 허용된 일정 필드·단위·현지 시각 검증 |
| FR9.4 | U2 | u2-linux-agent | CAL-004 | U2: 세션/이벤트 연결·중복/응답 유실 대조 |
| FR9.5 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | CAL-005 | U1: 승인 개정/취소에 포함할 미래 세션 영향 표현; U2: 승인된 미래 세션만 갱신/취소; U3: 승인 개정/취소의 미래 세션 영향 제공 |
| FR9.6 | U2 | u2-linux-agent | CAL-006 | U2: 사용자 수정·최신 원격 확인 불가 보류 |
| FR9.7 | U2 | u2-linux-agent | CAL-007 | U2: 세션별 실패·미확인 재시도·계획 원본 보존 |

각 단위의 Functional Design은 배정된 요구사항의 모든 수용 기준을 확인하고, 자기 부분의 규칙/검증과 다른 소유자 또는 전체 인수에서 확인할 연결을 명시한다. 이 표의 배정은 각 단위가 다른 단위의 역할까지 단독 수행한다는 뜻이 아니다.

U1의 역할은 교환 명세·규범·합성 사례이며 U2의 실행 코드나 U3의 실제 클라이언트 동작을 대신하지 않는다. U2와 U3는 같은 U1 버전에 각각 부합해야 한다. API 권한·사용자 승인 근거·실제 자료 전달의 성공은 단위 자체 대역 시험만으로 주장하지 않는다.

## 비기능 요구사항 책임 연결

다음 NFR 행은 단위별 상세 NFR 설계의 입력이다. 명세·소비자별 규칙·전체 검증을 구분하며 기존 NFR 수용 기준을 완화하지 않는다.

| Requirement | Unit ID | Directory | 단위별 책임 |
|---|---|---|---|
| NFR1 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | U1은 비밀 제외 명세/사례, U2는 보호된 비밀 참조·로그·전송, U3는 대화·저장 자료의 인증정보 제외 |
| NFR2 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | U1은 권한/정책 교환, U2는 원 권한·비공개 대상 확인, U3는 확인한 허용 범위와 미확인 보류 |
| NFR3 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | U1은 서비스별 동의/목적/필드 표현, U2·U3는 전송 전 허용 확인·철회 후 차단 |
| NFR4 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | U1은 기본 제외/별도 동의 사례, U2·U3는 GPS·FIT·수면/HRV·통증 기본 제외 적용 |
| NFR5 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | U1은 유일 ID·버전·내용 결합/음성 사례, U2는 로컬 무결성·중복/부분 실패, U3는 완전한 작성/저장·버전 유지 |
| NFR6 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | U1은 시간대/기간/시각 표현, U2는 집계/예약/게시 경계, U3는 목표/세션 시각 작성의 일관성 |
| NFR7 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | U1은 오류·상태 구분, U2는 처리별 진단/집계, U3는 실제 확인한 접근·승인·저장 상태 안내 |
| NFR8 | U2; U3 | u2-linux-agent; u3-chatgpt-workflow | U2는 수집·게시·평가·Calendar 재개, U3는 미완료 작성/저장 단계 보존·지원 절차 재시도 안내 |
| NFR9 | U2; U3 | u2-linux-agent; u3-chatgpt-workflow | U2 평가/검증과 U3 계획/설명에서 비진단·자료 부족·주의 조건·불확실성 표시 |
| NFR10 | U1; U2; U3 | u1-exchange-spec; u2-linux-agent; u3-chatgpt-workflow | U1은 대상/버전/상태 연결 명세, U2는 실행·검증·게시 결과 추적, U3는 승인 의사·저장 결과 근거 |
| NFR11 | U2; U3 | u2-linux-agent; u3-chatgpt-workflow | 양쪽 실제 지원·권한·저장/게시 성공을 모의 결과와 구분하고 미확인 자동화를 지원 확정으로 안내하지 않음 |

## 단위 내부의 구현·검증 흐름

아래는 **각 단위 내부**에서 산출물을 구성할 때의 의존/검증 흐름이다. 단위 간 개발 우선순위·일정·병렬 실행을 정하지 않는다. 이번 작업은 설계이며 구현은 아직 수행하지 않는다.

- **U1:** 승인된 용어/교환 경계 확인 → 명세·버전/호환 기준 작성 → 정상/음성/경계 합성 사례와 예상 판정 작성 → 참조·불완전·동의/비밀 제외·호환 정합 검사. 실제 형식과 승인 증명 방식은 Contract Design에서 결정한다.
- **U2:** U1 소비 범위와 설정/권한 계약 확인 → 각 소유 모듈의 기능과 적절한 검증 구성 → 모듈 간 상태·중복·충돌·실패 복구 통합 → 설치/예약/로그아웃 검증. 외부 API 실제 결과와 대역 결과를 분리한다.
- **U3:** U1 소비/생산 규약과 지원 조건 확인 → 목표·자료 읽기·계획 작성·개정·승인 의사·저장 확인 흐름 정의 → 합성 사례로 분기·표현·작성 결과 검증 → 실제 지원 환경의 읽기/쓰기·승인 근거·수동 대안 검증. 미지원 또는 신뢰 확인 불가 시 관련 경로는 보류한다.

## 전체 인수 검증으로 연결할 조건

1. U2가 허용된 운동을 로컬 보존하고 선택 저장소에 분석 자료를 독립 게시한다.
2. U3가 실제 지원된 환경에서 해당 자료를 읽어 목표·러닝 계획을 검토하고 명시적 사용자 승인 의사를 정확한 버전에 연결해 Drive 저장을 확인한다.
3. U2가 완전성·승인 근거·버전/내용·안전 기준을 독립 검증하고 허용된 LLM 평가를 수행한다. 원격 및 로컬/사설 유형 각각의 실제 호환성 증거가 필요하다.
4. 같은 검증 버전의 Calendar 세션을 게시하고 중복 조회·개정/취소·사용자 수정 충돌·권한 거절·응답 유실·부분 실패를 검증한다. 평가 호출 실패의 예외 정책이 승인/안전 검증을 우회하지 않아야 한다.
5. 금지 자료 전송·허위 성공·기존 자료 손실이 없고 Ubuntu 로그아웃/복귀 실행을 실제 환경에서 확인한다.

이는 제품 인수 시나리오의 자료 흐름이며 단위 간 경제적 구현 순서가 아니다. 적용되는 원문 AT-001~020과 AT-026·029·034·035의 P0 통제는 승인된 requirements.md를 따라 연결하며 어떤 단계도 현재 통과했다고 기록하지 않는다.

## 커버리지와 추적성

기능 요구사항 83개를 각각 한 행에 배정했고 미배정은 없다. U1은 30개, U2는 66개, U3는 33개 기능 행에 참여한다. 여러 단위가 참여하는 행은 32개이며 참여 건수의 합은 전체 요구사항 수와 다르다. 모든 단위에 담당 행이 있다. NFR 11개도 별도 표에 연결한다.

[traceability.json](traceability.json)은 기능 83개 각각에 대해 이 표에 있는 Unit ID 하나를 대표 target으로 기록한다. 대표 target이 단위별 책임 분담을 축소하지 않으며 전체 배정은 이 표를 기준으로 한다. 상류 ID·중복/누락·Unit ID/Directory·대표 target의 실제 행 포함 여부를 검사한다. 문서 매핑 결과는 코드/테스트 커버리지나 실제 서비스 연동 성공률이 아니다.
