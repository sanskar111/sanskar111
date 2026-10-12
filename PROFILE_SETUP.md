# Live profile setup

The profile refreshes daily around **05:47 IST** and can also run manually from [Actions → Refresh live profile](https://github.com/sanskar111/sanskar111/actions/workflows/live-profile.yml). GitHub may delay scheduled runs.

## Latest blog posts — activate when you have a feed

Add a repository **Actions variable** named `BLOG_RSS_URL` containing your public RSS/Atom feed URL in [repository variables](https://github.com/sanskar111/sanskar111/settings/variables/actions). Run the workflow once. It will show your five newest posts, newest first, using [gautamkrishnar/blog-post-workflow](https://github.com/gautamkrishnar/blog-post-workflow). Until then the section stays hidden.

## Weekly coding stats

1. Create a [WakaTime account](https://wakatime.com/) and install its [editor integration](https://wakatime.com/plugins).
2. Copy your key from [WakaTime API key settings](https://wakatime.com/api-key).
3. In [GitHub Actions secrets](https://github.com/sanskar111/sanskar111/settings/secrets/actions/new), create `WAKATIME_API_KEY` and paste the key there.
4. Run **Refresh live profile**. [athul/waka-readme](https://github.com/athul/waka-readme) will display total coding time and your five top languages over the rolling last seven days. Its version is pinned to a verified commit from February 2026.

The profile publishes aggregate coding time and language totals. Empty stats remain hidden until the action supplies data. The key stays in GitHub Secrets; it is never placed in your README.

## Daily joke and timestamp

No key is needed. The updater requests the Programming category from [JokeAPI](https://sv443.net/jokeapi/v2/) with safe mode enabled. It retains the last successful joke and its original date if the API is unavailable. The footer shows the last profile sync in IST. Optional blog or WakaTime failures do not prevent the joke refresh.

## Optional: Spotify now playing

This is separate from the scheduled profile workflow and is not enabled yet.

1. Use the [Novatorem template](https://github.com/novatorem/novatorem) and follow its [current setup guide](https://github.com/novatorem/novatorem/blob/main/SetUp.md).
2. Create a Spotify developer app. Configure an exact HTTPS redirect URI and authorize your account for `user-read-currently-playing` and `user-read-recently-played` to obtain a refresh token.
3. Import your widget repository into Vercel. Set `SPOTIFY_CLIENT_ID`, `SPOTIFY_SECRET_ID`, and `SPOTIFY_REFRESH_TOKEN` in Vercel's environment settings. Keep these credentials out of source files.
4. Deploy the widget, verify its `/api/orchestrator` endpoint, and add the following to your profile README after replacing both placeholders:

```markdown
## 🎧 Gotham soundtrack
[![Now playing](https://YOUR_DEPLOYMENT.vercel.app/api/orchestrator?background_color=0d1117&border_color=f4c542&show_status=true)](https://open.spotify.com/user/YOUR_SPOTIFY_USER)
```

The card displays current or recent listening activity publicly. Check Spotify's current developer-app eligibility and redirect-URI requirements during setup. GitHub caches embedded images, so updates may not appear immediately.
