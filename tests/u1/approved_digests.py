from hashlib import sha256


# JSON 블록의 바이트 지문. 기준 커밋 924706f7f24a5b81627afcef88c9c728062fd7ef.
SCHEMA_SHA256 = {
    "common": "99171540be84fb12fe644fb9cd63919d1f98193062fd1a35fcb033894a28f2a7",
    "C01": "1740cc716f68d5a2b3fa881d549f5c18f5b4bbfefe796e7eca06de5be0fb490d",
    "C02": "fbc2408354613f8ea2c0e8783076477d35a6ddfcf9f4d506afde3ffc72234cc7",
    "C03": "e42c6223be7e7bcd5da2d5cace5bf6f058a878bd03cbaf3de3e83444803c0838",
    "C04": "72de1d1f6579faa80242746553a0572641c8c4f32333ae9032de46b912e8b7b8",
    "C05": "2fdf03168165cc648deaa762d547fc33712934b2db565dd6e21e55a8df36a2c0",
    "C06": "4bed8448467fca57d7123875f581cd3d05567862600e4f5db442dd31f51829ed",
    "C07": "9dca085d0409a9d653dbfc785cf5211d7c0856a42ab9005a2921b88d1772ce67",
    "C08": "537623e7ccdb64c5b307bfe181e2f1d6ba974a48a8e934845cb951ef81490065",
    "LLM_REQUEST": "153f9ea884cbb7f0f23b72e55cd371ba3d73165ce3b250e81fa3ea7e740ba830",
    "LLM_RESPONSE": "81d0b3bf9e98fdcba3d9285d813f6695a01deb055fc24e86cddbf4f260898625",
    "EVALUATION": "946cfd09c96306beef70d9ec7973c3be74a8f70b91506543475e0400b7572e4b",
}
VECTORS_SHA256 = "660fe56f8f546dc263549119ae6afad22e0dd8f88a3d9585f5119c71df21b721"


def digest(path):
    # 체크아웃의 줄 끝 변환과 관계없이 승인 원본의 LF 기준으로 비교한다.
    return sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
