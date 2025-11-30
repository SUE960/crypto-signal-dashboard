"""
데이터 로딩 유틸리티

모든 데이터 파일을 로드하고 기본 전처리를 수행합니다.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os


class DataLoader:
    """데이터 로더 클래스"""
    
    def __init__(self, data_dir='/Volumes/T7/class/2025-FALL/big_data/data'):
        """
        Args:
            data_dir: 데이터 디렉토리 경로
        """
        self.data_dir = data_dir
        
    def load_whale_transactions(self):
        """
        고래 지갑 거래 데이터 로드 (시간별 집계)
        
        Returns:
            DataFrame: 시간별 거래 데이터
        """
        file_path = os.path.join(self.data_dir, 'whale_transactions_rows_ETH_rev1.csv')
        df = pd.read_csv(file_path)
        
        # 시간 컬럼을 datetime으로 변환 (오류값은 NaT로 처리)
        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
        
        # NaT(잘못된 날짜) 행 제거
        df = df.dropna(subset=['Time'])
        
        # timezone 제거 (naive datetime으로 통일)
        if df['Time'].dt.tz is not None:
            df['Time'] = df['Time'].dt.tz_localize(None)
        
        df = df.rename(columns={
            'Time': 'timestamp',
            'frequency': 'tx_frequency',
            'sum_amount': 'tx_amount',
            'sum_amount_usd': 'tx_amount_usd'
        })
        
        # 시간 순 정렬
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    
    def load_price_data(self, coin='ETH'):
        """
        가격 데이터 로드
        
        Args:
            coin: 'ETH' 또는 'BTC'
            
        Returns:
            DataFrame: 가격 데이터
        """
        file_path = os.path.join(self.data_dir, f'price_history_{coin.lower()}_rows.csv')
        df = pd.read_csv(file_path)
        
        # 타임스탬프를 datetime으로 변환 (오류값은 NaT로 처리)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # NaT(잘못된 날짜) 행 제거
        df = df.dropna(subset=['timestamp'])
        
        # timezone 제거 (naive datetime으로 통일)
        if df['timestamp'].dt.tz is not None:
            df['timestamp'] = df['timestamp'].dt.tz_localize(None)
        
        # 필요한 컬럼만 선택 및 이름 변경
        df = df.rename(columns={
            'open_price': f'{coin}_open',
            'high_price': f'{coin}_high',
            'low_price': f'{coin}_low',
            'close_price': f'{coin}_close',
            'volume': f'{coin}_volume',
            'trade_count': f'{coin}_trade_count'
        })
        
        # 시간 순 정렬
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    
    def load_telegram_data(self):
        """
        텔레그램 커뮤니티 데이터 로드
        
        Returns:
            DataFrame: 텔레그램 데이터 (없으면 빈 DataFrame)
        """
        file_path = os.path.join(self.data_dir, 'telegram_data.csv')
        
        if not os.path.exists(file_path):
            print(f"경고: {file_path} 파일이 없습니다. 빈 DataFrame을 반환합니다.")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        
        # 타임스탬프를 datetime으로 변환 (오류값은 NaT로 처리)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # NaT(잘못된 날짜) 행 제거
        df = df.dropna(subset=['timestamp'])
        
        # timezone 제거 (naive datetime으로 통일)
        if df['timestamp'].dt.tz is not None:
            df['timestamp'] = df['timestamp'].dt.tz_localize(None)
        
        # 시간 순 정렬
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    
    def load_twitter_data(self):
        """
        트위터 인플루언서 데이터 로드
        
        Returns:
            DataFrame: 트위터 데이터 (없으면 빈 DataFrame)
        """
        file_path = os.path.join(self.data_dir, 'twitter_influencer_labeled_rows.csv')
        
        if not os.path.exists(file_path):
            print(f"경고: {file_path} 파일이 없습니다. 빈 DataFrame을 반환합니다.")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        
        # post_date를 datetime으로 변환 (가능한 경우)
        if 'post_date' in df.columns:
            df['post_date'] = pd.to_datetime(df['post_date'], errors='coerce')
            
            # NaT가 아닌 행만 유지
            df = df.dropna(subset=['post_date'])
            
            # timezone 제거
            if df['post_date'].dt.tz is not None:
                df['post_date'] = df['post_date'].dt.tz_localize(None)
        
        # 감성 점수가 없는 경우 sentiment_score 활용
        if 'sentiment_score' in df.columns:
            df['sentiment_score'] = pd.to_numeric(df['sentiment_score'], errors='coerce')
        
        # 시간 순 정렬
        if 'post_date' in df.columns:
            df = df.sort_values('post_date').reset_index(drop=True)
        
        return df
    
    def load_coinness_data(self):
        """
        코인니스 뉴스 데이터 로드
        
        Returns:
            DataFrame: 코인니스 데이터 (없으면 빈 DataFrame)
        """
        file_path = os.path.join(self.data_dir, 'coinness_data.csv')
        
        if not os.path.exists(file_path):
            print(f"경고: {file_path} 파일이 없습니다. 빈 DataFrame을 반환합니다.")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        
        # timestamp를 datetime으로 변환
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            
            # NaT가 아닌 행만 유지
            df = df.dropna(subset=['timestamp'])
            
            # timezone 제거
            if df['timestamp'].dt.tz is not None:
                df['timestamp'] = df['timestamp'].dt.tz_localize(None)
            
            # 시간 순 정렬
            df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    
    def load_all_data(self):
        """
        모든 데이터를 로드하고 반환
        
        Returns:
            dict: 각 데이터프레임을 담은 딕셔너리
        """
        data = {
            'whale_transactions': self.load_whale_transactions(),
            'eth_price': self.load_price_data('ETH'),
            'btc_price': self.load_price_data('BTC'),
            'telegram': self.load_telegram_data(),
            'twitter': self.load_twitter_data(),
            'coinness': self.load_coinness_data()
        }
        
        return data
    
    @staticmethod
    def get_date_range(df, date_column='timestamp'):
        """
        데이터프레임의 날짜 범위를 반환
        
        Args:
            df: 데이터프레임
            date_column: 날짜 컬럼명
            
        Returns:
            tuple: (시작일, 종료일)
        """
        if df.empty or date_column not in df.columns:
            return None, None
        
        return df[date_column].min(), df[date_column].max()
    
    @staticmethod
    def fill_missing_hours(df, date_column='timestamp'):
        """
        빠진 시간을 채웁니다 (0으로 채우기)
        
        Args:
            df: 데이터프레임
            date_column: 날짜 컬럼명
            
        Returns:
            DataFrame: 빠진 시간이 채워진 데이터프레임
        """
        if df.empty:
            return df
        
        # 시간 범위 생성
        start_date = df[date_column].min()
        end_date = df[date_column].max()
        
        # 1시간 간격으로 전체 시간 범위 생성
        full_range = pd.date_range(start=start_date, end=end_date, freq='H')
        
        # 기존 데이터와 병합
        full_df = pd.DataFrame({date_column: full_range})
        merged_df = full_df.merge(df, on=date_column, how='left')
        
        # 수치형 컬럼은 0으로, 문자열은 ffill로 채우기
        for col in merged_df.columns:
            if col != date_column:
                if merged_df[col].dtype in ['float64', 'int64']:
                    merged_df[col] = merged_df[col].fillna(0)
                else:
                    merged_df[col] = merged_df[col].ffill()
        
        return merged_df


if __name__ == '__main__':
    # 테스트
    loader = DataLoader()
    data = loader.load_all_data()
    
    print("=== 데이터 로딩 테스트 ===\n")
    
    for name, df in data.items():
        if not df.empty:
            start, end = loader.get_date_range(df)
            print(f"{name}:")
            print(f"  행 수: {len(df)}")
            print(f"  기간: {start} ~ {end}")
            print(f"  컬럼: {list(df.columns)}")
            print()
        else:
            print(f"{name}: 데이터 없음\n")

