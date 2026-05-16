# CJ Tennis · Vue 3 + Capacitor → Android/iOS 앱

스매시 / 테니스타운류 **B2C 동호회 운영 앱**의 베타. 대진 운영부터 시작해서
회원가입 · 클럽 관리 · 모임/출석까지 단계별로 확장.

> 브랜치: **feature_andy_vue**

## 현재 상태 (v0.2)

| 영역 | 상태 |
|---|---|
| Vue 3 + Vite 웹앱 | ✅ 동작 (`npm run dev`) |
| Tailwind + Pinia + Vue Router | ✅ |
| 대진 자동생성 (임의 조 수) | ✅ |
| 복식 파트너 매칭 (NTRP/구력) | ✅ |
| 점수 입력 + 실시간 순위 | ✅ |
| 코트 타임테이블 | ✅ |
| Supabase 양방향 + Realtime | ✅ (.env 셋업 필요) |
| PWA 매니페스트 (홈 화면 추가) | ✅ |
| Android 네이티브 프로젝트 | ✅ `web/android/` |
| iOS 네이티브 프로젝트 | ⏳ macOS 필요 |
| 카카오/구글 로그인 | ⏳ 다음 라운드 |
| 회원가입 · 클럽 관리 | ⏳ 다음 라운드 |
| 출석/모임/일정 | ⏳ 다음 라운드 |
| 결제/구독 | 🚫 추후 |

## 디렉토리

```
.
├── src/                       ← 기존 Streamlit (참조용 보존)
├── web/                       ← Vue 3 + Vite 앱
│   ├── src/                   ← Vue 소스
│   ├── public/                ← 정적 자산
│   ├── android/               ← Capacitor가 생성한 Android 프로젝트
│   ├── capacitor.config.ts
│   └── package.json
└── supabase/
    └── schema.sql             ← 초기 1회 실행할 스키마
```

---

# 1. 웹으로 띄우기 (지금 바로)

```bash
cd web
npm install
npm run dev        # http://localhost:5174 (5173 점유 시 자동 다음 포트)
```

`.env`가 없으면 **localStorage 데모 모드**. 화면 상단에 노란 안내 카드가 떠.

선수 페이지에서 **🎾 CJ 50명 시드 로드** 누르면 실제 데이터 즉시 채워짐.

---

# 2. Supabase 연결 (실시간 공유)

너 PC가 꺼져도, 동료들 폰에서도 실시간 데이터를 같이 봐야 한다면 필수.

1. **https://supabase.com** 에서 GitHub로 가입 (1초)
2. **New project** → 이름 적고 2분 대기 (무료 티어 자동 선택)
3. 좌측 메뉴 **SQL Editor** → New query → 너 PC의 `supabase/schema.sql` 통째로 붙여넣고 **Run**
4. 좌측 **Settings → API**에서 다음 두 값 복사:
   - Project URL
   - anon public key
5. `web/.env` 파일 생성하고 붙여넣기:
   ```
   VITE_SUPABASE_URL=https://xxxxxx.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1...
   ```
6. `npm run dev` 재시작 → 우상단 칩이 **🟢 실시간**으로 바뀌면 연결 성공
7. (선택) **Authentication → Users** 에서 본인 이메일로 계정 생성 →
   해당 user의 `app_metadata`를 `{"role":"admin"}`으로 수정하면 관리자 권한

## 무료 티어 한도

500MB DB / 50,000 MAU / 2GB 대역폭 — 클럽 수십 개 운영해도 안 참.

---

# 3. Android 앱 빌드 (Windows에서 OK)

`web/android/` 폴더는 이미 생성돼 있어. APK 빌드만 하면 카톡으로 동료들한테 보낼 수 있어.

## 사전 준비 (1회)

1. **Android Studio** 설치: https://developer.android.com/studio
2. 설치 후 첫 실행 시 SDK 자동 다운로드 (~3GB)
3. **JDK 17** (Android Studio 번들 사용 OK)

## 빌드

```bash
cd web
npm run build               # dist/ 갱신
npx cap sync android        # dist를 android/ 안으로 복사
npx cap open android        # Android Studio 열림
```

Android Studio에서:
- 상단 **Build → Build Bundle(s) / APK(s) → Build APK(s)**
- 완료되면 우하단 알림에서 "Locate" 클릭 → `app-debug.apk` 위치 확인
- 그 APK 파일을 카톡으로 동료들에게 보내면 안드로이드에서 바로 설치 가능

## Play Store 정식 배포 시

- `Build → Generate Signed Bundle / APK` (Keystore 필요, 처음 한 번만 생성)
- Google Play Console($25 1회) 가입 → 새 앱 → 내부 테스트 트랙에 AAB 업로드
- 아이콘 512×512, 스크린샷, 개인정보처리방침 URL 등 메타 채우기
- 심사 (보통 몇 시간 ~ 며칠)

---

# 4. iOS 앱 (macOS 필요)

Windows에서는 빌드 불가. Mac이 생기면:

```bash
cd web
npx cap add ios
npm run cap:ios
```

---

# 5. 다음 라운드 작업 (B2C MVP)

요청하면 순서대로 진행:

- [ ] **멀티 테넌트 스키마**: `clubs`, `club_members`, `meetups`, `attendances`, `user_profiles`
- [ ] **카카오/구글 로그인**: Supabase Auth OAuth provider 설정 + UI
- [ ] **회원가입 → 클럽 가입/생성** 플로우
- [ ] **클럽 대시보드**: 멤버 목록, 등급, NTRP 분포, 최근 모임
- [ ] **정기 모임 등록 + 출석 체크**
- [ ] **개인 프로필**: 사진, NTRP, 전적, 코트 위치
- [ ] **푸시 알림** (`@capacitor/push-notifications` + FCM)
- [ ] **아이콘/스플래시 정식** (`@capacitor/assets`로 자동 생성)
- [ ] **에러 트래킹** (Sentry)
- [ ] **개인정보처리방침 / 이용약관 페이지**

---

# 6. 스코어링 규칙 (기존 동일)

- 한 매치 = 남단·남복·여복 3종목
- 2종목 이상 이긴 팀이 매치 승자
- 조별 승점: 승 3 / 무 1 / 패 0
- 타이브레이크: 승점 → 득실차 → 승수 → 팀명
