-- Clover Hollow: online saves and friends
-- Run in Supabase: SQL Editor -> New query -> paste -> Run.
-- Safe to run again: it updates what is already there and keeps all player data.

-- 1. Player profiles (one per account, with a shareable friend code)
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null default 'Farmer',
  friend_code text unique not null,
  created_at timestamptz not null default now()
);
alter table public.profiles drop constraint if exists profiles_display_name_length;
alter table public.profiles add constraint profiles_display_name_length
  check (char_length(display_name) between 1 and 24) not valid;

-- 2. One saved farm per player (the whole game state as JSON)
create table if not exists public.farms (
  user_id uuid primary key references auth.users(id) on delete cascade,
  state jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- 3. Neighbors (stored both directions so lookups stay simple)
create table if not exists public.friendships (
  user_id uuid not null references auth.users(id) on delete cascade,
  friend_id uuid not null references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (user_id, friend_id),
  check (user_id <> friend_id)
);

-- New accounts get a profile with a random 6-character friend code
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
declare code text;
begin
  loop
    code := upper(substr(md5(random()::text), 1, 6));
    exit when not exists (select 1 from public.profiles where friend_code = code);
  end loop;
  insert into public.profiles (id, display_name, friend_code)
  values (new.id, left(coalesce(nullif(trim(new.raw_user_meta_data->>'display_name'), ''), 'Farmer'), 24), code);
  return new;
end $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- Add a neighbor by friend code (creates both directions)
create or replace function public.add_friend(code text)
returns uuid language plpgsql security definer set search_path = public as $$
declare fid uuid;
begin
  select id into fid from public.profiles where friend_code = upper(trim(code));
  if fid is null then raise exception 'No farmer has that friend code'; end if;
  if fid = auth.uid() then raise exception 'That is your own friend code'; end if;
  insert into public.friendships values (auth.uid(), fid, now()) on conflict do nothing;
  insert into public.friendships values (fid, auth.uid(), now()) on conflict do nothing;
  return fid;
end $$;

-- Delete my account: removes the login, profile, farm and neighbor links (for EU privacy rights)
create or replace function public.delete_my_account()
returns void language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then raise exception 'Not signed in'; end if;
  delete from auth.users where id = auth.uid();
end $$;

revoke execute on function public.add_friend(text) from public, anon;
revoke execute on function public.delete_my_account() from public, anon;
grant execute on function public.add_friend(text) to authenticated;
grant execute on function public.delete_my_account() to authenticated;

-- Row level security: players only change their own data; neighbors can view farms
alter table public.profiles enable row level security;
alter table public.farms enable row level security;
alter table public.friendships enable row level security;

-- Players see their own profile and their neighbors' profiles (friend codes are not listable)
drop policy if exists "profiles readable by players" on public.profiles;
drop policy if exists "read own or neighbor profile" on public.profiles;
create policy "read own or neighbor profile" on public.profiles for select to authenticated
  using (id = auth.uid() or exists (select 1 from public.friendships f where f.user_id = auth.uid() and f.friend_id = profiles.id));
-- Players can only change their display name (not their friend code)
drop policy if exists "edit own profile" on public.profiles;
create policy "edit own profile" on public.profiles for update to authenticated
  using (id = auth.uid()) with check (id = auth.uid());
revoke update on public.profiles from authenticated, anon;
grant update (display_name) on public.profiles to authenticated;

drop policy if exists "read own or neighbor farm" on public.farms;
create policy "read own or neighbor farm" on public.farms for select to authenticated
  using (user_id = auth.uid() or exists (select 1 from public.friendships f where f.user_id = auth.uid() and f.friend_id = farms.user_id));
drop policy if exists "create own farm" on public.farms;
create policy "create own farm" on public.farms for insert to authenticated with check (user_id = auth.uid());
drop policy if exists "save own farm" on public.farms;
create policy "save own farm" on public.farms for update to authenticated
  using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists "see own neighbors" on public.friendships;
create policy "see own neighbors" on public.friendships for select to authenticated using (user_id = auth.uid());
drop policy if exists "remove own neighbors" on public.friendships;
create policy "remove own neighbors" on public.friendships for delete to authenticated using (user_id = auth.uid() or friend_id = auth.uid());
