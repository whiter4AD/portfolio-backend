-- ============================================================
--  Portfolio Database Schema — run this in Supabase SQL Editor
-- ============================================================

-- Enable UUID generation
create extension if not exists "pgcrypto";

-- ── PROJECTS ────────────────────────────────────────────────────
create table if not exists projects (
  id          uuid primary key default gen_random_uuid(),
  title       text not null,
  description text not null,
  tags        text[]   default '{}',
  image_url   text,
  live_url    text,
  github_url  text,
  featured    boolean  default false,
  "order"     integer  default 0,
  created_at  timestamptz default now(),
  updated_at  timestamptz default now()
);

-- Auto-update updated_at on any row change
create or replace function set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger projects_updated_at
  before update on projects
  for each row execute function set_updated_at();

-- ── BLOG POSTS ──────────────────────────────────────────────────
create table if not exists blog_posts (
  id          uuid primary key default gen_random_uuid(),
  title       text not null,
  slug        text not null unique,
  excerpt     text not null,
  content     text not null,
  tags        text[]   default '{}',
  cover_url   text,
  published   boolean  default false,
  created_at  timestamptz default now(),
  updated_at  timestamptz default now()
);

create trigger blog_posts_updated_at
  before update on blog_posts
  for each row execute function set_updated_at();

-- ── ROW LEVEL SECURITY ──────────────────────────────────────────
-- Public can only READ published content.
-- Writes require the service_role key (your backend uses anon key
-- so keep write operations server-side or add auth later).

alter table projects   enable row level security;
alter table blog_posts enable row level security;

-- Anyone can read projects
create policy "Public read projects"
  on projects for select using (true);

-- Anyone can read published posts
create policy "Public read published posts"
  on blog_posts for select using (published = true);

-- ── SEED DATA (optional — delete if not needed) ─────────────────
insert into projects (title, description, tags, featured, "order") values
  ('Project Alpha', 'A full-stack web app built with React and FastAPI.', array['React','FastAPI','PostgreSQL'], true,  1),
  ('Project Beta',  'Mobile-first design system and component library.',  array['Design','Figma','CSS'],          true,  2),
  ('Project Gamma', 'Open-source CLI tool for developers.',               array['Python','CLI','Open Source'],    false, 3),
  ('Project Delta', 'E-commerce storefront with real-time inventory.',    array['Next.js','Stripe','Supabase'],   false, 4);

insert into blog_posts (title, slug, excerpt, content, tags, published) values
  (
    'How I built my portfolio',
    'how-i-built-my-portfolio',
    'A walkthrough of the tech stack and design decisions behind this site.',
    '## Introduction\n\nThis is the full content of the post in Markdown...',
    array['meta','design','fastapi'],
    true
  );
