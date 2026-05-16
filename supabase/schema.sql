-- CJ Tennis · Supabase 스키마
-- Postgres 15+/Supabase. 모든 테이블 RLS 활성화. 반복 실행 안전(idempotent).

create extension if not exists "uuid-ossp";

-- 대회 ---------------------------------------------------------------
create table if not exists tournaments (
  id          uuid primary key default uuid_generate_v4(),
  name        text not null,
  format      text not null check (format in ('tournament','friendly')),
  created_by  uuid references auth.users(id) on delete set null,
  created_at  timestamptz not null default now()
);

-- 선수 ---------------------------------------------------------------
create table if not exists players (
  id            uuid primary key default uuid_generate_v4(),
  tournament_id uuid references tournaments(id) on delete cascade,
  name          text not null,
  team          text not null,
  gender        text not null check (gender in ('남','여')),
  ntrp          numeric(2,1),
  career_years  int,
  created_at    timestamptz not null default now()
);

create index if not exists players_team_idx on players(tournament_id, team);

-- 조 편성 ------------------------------------------------------------
create table if not exists groups (
  id            uuid primary key default uuid_generate_v4(),
  tournament_id uuid not null references tournaments(id) on delete cascade,
  name          text not null,
  teams         text[] not null default '{}',
  unique (tournament_id, name)
);

-- 매치 (조별 + 본선 통합) -------------------------------------------
create table if not exists matches (
  id            uuid primary key default uuid_generate_v4(),
  tournament_id uuid not null references tournaments(id) on delete cascade,
  stage         text not null check (stage in ('group','ko')),
  group_name    text,
  ko_label      text,
  ko_round      int,
  ko_position   int,
  home          text not null,
  away          text not null,
  scores        jsonb not null default '{
    "남단": {"home":0,"away":0,"homePlayers":[],"awayPlayers":[]},
    "남복": {"home":0,"away":0,"homePlayers":[],"awayPlayers":[]},
    "여복": {"home":0,"away":0,"homePlayers":[],"awayPlayers":[]}
  }'::jsonb,
  finalized     boolean not null default false,
  winner        text,
  feeds_home_from uuid references matches(id) on delete set null,
  feeds_away_from uuid references matches(id) on delete set null,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create index if not exists matches_tournament_idx on matches(tournament_id, stage);

create or replace function set_updated_at() returns trigger as $$
begin new.updated_at = now(); return new; end;
$$ language plpgsql;

drop trigger if exists matches_touch on matches;
create trigger matches_touch before update on matches
  for each row execute function set_updated_at();

-- RLS ---------------------------------------------------------------
alter table tournaments enable row level security;
alter table players     enable row level security;
alter table groups      enable row level security;
alter table matches     enable row level security;

-- 인증된 사용자: 읽기 허용 / admin 클레임: 쓰기 허용.
-- Postgres CREATE POLICY는 IF NOT EXISTS 미지원 → DROP 후 재생성.
drop policy if exists "read all auth" on tournaments;
create policy "read all auth" on tournaments
  for select to authenticated using (true);
drop policy if exists "read all auth" on players;
create policy "read all auth" on players
  for select to authenticated using (true);
drop policy if exists "read all auth" on groups;
create policy "read all auth" on groups
  for select to authenticated using (true);
drop policy if exists "read all auth" on matches;
create policy "read all auth" on matches
  for select to authenticated using (true);

drop policy if exists "admin write" on tournaments;
create policy "admin write" on tournaments
  for all to authenticated
  using (coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin')
  with check (coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin');
drop policy if exists "admin write" on players;
create policy "admin write" on players
  for all to authenticated
  using (coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin')
  with check (coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin');
drop policy if exists "admin write" on groups;
create policy "admin write" on groups
  for all to authenticated
  using (coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin')
  with check (coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin');
drop policy if exists "admin write" on matches;
create policy "admin write" on matches
  for all to authenticated
  using (coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin')
  with check (coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin');

-- 익명 데모 모드(앱이 아직 로그인 없이 동작): anon에게도 쓰기 임시 허용.
-- 정식 출시 전 반드시 제거하고 인증 강제로 전환할 것.
drop policy if exists "anon demo write" on tournaments;
create policy "anon demo write" on tournaments for all to anon using (true) with check (true);
drop policy if exists "anon demo write" on players;
create policy "anon demo write" on players for all to anon using (true) with check (true);
drop policy if exists "anon demo write" on groups;
create policy "anon demo write" on groups for all to anon using (true) with check (true);
drop policy if exists "anon demo write" on matches;
create policy "anon demo write" on matches for all to anon using (true) with check (true);

-- 실시간 게시 — 이미 추가돼 있을 수 있으므로 안전하게 처리
do $$
begin
  begin alter publication supabase_realtime add table tournaments; exception when duplicate_object then null; end;
  begin alter publication supabase_realtime add table matches;     exception when duplicate_object then null; end;
  begin alter publication supabase_realtime add table players;     exception when duplicate_object then null; end;
  begin alter publication supabase_realtime add table groups;      exception when duplicate_object then null; end;
end$$;
