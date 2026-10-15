# Clover Hollow: notes for Claude

Charlotte (GitHub: Crealotte) is building a FarmVille-inspired browser game with friends and testers. She isn't a programmer, so explain steps plainly, keep choices few, and do the technical work yourself.

- Read `docs/design-notes.md` before changing gameplay or art. It holds her decisions.
- `index.html` is the whole game today (vanilla JS, SVG art, saves to localStorage). Keep it working as a single page until the move to a build setup is agreed.
- Online play uses Supabase: `supabase/schema.sql` (profiles with friend codes, one JSON farm per player, friendships, row-level security). The Project URL and anon key go in the client. Never put the service_role key or database password in the repo.
- Hosting: GitHub Pages from `main`.
- `data/` is research data from the FarmVille fan wiki. Use it for reference only. Never copy FarmVille names or art into the game.
- Testers are in the EU, so the game needs a short privacy note before sign-ups open.
