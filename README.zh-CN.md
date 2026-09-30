# 绔彛杩為€氭€ф鏌ュ伐鍏?
[English](README.md)

妫€鏌ユ槑纭垪鍑虹殑 TCP 涓绘満鍜岀鍙ｆ槸鍚﹀彲浠ヨ繛鎺ワ紝鏀寔瓒呮椂銆佸苟鍙戝拰鎶ュ憡瀵煎嚭銆?
## 涓昏鍔熻兘

- 鎺ュ彈 `host:port` 鍙傛暟鎴栨枃鏈枃浠躲€?- 鏀寔鏂规嫭鍙?IPv6锛屼緥濡?`[::1]:8080`銆?- 鍙厤缃秴鏃跺拰鏈変笂闄愮殑骞跺彂鏁伴噺銆?- 鏄剧ず瑙ｆ瀽鍚庣殑瀵圭鍦板潃鍜岃繛鎺ヨ€楁椂銆?- 鏀寔 JSON 鍜?CSV 鎶ュ憡銆?- 浠讳竴杩炴帴澶辫触鏃惰繑鍥為潪闆堕€€鍑轰唬鐮併€?
## 瀹夎

```bash
git clone https://github.com/jellywong343-sys/port-connectivity-checker.git
cd port-connectivity-checker
python -m pip install -e .
```

## 浣跨敤

```bash
port-check example.com:443 localhost:8080
port-check --file examples/targets.txt --timeout 2
port-check --file examples/targets.txt --workers 5 --json report.json --csv report.csv
```

## 鍚堣浣跨敤

宸ュ叿鍙鏌ヤ綘鏄庣‘濉啓鐨勭洰鏍囷紝涓嶆壂鎻忕鍙ｈ寖鍥淬€傚彧娴嬭瘯浣犳嫢鏈夋垨鑾峰噯璇婃柇鐨勭郴缁熴€傜綉缁滆繃婊ゅ彲鑳借鍙敤鏈嶅姟鏄剧ず涓哄叧闂垨瓒呮椂銆?
娴嬭瘯浣跨敤妯℃嫙濂楁帴瀛楋紝涓嶈闂湡瀹炰富鏈恒€?
## 娴嬭瘯

```bash
python -m unittest discover -s tests -v
```

## 寮€婧愬崗璁?
MIT

