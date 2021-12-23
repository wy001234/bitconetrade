import pyupbit
import numpy as np

#ohlcv(당일 시가,고가, 저가, 종가, 거래량의 데이터)

df = pyupbit.get_ohlcv("KRW-BTC", count=7)

#변동폭 * k계산, (고가- 저가) *k값
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)

# ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)
# 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Down
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

#MDD계산
print("MDD(%): ", df['dd'].max())

# 엑셀 출력
df.to_excel("dd.xlsx")
