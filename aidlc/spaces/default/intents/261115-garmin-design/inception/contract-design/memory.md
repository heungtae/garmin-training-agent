<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs.

## Interpretations

- 2026-11-18T00:36:11Z — 사용자 변경에 따라 Ollama 사용을 제외하고 원격 OpenAI를 초기 검증 대상으로 유지했다. 기존 로컬/사설 연결 유형 P0는 대체 제공자 미정으로 남기며, 변경한 요약의 명시적 확인(c1e583e1)을 받은 후 계약 문서를 작성했다.
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs

- 2026-11-18T00:36:11Z — 교환 계약 8개·외부 소비 프로필 5개와 JSON Schema 12개를 정의했다. 승인 선언/정상 해시/원격 파일 소유는 실제 인간 의도와 내용·행위의 신뢰 검증을 대신하지 않도록 분리했다. 문서 구조 사례 47개·파싱 사례 7개와 참조 132개는 검사했으나 실제 승인/API/모델/환경 인수는 미검증이다.
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions

- 2026-11-18T00:36:11Z — 승인 발급/검증 프로필·U3 정책 최신성·실제 클라이언트 JSON 쓰기/읽기·Garmin 상세 계약·로컬/사설 대체 제공자·모델/비용·실행 한도·안전 규칙의 적격성이 미해소다. 각 차단 기능과 해소 조건을 계약 문서에 명시했다.
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
