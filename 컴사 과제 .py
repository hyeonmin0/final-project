import requests
import datetime
import math
import matplotlib.pyplot as plt

print("=== 기간별 환율 변화 조회 프로그램 ===")

baseCurrency = input("기준 통화 입력 (예: USD): ").upper()
targetCurrency = input("조회할 통화 입력 (예: KRW): ").upper()

startDate = input("조회 시작 날짜 (YYYY-MM-DD): ")
endDate = input("조회 종료 날짜 (YYYY-MM-DD): ")

# 날짜 유효성 체크
try:
    datetime.datetime.strptime(startDate, "%Y-%m-%d")
    datetime.datetime.strptime(endDate, "%Y-%m-%d")
except:
    print("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해주세요.")
    exit()

print()
print(f"{startDate} ~ {endDate} 기간 동안의 {baseCurrency} -> {targetCurrency} 환율 데이터를 조회합니다...")
print()

# Frankfurter API (무료, API키 불필요)
url = (
    f"https://api.frankfurter.app/{startDate}..{endDate}"
    f"?from={baseCurrency}&to={targetCurrency}"
)

response = requests.get(url)
data = response.json()

# API 오류 처리
if "rates" not in data:
    print("API 오류 발생. 응답:", data)
    exit()

rates = data["rates"]

dateList = []
rateList = []

# 날짜별 환율 저장
for date in sorted(rates.keys()):
    rate = rates[date][targetCurrency]
    dateList.append(date)
    rateList.append(rate)

print("조회된 날짜 수:", len(dateList))
print()

print("=== 통계 정보 ===")
minRate = min(rateList)
maxRate = max(rateList)
avgRate = sum(rateList) / len(rateList)

startRate = rateList[0]
endRate = rateList[-1]

changeRate = endRate - startRate
changePercent = (changeRate / startRate) * 100

print(f"최저 환율: {minRate}")
print(f"최고 환율: {maxRate}")
print(f"평균 환율: {avgRate:.4f}")
print(f"시작일 환율: {startRate}")
print(f"종료일 환율: {endRate}")
print(f"변동량: {changeRate:.4f} ({changePercent:.4f}%)")

absPercent = math.fabs(changePercent)
if changePercent > 0:
    print(f"기간 동안 환율이 총 {absPercent:.4f}% 상승했습니다.")
elif changePercent < 0:
    print(f"기간 동안 환율이 총 {absPercent:.4f}% 하락했습니다.")
else:
    print("기간 동안 환율 변화가 거의 없습니다.")

print()
print("그래프 생성 중...")

plt.figure(figsize=(10,5))
plt.plot(dateList, rateList, marker="o")
plt.title(f"{baseCurrency} -> {targetCurrency} 환율 변화 ({startDate} ~ {endDate})")
plt.xlabel("날짜")
plt.ylabel("환율")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()