# Setup checklist

- [x] GitHub repository `Crealotte/clover-hollow`
- [ ] Claude GitHub App installed on the repository (so Claude can push)
- [x] Supabase project created (Central EU) and the anon key added to `supabase-config.js`
- [x] Database tables created
- [ ] Run the updated `supabase/schema.sql` once more: Supabase → SQL Editor → New query → paste the whole file → Run. It is safe to run again and keeps all data. It adds "delete my account", hides friend codes from strangers, and stops players from changing their own friend code.
- [ ] Supabase → Authentication → URL Configuration → Site URL: `https://crealotte.github.io/clover-hollow/`
- [ ] Same page → Redirect URLs → Add URL: `https://crealotte.github.io/clover-hollow/**`
- [ ] GitHub → repository Settings → Pages → Source: Deploy from a branch → `main` / root → Save
- [x] Privacy note page (EU testers): `privacy.html`, linked from the sign-in panel
- [x] Online features in the game: sign in, cloud save, friend codes
- [ ] Visiting neighbors (next roadmap step)
- [ ] Before more than a handful of testers sign up: Supabase → Authentication → Emails → SMTP Settings → set up your own email sender. Supabase's built-in sender only allows a few sign-in emails per hour for the whole project.

## How online play works
- **Sign in:** players tap **Sign in** at the top right, type their email and tap the link Supabase emails them. There are no passwords. They stay signed in on that device.
- **Cloud save:** the farm still saves on the device first. While signed in, changes also go online at most every 15 seconds and when the tab is closed or hidden. When a device and the cloud both have a farm, the newer one wins. The first time someone signs in on a device they already played on while signed out, the game asks which farm to keep.
- **Friend codes:** every account gets a 6-character code (Friends panel). Adding a code makes both players neighbors right away. Neighbors can see each other's name, level and farm.
- **Delete my account** (Friends panel) removes the login, profile, online farm and neighbor links. The copy on that device stays.
