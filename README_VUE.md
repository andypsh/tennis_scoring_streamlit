# CJ Tennis · Vue 3 + Capacitor 포팅

기존 Streamlit 앱(`src/`)을 Vue 3로 다시 작성. 모바일 앱 배포는 Capacitor로,
데이터/인증은 Supabase로.

> 브랜치: **feature_andy_vue**
> 기존 Streamlit 코드는 `src/`에 그대로 보존 — Vue 코드는 `web/`에 신규.

## 디렉토리

```
.
├── src/                  ← 기존 Streamlit (그대로)
├── web/                  ← Vue 3 + Vite 앱 (신규)
│   ├── src/
│   │   ├── pages/        StandingsPage, ScorePage, BracketPage, DoublesPage, ...
│   │   ├── stores/       Pinia: auth, tournament
│   │   ├── lib/          scoring, bracket(자동생성), doubles(파트너매칭), supabase
│   │   ├── components/   NavBar
│   │   └── types/        도메인 타입
│   ├── capacitor.config.ts
│   └── package.json
└── supabase/
    └── schema.sql        ← Postgres 스키마 + RLS + Realtime
```

## 사전 요구

- **Node.js 18.18+** (LTS 20 권장). 현재 머신은 v16이라 빌드 실패함.
  - `nvm` 또는 [Node 공식 LTS 설치](https://nodejs.org/) 후 진행.
- macOS Xcode (iOS 빌드 시), Android Studio (Android 빌드 시)

## 1. 로컬 실행 (웹)

```bash
cd web
npm install
cp .env.example .env       # 비워두면 localStorage 데모 모드로 동작
npm run dev                # http://localhost:5173
```

`.env`가 비어있으면 Supabase 없이 **localStorage 데모 모드**로 동작합니다.
로그인은 `admin / admin`.

## 2. Supabase 연결

1. https://supabase.com 에서 프로젝트 생성
2. SQL Editor에 [supabase/schema.sql](supabase/schema.sql) 붙여넣고 실행
3. Settings → API 에서 URL / anon key 복사
4. `web/.env`:
   ```
   VITE_SUPABASE_URL=https://xxxxx.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOiJ...
   ```
5. Authentication → Users 에서 관리자 계정 생성. `app_metadata`에
   `{"role":"admin"}`를 넣으면 admin 권한.

> ⚠️ 현 1차 버전의 Vue 스토어는 로컬 우선이며 Supabase 양방향 동기화는
> 다음 단계로 분리. 스키마와 클라이언트 셋업만 선반영.

## 3. 모바일 배포 (Capacitor)

웹 앱이 동작한 뒤 한 줄로 iOS/Android 프로젝트 추가:

```bash
cd web
npm run build
npx cap add ios            # macOS + Xcode 필요
npx cap add android        # Android Studio 필요

npm run cap:ios            # build + sync + Xcode 열기
npm run cap:android        # build + sync + Android Studio 열기
```

스토어 등록 전:
- `capacitor.config.ts`의 `appId`(현재 `com.cj.tennis`) 정식 도메인으로 변경
- 아이콘/스플래시: `@capacitor/assets` 추천
- iOS: Push, App Tracking 등 권한 plist 조정

## 4. 주요 기능

| 페이지 | 기능 |
|---|---|
| `/standings` | 조 편성(2~6조), 라운드로빈 자동 생성, 실시간 조별 순위 |
| `/score` | 조별 매치 점수 입력 (남단/남복/여복, 종목 간 중복 출전 방지) |
| `/bracket` | **임의 조 수/진출 인원** 본선 대진표 자동 생성. 동일조 1라운드 충돌 자동 회피. 승자 자동 전파. |
| `/doubles` | NTRP/구력 기반 균형 페어 + 라운드별 매치업 자동 생성 |
| `/timetable` | 코트 수·시작시각·슬롯길이만 입력하면 매치 자동 배치 |
| `/players` | 엑셀(.xlsx) 일괄 업로드 (`이름`, `소속`, `성별`, `구력`, `ntrp` 컬럼) |

## 5. 스코어링 규칙 (기존 동일)

- 한 매치 = 남단·남복·여복 3종목
- 2종목 이상 이긴 팀이 매치 승자
- 조별 승점: 승 3 / 무 1 / 패 0
- 타이브레이크: 승점 → 득실차 → 승수 → 팀명

## 6. 다음 단계 후보

- [ ] Supabase 양방향 동기화 (현재 localStorage 우선)
- [ ] Realtime: 점수 입력 시 다른 기기 즉시 반영
- [ ] PWA manifest + 오프라인 캐시
- [ ] 다국어(영문)
- [ ] 회원 출석/모임 일정 (스매시/테니스타운 클럽 기능)
