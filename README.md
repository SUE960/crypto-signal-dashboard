# 암호화폐 커뮤니티-거래 상관관계 대시보드

텔레그램 커뮤니티 활동과 암호화폐 거래량/가격 변동 간의 상관관계를 분석하고 실시간 스파이크를 감지하는 대시보드입니다.

## 주요 기능

### 📊 Overview
- 실시간 ETH/BTC 가격 모니터링
- 24시간 거래량 및 커뮤니티 활동 통계
- 시계열 차트 (가격, 거래량, 감정 분석)
- 캔들스틱 차트 및 볼린저 밴드

### 🔍 상관관계 분석
- Pearson/Spearman 상관계수 히트맵
- 시차 상관관계 분석 (Lag Correlation)
- 그랜저 인과관계 검정 (Granger Causality)
- 변동성 분석 (커뮤니티 활동 급증 시 가격 변동성)

### 🚨 스파이크 알람
- Z-score 기반 이상치 탐지
- 이동평균 기반 급등/급락 감지
- 다중 지표 통합 스파이크 점수
- 실시간 알람 시스템
- 커스터마이징 가능한 알람 설정

## 프로젝트 구조

```
/Volumes/T7/class/2025-FALL/big_data/
├── data/                                    # 데이터 파일
│   ├── whale_transactions_rows_ETH_rev1.csv # 시간별 ETH 거래 집계
│   ├── price_history_eth_rows.csv          # ETH 가격 데이터
│   ├── price_history_btc_rows.csv          # BTC 가격 데이터
│   ├── telegram_data.csv                   # 텔레그램 커뮤니티 데이터 (수집 후 생성)
│   ├── processed_data.csv                  # 전처리된 통합 데이터 (생성)
│   └── alert_history.csv                   # 알람 이력 (생성)
├── scripts/
│   ├── collect_telegram_data.py            # 텔레그램 데이터 수집
│   └── preprocess_data.py                  # 데이터 전처리
├── analysis/
│   ├── correlation_analysis.py             # 상관관계 분석 모듈
│   └── spike_detector.py                   # 스파이크 감지 알고리즘
├── components/
│   ├── charts.py                           # Plotly 차트 컴포넌트
│   ├── metrics.py                          # 지표 계산 함수
│   ├── alerts.py                           # 알람 UI 컴포넌트
│   └── filters.py                          # 필터 UI 컴포넌트
├── utils/
│   ├── data_loader.py                      # 데이터 로딩 유틸
│   └── alert_system.py                     # 알람 시스템
├── app.py                                  # Streamlit 메인 애플리케이션
├── requirements.txt                        # 패키지 의존성
├── env.example                             # 환경 변수 예제
└── README.md                               # 이 파일
```

## 설치 및 실행

### 1. 환경 설정

```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. Telegram API 설정

1. https://my.telegram.org/auth 에 접속하여 로그인
2. "API development tools"를 클릭
3. 앱 정보를 입력하고 API ID와 API Hash 발급
4. `env.example` 파일을 복사하여 `.env` 파일 생성

```bash
cp env.example .env
```

5. `.env` 파일을 열어 API 정보 입력:

```
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_PHONE=+821012345678
TELEGRAM_CHANNELS=@Ethereum,@Bitcoin,@CryptoNews,@binance_announcements
```

### 3. 데이터 수집

```bash
# 텔레그램 데이터 수집
python scripts/collect_telegram_data.py
```

처음 실행 시 전화번호 인증이 필요합니다. SMS로 받은 인증 코드를 입력하세요.

### 4. 데이터 전처리

```bash
# 모든 데이터를 통합하고 파생 변수 생성
python scripts/preprocess_data.py
```

이 과정에서 `data/processed_data.csv` 파일이 생성됩니다.

### 5. 대시보드 실행

```bash
streamlit run app.py
```

브라우저에서 http://localhost:8501 로 접속하여 대시보드를 확인할 수 있습니다.

## 데이터 설명

### 고래 거래 데이터 (whale_transactions_rows_ETH_rev1.csv)
- `timestamp`: 시간 (1시간 단위)
- `tx_frequency`: 거래 빈도
- `tx_amount`: 거래 금액 (ETH)
- `tx_amount_usd`: 거래 금액 (USD)

### 가격 데이터 (price_history_eth_rows.csv, price_history_btc_rows.csv)
- `timestamp`: 시간
- `open_price`, `high_price`, `low_price`, `close_price`: OHLC 가격
- `volume`: 거래량
- `trade_count`: 거래 횟수

### 텔레그램 데이터 (telegram_data.csv)
- `timestamp`: 시간
- `channel`: 채널명
- `message_count`: 메시지 수
- `avg_views`: 평균 조회수
- `total_forwards`: 총 전달 횟수
- `total_reactions`: 총 반응 수
- `avg_sentiment`: 평균 감정 점수 (-1 ~ +1)

## 분석 방법

### 상관관계 분석
- **Pearson 상관계수**: 두 변수 간의 선형 관계 측정
- **Spearman 상관계수**: 순위 기반 비선형 관계 측정
- **시차 상관관계**: 시간차를 두고 변수 간 영향 관계 분석
- **그랜저 인과관계**: 한 변수가 다른 변수를 '야기'하는지 통계적 검정

### 스파이크 감지
- **Z-score 방식**: 평균에서 표준편차의 2.5배 이상 벗어난 값 감지
- **이동평균 방식**: 이동평균 대비 50% 이상 변화 감지
- **변화율 방식**: 단기간(3시간) 동안 30% 이상 급변 감지
- **다중 지표**: 여러 지표가 동시에 이상 신호를 보일 때 감지

## 활용 예시

### 1. 커뮤니티 활동과 가격의 관계 분석
- 텔레그램 메시지 수 증가가 가격 상승을 선행하는지 확인
- 시차 상관관계 분석으로 최적 시차 파악

### 2. 고래 거래 패턴 모니터링
- 고래 거래 급증 시 가격 변동성 측정
- 커뮤니티 활동과의 연관성 분석

### 3. 스파이크 알람 활용
- 커뮤니티 활동 급증 시 자동 알람
- 가격 급등/급락 감지
- 다중 지표 동시 이상 신호 감지

## 문제 해결

### 데이터 파일이 없다는 오류
```bash
# 전처리 스크립트를 먼저 실행하세요
python scripts/preprocess_data.py
```

### Telegram API 인증 오류
- `.env` 파일의 API 정보가 올바른지 확인
- 전화번호 형식이 +국가코드 형식인지 확인 (예: +821012345678)
- session_name.session 파일 삭제 후 재시도

### 메모리 부족 오류
- 날짜 필터로 분석 기간을 줄이세요
- 샘플링을 통해 데이터 크기 축소

## 기술 스택

- **데이터 수집**: Telethon (Telegram API)
- **데이터 처리**: pandas, numpy
- **분석**: scipy, statsmodels, scikit-learn
- **감정 분석**: VADER Sentiment
- **시각화**: Plotly
- **대시보드**: Streamlit

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.

## 참고 자료

- [Telethon 문서](https://docs.telethon.dev/)
- [Streamlit 문서](https://docs.streamlit.io/)
- [Plotly 문서](https://plotly.com/python/)
- [Granger Causality Test](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.grangercausalitytests.html)

