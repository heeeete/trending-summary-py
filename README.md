# 트렌딩 요약 API

Vercel에 배포된 간단한 국가별 트렌딩 정보 API입니다.

## API 사용법

### 트렌딩 정보 가져오기

```
GET /api/trending?country=[국가코드]
```

#### 쿼리 파라미터

- `country`: 국가 코드 (기본값: kr)
  - `kr`: 한국
  - `jp`: 일본
  - `us`: 미국

#### 예시 요청

```
/api/trending?country=kr
```

#### 응답 형식

```json
{
	"country": "KR",
	"trends": [
		// 트렌딩 정보 배열
	]
}
```

## 배포 방법

1. Vercel CLI 설치: `npm i -g vercel`
2. 로그인: `vercel login`
3. 배포: `vercel`
