<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs.

## Interpretations

- 2026-11-17T05:21:14Z — 승인된 계획에 따라 공통 교환 명세 spec·Linux service·ChatGPT 워크플로 spec의 3개 단위를 작성했다. 도메인 컴포넌트 8개와 엔티티 31개의 소유를 보존하고 FR 83개·NFR 11개를 연결했다.
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs

- 2026-11-17T05:21:14Z — U2와 U3는 U1 명세에 각각 의존하며 상대 구현 없이 자체 검증하도록 범위를 구분했다. 실제 Drive 왕복 자료 흐름·승인 신뢰·외부 권한과 제품 전체 인수는 별도 증거가 필요하며 단위 자체 대역 시험으로 대체하지 않는다.
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions

- 2026-11-17T05:21:14Z — 공통 명세의 실제 형식·승인 증명·정책 최신성·지원 도구 경로는 Contract Design의 해소 조건이다. 실제 필수 빌드/테스트에서 상대 구현이 필요해지면 의존 간선과 단위 계획을 재검토해야 한다.
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
