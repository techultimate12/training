#!/usr/bin/env python3
"""
YouTube Documentary Shorts Generator
=====================================

macOS-friendly Tkinter program that:
- Searches YouTube dynamically using yt-dlp
- Finds short-form videos (<= 180 seconds)
- Filters by educational/documentary-style categories
- Randomly selects one
- Autoplays it inside the Tkinter window using VLC
- Provides a browser fallback button

REQUIREMENTS
------------
1) Python 3 with Tkinter
2) yt-dlp:
       python3 -m pip install -U yt-dlp
3) python-vlc:
       python3 -m pip install python-vlc
4) VLC Media Player installed on macOS:
       https://www.videolan.org/vlc/

Run:
       python3 youtube_documentary_shorts_generator.py

Notes:
- YouTube search results change over time.
- "Shorts only" is approximated by requiring a video duration <= 180 seconds
  and using Shorts-oriented search terms.
- YouTube may occasionally change playback behavior; use the
  "Open on YouTube" fallback if embedded playback fails.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import random
import platform
import webbrowser
import time

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

try:
    import vlc
except ImportError:
    vlc = None


APP_TITLE = "Documentary Shorts Generator"
WINDOW_SIZE = "1180x760"
MAX_SHORT_SECONDS = 180

# Curated search prompts. The app searches YouTube live; these are not fixed videos.
CATEGORY_QUERIES = {
    "Science": [
        "science facts documentary shorts",
        "space science shorts educational",
        "physics facts shorts documentary",
        "biology facts shorts educational",
        "chemistry surprising facts shorts",
        "earth science mini documentary shorts",
        "astronomy facts shorts documentary",
        "science discoveries shorts educational",
        "ocean science facts shorts",
        "medical science facts shorts educational",
    ],
    "History": [
        "history mini documentary shorts",
        "ancient history facts shorts",
        "world history shorts documentary",
        "forgotten history shorts",
        "historical events explained shorts",
        "ancient civilizations shorts educational",
        "medieval history shorts documentary",
        "war history facts shorts educational",
        "archaeology discoveries shorts",
        "history mysteries shorts documentary",
    ],
    "Psychology": [
        "psychology facts shorts educational",
        "human behavior psychology shorts",
        "brain psychology facts shorts",
        "cognitive bias shorts educational",
        "social psychology facts shorts",
        "psychology experiments shorts documentary",
        "memory psychology shorts",
        "personality psychology facts shorts",
        "mental habits psychology shorts educational",
        "decision making psychology shorts",
    ],
    "Teens & Youth": [
        "teen psychology facts shorts educational",
        "adolescent brain development shorts",
        "teen study habits science shorts",
        "teen social media psychology shorts educational",
        "teen sleep science shorts",
        "youth mental health facts shorts educational",
        "teen technology habits shorts",
        "teen communication psychology shorts",
        "student productivity science shorts",
        "teen decision making brain shorts",
    ],
    "Shocking Facts": [
        "shocking science facts shorts educational",
        "surprising history facts shorts",
        "unbelievable true facts shorts documentary",
        "strange facts explained shorts",
        "disturbing history facts educational shorts",
        "unexpected science discoveries shorts",
        "weird true facts shorts educational",
        "things you did not know shorts documentary",
        "mind blowing facts shorts educational",
        "rare historical facts shorts",
    ],
    "Top 10 / Lists": [
        "top 10 science facts shorts",
        "top 10 history facts shorts",
        "top 10 strange facts shorts",
        "top 10 discoveries shorts educational",
        "top 10 mysteries shorts documentary",
        "top facts about space shorts",
        "top psychology facts shorts",
        "top historical mysteries shorts",
        "top animal facts shorts educational",
        "top technology facts shorts",
    ],
    "Technology": [
        "technology facts shorts documentary",
        "computer history shorts educational",
        "AI facts shorts educational",
        "internet history shorts documentary",
        "cybersecurity facts shorts educational",
        "inventions explained shorts",
        "future technology shorts documentary",
        "computer science facts shorts",
        "robotics facts shorts educational",
        "technology history mini documentary shorts",
    ],
    "Nature & Animals": [
        "animal facts documentary shorts",
        "nature facts shorts educational",
        "wildlife mini documentary shorts",
        "ocean animal facts shorts",
        "insect facts shorts educational",
        "deep sea facts shorts documentary",
        "evolution animal facts shorts",
        "rare animals shorts educational",
        "nature mysteries shorts documentary",
        "ecosystem facts shorts",
    ],
    "Mysteries & Unexplained": [
        "historical mysteries shorts documentary",
        "science mysteries shorts educational",
        "unsolved ancient mysteries shorts",
        "archaeology mysteries shorts",
        "strange historical mysteries shorts",
        "unexplained science facts shorts",
        "lost civilizations shorts documentary",
        "mysterious discoveries shorts educational",
        "ancient artifacts mystery shorts",
        "ocean mysteries shorts documentary",
    ],
    "Space": [
        "space facts shorts educational",
        "NASA facts shorts documentary",
        "black hole facts shorts",
        "solar system shorts educational",
        "universe facts shorts documentary",
        "astronomy discoveries shorts",
        "planet facts shorts educational",
        "space mysteries shorts documentary",
        "cosmology facts shorts",
        "space history shorts",
    ],
}


class ShortsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(960, 650)
        self.configure(bg="#06142d")

        self.current_video = None
        self.player = None
        self.vlc_instance = None
        self.searching = False
        self.recent_ids = []

        self._configure_styles()
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        if vlc is not None:
            try:
                self.vlc_instance = vlc.Instance("--no-video-title-show")
                self.player = self.vlc_instance.media_player_new()
            except Exception:
                self.player = None

        self.after(500, self._check_dependencies)

    def _configure_styles(self):
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass

        bg = "#06142d"
        panel = "#0b2247"
        panel2 = "#0f2e5c"
        text = "#edf8ff"
        muted = "#a9cbe8"

        s.configure("Root.TFrame", background=bg)
        s.configure("Header.TFrame", background=panel)
        s.configure("Panel.TFrame", background=panel2)

        s.configure("Root.TLabel", background=bg, foreground=text, font=("Helvetica", 11))
        s.configure("Header.TLabel", background=panel, foreground="white", font=("Helvetica", 25, "bold"))
        s.configure("Sub.TLabel", background=panel, foreground=muted, font=("Helvetica", 11))
        s.configure("Panel.TLabel", background=panel2, foreground=text, font=("Helvetica", 11))
        s.configure("VideoTitle.TLabel", background=panel2, foreground="white", font=("Helvetica", 15, "bold"))
        s.configure("Meta.TLabel", background=panel2, foreground="#8edaff", font=("Helvetica", 10))

        s.configure(
            "Accent.TButton",
            background="#148dff",
            foreground="white",
            font=("Helvetica", 11, "bold"),
            padding=(18, 9),
            borderwidth=0,
        )
        s.map("Accent.TButton", background=[("active", "#36a4ff"), ("disabled", "#30455d")])

        s.configure(
            "Secondary.TButton",
            background="#173e72",
            foreground="white",
            font=("Helvetica", 10, "bold"),
            padding=(13, 8),
            borderwidth=0,
        )
        s.map("Secondary.TButton", background=[("active", "#25558e")])

        s.configure("TCombobox", fieldbackground="#f2f7fb", foreground="#10213c", padding=6)

    def _build_ui(self):
        root = ttk.Frame(self, style="Root.TFrame", padding=18)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root, style="Header.TFrame", padding=16)
        header.pack(fill="x", pady=(0, 12))

        ttk.Label(header, text="Documentary Shorts Generator", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Random educational YouTube Shorts • Science • History • Psychology • Technology • Nature • Mysteries",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        controls = ttk.Frame(root, style="Root.TFrame")
        controls.pack(fill="x", pady=(0, 12))

        ttk.Label(controls, text="Category:", style="Root.TLabel").pack(side="left")

        self.category_var = tk.StringVar(value="Random")
        categories = ["Random"] + list(CATEGORY_QUERIES.keys())
        self.category_box = ttk.Combobox(
            controls,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=27,
        )
        self.category_box.pack(side="left", padx=(8, 12))

        self.generate_btn = ttk.Button(
            controls,
            text="Generate & Play",
            command=self.generate_video,
            style="Accent.TButton",
        )
        self.generate_btn.pack(side="left")

        ttk.Button(
            controls,
            text="Open on YouTube",
            command=self.open_youtube,
            style="Secondary.TButton",
        ).pack(side="left", padx=(10, 0))

        ttk.Button(
            controls,
            text="Pause / Resume",
            command=self.toggle_pause,
            style="Secondary.TButton",
        ).pack(side="left", padx=(10, 0))

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(controls, textvariable=self.status_var, style="Root.TLabel").pack(side="right")

        # Video display
        self.video_frame = tk.Frame(
            root,
            bg="black",
            highlightbackground="#1c5f9b",
            highlightthickness=2,
            height=500,
        )
        self.video_frame.pack(fill="both", expand=True)
        self.video_frame.pack_propagate(False)

        self.placeholder = tk.Label(
            self.video_frame,
            text="Click “Generate & Play” to search YouTube Shorts",
            bg="black",
            fg="#8ccfff",
            font=("Helvetica", 18, "bold"),
        )
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

        # Video info
        info = ttk.Frame(root, style="Panel.TFrame", padding=12)
        info.pack(fill="x", pady=(12, 0))

        self.title_var = tk.StringVar(value="No video selected")
        self.meta_var = tk.StringVar(value="")

        ttk.Label(
            info,
            textvariable=self.title_var,
            style="VideoTitle.TLabel",
            wraplength=1060,
            justify="left",
        ).pack(anchor="w")

        ttk.Label(
            info,
            textvariable=self.meta_var,
            style="Meta.TLabel",
            wraplength=1060,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

    def _check_dependencies(self):
        missing = []
        if yt_dlp is None:
            missing.append("yt-dlp")
        if vlc is None or self.player is None:
            missing.append("python-vlc / VLC")

        if missing:
            self.status_var.set("Setup required")
            messagebox.showinfo(
                "Additional setup required",
                "This program needs:\n\n"
                "• yt-dlp: python3 -m pip install -U yt-dlp\n"
                "• python-vlc: python3 -m pip install python-vlc\n"
                "• VLC Media Player installed on your Mac\n\n"
                "The app can still open selected videos in your browser if VLC playback is unavailable."
            )

    def generate_video(self):
        if self.searching:
            return

        if yt_dlp is None:
            messagebox.showerror(
                "yt-dlp not installed",
                "Install it first:\n\npython3 -m pip install -U yt-dlp"
            )
            return

        self.searching = True
        self.generate_btn.config(state="disabled")
        self.status_var.set("Searching YouTube…")
        self.title_var.set("Finding an interesting Short…")
        self.meta_var.set("")
        self.placeholder.config(text="Searching…")
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

        category = self.category_var.get()
        thread = threading.Thread(
            target=self._search_worker,
            args=(category,),
            daemon=True,
        )
        thread.start()

    def _search_worker(self, requested_category):
        try:
            if requested_category == "Random":
                category = random.choice(list(CATEGORY_QUERIES.keys()))
            else:
                category = requested_category

            query = random.choice(CATEGORY_QUERIES[category])

            search_opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "extract_flat": "in_playlist",
                "playlistend": 25,
                "socket_timeout": 15,
            }

            with yt_dlp.YoutubeDL(search_opts) as ydl:
                result = ydl.extract_info(f"ytsearch25:{query} #shorts", download=False)

            entries = result.get("entries", []) if result else []
            candidates = []

            for entry in entries:
                if not entry:
                    continue

                vid = entry.get("id")
                if not vid or vid in self.recent_ids:
                    continue

                duration = entry.get("duration")
                # extract_flat can occasionally omit duration; allow unknowns for detailed check.
                if duration is not None and duration > MAX_SHORT_SECONDS:
                    continue

                title = (entry.get("title") or "").lower()

                # Avoid obvious non-documentary content where possible.
                blocked_words = [
                    "music video", "dance challenge", "prank", "gaming montage",
                    "fortnite", "minecraft gameplay", "reaction only"
                ]
                if any(word in title for word in blocked_words):
                    continue

                candidates.append(entry)

            if not candidates:
                # Retry with a different search query in the same category.
                query = random.choice(CATEGORY_QUERIES[category])
                with yt_dlp.YoutubeDL(search_opts) as ydl:
                    result = ydl.extract_info(f"ytsearch25:{query} educational short", download=False)
                entries = result.get("entries", []) if result else []
                candidates = [
                    e for e in entries
                    if e and e.get("id")
                    and e.get("id") not in self.recent_ids
                    and (e.get("duration") is None or e.get("duration") <= MAX_SHORT_SECONDS)
                ]

            if not candidates:
                raise RuntimeError("No suitable short videos were found. Try again.")

            random.shuffle(candidates)

            detailed = None
            for candidate in candidates[:10]:
                vid = candidate.get("id")
                url = f"https://www.youtube.com/watch?v={vid}"

                detail_opts = {
                    "quiet": True,
                    "no_warnings": True,
                    "skip_download": True,
                    "socket_timeout": 20,
                    "format": "best[ext=mp4]/best",
                }

                try:
                    with yt_dlp.YoutubeDL(detail_opts) as ydl:
                        info = ydl.extract_info(url, download=False)

                    duration = info.get("duration")
                    if duration is not None and duration > MAX_SHORT_SECONDS:
                        continue
                    if info.get("is_live"):
                        continue

                    # Ensure a playable direct URL is available.
                    direct_url = info.get("url")
                    if not direct_url:
                        formats = info.get("formats") or []
                        playable = [
                            f for f in formats
                            if f.get("url")
                            and f.get("vcodec") not in (None, "none")
                            and f.get("acodec") not in (None, "none")
                        ]
                        if playable:
                            direct_url = playable[-1].get("url")

                    if not direct_url:
                        continue

                    detailed = {
                        "id": vid,
                        "title": info.get("title") or candidate.get("title") or "YouTube Short",
                        "channel": info.get("channel") or info.get("uploader") or "",
                        "duration": duration,
                        "category": category,
                        "query": query,
                        "youtube_url": f"https://www.youtube.com/shorts/{vid}",
                        "watch_url": url,
                        "direct_url": direct_url,
                    }
                    break

                except Exception:
                    continue

            if detailed is None:
                raise RuntimeError("Found Shorts, but none could be prepared for playback.")

            self.after(0, lambda: self._load_video(detailed))

        except Exception as exc:
            self.after(0, lambda: self._search_failed(str(exc)))

    def _load_video(self, video):
        self.current_video = video

        self.recent_ids.append(video["id"])
        self.recent_ids = self.recent_ids[-20:]

        duration = video.get("duration")
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            duration_text = f"{minutes}:{seconds:02d}"
        else:
            duration_text = "short-form"

        self.title_var.set(video["title"])
        self.meta_var.set(
            f'{video["category"]}  •  {duration_text}'
            + (f'  •  {video["channel"]}' if video["channel"] else "")
        )

        self.status_var.set("Loading video…")
        self.placeholder.place_forget()

        if self.player is None or self.vlc_instance is None:
            self.status_var.set("Embedded VLC unavailable — opening YouTube")
            webbrowser.open(video["youtube_url"])
            self._finish_search()
            return

        try:
            self.update_idletasks()
            handle = self.video_frame.winfo_id()

            system = platform.system()
            if system == "Darwin":
                # macOS: VLC accepts the native NSView handle.
                self.player.set_nsobject(handle)
            elif system == "Windows":
                self.player.set_hwnd(handle)
            else:
                self.player.set_xwindow(handle)

            media = self.vlc_instance.media_new(video["direct_url"])
            media.add_option(":network-caching=1200")
            self.player.set_media(media)

            result = self.player.play()
            self.status_var.set("Playing")
            self.after(1800, self._verify_playback)

        except Exception as exc:
            self.status_var.set("Embedded playback failed")
            self.placeholder.config(text="Embedded playback failed.\nUse “Open on YouTube”.")
            self.placeholder.place(relx=0.5, rely=0.5, anchor="center")
            messagebox.showwarning(
                "Playback issue",
                f"VLC could not start embedded playback:\n\n{exc}\n\n"
                "You can use the Open on YouTube button."
            )

        self._finish_search()

    def _verify_playback(self):
        if self.player is None or not self.current_video:
            return
        try:
            state = self.player.get_state()
            bad_states = {vlc.State.Error, vlc.State.Ended}
            if state in bad_states:
                self.status_var.set("VLC stream unavailable — use Open on YouTube")
        except Exception:
            pass

    def _search_failed(self, message):
        self.placeholder.config(text="No suitable Short found.\nClick Generate & Play to try again.")
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")
        self.title_var.set("Search did not return a playable Short")
        self.meta_var.set("")
        self.status_var.set("Ready to retry")
        self._finish_search()
        messagebox.showwarning("Search result", message)

    def _finish_search(self):
        self.searching = False
        self.generate_btn.config(state="normal")

    def open_youtube(self):
        if not self.current_video:
            messagebox.showinfo("No video", "Generate a video first.")
            return
        webbrowser.open(self.current_video["youtube_url"])

    def toggle_pause(self):
        if self.player is None:
            return
        try:
            if self.player.is_playing():
                self.player.pause()
                self.status_var.set("Paused")
            else:
                self.player.play()
                self.status_var.set("Playing")
        except Exception:
            pass

    def on_close(self):
        try:
            if self.player is not None:
                self.player.stop()
        except Exception:
            pass
        self.destroy()


if __name__ == "__main__":
    ShortsApp().mainloop()
