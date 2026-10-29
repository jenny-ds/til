---
date: 2026-10-28
topic: dev-basics
tags: [dns, ip-address, nxdomain]
source: books/vibe-coder-minimum-ai-it-knowledge
type: reading
---

# DNS와 DNS 룩업

## 오늘 배운 것

- DNS는 google.com 같은 도메인 이름을 IP 주소로 바꿔주는 시스템이고, 그 과정이 DNS 룩업이다.
- IP 주소는 사람이 외우기 어려워서 도메인 이름을 쓴다.
- NXDOMAIN 에러는 DNS에 물어보니 그런 도메인이 없다는 뜻이다.

## Q&A

**Q. IP 주소란?**
인터넷에 연결된 각 기기들이 통신하기 위해 사용하는 고유한 주소이다.

**Q. IP 주소는 어떻게 생겼나?**
111.222.121.123처럼 0~255 사이 숫자와 마침표로 구성된 IPv4 형식이 있고, 이 주소가 부족해서 새로 만들어진 IPv6 형식이 있다.

**Q. 왜 도메인 이름을 쓰나?**
IP 주소는 사람이 외우기 어렵기 때문에 google.com 같은 도메인 이름을 쓴다.

**Q. DNS와 DNS 룩업은?**
google.com을 입력했을 때 다시 IP 주소로 변환해주는 시스템이 DNS(Domain Name System)이고, 그 변환 과정이 DNS 룩업이다.

**Q. 크롬의 "DNS_PROBE_FINISHED_NXDOMAIN"은 무슨 뜻인가?**
- DNS_PROBE: Chrome이 접속 실패 후 DNS 쪽 문제인지 진단(probe)을 돌림
- FINISHED: 그 진단이 끝났고
- NXDOMAIN: 결과가 "그런 도메인은 존재하지 않음(Non-eXistent Domain)"

즉, DNS에 물어보니 그런 도메인은 없다는 의미이다.

**Q. 이 에러가 뜨면 어디가 문제인가?**
내 인터넷 환경이 아닌 해당 도메인의 문제일 가능성이 높다. 물론 인터넷 연결에 일시적 문제가 있을 수도 있다.
