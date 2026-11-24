# 빌드 및 검증 환경

교환 산출물은 JSON Schema와 로컬 레지스트리입니다. 배포용 컴파일 단계가 없으며 메타스키마 검사로 명세를 확인합니다. 저장소 루트에서 Python 3 가상환경을 준비합니다.

```bash
python3 -m venv .u1-test-venv
.u1-test-venv/bin/python3 -m pip install -r tests/u1/requirements.txt
.u1-test-venv/bin/python3 -m pip check
```

형식 검증이 실패하면 위 가상환경의 인터프리터와 requirements 설치 여부를 확인합니다. 설치 후 검증은 원격 스키마 조회 없이 실행합니다.
