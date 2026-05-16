# CJ Tennis · Vue 3 + Capacitor 포팅

기존 Streamlit 앱(`src/`)을 Vue 3로 다시 작성. 웹은 PWA로 설치 가능,
모바일 앱은 Capacitor로 iOS/Android 패키징, 데이터/인증은 Supabase로.

> 브랜치: **feature_andy_vue**
> 기존 Streamlit 코드는 `src/`에 그대로 보존 — Vue 코드는 `web/`에 신규.

## 디렉토리

```
.
├── src/                  ← 기존 Streamlit (그대로)
├── web/                  ← Vue 3 + Vite 앱 (신규)
│   ├── src/
│   │   ├── pages/        Standings / Score / Bracket / Doubles / Timetable / Players / Login
│   │   ├── stores/       Pinia: auth, tournament (Supabase ↔ localStorage 양방향)
│   │   ├── lib/          scoring, bracket(자동생성), doubles(파트너매칭), supabase, sync
│   │   ├── components/   NavBar
│   │   └── types/        도메인 타입
│   ├── public/           favicon.svg (PWA 아이콘)
│   ├── capacitor.config.ts
│   └── package.json
└── supabase/
    └── schema.sql        ← Postgres 스키마 + RLS + Realtime
```

## 사전 요구

- **Node.js 16.18+** (현재 머신 OK).
  Capacitor iOS 빌드 시에는 18 LTS 권장.
- macOS Xcode (iOS 빌드 시), Android Studio (Android 빌드 시)

## 1. 로컬 실행 (웹)

```bash
cd web
npm install
cp .env.example .env       # 비워두면 localStorage 데모 모드로 동작
npm run dev                # http://localhost:5173
```

`.env`가 비어있으면 **localStorage 데모 모드**로 자동 전환.
로그인은 `admin / admin`.

NavBar의 상단 우측 칩이 현재 동기화 상태를 보여줍니다:
- 🟢 **실시간** — Supabase 연결 + 실시간 구독 활성
- 🟡 **동기화…** — 서버에 푸시 중
- 🔴 **오프라인** — 네트워크/Supabase 실패, 로컬 캐시만 사용
- ⚪ **로컬** — `.env` 미설정 (데모 모드)

## 2. Supabase 연결 (양방향 실시간 동기화)

1. https://supabase.com 에서 프로젝트 생성
2. SQL Editor에 [supabase/schema.sql](supabase/schema.sql) 붙여넣고 실행
3. Settings → API 에서 URL / anon key 복사
4. `web/.env`:
   ```
   VITE_SUPABASE_URL=https://xxxxx.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOiJ...
   ```
5. Authentication → Users 에서 관리자 계정 생성.
   `app_metadata`에 `{"role":"admin"}`를 넣으면 admin 권한.
6. 브라우저에서 로그인 → 점수 입력 → 다른 기기/탭에서 즉시 반영되는지 확인.

동기화 동작:
- 앱 시작 시 로컬 캐시 즉시 표시 → 서버에서 풀(pull) → UI 갱신
- 점수/조 편성/선수 변경 → 즉시 푸시 (낙관적 업데이트)
- 다른 클라이언트의 변경은 Realtime 채널로 자동 반영

## 3. PWA 설치 (모바일 홈 화면)

`npm run build && npm run preview` 후 모바일 사파리/크롬에서:
- iOS: 공유 → "홈 화면에 추가"
- Android: 메뉴 → "앱 설치"

오프라인 캐시 + 네이티브 앱과 거의 동일한 UX (스플래시, 풀스크린).

## 4. 모바일 네이티브 배포 (Capacitor)

```bash
cd web
npm run build
npx cap add ios            # macOS + Xcode 필요
npx cap add android        # Android Studio 필요

npm run cap:ios            # build + sync + Xcode 열기
npm run cap:android        # build + sync + Android Studio 열기
```

스토어 등록 전 체크리스트:
- `capacitor.config.ts`의 `appId`(현재 `com.cj.tennis`) 정식 도메인으로 변경
- 아이콘/스플래시: `@capacitor/assets` 추천
- iOS: Push, App Tracking 등 권한 plist 조정

## 5. 주요 기능

| 페이지 | 기능 |
|---|---|
| `/standings` | 조 편성(2~6조), 라운드로빈 자동 생성, 실시간 조별 순위 |
| `/score` | 조별 매치 점수 입력 (남단/남복/여복, 종목 간 중복 출전 방지) |
| `/bracket` | **임의 조 수/진출 인원** 본선 대진표 자동 생성. 동일조 1라운드 충돌 자동 회피. 승자 자동 전파. |
| `/doubles` | NTRP/구력 기반 균형 페어 + 라운드별 매치업 자동 생성 |
| `/timetable` | 코트 수·시작시각·슬롯길이만 입력하면 매치 자동 배치 |
| `/players` | 엑셀(.xlsx) 일괄 업로드 (`이름`, `소속`, `성별`, `구력`, `ntrp` 컬럼) |

## 6. 스코어링 규칙 (기존 동일)

- 한 매치 = 남단·남복·여복 3종목
- 2종목 이상 이긴 팀이 매치 승자
- 조별 승점: 승 3 / 무 1 / 패 0
- 타이브레이크: 승점 → 득실차 → 승수 → 팀명

## 7. 다음 단계 후보

- [ ] 매치별 사진/영상 첨부 (Supabase Storage)
- [ ] 회원 출석/모임 일정 (스매시·테니스타운 클럽 기능)
- [ ] 코트 예약
- [ ] 다국어(영문)
- [ ] 푸시 알림 (`@capacitor/push-notifications`)
