"""
크립토 시그널 대시보드 - 모던 블랙 테마

텔레그램, 뉴스, 트위터 데이터를 통합하여 실시간 시장 신호 제공
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime, timedelta

# 경로 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.data_loader import DataLoader
from utils.composite_score import CompositeScoreCalculator
from analysis.spike_detector import SpikeDetector

# 페이지 설정
st.set_page_config(
    page_title="Crypto Signal Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"  # 사이드바 숨김
)

# 모던 블랙 테마 CSS
st.markdown("""
<style>
    /* 전역 스타일 */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    /* 사이드바 완전 제거 */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* 메인 컨텐츠 너비 */
    .main .block-container {
        max-width: 100%;
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    
    /* 상단 네비게이션 */
    .top-nav {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1.5rem 3rem;
        margin: -2rem -3rem 2rem -3rem;
        border-bottom: 1px solid #333;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo {
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 신호 박스 카드 - 작고 컴팩트 */
    .signal-box {
        background: rgba(50, 50, 50, 0.3);
        border: 1px solid rgba(100, 100, 100, 0.3);
        border-radius: 8px;
        padding: 12px 8px;
        margin: 4px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
        backdrop-filter: blur(10px);
    }
    
    .signal-box:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 212, 255, 0.5);
        box-shadow: 0 4px 16px rgba(0, 212, 255, 0.15);
    }
    
    .signal-title {
        font-size: 11px;
        font-weight: 600;
        color: #00d4ff;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        text-align: center;
    }
    
    .signal-arrow {
        font-size: 20px;
        text-align: center;
        margin: 4px 0;
        color: #7b2ff7;
        line-height: 1;
    }
    
    .signal-value {
        font-size: 18px;
        font-weight: 700;
        text-align: center;
        color: #00d4ff;
        line-height: 1.2;
    }
    
    .signal-label {
        font-size: 9px;
        text-align: center;
        color: #888;
        text-transform: uppercase;
        margin-top: 2px;
    }
    
    /* 종합 점수 카드 - 상단 강조 */
    .score-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        border-radius: 12px;
        padding: 20px 40px;
        text-align: center;
        margin: 16px 0 24px 0;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
        border: 2px solid rgba(59, 130, 246, 0.5);
    }
    
    .score-value {
        font-size: 48px;
        font-weight: 900;
        color: #ffffff;
        line-height: 1;
        margin: 8px 0;
    }
    
    .score-label {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .score-change {
        font-size: 18px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    /* 차트 컨테이너 */
    .chart-container {
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    
    /* 지표 리스트 - Upbit 스타일 */
    .indicator-list {
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 12px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .indicator-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 8px;
        border-bottom: 1px solid #1a1a1a;
        transition: background 0.2s;
    }
    
    .indicator-item:hover {
        background: rgba(255, 255, 255, 0.05);
    }
    
    .indicator-name {
        font-size: 13px;
        color: #ffffff;
        font-weight: 500;
    }
    
    .indicator-value {
        font-size: 16px;
        font-weight: 700;
        text-align: right;
    }
    
    .indicator-change {
        font-size: 12px;
        text-align: right;
        margin-top: 2px;
    }
    
    .positive {
        color: #ef4444;
    }
    
    .negative {
        color: #3b82f6;
    }
    
    .neutral {
        color: #888;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 8px;
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #888;
        font-weight: 600;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7b2ff7 0%, #00d4ff 100%);
        color: #ffffff;
    }
    
    /* CTA 버튼 */
    .cta-button {
        background: linear-gradient(135deg, #00ff87 0%, #00d4ff 100%);
        color: #000;
        padding: 20px 48px;
        border-radius: 12px;
        font-size: 20px;
        font-weight: 700;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        margin: 32px auto;
        box-shadow: 0 8px 32px rgba(0, 255, 135, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 48px rgba(0, 255, 135, 0.5);
    }
    
    /* 스파이크 알람 */
    .spike-alert {
        background: linear-gradient(135deg, #ff0055 0%, #ff8800 100%);
        border-radius: 12px;
        padding: 16px 24px;
        margin: 8px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* 데이터 테이블 */
    .dataframe {
        background-color: #1a1a1a;
        color: #ffffff;
        border-radius: 12px;
    }
    
    /* 차트 배경 */
    .js-plotly-plot {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def load_all_data():
    """모든 데이터 로드 (5분 캐시)"""
    loader = DataLoader()
    
    # 전처리된 데이터 로드 (상대 경로)
    try:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'processed_data.csv')
        df_main = pd.read_csv(data_path)
        df_main['timestamp'] = pd.to_datetime(df_main['timestamp'])
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        df_main = pd.DataFrame()
    
    # 개별 소스 데이터
    data = loader.load_all_data()
    
    return df_main, data


def create_signal_box_html(source_name, score, arrow="", color="#00d4ff"):
    """신호 박스 HTML 생성 - 컴팩트 버전"""
    # 점수가 0이면 화살표만 표시
    if score == 0:
        return f"""
        <div style="text-align: center; padding: 12px 0; color: {color}; font-size: 24px;">
            {source_name}
        </div>
        """
    
    return f"""
    <div class="signal-box">
        <div class="signal-title">{source_name}</div>
        <div class="signal-value">{score:.1f}</div>
    </div>
    """


def render_top_navigation():
    """상단 네비게이션 렌더링"""
    st.markdown("""
    <div class="top-nav">
        <div class="logo">🚀 CRYPTO SIGNAL DASHBOARD</div>
        <div style="color: #888; font-size: 14px;">
            Real-time Market Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_signal_boxes(df_main, data):
    """신호 박스 렌더링 - Upbit 스타일"""
    
    if df_main.empty:
        st.warning("데이터가 없습니다. data/processed_data.csv 파일을 확인해주세요.")
        return df_main
    
    # 종합 점수 계산
    calculator = CompositeScoreCalculator()
    try:
        df_scored = calculator.calculate_composite_score(
            df_main, 
            df_news=data.get('coinness', pd.DataFrame()), 
            df_twitter=data.get('twitter', pd.DataFrame())
        )
    except Exception as e:
        st.error(f"종합 점수 계산 실패: {e}")
        import traceback
        st.code(traceback.format_exc())
        df_scored = df_main.copy()
        df_scored['composite_score'] = 50
        df_scored['telegram_score'] = 50
        df_scored['news_score'] = 50
        df_scored['twitter_score'] = 50
    
    # 최근 점수
    if not df_scored.empty:
        telegram_score = df_scored['telegram_score'].iloc[-1]
        news_score = df_scored['news_score'].iloc[-1]
        twitter_score = df_scored['twitter_score'].iloc[-1]
        composite_score = df_scored['composite_score'].iloc[-1]
        
        # 24시간 전 점수
        if len(df_scored) > 24:
            composite_score_24h = df_scored['composite_score'].iloc[-25]
            score_change = composite_score - composite_score_24h
            score_change_pct = (score_change / composite_score_24h) * 100 if composite_score_24h != 0 else 0
        else:
            score_change = 0
            score_change_pct = 0
    else:
        telegram_score = news_score = twitter_score = composite_score = 50
        score_change = 0
        score_change_pct = 0
    
    # 신호 레벨 결정
    signal_summary = calculator.get_signal_summary(df_scored)
    
    # 종합 점수 카드 (최상단 강조)
    change_class = "positive" if score_change > 0 else "negative" if score_change < 0 else "neutral"
    change_symbol = "▲" if score_change > 0 else "▼" if score_change < 0 else "−"
    
    st.markdown(f"""
    <div class="score-card">
        <div class="score-label">COMPOSITE MARKET SIGNAL</div>
        <div class="score-value">{composite_score:.1f}</div>
        <div class="score-change {change_class}">
            {change_symbol} {abs(score_change):.1f} ({abs(score_change_pct):.2f}%) | 
            {signal_summary['current_level'].replace('_', ' ').upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return df_scored, {
        'telegram': telegram_score,
        'news': news_score,
        'twitter': twitter_score,
        'composite': composite_score
    }


def render_spike_table(df):
    """스파이크 알람 시계열 표"""
    st.markdown("## 🔔 Spike Alerts")
    
    if df.empty:
        st.warning("데이터가 없습니다.")
        return
    
    try:
        # 스파이크 감지
        detector = SpikeDetector(df)
        
        # 최근 스파이크만
        recent_spikes = []
        
        if 'message_count' in df.columns:
            msg_spikes = detector.detect_zscore_spike('message_count', threshold=2.0)
            if not msg_spikes.empty:
                recent_spikes.append(msg_spikes.tail(10))
        
        if recent_spikes:
            spike_df = pd.concat(recent_spikes).sort_values('timestamp', ascending=False)
            
            for _, row in spike_df.head(5).iterrows():
                st.markdown(f"""
                <div class="spike-alert">
                    <strong>⚡ SPIKE DETECTED</strong> | 
                    {row['timestamp'].strftime('%Y-%m-%d %H:%M')} | 
                    {row['spike_column']}: {row['spike_magnitude']:.2f}σ
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent spikes detected")
    except Exception as e:
        st.error(f"스파이크 감지 오류: {e}")


def render_cta_button():
    """차익거래 CTA 버튼"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h2 style="margin-bottom: 24px;">💰 지금이 기회입니다</h2>
            <p style="font-size: 18px; color: #888; margin-bottom: 32px;">
                실시간 시장 신호를 활용한 스마트 차익거래 전략
            </p>
            <a href="https://whale-arbitrage-qwodzy8wpnhpgxaxt23rj8.streamlit.app/" 
               target="_blank" class="cta-button">
                차익거래 시작하기 →
            </a>
        </div>
        """, unsafe_allow_html=True)


def main():
    """메인 함수 - Upbit 스타일 레이아웃"""
    # 상단 네비게이션
    render_top_navigation()
    
    # 데이터 로드
    with st.spinner("Loading market data..."):
        df_main, data = load_all_data()
    
    if df_main.empty:
        st.error("데이터를 로드할 수 없습니다. 먼저 python scripts/preprocess_data.py를 실행하세요.")
        return
    
    # 신호 박스 (종합 점수 카드)
    df_scored, scores = render_signal_boxes(df_main, data)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upbit 스타일 레이아웃: 차트(왼쪽) + 지표(오른쪽)
    col_chart, col_indicators = st.columns([7, 3])
    
    with col_chart:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 📈 종합 점수 추이")
        
        if not df_scored.empty and 'composite_score' in df_scored.columns:
            # 종합 점수 차트
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_scored['timestamp'],
                y=df_scored['composite_score'],
                name='Composite Score',
                line=dict(color='#3b82f6', width=2.5),
                fill='tozeroy',
                fillcolor='rgba(59, 130, 246, 0.1)'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='#0a0a0a',
                plot_bgcolor='#0a0a0a',
                height=500,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#1a1a1a',
                    title='시간'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#1a1a1a',
                    title='점수',
                    range=[0, 100]
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_indicators:
        st.markdown('<div class="indicator-list">', unsafe_allow_html=True)
        st.markdown("### 📊 시장 지표")
        
        # 지표 데이터 준비
        indicators = [
            {
                'name': '텔레그램 신호',
                'value': scores['telegram'],
                'change': 0,  # 실제로는 24h 변화율 계산
                'trend': 'neutral'
            },
            {
                'name': '뉴스 신호',
                'value': scores['news'],
                'change': 0,
                'trend': 'neutral'
            },
            {
                'name': '트위터 신호',
                'value': scores['twitter'],
                'change': 0,
                'trend': 'neutral'
            },
        ]
        
        # ETH/BTC 가격 추가
        if not df_scored.empty:
            if 'ETH_close' in df_scored.columns:
                eth_price = df_scored['ETH_close'].iloc[-1]
                eth_change = df_scored['ETH_price_change_pct'].iloc[-1] if 'ETH_price_change_pct' in df_scored.columns else 0
                indicators.append({
                    'name': 'ETH 가격',
                    'value': eth_price,
                    'change': eth_change,
                    'trend': 'positive' if eth_change > 0 else 'negative' if eth_change < 0 else 'neutral',
                    'is_price': True
                })
            
            if 'BTC_close' in df_scored.columns:
                btc_price = df_scored['BTC_close'].iloc[-1]
                btc_change = df_scored['BTC_price_change_pct'].iloc[-1] if 'BTC_price_change_pct' in df_scored.columns else 0
                indicators.append({
                    'name': 'BTC 가격',
                    'value': btc_price,
                    'change': btc_change,
                    'trend': 'positive' if btc_change > 0 else 'negative' if btc_change < 0 else 'neutral',
                    'is_price': True
                })
        
        # 지표 표시
        for ind in indicators:
            is_price = ind.get('is_price', False)
            value_format = f"${ind['value']:,.0f}" if is_price else f"{ind['value']:.1f}"
            change_symbol = "▲" if ind['change'] > 0 else "▼" if ind['change'] < 0 else "−"
            
            st.markdown(f"""
            <div class="indicator-item">
                <div>
                    <div class="indicator-name">{ind['name']}</div>
                </div>
                <div>
                    <div class="indicator-value {ind['trend']}">{value_format}</div>
                    <div class="indicator-change {ind['trend']}">{change_symbol} {abs(ind['change']):.2f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 탭 UI
    tab1, tab2, tab3, tab4 = st.tabs(["📊 종합", "💬 텔레그램", "📰 뉴스", "🐦 트위터"])
    
    with tab1:
        render_spike_table(df_scored)
    
    with tab2:
        st.markdown("### 텔레그램 분석")
        st.info("텔레그램 커뮤니티 활동 상세 분석")
    
    with tab3:
        st.markdown("### 뉴스 분석")
        st.info("코인니스 뉴스 감성 분석")
    
    with tab4:
        st.markdown("### 트위터 분석")
        st.info("인플루언서 트윗 분석")
    
    # CTA 버튼
    render_cta_button()


if __name__ == '__main__':
    main()
