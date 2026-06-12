"""
axiom_nebula.py
AXIOM — AI Ethics & Responsible AI Oracle
Theme: NEBULA  |  Deep navy · Electric cyan · Violet · Neural constellation BG
Run with: python axiom_nebula.py
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from chatbot_engine import FAQChatbot

# ── Nebula Palette ─────────────────────────────────────────────────────────────
BG_VOID      = "#060B18"   # deepest space
BG_PANEL     = "#0D1B35"   # main panel
BG_CARD      = "#122350"   # card surface
BG_GLASS     = "#1A3A7A"   # slightly lighter glass

CYAN         = "#00B4D8"   # electric cyan — primary accent
VIOLET       = "#7B5EEA"   # violet — secondary accent
VIOLET_PALE  = "#C8A8FF"   # soft violet / headings
BLUE_MID     = "#4A9EF5"   # mid-blue
CYAN_GLOW    = "#00D4FF"   # glow cyan

# ── NEW vivid accent palette ───────────────────────────────────────────────────
MAGENTA      = "#FF2D78"   # hot pink / magenta
MAGENTA_PALE = "#FF80AB"   # soft pink
AMBER        = "#FFB830"   # golden amber
AMBER_PALE   = "#FFD97D"   # pale gold
EMERALD      = "#00E5A0"   # neon emerald
EMERALD_DIM  = "#007A55"   # dim emerald border
ORANGE       = "#FF6B35"   # vivid orange
ORANGE_PALE  = "#FFAA80"   # soft orange
TEAL         = "#00F5D4"   # bright teal

TEXT_PRIMARY = "#E8F4FF"   # soft white
TEXT_MUTED   = "#4A6FA0"   # muted blue
TEXT_DIM     = "#1A3A7A"   # very dim

USER_BG      = "#0D1820"   # slightly orange-tinted dark
BOT_BG       = "#060E1C"   # slightly teal-tinted dark

# ── Fonts ──────────────────────────────────────────────────────────────────────
FONT_DISPLAY  = ("Courier New", 18, "bold")
FONT_HEADING  = ("Courier New", 12, "bold")
FONT_BODY     = ("Consolas",    11)
FONT_SMALL    = ("Consolas",     9)
FONT_BADGE    = ("Courier New",  8, "bold")
FONT_INPUT    = ("Consolas",    12)
FONT_MONO     = ("Courier New",  9)


# ── Neural Constellation Background ───────────────────────────────────────────
class NebulaCanvas(tk.Canvas):
    """
    Drifting neural nodes connected by fading cyan/violet synapses.
    Pulse signals travel along edges — electric thought firing through a nebula.
    """
    NODE_COUNT   = 38
    CONNECT_DIST = 200
    PULSE_RATE   = 0.013

    def __init__(self, master, **kw):
        super().__init__(master, bg=BG_VOID, highlightthickness=0, **kw)
        self.nodes  = []
        self.pulses = []
        self._init_nodes()
        self._animate()

    def _init_nodes(self):
        W, H = 1400, 900
        colors = [CYAN, VIOLET, VIOLET_PALE, BLUE_MID, CYAN_GLOW, "#9B7EFF",
                  MAGENTA, AMBER, EMERALD, TEAL, ORANGE_PALE, MAGENTA_PALE]
        for _ in range(self.NODE_COUNT):
            self.nodes.append({
                'x':     random.uniform(0, W),
                'y':     random.uniform(0, H),
                'vx':    random.uniform(-0.28, 0.28),
                'vy':    random.uniform(-0.28, 0.28),
                'r':     random.uniform(1.4, 3.2),
                'phase': random.uniform(0, math.tau),
                'color': random.choice(colors),
            })

    @staticmethod
    def _hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def _fade_color(hex_color, alpha):
        """Blend toward BG_VOID (#060B18)."""
        bg = (6, 11, 24)
        r, g, b = NebulaCanvas._hex_to_rgb(hex_color)
        r2 = int(bg[0] + (r - bg[0]) * alpha)
        g2 = int(bg[1] + (g - bg[1]) * alpha)
        b2 = int(bg[2] + (b - bg[2]) * alpha)
        return f'#{r2:02x}{g2:02x}{b2:02x}'

    def _animate(self):
        self.delete("neo")
        W = self.winfo_width()  or 1400
        H = self.winfo_height() or 900
        t_global = time.time()
        nodes = self.nodes

        # move
        for n in nodes:
            n['x'] += n['vx']; n['y'] += n['vy']
            if n['x'] < -20:  n['x'] = W + 20
            if n['x'] > W+20: n['x'] = -20
            if n['y'] < -20:  n['y'] = H + 20
            if n['y'] > H+20: n['y'] = -20

        # star dust
        for i in range(0, 80, 4):
            sx = (i * 173.1) % W
            sy = (i * 97.7)  % H
            self.create_oval(sx-0.6, sy-0.6, sx+0.6, sy+0.6,
                             fill="#C8A8FF", outline="", tags="neo")

        # edges
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                dx = nodes[i]['x'] - nodes[j]['x']
                dy = nodes[i]['y'] - nodes[j]['y']
                dist = math.hypot(dx, dy)
                if dist < self.CONNECT_DIST:
                    alpha = (1 - dist / self.CONNECT_DIST) ** 1.6 * 0.50
                    ec = self._fade_color(TEXT_DIM, alpha)
                    self.create_line(nodes[i]['x'], nodes[i]['y'],
                                     nodes[j]['x'], nodes[j]['y'],
                                     fill=ec, width=1, tags="neo")
                    if random.random() < self.PULSE_RATE * (1 - dist/self.CONNECT_DIST):
                        self.pulses.append({
                            'i': i, 'j': j, 't': 0.0,
                            'speed': random.uniform(0.018, 0.040),
                            'color': random.choice([CYAN, VIOLET_PALE, "#FFFFFF", CYAN_GLOW,
                                                     MAGENTA_PALE, AMBER_PALE, EMERALD, TEAL]),
                        })

        # pulses
        alive = []
        for p in self.pulses:
            p['t'] += p['speed']
            if p['t'] >= 1.0: continue
            ni, nj = nodes[p['i']], nodes[p['j']]
            px = ni['x'] + (nj['x'] - ni['x']) * p['t']
            py = ni['y'] + (nj['y'] - ni['y']) * p['t']
            tail = max(0.0, p['t'] - 0.18)
            tx = ni['x'] + (nj['x'] - ni['x']) * tail
            ty = ni['y'] + (nj['y'] - ni['y']) * tail
            self.create_line(tx, ty, px, py, fill=p['color'], width=2, tags="neo")
            r2 = 3
            self.create_oval(px-r2, py-r2, px+r2, py+r2,
                             fill=p['color'], outline="", tags="neo")
            alive.append(p)
        self.pulses = alive

        # nodes
        for n in nodes:
            phase = n['phase'] + t_global * 1.4
            pulse_scale = 0.7 + 0.3 * math.sin(phase)
            r = n['r'] * pulse_scale
            glow_r  = r * 3.2
            glow_col = self._fade_color(n['color'], 0.22)
            self.create_oval(n['x']-glow_r, n['y']-glow_r,
                             n['x']+glow_r, n['y']+glow_r,
                             fill=glow_col, outline="", tags="neo")
            self.create_oval(n['x']-r, n['y']-r,
                             n['x']+r, n['y']+r,
                             fill=n['color'], outline="", tags="neo")

        self.after(33, self._animate)


# ── Typing indicator ───────────────────────────────────────────────────────────
class TypingDots(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, bg=BOT_BG, **kw)
        self.dots = []
        for _ in range(3):
            d = tk.Label(self, text="◆", font=("Consolas", 9),
                         bg=BOT_BG, fg=TEXT_MUTED)
            d.pack(side=tk.LEFT, padx=2)
            self.dots.append(d)
        self.phase = 0
        self._blink()

    def _blink(self):
        colors = [TEXT_MUTED, TEXT_MUTED, TEXT_MUTED]
        colors[self.phase % 3] = MAGENTA
        for i, d in enumerate(self.dots):
            d.config(fg=colors[i])
        self.phase += 1
        self._job = self.after(350, self._blink)

    def destroy(self):
        if hasattr(self, '_job'): self.after_cancel(self._job)
        super().destroy()


# ── Separator ──────────────────────────────────────────────────────────────────
class OrnateLineSeparator(tk.Canvas):
    def __init__(self, master, **kw):
        kw.setdefault('height', 18)
        kw.setdefault('bg', BG_PANEL)
        kw.setdefault('highlightthickness', 0)
        super().__init__(master, **kw)
        self.bind("<Configure>", self._draw)

    def _draw(self, e=None):
        self.delete("all")
        w = self.winfo_width() or 600
        cy = 9
        self.create_line(0, cy, w, cy, fill=TEXT_DIM, width=1)
        for xpos in [w // 4, w // 2, 3 * w // 4]:
            r = 4
            self.create_polygon(xpos, cy-r, xpos+r, cy,
                                xpos, cy+r, xpos-r, cy,
                                fill=VIOLET, outline=CYAN, width=1)


class NeonLine(tk.Canvas):
    def __init__(self, master, color=TEXT_DIM, **kw):
        kw.setdefault('height', 2)
        kw.setdefault('bg', BG_PANEL)
        kw.setdefault('highlightthickness', 0)
        super().__init__(master, **kw)
        self.color = color
        self.bind("<Configure>", self._draw)

    def _draw(self, e=None):
        self.delete("all")
        w = self.winfo_width()
        self.create_line(0, 1, w, 1, fill=self.color, width=1)


# ── Glitch title ───────────────────────────────────────────────────────────────
class GlitchLabel(tk.Label):
    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789✦◆◈█▓░"
    def __init__(self, master, text, **kw):
        super().__init__(master, **kw)
        self._target   = text
        self._revealed = 0
        self._scramble_step()

    def _scramble_step(self):
        if self._revealed >= len(self._target):
            self.config(text=self._target); return
        scrambled = (
            self._target[:self._revealed]
            + random.choice(self.CHARS)
            + "".join(random.choice(self.CHARS)
                      for _ in range(min(4, len(self._target)-self._revealed-1)))
        )
        self.config(text=scrambled[:len(self._target)])
        self._revealed += 1
        self.after(55, self._scramble_step)


# ── Confidence bar ─────────────────────────────────────────────────────────────
class ConfBar(tk.Canvas):
    def __init__(self, master, value=0.0, **kw):
        kw.setdefault('height', 6)
        kw.setdefault('bg', BG_CARD)
        kw.setdefault('highlightthickness', 0)
        super().__init__(master, **kw)
        self._value  = 0
        self._target = value
        self._animate_to(value)
        self.bind("<Configure>", self._draw)

    def _animate_to(self, target):
        self._target = target; self._tick()

    def _tick(self):
        if abs(self._value - self._target) < 0.01:
            self._value = self._target; self._draw(); return
        self._value += (self._target - self._value) * 0.15
        self._draw()
        self.after(16, self._tick)

    def _draw(self, e=None):
        self.delete("all")
        w = self.winfo_width() or 200
        h = self.winfo_height() or 6
        self.create_rectangle(0, 0, w, h, fill=TEXT_DIM, outline="")
        fw = int(w * self._value)
        if fw > 0:
            color = EMERALD if self._value > 0.7 else (AMBER if self._value > 0.4 else MAGENTA)
            self.create_rectangle(0, 0, fw, h, fill=color, outline="")
            gx = max(0, fw - 8)
            self.create_rectangle(gx, 0, fw, h, fill=TEAL, outline="")


# ── Scrollable chat area ───────────────────────────────────────────────────────
class ChatArea(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, bg=BG_PANEL, **kw)
        self.canvas = tk.Canvas(self, bg=BG_PANEL, highlightthickness=0, bd=0)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.canvas.yview,
                                bg=BG_CARD, troughcolor=BG_PANEL,
                                activebackground=CYAN, width=6)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.inner = tk.Frame(self.canvas, bg=BG_PANEL)
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._on_frame_config)
        self.canvas.bind("<Configure>", self._on_canvas_config)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_frame_config(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_config(self, e):
        self.canvas.itemconfig(self.window_id, width=e.width)

    def _on_mousewheel(self, e):
        self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")

    def scroll_bottom(self):
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)


# ── Main App ───────────────────────────────────────────────────────────────────
class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ AXIOM — Nebula | AI Ethics Oracle")
        self.geometry("1120x740")
        self.minsize(820, 580)
        self.configure(bg=BG_VOID)
        self.bot = FAQChatbot()
        self.msg_count = 0
        self._build_ui()
        self._show_welcome()

    def _build_ui(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sb = tk.Frame(self, bg=BG_PANEL, width=250)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)

        # Logo canvas — neural constellation backdrop
        logo_canvas = NebulaCanvas(sb, height=140)
        logo_canvas.pack(fill=tk.X)

        tk.Label(logo_canvas, text="✦", font=("Courier New", 30),
                 fg=MAGENTA, bg=BG_VOID).place(relx=0.5, rely=0.18, anchor="center")
        GlitchLabel(logo_canvas, text="AXIOM",
                    font=("Courier New", 18, "bold"),
                    fg=AMBER, bg=BG_VOID).place(relx=0.5, rely=0.58, anchor="center")
        tk.Label(logo_canvas, text="AI Ethics & Responsible AI Oracle",
                 font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_VOID).place(
                     relx=0.5, rely=0.82, anchor="center")

        OrnateLineSeparator(sb).pack(fill=tk.X, padx=12, pady=4)

        # Status badge
        status = tk.Frame(sb, bg=BG_CARD,
                          highlightthickness=1,
                          highlightbackground=TEXT_DIM,
                          padx=14, pady=8)
        status.pack(fill=tk.X, padx=14, pady=10)

        hdr_row = tk.Frame(status, bg=BG_CARD)
        hdr_row.pack()
        tk.Label(hdr_row, text="— ✦ —", font=FONT_MONO,
                 fg=TEXT_DIM, bg=BG_CARD).pack(side=tk.LEFT)
        dot = tk.Label(hdr_row, text="  ORACLE ONLINE  ", font=FONT_BADGE,
                       fg=TEAL, bg=BG_CARD)
        dot.pack(side=tk.LEFT)
        tk.Label(hdr_row, text="— ✦ —", font=FONT_MONO,
                 fg=TEXT_DIM, bg=BG_CARD).pack(side=tk.LEFT)
        self._pulse_dot(dot)

        # Stats
        stats = tk.Frame(sb, bg=BG_PANEL, pady=6)
        stats.pack(fill=tk.X, padx=14)
        for label, value, color in [
            ("KNOWLEDGE BASE", "25 AI Ethics FAQs loaded",      EMERALD),
            ("ENGINE",         "TF-IDF + Cosine Similarity",   AMBER),
            ("NLP PIPELINE",   "NLTK · Lemmatize · Bigrams",   MAGENTA_PALE),
        ]:
            tk.Label(stats, text=label, font=FONT_BADGE,
                     fg=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w", pady=(6,0))
            tk.Label(stats, text=value, font=FONT_SMALL,
                     fg=color, bg=BG_PANEL).pack(anchor="w", pady=(1,0))

        OrnateLineSeparator(sb).pack(fill=tk.X, padx=12, pady=6)

        # Quick topics
        tk.Label(sb, text="◈  QUICK TOPICS",
                 font=FONT_BADGE, fg=TEXT_MUTED, bg=BG_PANEL).pack(
            anchor="w", padx=14, pady=(4,4))

        topics = [
            ("✦", "What is AI bias?",                   CYAN),
            ("◈", "What is explainable AI?",             EMERALD),
            ("◆", "What are deepfakes?",                 VIOLET_PALE),
            ("✦", "What is the EU AI Act?",              MAGENTA_PALE),
            ("◈", "What is the alignment problem?",      AMBER),
            ("◆", "AI and privacy surveillance",         TEAL),
            ("✦", "What is responsible AI?",             ORANGE_PALE),
            ("◈", "AI and misinformation",               VIOLET),
        ]
        for icon, q, icon_color in topics:
            btn = tk.Label(sb, text=f"  {icon}  {q}",
                           font=FONT_SMALL, fg=icon_color,
                           bg=BG_PANEL, anchor="w", cursor="hand2",
                           padx=10, pady=5)
            btn.pack(fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn, c=icon_color: b.config(fg=TEXT_PRIMARY, bg=BG_GLASS))
            btn.bind("<Leave>", lambda e, b=btn, c=icon_color: b.config(fg=c, bg=BG_PANEL))
            btn.bind("<Button-1>", lambda e, q=q: self._quick_send(q))

        self.msg_counter = tk.Label(sb, text="0 messages",
                                    font=FONT_BADGE, fg=TEXT_DIM, bg=BG_PANEL)
        self.msg_counter.pack(side=tk.BOTTOM, pady=12)

    # ── Main area ──────────────────────────────────────────────────────────────
    def _build_main(self):
        main = tk.Frame(self, bg=BG_PANEL)
        main.grid(row=0, column=1, sticky="nsew")
        main.rowconfigure(2, weight=1)
        main.columnconfigure(0, weight=1)

        header = tk.Frame(main, bg=BG_PANEL, height=58, pady=10)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        tk.Label(header, text="◈  AI ETHICS & RESPONSIBLE AI — KNOWLEDGE INTERFACE",
                 font=FONT_HEADING, fg=AMBER, bg=BG_PANEL).pack(side=tk.LEFT, padx=18)

        self.conf_label = tk.Label(header, text="CONFIDENCE: —",
                                   font=FONT_BADGE, fg=TEXT_MUTED, bg=BG_PANEL)
        self.conf_label.pack(side=tk.RIGHT, padx=18)

        OrnateLineSeparator(main).grid(row=1, column=0, sticky="ew")

        self.chat = ChatArea(main)
        self.chat.grid(row=2, column=0, sticky="nsew")

        NeonLine(main, color=TEXT_DIM).grid(row=3, column=0, sticky="ew")

        conf_row = tk.Frame(main, bg=BG_PANEL, height=14, pady=2)
        conf_row.grid(row=4, column=0, sticky="ew", padx=18)
        conf_row.grid_propagate(False)
        tk.Label(conf_row, text="MATCH  ", font=FONT_BADGE,
                 fg=TEXT_MUTED, bg=BG_PANEL).pack(side=tk.LEFT)
        self.conf_bar = ConfBar(conf_row, value=0)
        self.conf_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=4)

        input_row = tk.Frame(main, bg=BG_PANEL, pady=14)
        input_row.grid(row=5, column=0, sticky="ew", padx=18)
        input_row.columnconfigure(0, weight=1)

        input_wrap = tk.Frame(input_row, bg=BG_CARD,
                              highlightthickness=1,
                              highlightbackground=TEXT_DIM)
        input_wrap.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        input_wrap.columnconfigure(0, weight=1)

        self.entry = tk.Entry(input_wrap, font=FONT_INPUT,
                              bg=BG_CARD, fg=TEXT_PRIMARY,
                              insertbackground=CYAN,
                              relief="flat", bd=8)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_send)

        self._ph = True
        self.entry.insert(0, "Ask anything about AI Ethics & Responsible AI…")
        self.entry.config(fg=TEXT_MUTED)
        self.entry.bind("<FocusIn>",  lambda e: self._clear_ph(e, input_wrap))
        self.entry.bind("<FocusOut>", lambda e: self._add_ph(e, input_wrap))

        send_btn = tk.Button(input_row, text="SEND  ▶",
                             font=FONT_BADGE,
                             bg=MAGENTA, fg=TEXT_PRIMARY,
                             activebackground=MAGENTA_PALE,
                             activeforeground=BG_VOID,
                             relief="flat", bd=0, padx=16, pady=10,
                             cursor="hand2", command=self._on_send)
        send_btn.grid(row=0, column=1)

        clear_btn = tk.Button(input_row, text="⟳",
                              font=("Consolas", 14),
                              bg=BG_CARD, fg=TEXT_MUTED,
                              activebackground=BG_GLASS,
                              relief="flat", bd=0, padx=10,
                              cursor="hand2", command=self._clear_chat)
        clear_btn.grid(row=0, column=2, padx=(4, 0))

    # ── Welcome ────────────────────────────────────────────────────────────────
    def _show_welcome(self):
        welcome = (
            "AXIOM online. Neural constellation active.\n\n"
            "I am your knowledge interface for AI Ethics & Responsible AI — "
            "covering bias, fairness, explainability, deepfakes, AI governance, privacy, "
            "alignment, human rights, and more.\n\n"
            "Select a topic from the sidebar, or transmit your query below."
        )
        self.after(200, lambda: self._add_bot_bubble(welcome, conf=None, delay=True))

    # ── Placeholder helpers ────────────────────────────────────────────────────
    def _clear_ph(self, e, wrap):
        wrap.config(highlightbackground=AMBER)
        if self._ph:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=TEXT_PRIMARY)
            self._ph = False

    def _add_ph(self, e, wrap):
        wrap.config(highlightbackground=TEXT_DIM)
        if not self.entry.get():
            self.entry.insert(0, "Ask anything about AI Ethics & Responsible AI…")
            self.entry.config(fg=TEXT_MUTED)
            self._ph = True

    # ── Status pulse ───────────────────────────────────────────────────────────
    def _pulse_dot(self, dot, toggle=True):
        dot.config(fg=MAGENTA if toggle else AMBER)
        self.after(900, lambda: self._pulse_dot(dot, not toggle))

    # ── Send logic ─────────────────────────────────────────────────────────────
    def _on_send(self, e=None):
        text = self.entry.get().strip()
        if not text or self._ph: return
        self.entry.delete(0, tk.END)
        self._ph = False
        self._add_user_bubble(text)
        threading.Thread(target=self._respond, args=(text,), daemon=True).start()

    def _quick_send(self, q):
        if self._ph:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=TEXT_PRIMARY)
            self._ph = False
        self.entry.delete(0, tk.END)
        self.entry.insert(0, q)
        self._on_send()

    def _respond(self, text):
        typing = self._add_typing()
        time.sleep(0.7 + random.uniform(0, 0.4))
        answer, confidence = self.bot.get_answer(text)
        self.after(0, lambda: self._finish_response(typing, answer, confidence))

    def _finish_response(self, typing, answer, confidence):
        typing.destroy()
        self._add_bot_bubble(answer, conf=confidence, delay=True)
        self.conf_bar._animate_to(confidence if confidence else 0)
        pct   = f"{int((confidence or 0)*100)}%"
        color = EMERALD if (confidence or 0) > 0.6 else (AMBER if (confidence or 0) > 0.3 else MAGENTA)
        self.conf_label.config(text=f"CONFIDENCE: {pct}", fg=color)

    # ── Bubble factories ───────────────────────────────────────────────────────
    def _add_user_bubble(self, text):
        self.msg_count += 1
        self.msg_counter.config(text=f"{self.msg_count} messages")
        row = tk.Frame(self.chat.inner, bg=BG_PANEL, pady=6)
        row.pack(fill=tk.X, padx=18)
        ts = time.strftime("%H:%M")
        tk.Label(row, text=f"YOU  {ts}", font=FONT_BADGE,
                 fg=ORANGE_PALE, bg=BG_PANEL).pack(anchor="e", padx=4)
        bubble = tk.Frame(row, bg=USER_BG,
                          highlightthickness=1,
                          highlightbackground=ORANGE)
        bubble.pack(anchor="e", padx=4)
        tk.Label(bubble, text=text, font=FONT_BODY,
                 fg=TEXT_PRIMARY, bg=USER_BG,
                 wraplength=520, justify="left",
                 padx=14, pady=10).pack()
        self.chat.scroll_bottom()
        self._fade_in(row)

    def _add_bot_bubble(self, text, conf=None, delay=False):
        self.msg_count += 1
        self.msg_counter.config(text=f"{self.msg_count} messages")
        row = tk.Frame(self.chat.inner, bg=BG_PANEL, pady=6)
        row.pack(fill=tk.X, padx=18)
        ts = time.strftime("%H:%M")

        hdr = tk.Frame(row, bg=BG_PANEL)
        hdr.pack(anchor="w", padx=4)
        tk.Label(hdr, text="— ✦ —", font=FONT_MONO,
                 fg=VIOLET_PALE, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(hdr, text="  AXIOM ", font=FONT_BADGE,
                 fg=EMERALD, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(hdr, text=f"  {ts}  ", font=FONT_BADGE,
                 fg=TEAL, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(hdr, text="— ✦ —", font=FONT_MONO,
                 fg=VIOLET_PALE, bg=BG_PANEL).pack(side=tk.LEFT)

        bubble = tk.Frame(row, bg=BOT_BG,
                          highlightthickness=1,
                          highlightbackground=EMERALD_DIM)
        bubble.pack(anchor="w", padx=4, fill=tk.X)

        tk.Frame(bubble, bg=EMERALD, height=2).pack(fill=tk.X)

        self._text_label = tk.Label(bubble, text="", font=FONT_BODY,
                                    fg=TEXT_PRIMARY, bg=BOT_BG,
                                    wraplength=580, justify="left",
                                    padx=14, pady=10)
        self._text_label.pack(anchor="w", fill=tk.X)

        if conf is not None:
            topic = self._guess_topic(text)
            tk.Label(bubble,
                     text=f"— on: {topic}   ( confidence: {int(conf*100)}% )",
                     font=FONT_MONO, fg=AMBER_PALE, bg=BOT_BG,
                     anchor="e", padx=14, pady=4).pack(anchor="e", fill=tk.X)

        if delay:
            self._typewrite(self._text_label, text, 0)
        else:
            self._text_label.config(text=text)

        self.chat.scroll_bottom()
        self._fade_in(row)

    def _guess_topic(self, answer_text):
        keywords = {
            "AI ethics":            "AI Ethics",
            "bias":                 "Algorithmic Bias",
            "fairness":             "AI Fairness",
            "explainab":            "Explainable AI (XAI)",
            "black box":            "Black Box Problem",
            "accountab":            "AI Accountability",
            "transparent":          "AI Transparency",
            "deepfake":             "Deepfakes",
            "copyright":            "AI & Copyright",
            "GDPR":                 "GDPR & AI",
            "EU AI Act":            "EU AI Act",
            "safety":               "AI Safety",
            "alignment":            "AI Alignment",
            "surveillance":         "Privacy & Surveillance",
            "differential privacy": "Differential Privacy",
            "federated":            "Federated Learning",
            "human rights":         "AI & Human Rights",
            "model card":           "Model Cards",
            "carbon":               "AI Carbon Footprint",
            "employment":           "AI & Employment",
            "responsible":          "Responsible AI",
            "misinformation":       "AI Misinformation",
            "existential":          "Existential Risk",
            "governance":           "AI Governance",
            "digital divide":       "AI Equity",
        }
        for kw, topic in keywords.items():
            if kw.lower() in answer_text.lower():
                return topic
        return "General AI"

    def _add_typing(self):
        row = tk.Frame(self.chat.inner, bg=BG_PANEL, pady=6)
        row.pack(fill=tk.X, padx=18)
        hdr2 = tk.Frame(row, bg=BG_PANEL)
        hdr2.pack(anchor="w", padx=4)
        tk.Label(hdr2, text="— ✦ —", font=FONT_MONO,
                 fg=VIOLET_PALE, bg=BG_PANEL).pack(side=tk.LEFT)
        tk.Label(hdr2, text="  AXIOM", font=FONT_BADGE,
                 fg=EMERALD, bg=BG_PANEL).pack(side=tk.LEFT)
        dots = TypingDots(row)
        dots.pack(anchor="w", padx=18, pady=6)
        self.chat.scroll_bottom()
        orig_destroy = row.destroy
        def destroy_all():
            dots.destroy(); orig_destroy()
        row.destroy = destroy_all
        return row

    def _typewrite(self, label, text, idx):
        if idx <= len(text):
            label.config(text=text[:idx])
            self.chat.scroll_bottom()
            speed = 10 if idx < len(text)*0.3 else 7
            self.after(speed, lambda: self._typewrite(label, text, idx+1))

    def _fade_in(self, widget):
        def step(n):
            if n > 8: return
            self.chat.scroll_bottom()
            self.after(30, lambda: step(n+1))
        step(0)

    def _clear_chat(self):
        for w in self.chat.inner.winfo_children(): w.destroy()
        self.msg_count = 0
        self.msg_counter.config(text="0 messages")
        self.conf_bar._animate_to(0)
        self.conf_label.config(text="CONFIDENCE: —", fg=TEXT_MUTED)
        self._show_welcome()


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
