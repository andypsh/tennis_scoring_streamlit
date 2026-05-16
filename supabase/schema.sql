-- CJ Tennis · Supabase 스키마
-- Postgres 17 / Supabase 기준. 모든 테이블 RLS 활성화 권장.

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

-- 데모: 인증된 사용자는 모두 읽기, admin 클레임만 쓰기.
-- 운영 시 더 세분화 필요.
create policy if not exists "read all auth" on tournaments
  for select using (auth.role() = 'authenticated');
create policy if not exists "read all auth" on players
  for select using (auth.role() = 'authenticated');
create policy if not exists "read all auth" on groups
  for select using (auth.role() = 'authenticated');
create policy if not exists "read all auth" on matches
  for select using (auth.role() = 'authenticated');

create policy if not exists "admin write" on tournaments
  for all using (auth.jwt() ->> 'role' = 'admin')
  with check (auth.jwt() ->> 'role' = 'admin');
create policy if not exists "admin write" on players
  for all using (auth.jwt() ->> 'role' = 'admin')
  with check (auth.jwt() ->> 'role' = 'admin');
create policy if not exists "admin write" on groups
  for all using (auth.jwt() ->> 'role' = 'admin')
  with check (auth.jwt() ->> 'role' = 'admin');
create policy if not exists "admin write" on matches
  for all using (auth.jwt() ->> 'role' = 'admin')
  with check (auth.jwt() ->> 'role' = 'admin');

-- 실시간 게시 ----------------------------------------------------
alter publication supabase_realtime add table matches;
alter publication supabase_realtime add table players;
alter publication supabase_realtime add table groups;
