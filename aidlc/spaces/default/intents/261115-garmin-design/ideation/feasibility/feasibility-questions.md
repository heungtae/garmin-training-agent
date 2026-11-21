# 타당성 및 제약 확인

입력: [승인된 목적 정의](../intent-capture/intent-statement.md), 요구사항 문서의 VAL-001~008 및 OPEN-001~020. 개인용·P0 우선·사용자 승인 경계는 기존 결정을 유지한다. 비밀키·토큰·실제 건강 데이터는 답변에 포함하지 않는다.

## Q1. Garmin 연동의 현재 접근 상태는 무엇인가요?
A. 공식 API 접근 권한과 문서가 있다. 비밀정보 없이 API 이름과 공개 문서 또는 승인 범위를 설명한다.
B. Garmin Connect 개인 계정만 있고 별도 API 접근 권한은 확인하지 않았다.
C. Not yet defined — 접근 상태를 아직 모른다.
X. Other (please specify)

[Answer]: A. 공식 API 접근 권한을 보유함(사용자 확인). 키 이름은 `GARMIN_API_KEY`. 제공 문서: https://developer.garmin.com/gc-developer-program/personal/swagger-docs/ . 키 값은 제공받거나 저장하지 않았다. 실제 호출 성공과 세부 권한 범위는 미검증이다.

## Q2. ChatGPT·Google·GitHub 연동 환경은 어느 정도 준비되어 있나요?
A. 실제 사용할 ChatGPT 웹·모바일 환경 및 Drive/GitHub 읽기·쓰기, Calendar 권한을 확인했다. 확인한 환경·동작을 비밀정보 없이 설명한다.
B. 계정은 있으나 각 환경의 읽기·쓰기 가능 여부와 프로그램용 권한은 미검증이다.
C. Not yet defined — 계정·환경도 아직 정하지 않았다.
X. Other (please specify)

[Answer]: B. 계정은 있으나 각 환경의 읽기·쓰기 가능 여부와 프로그램용 권한은 미검증이다.

## Q3. 기술 및 운영 환경 제약은 무엇인가요?
A. 문서의 Rust·Linux 조건을 유지한다. 대상 배포판·버전, 개발 경험 및 추가 필수 기술을 설명한다.
B. Rust·Linux만 확정하며 배포판·실행 보장 범위·나머지 기술은 설계에서 비교한다. 개발 경험은 미정으로 기록한다.
C. Not yet defined — 문서의 확정 조건도 재검토가 필요하다.
X. Other (please specify)

[Answer]: A. Rust·Linux 조건을 유지하고 환경을 지정한다. 상세 값은 Q7에서 추가 확인한다.

## Q4. 개인정보 외에 적용해야 할 규정이나 저장 지역 제한이 있나요?
A. 현재 알고 있는 추가 조직 규정·인증·저장 지역 제약은 없다. 문서의 최소 권한·비공개·동의 범위·비밀정보 보호 조건을 유지한다. 법적 적용 여부를 검증한 것으로 간주하지 않는다.
B. 추가 규정이나 지역 제약이 있다(설명 필요).
C. Not yet defined — 추가 확인이 필요하다.
X. Other (please specify)

[Answer]: A. 현재 알고 있는 추가 조직 규정·인증·저장 지역 제약은 없다. 문서의 최소 권한·비공개·동의 범위·비밀정보 보호 조건을 유지한다. 법적 적용 여부를 검증한 것으로 간주하지 않는다.

## Q5. 예산·일정·조직상 제약은 무엇인가요?
A. 현재 정해진 예산 상한·마감·조직상 차단 요인은 없다. 유료 서비스 사용은 비용 조건을 정한 뒤 검토한다.
B. 비용 상한, 목표일, 개발 가능 시간 또는 차단 요인이 있다(설명 필요).
C. Not yet defined
X. Other (please specify)

[Answer]: A. 현재 정해진 예산 상한·마감·조직상 차단 요인은 없다. 유료 서비스 사용은 비용 조건을 정한 뒤 검토한다.

## Q6. 이 제품에 사용할 기존 AWS 또는 필수 클라우드 환경이 있나요?
A. 제품에 사용할 필수 AWS 계정·서비스는 없다. Linux 개인 PC 중심이며 AI-DLC 사용을 AWS 배포나 Bedrock 선택으로 간주하지 않는다.
B. 기존 계정·서비스 또는 필수 클라우드 환경이 있다(비밀정보 없이 설명 필요).
C. Not applicable — 현재 클라우드 환경은 검토 대상이 아니다.
X. Other (please specify)

[Answer]: A. 제품에 사용할 필수 AWS 계정·서비스는 없다. Linux 개인 PC 중심이며 AI-DLC 사용을 AWS 배포나 Bedrock 선택으로 간주하지 않는다.

## Q7. Q3에서 지정할 환경의 상세 값은 무엇인가요?
A. 대상 Linux 배포판·버전, 로그아웃 중 실행 필요 여부, Rust 개발 경험, 추가 필수 기술을 직접 설명한다.
B. 현재 개발 PC 환경을 기준으로 검토한다. 개발 경험과 추가 기술은 별도로 설명한다.
C. Not yet defined — 아직 정하지 않은 항목은 미정으로 남긴다.
X. Other (please specify)

[Answer]: A. 대상은 Ubuntu 24.04 이상이다. 로그아웃 중 자동 실행이 필요하다. Rust 개발 경험은 없으며 추가 필수 기술은 없다.

## Consolidated Summary Confirmation

- Garmin 공식 API 접근 권한을 보유한다는 사용자 확인을 받았다. 키 이름은 GARMIN_API_KEY이며 값은 수집하지 않았다. 제공된 Personal API Swagger 문서와 실제 호출·세부 권한 범위는 구분하며 후자는 미검증이다.
- ChatGPT·Google·GitHub 계정은 있으나 환경별 읽기·쓰기 및 프로그램용 권한은 미검증이다.
- Rust·Linux를 유지하며 Ubuntu 24.04 이상을 대상으로 한다. 로그아웃 중 자동 실행이 필요하다. Rust 개발 경험과 추가 필수 기술은 없다.
- 알려진 추가 조직 규정·인증·저장 지역 제약은 없다. 최소 권한·비공개·동의 범위·비밀정보 보호 조건을 유지하며 법적 적용 여부를 검증한 것으로 간주하지 않는다.
- 정해진 예산 상한·마감·조직상 차단 요인은 없다. 유료 서비스는 비용 조건을 정한 뒤 검토한다.
- 필수 AWS 계정·서비스는 없다. Linux 개인 PC 중심이며 AI-DLC 사용을 AWS 배포나 Bedrock 선택으로 간주하지 않는다.

위 답변을 바탕으로 타당성 평가, 제약 목록, 위험·가정·이슈·의존성 기록을 작성해도 될까요?

- Looks correct
- Request changes

[Answer]: Looks correct
