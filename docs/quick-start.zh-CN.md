# 涓枃蹇€熷紑濮?
鏈枃妗ｇ敤浜庡揩閫熻鏄?HelixDesk AI 褰撳墠鍚庣鐗堟湰鐨勬湰鍦板惎鍔ㄦ柟寮忋€?
## 1. 閫傜敤鑼冨洿

褰撳墠蹇€熷紑濮嬩富瑕侀拡瀵逛粨搴撻噷鐨?`apps/control-api`銆?
褰撳墠宸插叿澶囷細

- 鎺у埗灞?API
- SQLite / PostgreSQL 鍏煎鎸佷箙鍖?- Chatwoot webhook 鎺ュ叆楠ㄦ灦
- AstrBot 閫傞厤鍣ㄩ鏋?- 璺敱銆佹帴绠°€佹仮澶?AI銆佸仴搴锋鏌ョ瓑鍩虹鑳藉姏

## 2. 涓€閿惎鍔?
鍦ㄤ粨搴撴牴鐩綍鎵ц锛?
```powershell
.\scripts\dev.ps1
```

杩欎釜鑴氭湰浼氳嚜鍔細

- 鍒涘缓 Python 铏氭嫙鐜
- 瀹夎鍚庣渚濊禆
- 鍚姩 `uvicorn app.main:app --reload`

## 3. 榛樿閰嶇疆

褰撳墠榛樿閰嶇疆瑙佷粨搴撴牴鐩綍鐨?`.env.example`銆?
鍏抽敭椤瑰寘鎷細

- `DATABASE_URL`
- `CHATWOOT_BASE_URL`
- `CHATWOOT_ACCOUNT_ID`
- `CHATWOOT_API_TOKEN`
- `CHATWOOT_WEBHOOK_SECRET`
- `CHATWOOT_MOCK_MODE`
- `ASTRBOT_BASE_URL`
- `ASTRBOT_CHAT_PATH`
- `ASTRBOT_API_KEY`
- `ASTRBOT_MOCK_MODE`

鏈湴榛樿琛屼负锛?
- 鏁版嵁搴撳瓨鍌ㄥ埌 `apps/control-api/data/app.db`
- Chatwoot 閫傞厤鍣ㄩ粯璁や娇鐢?mock 妯″紡
- AstrBot 閫傞厤鍣ㄩ粯璁や娇鐢?mock 妯″紡

## 4. 甯哥敤鎺ュ彛

### 绠＄悊鎺ュ彛

- `GET /api/admin/system-settings`
- `PUT /api/admin/system-settings`
- `GET /api/admin/business-hours`
- `PUT /api/admin/business-hours`
- `GET /api/admin/presets`
- `POST /api/admin/presets`
- `POST /api/admin/conversations/{conversation_id}/handover`
- `POST /api/admin/conversations/{conversation_id}/restore-ai`

### 杩愯鏃舵帴鍙?
- `POST /api/runtime/chatwoot/webhook`
- `POST /api/runtime/route-message`
- `GET /api/runtime/health`

## 5. 鏈湴楠岃瘉

鍦?`apps/control-api` 鐩綍鎵ц锛?
```powershell
.\.venv\Scripts\python -m pytest -q
```

褰撳墠 smoke tests 瑕嗙洊浜嗭細

- 鏍硅矾鐢卞彲鐢ㄦ€?- AI 璺敱鍥炲
- 浜哄伐鎺ョ鎷︽埅
- Chatwoot webhook 绛惧悕鏍￠獙
- Chatwoot webhook 鍥炲啓娴佺▼

## 6. 涓嬩竴姝ュ缓璁?
濡傛灉浣犲噯澶囩户缁帹杩涢」鐩紝鎺ㄨ崘鐨勯『搴忔槸锛?
1. 鎺ュ叆鐪熷疄 Chatwoot webhook
2. 瀵归綈 AstrBot 鐨勫疄闄?HTTP 鎺ュ彛
3. 澧炲姞 Alembic 杩佺Щ
4. 寮€濮嬬嫭绔嬬鐞嗗悗鍙板墠绔紑鍙?