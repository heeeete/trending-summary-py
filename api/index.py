from flask import Flask, jsonify, request
from flask_cors import CORS
from trendspy import Trends
import os

app = Flask(__name__)

# 환경 변수로 환경 구분 (개발/프로덕션)
ENV = os.environ.get('FLASK_ENV', 'development')

# CORS 설정
# if ENV == 'production':
#     # 프로덕션 환경: 특정 도메인만 허용
#     allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'https://your-frontend-domain.com')
#     CORS(app, resources={r"/*": {"origins": allowed_origins.split(',')}})
# else:
    # 개발 환경: 모든 요청 허용
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/trending', methods=['GET'])
def get_trending():
    # 쿼리 파라미터 파싱
    country = request.args.get('country', 'kr').lower()

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

        # TrendKeyword 객체를 딕셔너리로 변환
        serializable_trends = []
        for trend in trends:
            # 객체의 속성을 딕셔너리로 변환
            try:
                # __dict__를 사용하여 객체의 모든 속성을 딕셔너리로 변환
                trend_dict = trend.__dict__
                # 또는 직접 필요한 속성만 추출
                # trend_dict = {
                #     "title": getattr(trend, "title", ""),
                #     "query": getattr(trend, "query", ""),
                #     # 다른 필요한 속성들...
                # }
                serializable_trends.append(trend_dict)
            except:
                # 객체를 문자열로 변환하여 추가
                serializable_trends.append(str(trend))

        # JSON 응답 생성
        response = {
            'country': geo_code,
            'trends': serializable_trends
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': '트렌딩 API에 오신 것을 환영합니다',
        'endpoints': {
            'trending': '/api/trending?country=[kr|jp|us]'
        }
    })

# 잘못된 URL 형식도 지원
@app.route('/country=<country>', methods=['GET'])
def redirect_country(country):
    return get_trending()

if __name__ == '__main__':
    app.run(debug=True)
