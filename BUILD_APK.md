# 📱 APK 빌드 가이드 (Plan A — 사이드로드)

> Android Studio 설치 끝났다면 여기부터 따라가면 돼. 빌드 → 너 폰 / 동료 폰에 카톡으로 보내기.
> 빌드 자체는 5~10분이면 끝남.

---

## 1. Android Studio 설치 후 첫 설정 (1회만)

처음 켜면:
1. **Welcome to Android Studio** → "Standard" 설치 선택 → 다음
2. 라이선스 동의 → 다운로드 시작 (~3GB, 10~20분)
3. 다 받아지면 메인 화면

## 2. 프로젝트 열기

메인 화면에서 **Open** 클릭 → 다음 경로 선택:

```
C:\Users\andyp\Desktop\tennis_scoring_streamlit\web\android
```

> ⚠️ `web` 폴더가 아니라 `web\android` 폴더를 골라야 해.

처음 열면 Android Studio가 자동으로:
- Gradle sync (1~3분)
- 필요한 SDK 자동 다운로드 (1~5분, 처음 한 번만)

우하단 진행바가 사라지면 끝. 만약 "Install missing SDK" 같은 메시지 뜨면 모두 Accept → Install.

## 3. APK 빌드

상단 메뉴:

**Build → Build Bundle(s) / APK(s) → Build APK(s)**

3~5분 기다리면 우하단에 알림 뜸:

```
APK(s) generated successfully.
Module 'app': 1 APK
```

**locate** 링크 클릭하면 파일 탐색기로 APK 위치 열림. 보통:

```
C:\Users\andyp\Desktop\tennis_scoring_streamlit\web\android\app\build\outputs\apk\debug\app-debug.apk
```

이 파일이 너가 배포할 APK야. 보통 5~10MB.

## 4. 폰에 설치하기

### 4a. 너 폰에 USB로 — 가장 빠름
1. 폰에 **개발자 옵션 → USB 디버깅** 켜기
2. USB로 연결, "이 컴퓨터를 신뢰" 허용
3. Android Studio 상단 가운데 ▶️ Run 버튼 누르면 자동 설치 + 실행

### 4b. 카톡/이메일로 동료에게
1. `app-debug.apk` 파일을 카톡 "나에게" 또는 친구에게 발송
2. 받는 사람: 카톡에서 파일 탭 → "설치 허용 안 됨" 뜨면
   **설정 → 알 수 없는 앱 설치 → 카카오톡 허용** ON
3. 다시 설치 → "CJ Tennis" 앱 생김

### 4c. Google Drive / 회사 URL로
- APK 업로드 → 다운로드 링크 카톡으로 공유
- 같은 절차로 설치

---

## 5. 첫 실행 동작 체크

앱 열면:
1. 노란 테니스 공 + "CJ TENNIS" 스플래시 잠깐
2. 메인 화면: 우상단 칩이 **🟢 실시간** 으로 바뀌어야 함 (Supabase 연결 OK 신호)
3. **선수** 탭 → 🎾 **CJ 50명 시드 로드** → 50명 한번에 표시
4. **조별순위** → 조 편성 → 대진 생성 → 점수 입력
5. **다른 폰**에서 같은 앱 열면 같은 데이터 자동 동기화

만약 칩이 **🔴 오프라인** 이면 Supabase URL/key가 안 박힌 빌드. 다시:
```
cd C:\Users\andyp\Desktop\tennis_scoring_streamlit\web
npm run build
npx cap sync android
```
다시 Android Studio로 가서 Build APK 재실행.

---

## 6. 자주 막히는 부분

### "SDK location not found"
File → Settings → Appearance & Behavior → System Settings → Android SDK
→ SDK Location 메모 → 그 경로를 `web/android/local.properties` 파일에 한 줄 추가:
```
sdk.dir=C:\\Users\\andyp\\AppData\\Local\\Android\\Sdk
```
역슬래시 두 개씩.

### "Gradle sync failed: Could not find tools.jar"
JDK 17 사용 중인지 확인. File → Settings → Build → Gradle → Gradle JDK → "Embedded JDK" 선택.

### "Unable to install APK on device"
- USB 디버깅 다시 확인
- 기존 동일 패키지 다른 서명 앱이 깔려 있으면 먼저 삭제 후 재설치

### "앱이 설치되지 않았습니다" (폰에서 카톡으로 받은 후)
- 설정 → 보안 → 알 수 없는 출처 허용 (제조사마다 메뉴 위치 약간 다름)
- 또는 카톡 앱에 설치 권한 허용

---

## 7. 다음 단계 후보 (오늘 끝나면)

- 📦 **서명된 AAB 빌드** (Google Play 정식 출시용, Production 키스토어 1회 생성)
- 🔐 **카카오 로그인** + **회원가입** 플로우
- 🏟️ **멀티 테넌트** (`clubs / meetups / attendances`)
- 🔔 **푸시 알림** (`@capacitor/push-notifications` + FCM)
- 🛒 **Google Play Console 가입 + Internal Testing 트랙 업로드**
