# Crypto Signal Dashboard

실시간 암호화폐 시장 신호 대시보드

## 🚀 Features

- 📊 텔레그램, 뉴스, 트위터 데이터 통합 분석
- 🐋 고래 거래 모니터링
- 📈 실시간 가격 추적
- 🔔 스파이크 알람 시스템
- 💡 종합 시장 신호 점수

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🎯 Usage

```bash
streamlit run main.py
```

## 📁 Project Structure

```
.
├── main.py                 # 메인 애플리케이션
├── requirements.txt        # 의존성 패키지
├── data/                   # 데이터 파일
│   └── processed_data.csv
├── utils/                  # 유틸리티 모듈
│   ├── data_loader.py
│   ├── composite_score.py
│   └── sentiment_analyzer.py
├── analysis/              # 분석 모듈
│   ├── correlation_analysis.py
│   └── spike_detector.py
├── components/            # UI 컴포넌트
│   ├── charts.py
│   ├── metrics.py
│   ├── filters.py
│   └── alerts.py
└── scripts/              # 데이터 수집 스크립트
    ├── collect_telegram_data.py
    ├── collect_coinness_selenium.py
    └── preprocess_data.py
```

## 🌐 Deployment

Streamlit Cloud로 배포:
1. GitHub 저장소 연결
2. Main file path: `main.py`
3. Python version: 3.11

## 📄 License

MIT
