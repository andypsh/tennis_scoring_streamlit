# CJ Tennis · Vue 포팅 기술 가이드 (v0.2)

> 대상 브랜치: `feature_andy_vue`
> 작성일: 2026-05-16
> 상태: 베타 (B2C MVP 전 단계)

기존 Streamlit 기반 점수 관리 도구를 **Vue 3 + Vite + Capacitor** 스택으로
재구현하면서 모바일 앱(Android/iOS)·PWA·Supabase 실시간 동기화까지 묶은
풀스택 SPA로 확장했다. 이 문서는 오늘(2026-05-16) 작업이 끝난 시점의
구조·데이터 모델·알고리즘·빌드 경로를 한 곳에 모아 정리한 기술문서다.
운영 가이드(README)는 [`README_VUE.md`](../README_VUE.md)를 참고.

---

## 1. 오늘 작업 요약

5개의 커밋으로 다음을 완료했다.

| 커밋 | 핵심 변경 |
|---|---|
| `49165e0` | Vue 3 + Vite + TS + Tailwind + Pinia 스캐폴드. Streamlit 4페이지 → Vue 7페이지로 재구성. 대진/복식/스코어링 라이브러리 신규 작성. |
| `60ad718` | `lib/sync.ts` 추가로 Supabase pull/push + Realtime 채널 구독. NavBar에 동기화 상태 칩. PWA 매니페스트. Node 16 호환을 위한 툴체인 다운그레이드(Vite 4.5 / vue-tsc 1.8 / Capacitor 5). |
| `7efe77a` | 실제 CJ 50명 시드 데이터(`seedPlayers.ts`). `parseNumeric()` 으로 `"7년"`, `"NTRP 3.5"` 같은 문자열 셀 안전 파싱. dev/preview 포트 5174/4174로 이동. |
| `5deb852` | `npx cap add android` 결과물 커밋(`web/android/`). 미설정 환경에서 떠 있는 `SetupNotice.vue` 안내 카드. README 로드맵 정비. |
| `819a7bc` | Supabase 스키마 idempotent 화 (`CREATE POLICY IF NOT EXISTS` 미지원 → `DROP + CREATE`). admin JWT 클레임 경로 수정(`auth.jwt() -> 'app_metadata' ->> 'role'`). 익명 데모 쓰기 정책 추가. `alter publication ... add table` 을 `do$$ ... exception when duplicate_object$$` 로 감쌈. |

빌드 검증: `vue-tsc --noEmit` 통과, `vite build` 8 chunk 성공, `vite preview` 4173/4174 기동 OK,
Supabase SQL Editor에서 스키마 `Success. No rows returned.` 확인,
anon REST 키로 `insert/select/delete` 200/201/204 통과.

---

## 2. 아키텍처 개요

```
┌──────────────────────────────────────────────────────────────────┐
│                        Vue 3 SPA  (web/src)                       │
│                                                                   │
│   ┌──────────────┐   ┌─────────────────┐   ┌──────────────────┐  │
│   │  pages/*.vue │ ◀ │  stores (Pinia) │ ▶ │  lib/*  (algos)  │  │
│   │   라우트 화면 │   │  tournament·auth│   │ bracket/doubles/ │  │
│   └──────────────┘   └─────────────────┘   │ scoring/sync     │  │
│           ▲                  │              └──────────────────┘  │
│           │            persist│push                     │          │
│           │                  ▼                         ▼          │
│   ┌──────────────┐   ┌─────────────────┐   ┌──────────────────┐  │
│   │ components/  │   │   localStorage  │   │ Supabase JS SDK  │  │
│   │ NavBar/Setup │   │ cj_tennis_state │   │  PostgREST + WS  │  │
│   └──────────────┘   └─────────────────┘   └──────────────────┘  │
│                                                       │           │
└───────────────────────────────────────────────────────┼───────────┘
                                                        │
                       ┌────────────────────────────────▼──────┐
                       │ Supabase Postgres (tournaments/players │
                       │ /groups/matches) + Realtime publication│
                       │ + RLS                                   │
                       └─────────────────────────────────────────┘
                                                        ▲
              ┌─────────────────────────────┐           │
              │  Capacitor 5 네이티브 쉘    │ ◀ dist ───┘
              │  web/android/  (web/ios/)   │
              └─────────────────────────────┘
```

### 설계 원칙

1. **로컬 우선(local-first).** 모든 mutate는 즉시 `localStorage`에 영속화한 뒤,
   Supabase가 설정돼 있으면 비동기 푸시. 오프라인/네트워크 실패에도 화면이 멈추지 않는다.
2. **데모 모드 폴백.** `.env`에 Supabase URL/Key가 없으면 `hasSupabase=false`로 모든 sync 함수가 no-op. 인증도 admin/admin 하드코딩으로 통과시켜 데모 가능.
3. **Echo 방지.** Realtime 구독 중 자기 자신의 push로 인한 이벤트는 `suppressRealtime` 플래그로 무시.
4. **단일 통합 매치 테이블.** 조별·본선 모두 `matches` 한 테이블에 `stage in ('group','ko')`로 구분. 클라이언트에서 분리.

---

## 3. 디렉토리 구조

```
.
├── docs/
│   └── VUE_TECHNICAL_GUIDE.md      ← (이 문서)
├── README_VUE.md                   ← 운영 가이드
├── src/                            ← 기존 Streamlit (참조용 보존)
├── supabase/
│   └── schema.sql                  ← 1회 실행할 DB 스키마 + RLS + Realtime
└── web/                            ← Vue 앱 루트
    ├── capacitor.config.ts         ← 앱 ID com.cj.tennis, webDir dist
    ├── vite.config.ts              ← dev:5174 / preview:4174
    ├── tailwind.config.js
    ├── tsconfig.json               ← path alias @/* → src/*
    ├── public/
    │   ├── manifest.webmanifest    ← PWA 매니페스트
    │   ├── favicon.svg
    │   └── players-sample.csv      ← 엑셀 업로드 테스트용 50명 데이터
    ├── android/                    ← npx cap add android 결과물
    │   ├── app/build.gradle
    │   └── ...
    └── src/
        ├── main.ts                 ← createApp + Pinia + Router
        ├── App.vue                 ← <SetupNotice/> + <NavBar/> + <RouterView/>
        ├── env.d.ts
        ├── style.css               ← Tailwind layers
        ├── components/
        │   ├── NavBar.vue          ← 라우트 링크 + 동기화 상태 칩
        │   └── SetupNotice.vue     ← Supabase 미설정 시 5단계 가이드
        ├── pages/
        │   ├── LoginPage.vue
        │   ├── PlayersPage.vue     ← 엑셀 업로드 + 50명 시드 로드 버튼
        │   ├── StandingsPage.vue   ← 조 편성 + 조별 순위
        │   ├── ScorePage.vue       ← 매치 점수 입력 (3종목 동시 출전 방지)
        │   ├── BracketPage.vue     ← 본선 대진표
        │   ├── TimetablePage.vue   ← 코트·슬롯 자동 배치
        │   └── DoublesPage.vue     ← 복식 파트너 매칭
        ├── router/index.ts
        ├── stores/
        │   ├── tournament.ts       ← 전역 상태 + 영속 + sync 오케스트레이션
        │   └── auth.ts             ← Supabase Auth 세션 / 데모 모드 role
        ├── lib/
        │   ├── scoring.ts          ← 매치/조별 순위 계산
        │   ├── bracket.ts          ← 본선 시드/대진 생성, 승자 전파
        │   ├── doubles.ts          ← NTRP/구력 기반 균형 페어
        │   ├── sync.ts             ← Supabase pull/push + Realtime
        │   └── supabase.ts         ← createClient + hasSupabase 플래그
        ├── data/
        │   └── seedPlayers.ts      ← 실제 CJ 50명 시드(10팀 × 남3·여2)
        └── types/
            └── domain.ts           ← Player/Match/Group/Bracket/Scores
```

---

## 4. 모듈별 책임

### 4.1 `types/domain.ts`

핵심 타입 정의. 종목은 고정 3종(`남단`/`남복`/`여복`).

```ts
type EventKey = '남단' | '남복' | '여복'
const EVENT_PLAYER_COUNT: Record<EventKey, number> = { 남단: 1, 남복: 2, 여복: 2 }
const EVENT_GENDER:       Record<EventKey, '남'|'여'> = { 남단: '남', 남복: '남', 여복: '여' }
```

- `Match`: 조별. `stage='group'`, 3종목 score 합쳐 winner 결정.
- `BracketNode`: 본선. `feedsHomeFrom`/`feedsAwayFrom`로 부모 노드 연결.
- `emptyScores()`: 모든 종목 0:0, 출전 선수 빈 배열.

### 4.2 `lib/scoring.ts`

- `evaluateMatch(scores)` → `{ homeWonEvents, awayWonEvents, goalDiff }`
- `matchWinner(home, away, scores)` → 2종목 이상 이긴 팀, 없으면 null
- `calculateStandings(teams, matches)`: 승점(승 3 / 무 1 / 패 0), 득실차, 승수, 팀명 순으로 정렬

### 4.3 `lib/bracket.ts`

본선 대진표 자동 생성. 4가지를 한꺼번에 처리한다.

1. **시드 추출**: 각 조 1~`advancePerGroup`위 → 글로벌 시드(rank 우선, 같은 rank 안에선 조 이름)
2. **bracket size 결정**: `nextPowerOfTwo(seedCount)` 까지 BYE 채움 (`bracketSize ≥ 2`)
3. **표준 시드 매칭**: 재귀적으로 `[1,2] → [1,4,2,3] → [1,8,4,5,2,7,3,6]` 펼침
4. **같은 조 1라운드 충돌 회피**: 다른 조인 후순위 슬롯의 away와 swap
5. **BYE 자동 통과 + 승자 전파**: `propagateWinner(nodes, updated)` 가 부모 노드의 home/away를 채움

```ts
generateRoundRobin(tournamentId, groups): Match[]
generateKnockoutBracket(tournamentId, groups, matches, { advancePerGroup }): BracketNode[]
evaluateBracketNode(node): { homeWins, awayWins, winner }
propagateWinner(nodes, updated): void
```

### 4.4 `lib/doubles.ts`

복식 파트너 매칭. NTRP가 비면 구력으로, 둘 다 비면 3.0으로 폴백.

```ts
makeBalancedRound(players): { pairs, matchups }
makeMultipleRounds(players, rounds): Array<...>
```

- **페어링 전략**: NTRP 내림차순 정렬 → 양 끝에서 강+약을 묶어 라운드 내 페어 합 평준화
- **매치업**: 페어를 합 순으로 다시 정렬해 이웃 페어끼리 매칭 → `ratingGap` 최소화
- **다라운드**: 24회 셔플 트라이얼, `score = 재사용페어수×100 + gapTotal` 최소를 선택해 이전 라운드 페어 재사용 회피

### 4.5 `lib/sync.ts`

Supabase pull/push + Realtime. `hasSupabase=false`면 모든 함수가 안전하게 no-op.

| 함수 | 역할 |
|---|---|
| `ensureTournament(name?)` | 최근 tournaments row가 있으면 그 id, 없으면 새로 만들고 id 반환 |
| `pullSnapshot()` | tournament + groups + players + matches 한 번에 fetch. `stage`로 group/ko 분리 |
| `pushPlayers/Groups/Matches(...)` | 단순 delete-then-insert 풀 리플레이스 |
| `subscribeRealtime(tournamentId, { onChange })` | matches/players/groups 3개 테이블 변경 이벤트 단일 채널 구독, unsubscribe 함수 반환 |

row mapper(`rowToMatch`/`rowToBracketNode`/`rowToPlayer`)에서 DB snake_case ↔ TS camelCase 변환.

### 4.6 `stores/tournament.ts`

Pinia 스토어. 거의 모든 사용자 액션이 여기를 통과한다.

핵심 패턴:

```ts
// 모든 mutate 액션의 공통 마무리
this.persist()                  // localStorage 즉시 반영
void this.flushRemote('matches')// fire-and-forget Supabase push
```

`loadAll()` 시퀀스:

1. localStorage 캐시 즉시 적용 (오프라인 부팅 가속)
2. `hasSupabase`면 `ensureTournament` → `pullSnapshot` → 상태 덮어쓰기
3. `subscribeRealtime` 등록. 콜백에선 `refreshFromRemote()` 호출
4. 자기 자신의 push로 인한 echo는 `suppressRealtime` 플래그로 차단

`parseNumeric()` (29~38행): 엑셀 셀이 `7`, `"7"`, `"7년"`, `"0.5년"`, `"NTRP 3.5"` 등 어떤 형태든 첫 숫자 토큰을 추출. 이전 버전은 `typeof number`만 받아서 `"7년"`이 `null`로 떨어지는 버그 있었음.

`importPlayers(rows)`: 한국어 컬럼명(`이름`/`소속`/`성별`/`구력`)과 영어 키 둘 다 허용.

### 4.7 `stores/auth.ts`

- Supabase가 설정돼 있으면 `auth.getSession()` + `onAuthStateChange`로 role 추적
- 미설정이면 `localStorage.cj_role` 또는 `'admin'` 폴백 (데모 편의)
- `signIn(email, password)`: 데모 모드에선 `admin/admin` 하드코딩, 운영에선 `signInWithPassword`
- role은 JWT의 `app_metadata.role` 클레임에서 읽음 (스키마 RLS와 일치)

### 4.8 컴포넌트

- `NavBar.vue`: 라우트 7개 링크 + 우상단 동기화 상태 칩
  - 🟢 실시간 / 🟡 동기화… / 🔴 오프라인 / ⚪ 로컬 데모
- `SetupNotice.vue`: `hasSupabase=false`일 때 화면 상단 노란 카드. Supabase 가입 5단계를 펼침형으로 표시. "다시 보지 않기" → `localStorage.cj_setup_dismissed`.

---

## 5. 데이터 모델

### 5.1 도메인 → 테이블 매핑

| 도메인 | 테이블 | 비고 |
|---|---|---|
| `Tournament` | `tournaments` | 한 row가 한 대회 |
| `Player` | `players` | (tournament_id, team) 인덱스 |
| `Group` | `groups` | `teams text[]`로 팀명 직접 저장 |
| `Match` (조별) | `matches` (stage='group') | scores는 jsonb |
| `BracketNode` (본선) | `matches` (stage='ko') | ko_label/ko_round/ko_position + feeds_*_from |

### 5.2 `matches.scores` JSON 모양

```json
{
  "남단": {"home":0,"away":0,"homePlayers":[],"awayPlayers":[]},
  "남복": {"home":0,"away":0,"homePlayers":[],"awayPlayers":[]},
  "여복": {"home":0,"away":0,"homePlayers":[],"awayPlayers":[]}
}
```

`set_updated_at()` 트리거가 `updated_at`을 자동 갱신.

### 5.3 RLS

- `read all auth`: authenticated role은 모든 row SELECT
- `admin write`: JWT `app_metadata.role = 'admin'` 인 authenticated 만 INSERT/UPDATE/DELETE
- `anon demo write`: **베타 한정 임시 정책.** anon role 전체 쓰기 허용. **정식 출시 전 반드시 제거** 후 인증 강제로 전환.

스키마는 idempotent. `CREATE POLICY IF NOT EXISTS`는 Postgres에 없으므로
`drop policy if exists ... ; create policy ...` 패턴을 사용. publication 추가도
`exception when duplicate_object then null` 로 감싸 반복 실행 안전.

### 5.4 Realtime

`supabase_realtime` publication에 `tournaments/matches/players/groups` 4개 테이블 add.
클라이언트는 `tournament:<id>` 채널 하나로 3개 테이블의 `postgres_changes` 이벤트를 구독.

---

## 6. 라우팅 / 페이지

`createWebHashHistory` 사용 (Capacitor `file://` 환경에서 안전).

| Path | 컴포넌트 | 역할 |
|---|---|---|
| `/login` | LoginPage | 데모 모드면 admin/admin, 운영이면 Supabase 비번 로그인 |
| `/players` | PlayersPage | 엑셀 업로드 / 🎾 CJ 50명 시드 로드 / 샘플 CSV 다운로드 |
| `/standings` | StandingsPage | 조 편성 + 조별 라운드로빈 순위표 |
| `/score` | ScorePage | 매치 3종목 점수 입력. 종목간 중복 출전 방지 |
| `/bracket` | BracketPage | 본선 자동 생성 (advancePerGroup 선택) + 회차별 점수 입력 |
| `/timetable` | TimetablePage | 코트·슬롯 자동 배치 |
| `/doubles` | DoublesPage | NTRP/구력 기반 균형 페어 + 라운드 매치업 |

`/` → `/standings` 리다이렉트.

---

## 7. 빌드 & 배포 경로

### 7.1 웹 (로컬/Vercel/Netlify)

```bash
cd web
npm install
npm run dev        # http://localhost:5174
npm run build      # → dist/  (vue-tsc + vite build)
npm run preview    # http://localhost:4174
```

`vite.config.ts` 의 `strictPort: false`로 포트 충돌 시 자동 다음 포트 사용.

### 7.2 PWA

`public/manifest.webmanifest` + `index.html`의 `<link rel="manifest">`만으로
"홈 화면에 추가" 가능. 별도 Service Worker는 아직 없음 (오프라인 캐시는
localStorage가 담당).

### 7.3 Android (Capacitor 5)

```bash
cd web
npm run build
npx cap sync android    # dist/ → android/app/src/main/assets/public/
npx cap open android    # Android Studio 열림
```

Android Studio: **Build → Build Bundle(s) / APK(s) → Build APK(s)** → `app-debug.apk` 생성.
카톡으로 공유하면 사이드로드 가능. 정식 배포는 Generated Signed Bundle + Play Console.

앱 ID: `com.cj.tennis`. 아이콘/스플래시는 Capacitor 디폴트 그대로 (정식 출시 전 `@capacitor/assets`로 교체 예정).

### 7.4 iOS

Windows에서는 빌드 불가. macOS에서 `npx cap add ios && npm run cap:ios`.

### 7.5 툴체인 핀

Node 16 호환이 목표이므로 의도적으로 다운그레이드해 둠.

| 패키지 | 버전 | 비고 |
|---|---|---|
| vite | ^4.5.5 | 5.x는 Node 18+ 요구 |
| vue-tsc | ^1.8.27 | 2.x는 TS 5.4+ 요구 |
| @vitejs/plugin-vue | ^4.6.2 | vite 4 호환 |
| typescript | ~5.2.2 | vue-tsc 1.x 호환 |
| @capacitor/* | ^5.7.8 | 6.x는 Node 18+ |

---

## 8. 환경 변수

`web/.env` (gitignored, `.env.example`만 커밋):

```
VITE_SUPABASE_URL=https://xxxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1...
```

`lib/supabase.ts` 가 두 값이 모두 있을 때만 `createClient` 호출하고
`hasSupabase=true`를 export. 둘 중 하나라도 없으면 전체 앱이 로컬 데모 모드.

---

## 9. 알려진 제약 / 다음 단계 진입 전 정리할 것

- [ ] **익명 데모 쓰기 정책 (`anon demo write`) 제거.** 정식 출시 전 인증 강제로 전환.
- [ ] **Service Worker** 미존재 → 새로고침 오프라인 부팅 불가 (localStorage가 있어도 첫 HTML 로드는 네트워크 필요)
- [ ] **PWA 아이콘/스플래시 정식 제작.** 현재는 단순 favicon.svg.
- [ ] **단일 토너먼트 전제.** `pullSnapshot`이 가장 최근 1개만 가져옴 → 멀티 대회 동시 운영 시 UI에서 선택자 필요.
- [ ] **푸시 리플레이스 전략의 한계.** `pushPlayers`/`pushMatches`가 `delete-then-insert`라 동시에 두 명이 편집하면 마지막 푸시 승. 본격 다인 편집이 필요해지면 row-level upsert로 전환.
- [ ] **iOS 빌드 검증** 미수행 (macOS 필요).
- [ ] **테스트 코드 0개.** vitest + 핵심 알고리즘(bracket/doubles/scoring) 단위 테스트 우선 추가 권장.

---

## 10. 다음 라운드 (B2C MVP)

순서대로 진행 예정 (README와 동기):

1. 멀티 테넌트 스키마: `clubs`, `club_members`, `meetups`, `attendances`, `user_profiles`
2. 카카오/구글 OAuth (Supabase Auth provider)
3. 회원가입 → 클럽 가입/생성 플로우
4. 클럽 대시보드 (멤버, NTRP 분포, 최근 모임)
5. 정기 모임 등록 + 출석 체크
6. 개인 프로필 (사진, NTRP, 전적)
7. 푸시 알림 (`@capacitor/push-notifications` + FCM)
8. 아이콘/스플래시 (`@capacitor/assets`)
9. Sentry / 개인정보처리방침 / 이용약관

---

## 부록 A. 스코어링 규칙 (기존과 동일)

- 한 매치 = 남단·남복·여복 3종목
- **2종목 이상 이긴 팀이 매치 승자**
- 조별 승점: 승 3 / 무 1 / 패 0
- 타이브레이크: 승점 → 득실차 → 승수 → 팀명

## 부록 B. 커밋 SHA 빠른 참조

```
49165e0  feat: Vue 3 + Capacitor 포팅 (대진표 자동생성 + 복식 매칭 포함)
60ad718  feat: Supabase 실시간 동기화 + PWA 매니페스트 + Node 16 빌드 호환
7efe77a  feat: 실제 CJ 50명 시드 데이터 + '7년' 같은 문자열 구력 파싱
5deb852  feat: Android 네이티브 프로젝트 + 인앱 Supabase 셋업 안내
819a7bc  fix:  schema RLS idempotent + anon demo write policy + safe publication add
```
