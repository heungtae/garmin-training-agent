## Summary

- Builds: 승인된 U1 교환 스키마 12개, 등록 fragment, 고정 로컬 registry 및 독립 검증
- Touches: `spec/u1/`, `tests/u1/`, 이 intent의 구현·검증·리뷰 기록
- Tests: 세 검증 영역에 각 5~8개 테스트를 두고 스키마 12개 전수 검사와 합성 계약 경계 사례를 포함합니다.

## 승인 기준과 범위

기준 커밋은 `924706f7f24a5b81627afcef88c9c728062fd7ef`입니다. 기존 `261115-garmin-design`의 Contract Design 계약 요약, U1 Functional Design의 엔티티·규칙·흐름, U1 NFR 설계와 단위 추적표를 사용합니다. JSON Schema Draft 2020-12, 승인된 ID와 참조, 필수 필드와 등록 항목을 보존합니다. 기준 내용이나 공유 계약의 변경이 필요하면 차이를 보고하고 결정을 받습니다.

## 실행 순서

- [x] Step 1. `spec/u1/`과 `tests/u1/`의 구조를 준비합니다. 테스트 전용 Python 환경에서 `unittest`와 Draft 2020-12를 지원하는 `jsonschema`를 사용합니다. 테스트 의존성 버전을 명시하고 단위 범위 명령이 실행되는지 확인합니다.
- [x] Step 2. 스키마 Red. 승인 기준 대비 12개 스키마의 누락, ID 중복, dialect, 메타스키마, 필수 필드와 승인 JSON 구조 대조 테스트를 추가하고 실패 결과를 기록합니다.
- [x] Step 3. 스키마 Green. 승인된 JSON 블록을 Common과 C01~C08을 포함한 12개 파일로 옮기고 전수 검사를 통과시킵니다.
- [x] Step 4. 스키마 Refactor. 승인된 JSON 의미를 유지한 채 테스트의 반복을 정리하고 재실행합니다.
- [x] Step 5. registry Red. 등록 fragment 일치, 로컬 참조 닫힘, 중복과 개발 중 누락, 미등록 URI 거부, 외부 조회 금지를 검사합니다.
- [x] Step 6. registry Green. 승인 등록 항목과 로컬 파일을 사용하는 고정 registry를 구성하고 스키마 로딩부터 검증까지 연결합니다.
- [x] Step 7. registry Refactor. 로딩과 검증 단계의 중복을 정리하고 전체 U1 테스트를 재실행합니다.
- [x] Step 8. 계약 사례 Red. 승인된 합성 사례로 정상, 필수 필드 누락, enum 및 버전, 형식과 경계, 계약 간 참조의 기대값을 정의합니다.
- [x] Step 9. 계약 사례 Green. 고정 registry로 사례를 독립 검증합니다. 합성 사례에서 구조 검증과 의미 규범의 기대값을 구분하고, 실행하지 않은 제품 의미 검사, 재시도 및 동시성 항목을 기록합니다.
- [x] Step 10. 계약 사례 Refactor. 입력 재사용을 정리하고 합성 사례가 실제 사용자 데이터를 포함하지 않는지 확인합니다.
- [ ] Step 11. 승인 설계와 파일·테스트의 추적표, Red/Green 명령 및 결과, 미검증 범위를 기록합니다. 구현 결과를 독립 리뷰에 제출하고 검증·리뷰 증거를 개별 PR에 연결합니다. PR 대상은 `main`이며 이슈는 머지 전까지 열린 상태로 둡니다.

## Assumptions

Python과 검증 라이브러리는 U1 테스트를 위한 선택입니다. 스키마 계약과 소비자 기술 선택에는 영향을 주지 않습니다. U2, U3, 제품 SDK, DB, Garmin 연결 및 배포는 범위 밖입니다.

## Testing Contract

```json
{
  "version": 1,
  "methodology": "tdd",
  "source": "team",
  "ordering": "각 검증 항목의 실패 테스트를 먼저 작성한 뒤 그 테스트를 통과하도록 구현합니다.",
  "scope": "express",
  "test_strategy": "standard",
  "project_type": "greenfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop`, `classic` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "team",
      "text": "- **Methodology**: tdd\n- **Methodology evidence**: Q3의 B를 선택했습니다.\n- **Ordering**: 각 검증 항목의 실패 테스트를 먼저 작성한 뒤 그 테스트를 통과하도록 구현합니다.\n- 승인 기준의 스키마 12개에 대한 메타스키마 검사, 로컬 참조 검사, 정상·오류·경계의 합성 사례 검증을 포함합니다. 재시도·동시성 조건 중 U1에서 확인 가능한 범위와 미실행 범위를 기록합니다.\n- U1 자체 검증은 U2, U3, SDK 또는 DB 설치를 요구하지 않습니다. 실행 명령과 결과를 개별 PR에 기록합니다."
    }
  ],
  "obligations": {
    "strategy": "standard",
    "strategy_volume": [
      "Five to eight tests per component.",
      "Unit tests plus integration tests for key boundaries.",
      "Add E2E, performance, or security tests when requirements demand them."
    ],
    "scope_floor": [
      "Keep the existing test suite green.",
      "This scope adds no extra new-test floor beyond the selected test strategy."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "tdd",
    "runner_step": "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - Red: write the failing tests and record the failing command output.",
      "Data model / database behavior - Green: implement only enough behavior to pass.",
      "Data model / database behavior - Refactor: improve the implementation while tests stay green.",
      "Repository / data access - Red: write the failing tests and record the failing command output.",
      "Repository / data access - Green: implement only enough behavior to pass.",
      "Repository / data access - Refactor: improve the implementation while tests stay green.",
      "Business logic - Red: write the failing tests and record the failing command output.",
      "Business logic - Green: implement only enough behavior to pass.",
      "Business logic - Refactor: improve the implementation while tests stay green.",
      "API / endpoint - Red: write the failing tests and record the failing command output.",
      "API / endpoint - Green: implement only enough behavior to pass.",
      "API / endpoint - Refactor: improve the implementation while tests stay green.",
      "Frontend behavior - Red: write the failing tests and record the failing command output.",
      "Frontend behavior - Green: implement only enough behavior to pass.",
      "Frontend behavior - Refactor: improve the implementation while tests stay green.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:2449f9e3ae18c0488b02428d42fcc1ecc00ffba949dbc0359e702a705e172370",
  "contract_sha256": "sha256:7ac55d001e7fd652748facc313a57fde7df63ebcfd2ef295246e1a0acbb331cf"
}
```
