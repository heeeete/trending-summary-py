from flask import Flask, jsonify, request
from flask_cors import CORS
from trendspy import Trends
import os

app = Flask(__name__)

# CORS 설정
# 허용할 도메인 목록
allowed_origins = [
    'https://v0-modern-trending-summary.vercel.app',
    'http://localhost:3000',  # 로컬 개발 환경
    'http://localhost:3001',  # 로컬 개발 환경 (다른 포트)
    'http://127.0.0.1:3000',  # 로컬 개발 환경
    'http://127.0.0.1:3001',  # 로컬 개발 환경 (다른 포트)
]

CORS(app, resources={r"/*": {"origins": allowed_origins}})

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
        for trend in trends[:20]:  # 최대 20개로 제한
            # 객체의 속성을 딕셔너리로 변환
            try:
                # __dict__를 사용하여 객체의 모든 속성을 딕셔너리로 변환
                trend_dict = trend.__dict__
                serializable_trends.append(trend_dict)
            except:
                # 객체를 문자열로 변환하여 추가
                serializable_trends.append(str(trend))

        # JSON 응답 생성
        response = {
            'country': geo_code,
            'trends': serializable_trends
        }

        # 캐시 방지 헤더 추가
        resp = jsonify(response)
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
        return resp
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    # 캐시 방지 헤더 추가
    resp = jsonify({
        'message': '트렌딩 API에 오신 것을 환영합니다',
        'endpoints': {
            'trending': '/api/trending?country=[kr|jp|us]'
        }
    })
    return resp



if __name__ == '__main__':
    # 개발 환경에서는 디버그 모드 활성화
    app.run(debug=True)
