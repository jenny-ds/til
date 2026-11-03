---
date: 2026-11-03
topic: dev-basics
tags: [database, sql, crud, schema, nosql]
source: books/vibe-coder-minimum-ai-it-knowledge
type: reading
---

# 데이터베이스와 SQL에 대하여

## 오늘 배운 것

- 데이터베이스는 데이터를 체계적으로 저장하는 곳이고, 관계형 DB는 데이터를 테이블로 관리한다.
- 테이블의 구조를 미리 정해둔 설계도를 스키마라 하고, 데이터를 다룰 때는 SQL이라는 언어를 쓴다.
- 데이터 조작의 기본은 CRUD이고, SQL로는 INSERT, SELECT, UPDATE, DELETE에 해당한다. 테이블 구조에 얽매이지 않는 방식은 NoSQL이라 한다.

## 상세 내용

서비스의 회원 정보나 주문 내역은 어디에 저장될까? 바로 데이터베이스다. 가장 많이 쓰는 관계형 DB는 데이터를 엑셀 시트처럼 테이블에 저장한다.

- 레코드: 테이블의 가로 한 줄. 예) 회원 한 명의 정보
- 칼럼: 테이블의 세로 한 줄. 예) 이름, 이메일 같은 항목

테이블을 만들기 전에 어떤 칼럼이 있고 각 칼럼에 어떤 타입이 들어갈지 정해두는데, 이 설계도를 스키마라 한다.

데이터를 다루는 기본 동작은 생성, 조회, 수정, 삭제 4가지로 CRUD라 부르고, DB에 이 명령을 내리는 언어가 SQL이다.

1. Create → INSERT
2. Read → SELECT
3. Update → UPDATE
4. Delete → DELETE

```sql
SELECT name, email FROM users WHERE id = 1;
```

전에 배운 API의 HTTP 메서드(POST, GET, PUT, DELETE)도 CRUD에 대응된다.
앱에서 API를 호출하면 서버가 SQL로 DB를 조작하는 구조다.

반면 NoSQL은 정해진 스키마 없이 JSON 같은 형태로 데이터를 자유롭게 저장하는 DB다(예: MongoDB). 구조가 자주 바뀌거나 데이터 양이 많을 때 유리하다.
