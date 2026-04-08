# HelixDesk AI

[English](README.md) | [绠€浣撲腑鏂嘳(README.zh-CN.md)

HelixDesk AI 鏄竴涓妸 `Chatwoot` 鍜?`AstrBot` 缂濆悎璧锋潵鐨勭粺涓€ AI 瀹㈡湇骞冲彴銆傚畠鐨勫畾浣嶄笉鏄浛浠ｈ繖涓や釜椤圭洰锛岃€屾槸鍦ㄤ腑闂村鍔犱竴灞傗€滅鐞嗗憳鍙帶鐨勮皟搴︿笌閰嶇疆灞傗€濓紝璁╀紒涓氳兘澶熺湡姝ｆ妸 AI 瀹㈡湇杩愯惀璧锋潵銆?
瀹冪殑鏍稿績鐩爣寰堟槑纭細

- 缁х画鎶?`Chatwoot` 褰撲綔瀹㈡湇宸ヤ綔鍙板拰浼氳瘽涓績
- 缁х画鎶?`AstrBot` 褰撲綔 AI 寮曟搸銆佺煡璇嗗簱鍜岃嚜鍔ㄥ寲鑳藉姏搴曞骇
- 鐢ㄧ嫭绔嬬殑鎺у埗灞傛壙鎺モ€滃叏灞€寮€鍏炽€佸畾鏃跺惎鍋溿€丄I 棰勮銆佷汉宸ユ帴绠°€佹仮澶?AI銆佸璁℃棩蹇椻€濈瓑骞冲彴鑳藉姏

## 椤圭洰瀹氫綅

寰堝鍥㈤槦骞朵笉闇€瑕侀噸鍐欐暣涓鏈嶇郴缁燂紝鍙槸缂哄皯涓€涓兘鎶娾€滀汉宸ュ鏈嶇郴缁熲€濆拰鈥淎I 鏈哄櫒浜虹郴缁熲€濈湡姝ｄ覆璧锋潵鐨勪腑闂村眰銆?
HelixDesk AI 瑙ｅ喅鐨勬鏄繖閮ㄥ垎闂锛?
- 绠＄悊鍛樺彲缁熶竴鎺у埗 AI 寮€鍏?- 鏀寔鎸夎惀涓氭椂娈佃嚜鍔ㄥ紑鍚垨鍏抽棴 AI
- 鏀寔 AI 鑷姩鍥炲鐢ㄦ埛娑堟伅
- 鏀寔浜哄伐鎺ョ鍜屾仮澶?AI
- 鏀寔涓轰笉鍚屼笟鍔″満鏅厤缃?AI 棰勮
- 鏀寔 Chatwoot webhook 缂栨帓鍜屾秷鎭洖鍐?- 鏀寔瀹¤鏃ュ織鍜岃繍琛屾€佽褰?
## 褰撳墠瀹炵幇鑼冨洿

褰撳墠浠撳簱宸茬粡鍖呭惈绗竴鐗堝悗绔帶鍒跺眰瀹炵幇锛岄噸鐐瑰厛鎶娾€滆皟搴︿腑鍙扳€濊窇閫氥€?
鐩墠宸插畬鎴愶細

- `FastAPI` 鎺у埗灞傚悗绔?- `SQLite / PostgreSQL` 鍏煎鐨勬暟鎹寔涔呭寲
- 绯荤粺璁剧疆銆佽惀涓氭椂娈点€丄I 棰勮銆佷細璇濈姸鎬併€佸璁℃棩蹇?- Chatwoot webhook 鏍￠獙涓庢秷鎭洖鍐欓鏋?- AstrBot 鍙厤缃ˉ鎺ラ€傞厤鍣?- 璺敱銆佹帴绠°€亀ebhook 鏍￠獙鐩稿叧鐨?smoke tests

褰撳墠杩樻湭瀹屾垚锛?
- 鐙珛绠＄悊鍚庡彴鍓嶇
- AstrBot 鐪熷疄鐢熶骇鎺ュ彛鑱旇皟
- 鏇村畬鏁寸殑 Chatwoot 鐢熶骇绾ф帴鍏?- 鏁版嵁杩佺Щ鍜屾洿瀹屾暣鐨勯儴缃叉祦绋?
## 鏁翠綋鏋舵瀯

```mermaid
flowchart LR
    U["鐢ㄦ埛"] --> CW["Chatwoot"]
    CW --> WH["Webhook 鎺ユ敹灞?]
    WH --> RT["璺敱鍐崇瓥寮曟搸"]

    RT -->|AI 璺緞| AB["AstrBot 閫傞厤鍣?]
    AB --> RW["娑堟伅鍥炲啓鍣?]
    RW --> CW

    RT -->|浜哄伐璺緞| AG["Chatwoot 浜哄伐瀹㈡湇"]

    ADM["绠＄悊鍚庡彴"] --> API["鎺у埗灞?API"]
    API --> CFG["璁剧疆 / 棰勮 / 鏃舵瑙勫垯"]
    API --> HD["浜哄伐鎺ョ鐘舵€?]
    API --> AUD["瀹¤鏃ュ織"]

    SCH["瀹氭椂璋冨害鍣?] --> CFG
    DB["PostgreSQL / SQLite"] --> API
```

## 浠撳簱缁撴瀯

```text
apps/
  control-api/   FastAPI 鎺у埗灞傚悗绔?  admin-web/     瑙勫垝涓殑鐙珛绠＄悊鍚庡彴鍓嶇

deploy/
  compose/       Docker Compose 閰嶇疆
  docker/        Docker 鏋勫缓鏂囦欢

docs/
  涓枃鏂囨。銆佹埅鍥捐鏄庣瓑琛ュ厖鏉愭枡

scripts/
  dev.ps1        鏈湴寮€鍙戝惎鍔ㄨ剼鏈?```

## 蹇€熷紑濮?
### 鏈湴鍚姩

```powershell
.\scripts\dev.ps1
```

榛樿鏈湴琛屼负锛?
- 鏁版嵁搴擄細`sqlite:///./data/app.db`
- Chatwoot 閫傞厤鍣細榛樿 `mock mode`
- AstrBot 閫傞厤鍣細榛樿 `mock mode`

### 甯哥敤鎺ュ彛

- `GET /api/admin/system-settings`
- `PUT /api/admin/system-settings`
- `GET /api/admin/business-hours`
- `POST /api/runtime/chatwoot/webhook`
- `POST /api/runtime/route-message`
- `GET /api/runtime/health`

濡傛灉浣犳洿鎯崇湅涓枃鍚姩璇存槑锛屽彲浠ョ洿鎺ョ湅 [docs/quick-start.zh-CN.md](docs/quick-start.zh-CN.md)銆?
## 涓轰粈涔堜笉鐩存帴鎶婁袱涓」鐩‖鍚堝苟

HelixDesk AI 鐨勮璁℃€濊矾鏄€滃钩鍙扮骇闆嗘垚鈥濓紝鑰屼笉鏄妸涓や釜涓婃父浠撳簱鐩存帴鎻夋垚涓€涓崟浣撱€?
鍘熷洜寰堢幇瀹烇細

- `Chatwoot` 鏇村亸瀹㈡湇宸ュ崟涓庡骇甯伐浣滄祦
- `AstrBot` 鏇村亸 AI銆佺煡璇嗗簱銆佹満鍣ㄤ汉鍜屾彃浠惰兘鍔?- 涓よ竟鎶€鏈爤銆佹暟鎹ā鍨嬨€佸崌绾ц妭濂忛兘涓嶅悓
- 鐩存帴纭悎浼氳鍚庣画鍗囩骇鍜岀淮鎶ゆ垚鏈緢楂?
鎵€浠ユ洿鍚堢悊鐨勬柟寮忔槸锛?
- 淇濈暀 Chatwoot 鐨勫鏈嶄腑蹇冭兘鍔?- 淇濈暀 AstrBot 鐨?AI 鑳藉姏
- 鍦ㄤ腑闂村缓璁剧嫭绔嬫帶鍒跺眰鍜岀鐞嗗悗鍙?
## 褰撳墠浜у搧璺嚎鍥?
### 绗竴闃舵锛氬熀纭€闂幆

- [x] 鎺у埗灞?API 楠ㄦ灦
- [x] 杩愯鎬佷笌閰嶇疆鎸佷箙鍖?- [x] 鍩虹璺敱涓?mock AI 鍥炲
- [x] 浜哄伐鎺ョ涓庢仮澶?AI
- [x] 浠撳簱鍒濆鍖栦笌鍏紑鍙戝竷

### 绗簩闃舵锛氱湡瀹為泦鎴?
- [ ] 鎺ュ叆鐪熷疄 Chatwoot 璐﹀彿鍜屾秷鎭簨浠?- [ ] 鎺ュ叆 AstrBot 鐪熷疄妗ユ帴鎺ュ彛
- [ ] 澧炲姞绛惧悕鏍￠獙銆侀噸璇曞拰骞傜瓑鎺у埗
- [ ] 寮曞叆 Alembic 绠＄悊鏁版嵁搴撹縼绉?
### 绗笁闃舵锛氬悗鍙颁綋楠?
- [ ] 鏋勫缓鐙珛绠＄悊鍚庡彴
- [ ] 鍙鍖栫鐞?AI 棰勮
- [ ] 灞曠ず杩愯鐘舵€併€佹帴绠＄姸鎬佸拰鍋ュ悍妫€鏌?- [ ] 鍦?UI 涓煡鐪嬪璁℃棩蹇?
### 绗洓闃舵锛氱敓浜у寲鑳藉姏

- [ ] 瀹屽杽閮ㄧ讲妯℃澘鍜岀幆澧冨彉閲忔ā鏉?- [ ] 寮曞叆 Redis 浣滀负杩愯鎬佺紦瀛?- [ ] 澧炲姞鐩戞帶銆佹棩蹇楀拰鎸囨爣
- [ ] 鍔犲己 AI 鑷姩鍥炲鐨勫畨鍏ㄩ槻鎶?
鏇磋缁嗙殑涓枃璺嚎鍥惧湪 [docs/roadmap.zh-CN.md](docs/roadmap.zh-CN.md)銆?
## 涓枃鏂囨。绱㈠紩

- [涓枃蹇€熷紑濮媇(docs/quick-start.zh-CN.md)
- [涓枃璺嚎鍥綸(docs/roadmap.zh-CN.md)
- [涓枃鎴浘璇存槑](docs/screenshots/README.zh-CN.md)

## 鎴浘瑙勫垝

褰撳墠浠撳簱杩樻病鏈夋寮忎骇鍝佹埅鍥撅紝浣嗗凡缁忎负鎴浘鏁寸悊濂戒簡鍛藉悕鍜屾斁缃害瀹氥€?
寤鸿鎴浘娓呭崟锛?
1. 鎬昏 Dashboard
2. 鍏ㄥ眬 AI 寮€鍏充笌钀ヤ笟鏃舵
3. AI 棰勮绠＄悊椤?4. 浜哄伐鎺ョ鎺у埗鍙?5. 杩愯鍋ュ悍鐘舵€佷笌瀹¤鏃ュ織
6. Chatwoot 鍒?AstrBot 鐨勬秷鎭祦杞浘

鎴浘璇存槑鏂囨。锛?
- 鑻辨枃鐗堬細[docs/screenshots/README.md](docs/screenshots/README.md)
- 涓枃鐗堬細[docs/screenshots/README.zh-CN.md](docs/screenshots/README.zh-CN.md)

## 寮€鍙戣鏄?
- 褰撳墠浠撳簱鐨勯噸鐐瑰疄鐜扮洰鏍囦粛鐒舵槸鍚庣鎺у埗灞?- 澶栭儴闆嗘垚榛樿寮€鍚?`mock mode`锛屾柟渚挎湰鍦板畨鍏ㄥ紑鍙?- 杩欎釜浠撳簱鍦ㄥ綋鍓嶇幆澧冧笅鐨勮繙绔悓姝ラ儴鍒嗕娇鐢ㄤ簡 GitHub API 浣滀负琛ュ厖锛屽洜涓虹洿杩?`git push` 涓嶇ǔ瀹?
## 浠撳簱淇℃伅

- 浜у搧鍚嶏細`HelixDesk AI`
- 浠撳簱鍚嶏細`helixdesk-ai`
- 鍏紑浠撳簱锛歔https://github.com/GoSim7/helixdesk-ai](https://github.com/GoSim7/helixdesk-ai)
