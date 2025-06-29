from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
from trendspy import Trends

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 쿼리 파라미터 파싱
        query_components = parse_qs(urlparse(self.path).query)
        country = query_components.get('country', ['kr'])[0].lower()

        # 국가 코드 매핑
        country_mapping = {
            'kr': 'KR',  # 한국
            'jp': 'JP',  # 일본
            'us': 'US',  # 미국
        }

        geo_code = country_mapping.get(country, 'KR')  # 기본값은 한국

        # 트렌딩 데이터 가져오기
        try:
            tr = Trends()
            trends = tr.trending_now(geo=geo_code)

            # 응답 준비
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # JSON 응답 생성
            response = {
                'country': geo_code,
                'trends': trends
            }

            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

