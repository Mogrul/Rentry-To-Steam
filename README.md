# Rentry To Steam

A small Python utility that takes a **RimSort-exported Rentry mod list**, extracts the Steam Workshop items, and automatically subscribes your Steam account to every item.

Useful for quickly subscribing to an entire RimWorld mod list without manually opening and subscribing to every Workshop item.

**Repository:** [github.com/Mogrul/Rentry-To-Steam](https://github.com/Mogrul/Rentry-To-Steam?utm_source=chatgpt.com)

## ✨ Features

* 📋 Use Rentry mod lists exported by **RimSort**
* 🔐 Authenticate using your existing Steam browser session
* 🍪 Supports Netscape-format browser cookie exports
* ⚡ Automatically subscribe to every Steam Workshop item
* 📦 Managed with `uv`

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Mogrul/Rentry-To-Steam.git
cd Rentry-To-Steam
```

Install the dependencies with `uv`:

```bash
uv sync
```

---

## 📋 Rentry Mod List

This utility is designed to work with **Rentry mod lists exported using [RimSort](https://github.com/RimSort/RimSort)**.

Create or export your RimWorld mod list from RimSort using its Rentry export functionality.

The resulting Rentry page contains the Steam Workshop links for the mods in your list, which `Rentry To Steam` uses to find the Workshop item IDs.

You **do not need to manually create or modify the Rentry page**.

---

## 🍪 Steam Authentication

The script uses your existing Steam Community browser session.

You will need to export your Steam cookies in **Netscape cookie format**.

A browser extension such as **Get cookies.txt** can be used to export the cookies.

Export the cookies while logged into:

```text
https://steamcommunity.com/
```

Save the exported file as:

```text
.cookies/steam.txt
```

Your project should look like:

```text
Rentry-To-Steam/
├── .cookies/
│   └── steam.txt
├── python_to_steam/
│   └── ...
├── pyproject.toml
├── uv.lock
└── README.md
```

Make sure `.cookies/` is included in `.gitignore`:

```gitignore
.cookies/
```

### ⚠️ Keep your cookie file private

`steam.txt` contains your Steam authentication session.

**Do not upload it to GitHub or share it with anyone.**

Treat the cookie file like a password. If it is compromised, invalidate your Steam web sessions immediately.

---

## 🚀 Usage

Once your Steam cookies are configured and you have a RimSort Rentry mod list, run:

```bash
uv run python -m python_to_steam <rentry_url>
```

For example:

```bash
uv run python -m python_to_steam https://rentry.co/my-rimworld-modlist
```

The utility will:

1. Fetch the Rentry mod list
2. Find the Steam Workshop links exported by RimSort
3. Extract the Workshop item IDs
4. Connect to Steam using your authenticated session
5. Subscribe to each Workshop item

---

## 🔧 Requirements

* Python **3.10+**
* [uv](https://docs.astral.sh/uv/)
* [RimSort](https://github.com/RimSort/RimSort)
* A Steam account
* Steam Community browser cookies
* A Rentry mod list exported using RimSort

---

## 🔒 Security

This utility does **not** require your Steam username or password.

Authentication is performed using your existing Steam Community session cookie.

Never:

* Commit `.cookies/steam.txt`
* Upload it to GitHub
* Send it to other people
* Post it in screenshots or logs

If you accidentally expose your cookies, invalidate your Steam web sessions immediately.

---

## 📜 License

MIT License

Copyright © 2026 Mogrul
