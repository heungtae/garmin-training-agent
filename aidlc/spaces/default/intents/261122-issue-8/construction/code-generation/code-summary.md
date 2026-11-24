# Garmin #8 코드 생성 결과

## 구현 범위

- `spec/u1/*.schema.json`의 JSON Schema Draft 2020-12 파일 12개는 승인 기준 커밋 `924706f7f24a5b81627afcef88c9c728062fd7ef`의 계약 요약 JSON 블록을 옮긴 것입니다. Common, C01~C08, LLM_REQUEST, LLM_RESPONSE, EVALUATION을 포함합니다.
- `spec/u1/registry.json`은 Common과 C01~C08의 버전 ID 및 C03 등록 Detail fragment를 고정합니다. 보존한 U2 소유 LLM_REQUEST, LLM_RESPONSE, EVALUATION은 별도 `spec/u1/u2-owned-registry.json`에 등록합니다.
- `tests/u1/u1_validation.py`는 명세 파일과 registry를 연결하고 라이브러리의 로컬 참조 해석 및 형식 검사를 사용합니다. 등록되지 않은 식별자와 fragment는 거절합니다. 소비자는 제품 SDK나 DB 없이 명세 파일을 읽을 수 있습니다.
- `tests/u1/contract-cases.json`은 승인된 합성 사례와 기대값을 보존합니다. Python 의존성은 `tests/u1/requirements.txt`에 두었습니다.

## 추적 및 검증

| 승인 설계 범위 | 구현 및 증거 |
| --- | --- |
| 계약 요약 공통 형식, C01~C08 및 LLM 형식 | `spec/u1/*.schema.json`, 공통 및 보존 검사의 승인 커밋 SHA-256 지문과 메타스키마 대조 |
| U1 WF1과 계약 요약의 고정 버전 및 로컬 참조 원칙 | `spec/u1/registry.json`, `tests/u1/test_registry.py`의 전체 참조, Detail fragment, 미등록 버전·URI, 중복·누락 확인 |
| U1 WF2~WF7 데이터 형식 및 합성 기대값 | `tests/u1/test_contract_cases.py`의 공통 구조 사례 43개와 별도 URI·날짜시간 형식 사례 |
| U2 소유 구조 및 승인 원본 보존 | `tests/u1/check_preserved_contracts.py`의 U2 사례 11개, 원본 전체 지문 및 사례 소유자 확인 |

현재 intent는 Requirements Analysis와 Units Generation을 건너뛴 단계 수준 실행입니다. 자동 추적 도구가 할당한 상류 ID는 0개입니다. 추적 파일의 BR7.4는 기존 승인 U1 설계에서 가져왔으며, 공통 검사가 U2 소유 스키마 없이 실행되는 범위를 가리킵니다. U2 소유 사례와 전체 원본 보존은 별도 검사에 기록했습니다.

## 테스트 결과

Python 3.14 격리 환경에서 공통 검사 18개와 별도 보존 검사 5개가 통과했습니다. Common 및 C01~C08 파일과 공통 fixture만 복사한 임시 검증 디렉터리에서도 공통 검사 18개가 통과했습니다. 두 검사 모두 외부 스키마 조회 없이 합성 자료를 사용합니다.

```bash
python3 -m venv .u1-test-venv
.u1-test-venv/bin/python3 -m pip install -r tests/u1/requirements.txt
PYTHONDONTWRITEBYTECODE=1 .u1-test-venv/bin/python3 -m unittest discover -s tests/u1 -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 .u1-test-venv/bin/python3 -m unittest discover -s tests/u1 -p 'check_preserved_contracts.py' -v
```

승인 기준 커밋 `924706f7f24a5b81627afcef88c9c728062fd7ef`에서 JSON 코드 블록의 LF 바이트를 추출해 SHA-256 지문을 고정했습니다. 재실행에는 Git 이력이나 작업 트리의 계약 요약이 필요하지 않습니다.

| 구간 | Red | Green 및 정리 후 |
| --- | --- | --- |
| 스키마 | 스키마 파일이 없을 때 5개 테스트에서 실패 1건과 하위 검사 오류 37건 | 스키마를 옮긴 뒤 5개 통과 |
| registry | 구현 전 `u1_validation` 모듈 미존재 오류 | registry와 로컬 검증 경로를 추가한 뒤 누적 13개 통과 |
| 합성 계약 사례 | 사례 파일 미존재 오류 | 승인 사례와 형식 검사를 포함한 최초 구현에서 누적 19개 통과. 리뷰 대응 후 공통 검사와 보존 검사를 각각 18개, 5개 실행 |

## 남은 검증과 인계

합성 사례 파일의 원시 JSON 파싱 및 제품 의미 게이트 기대값은 보존했습니다. 실제 제품 판정, RFC 8785 전체 적격성, 재시도 및 동시성, 외부 연동은 실행하지 않았습니다. 공통 43개와 U2 소유 11개 승인 사례의 `expectedSchema`와 별도 URI·날짜시간 경계 결과를 확인했습니다. 리뷰 지적에 대응한 변경의 재검토와 PR 연결이 남아 있습니다.
