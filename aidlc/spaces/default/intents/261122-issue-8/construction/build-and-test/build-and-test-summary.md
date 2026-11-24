# 빌드 및 테스트 요약

공통 검증 18개와 별도 보존 검증 5개가 통과했습니다. 승인 계약 구조와 재현 가능한 로컬 검증 기준으로 PR 검토가 가능합니다.

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| U1-SCHEMA | 승인 계약 요약과 구현 계획 | Draft 2020-12 명세 12개의 지문 및 구조 일치 | 공통 9개와 보존 3개 통과 | test-results.md, test_schemas.py, check_preserved_contracts.py | Build and Test | Met |
| U1-REGISTRY | 승인 계약 C01~C03, U1 WF1 | 등록 ID·fragment 및 참조를 로컬에서 해석하고 미등록 참조 거부 | 버전, fragment, 외부 참조 거부 검사 통과 | test-results.md, test_registry.py | Build and Test | Met |
| U1-VECTORS | 승인 계약 사례와 구현 계획 | 정상·오류·경계의 승인 합성 구조 판정 | 공통 43개 및 보존 11개 사례 통과 | test-results.md | Build and Test | Met |
| BR7.4 | 승인 U1 기능 설계 | 공통 검사와 U2 소유 구조 검사의 분리 | 별도 실행과 재검토 완료 | cross-unit-traceability.md, code-generation/reviews/review-02.md | Build and Test | Met |

제품 의미 판정, RFC 8785 전체 적격성, 실제 재시도·동시성, Garmin 연동 및 배포 준비도는 검증하지 않았습니다. 이 작업에서는 스키마와 합성 구조 사례의 판정 범위를 확인했습니다.
