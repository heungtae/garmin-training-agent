# 교환 계약 경계 검증

빌드 지침의 가상환경에서 다음 두 명령을 실행합니다.

```bash
PYTHONDONTWRITEBYTECODE=1 .u1-test-venv/bin/python3 -m unittest discover -s tests/u1 -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 .u1-test-venv/bin/python3 -m unittest discover -s tests/u1 -p 'check_preserved_contracts.py' -v
```

공통 경로는 Common 및 C01~C08 스키마, 고정 레지스트리, 등록 Detail fragment, 합성 경계 사례를 검사합니다. 보존 경로는 U2 소유 스키마 세 개와 해당 합성 구조 사례를 별도로 확인합니다. 제품 소비자, DB와 외부 서비스는 이 실행에 연결하지 않습니다.
