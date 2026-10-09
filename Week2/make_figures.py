"""Figures for the Week 2 notes (Atoms and their structure). Run from this folder: python make_figures.py"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

plt.rcParams.update({"font.size": 11, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False,
                     "savefig.dpi": 160, "savefig.bbox": "tight"})
BLUE, RED, GREY, GOLD = "#3b3b98", "#c0392b", "#7f8c8d", "#f1c40f"
OUT = "fig/"
os.makedirs(OUT, exist_ok=True)

h, c, e, me, eps0 = 6.62607015e-34, 2.99792458e8, 1.602176634e-19, 9.1093837e-31, 8.8541878e-12
R_H = 1.0967758e7


def wl_to_rgb(wl):
    """Approximate colour of a visible wavelength (nm)."""
    if wl < 380 or wl > 750:
        return (0.5, 0.5, 0.5)
    if wl < 440:   r, g, b = -(wl - 440) / 60, 0, 1
    elif wl < 490: r, g, b = 0, (wl - 440) / 50, 1
    elif wl < 510: r, g, b = 0, 1, -(wl - 510) / 20
    elif wl < 580: r, g, b = (wl - 510) / 70, 1, 0
    elif wl < 645: r, g, b = 1, -(wl - 645) / 65, 0
    else:          r, g, b = 1, 0, 0
    f = 1.0
    if wl < 420: f = 0.4 + 0.6 * (wl - 380) / 40
    elif wl > 700: f = 0.4 + 0.6 * (750 - wl) / 50
    return (r * f, g * f, b * f)


# 1. Alpha-particle trajectories: plum pudding vs nuclear atom
def trajectories(ax, R1, title, bs=None):
    D = 0.30  # head-on distance of closest approach (sets the force scale)
    K = 1.0  # kinetic energy units; force constant k = D*K for F = kqQ/r^2 with KE = 1
    for b in (bs if bs is not None else np.linspace(-4.5, 4.5, 19)):
        x, y = -12.0, b
        vx, vy = np.sqrt(2 * K), 0.0
        xs, ys = [x], [y]
        dt = 0.001
        for _ in range(20000):
            r = np.hypot(x, y)
            if r > R1:
                F = D * K / r**2
            else:
                F = D * K * r / R1**3
            ax_, ay_ = F * x / r, F * y / r
            vx += ax_ * dt; vy += ay_ * dt
            x += vx * dt; y += vy * dt
            xs.append(x); ys.append(y)
            if abs(x) > 12.5 or abs(y) > 12.5:
                break
        xs=np.array(xs)
        ys=np.array(ys)
        cond=(np.abs(xs)<12)*(np.abs(ys)<9)
        xs=xs[cond]
        ys=ys[cond]
        ax.plot(xs, ys, color=BLUE, lw=0.9)
        # arrow over the final segment
        ax.annotate(
            "",
            xy=(xs[-1], ys[-1]),          # arrow tip
            xytext=(xs[-2], ys[-2]),      # arrow tail
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=2, shrinkA=0.1, shrinkB=0.1),
        )
    ax.set_xlim(-12, 12); ax.set_ylim(-9, 9); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=11)


fig, axs = plt.subplots(1, 2, figsize=(9, 3.8))
axs[0].add_patch(Circle((0, 0), 6, color="#f5b7b1", alpha=0.6))
for (px, py) in [(-3, -3), (2, 3), (-1, -3), (3, -1), (0, 0.8), (-4, -1), (1.5, -4)]:
    axs[0].add_patch(Circle((px, py), 0.3, color="#2e86c1"))
trajectories(axs[0], 6.0, "Plum pudding: positive charge spread out")
axs[1].add_patch(Circle((0, 0), 0.35, color=RED, zorder=5))
axs[1].add_patch(Circle((0, 0), 6, color="#f5b7b1", alpha=0.1))
for theta in np.linspace(0,2*np.pi,7):
    px=np.sin(theta)*4
    py=np.cos(theta)*4
    axs[1].add_patch(Circle((px, py), 0.3, color="#2e86c1"))
trajectories(axs[1], 0.1, "Rutherford: charge concentrated in a nucleus",bs=np.concatenate([np.linspace(-4.5, 4.5, 19), [-0.15,0,0.15]]))
fig.text(0.5, 0.02, "α particles enter from the left", ha="center", fontsize=9, color=GREY)
fig.savefig(OUT + "rutherford.png"); plt.close(fig)

# 2. Emission and absorption spectra
H = [656.3, 486.1, 434.0, 410.2]
Hg = [404.7, 435.8, 546.1, 577.0, 579.1]
Ne = [585.2, 588.2, 594.5, 597.6, 603.0, 607.4, 609.6, 614.3, 616.4, 621.7, 626.6, 630.5,
      633.4, 638.3, 640.2, 650.7, 659.9, 667.8, 671.7, 692.9, 703.2]
fig, axs = plt.subplots(4, 1, figsize=(8, 3.8), sharex=True)
for ax, lines, name in zip(axs[:3], [H, Hg, Ne], ["hydrogen", "mercury", "neon"]):
    ax.set_facecolor("black")
    for wl in lines:
        ax.axvline(wl, color=wl_to_rgb(wl), lw=2.2)
    ax.set_yticks([]); ax.set_ylabel(name, rotation=0, ha="right", va="center")
ax = axs[3]
wls = np.linspace(380, 750, 800)
for i in range(len(wls) - 1):
    ax.axvspan(wls[i], wls[i + 1], color=wl_to_rgb(wls[i]), lw=0)
for wl in H:
    ax.axvline(wl, color="black", lw=2.2)
ax.set_yticks([]); ax.set_ylabel("hydrogen\n(absorption)", rotation=0, ha="right", va="center")
ax.set_xlim(380, 720); ax.set_xlabel("wavelength (nm)")
for a in axs:
    for s in a.spines.values(): s.set_visible(False)
fig.savefig(OUT + "spectra.png"); plt.close(fig)

# 3. Hydrogen energy-level diagram with series
E = lambda n: -13.6057 / n**2
fig, ax = plt.subplots(figsize=(7.5, 5.2))
for n in range(1, 8):
    ax.plot([0, 10], [E(n), E(n)], color="black", lw=1.2)
    if n <= 3:
        ax.text(10.15, E(n), f"n = {n}   {E(n):.2f} eV", va="center", fontsize=9)
ax.text(10.15, -0.5, "n = 4, 5, 6, …", va="center", fontsize=9)
ax.plot([0, 10], [0, 0], color=GREY, ls="--", lw=1); ax.text(10.15, 0.25, "n = ∞   0 eV (ionised)", fontsize=9, color=GREY)
series = [(1, "Lyman (UV)", 0.4, "#8e44ad"), (2, "Balmer (visible)", 4.0, None), (3, "Paschen (IR)", 7.4, "#a04000")]
for m, name, x0, col in series:
    for i, n in enumerate(range(m + 1, m + 6)):
        x = x0 + 0.38 * i
        cc = col if col else wl_to_rgb(1e9 / (R_H * (1 / m**2 - 1 / n**2)))
        ax.annotate("", xy=(x, E(m)), xytext=(x, E(n)), arrowprops=dict(arrowstyle="-|>", color=cc, lw=1.6, shrinkA=0, shrinkB=0))
    ax.text(x0 - 0.1, E(m) - 0.6, name, fontsize=9.5, va="top")
ax.set_xlim(0, 13.5); ax.set_ylim(-14.6, 1.0); ax.set_xticks([])
ax.set_ylabel("energy (eV)")
ax.spines["bottom"].set_visible(False)
fig.savefig(OUT + "energy_levels.png"); plt.close(fig)

# 4. Balmer series lines with series limit
fig, ax = plt.subplots(figsize=(8, 1.9))
ax.set_facecolor("black")
for n in range(3, 40):
    wl = 1e9 / (R_H * (1 / 4 - 1 / n**2))
    ax.axvline(wl, color=wl_to_rgb(wl) if wl > 380 else (0.55, 0.45, 0.85), lw=1.6 if n < 10 else 0.6)
    if n <= 6:
        ax.text(wl, 1.08, f"n={n}\n{wl:.0f}", ha="center", fontsize=8, transform=ax.get_xaxis_transform())
lim = 1e9 / (R_H / 4)
ax.axvline(lim, color="white", ls=":", lw=1)
ax.text(lim, 1.08, "limit\n365", ha="center", fontsize=8, transform=ax.get_xaxis_transform())
ax.set_xlim(350, 680); ax.set_yticks([]); ax.set_xlabel("wavelength (nm)")
fig.savefig(OUT + "balmer.png"); plt.close(fig)

# 5. Bohr orbits to scale (r ∝ n^2)
fig, ax = plt.subplots(figsize=(5, 5))
for n in range(1, 5):
    ax.add_patch(Circle((0, 0), n**2, fill=False, ls="--", color=GREY))
    ax.text(n**2 * np.cos(0.6), n**2 * np.sin(0.6) + 0.3, f"n = {n}", fontsize=9)
ax.add_patch(Circle((0, 0), 0.25, color=RED))
ax.annotate("", xy=(0, -1), xytext=(0, 0), arrowprops=dict(arrowstyle="->"))
ax.text(0.15, -0.9, "$a_0$", fontsize=10)
ax.set_xlim(-17, 17); ax.set_ylim(-17, 17); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Bohr orbits drawn to scale: $r_n = a_0 n^2$", fontsize=11)
fig.savefig(OUT + "bohr_orbits.png"); plt.close(fig)

# 6. de Broglie standing waves on Bohr orbits
fig, axs = plt.subplots(1, 3, figsize=(9, 3.2))
th = np.linspace(0, 2 * np.pi, 800)
for ax, k, title, ok in zip(axs, [3, 4, 3.5], ["n = 3: three wavelengths", "n = 4: four wavelengths", "3.5 wavelengths: no fit"], [True, True, False]):
    ax.plot(np.cos(th), np.sin(th), color=GREY, ls="--", lw=1)
    rr = 1 + 0.15 * np.cos(k * th)
    ax.plot(rr * np.cos(th), rr * np.sin(th), color=BLUE if ok else RED, lw=2)
    ax.add_patch(Circle((0, 0), 0.08, color=RED))
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, fontsize=10)
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
fig.savefig(OUT + "debroglie_orbits.png"); plt.close(fig)

# 7. de Broglie wavelengths across scales
objs = [("electron, 54 eV\n(Davisson–Germer)", me, np.sqrt(2 * 54 * e / me)),
        ("electron at 100 m s$^{-1}$", me, 100.0),
        ("phthalocyanine\nat 150 m s$^{-1}$", 8.5e-25, 150.0),
        ("thermal neutron\n(2200 m s$^{-1}$)", 1.675e-27, 2200.0),
        ("tennis ball\n(serve, 65 m s$^{-1}$)", 0.06, 64.7)]
fig, ax = plt.subplots(figsize=(7.5, 3.6))
names = [o[0] for o in objs]
lams = [h / (m * v) for _, m, v in objs]
ax.barh(range(len(objs)), lams, color=[BLUE, BLUE, "#27ae60", BLUE, RED])
ax.set_xscale("log"); ax.set_yticks(range(len(objs))); ax.set_yticklabels(names, fontsize=9)
ax.invert_yaxis(); ax.set_xlim(1e-36, 1e0)
for i, l in enumerate(lams):
    ax.text(l * 3, i, f"{l:.1e} m", va="center", fontsize=9)
ax.axvline(2.5e-10, color=GREY, ls=":"); ax.text(3e-10, 4.45, "atom\nspacing", fontsize=8, color=GREY)
ax.set_xlabel("de Broglie wavelength λ = h/p (m)")
fig.savefig(OUT + "debroglie_scales.png"); plt.close(fig)

# 8. Davisson–Germer geometry and diffraction condition
fig, ax = plt.subplots(figsize=(6.2, 3.6)); ax.set_aspect("equal"); ax.axis("off")
for i in range(-5, 6):
    ax.add_patch(Circle((i * 1.0, 0), 0.12, color=GREY))
ax.plot([-5.5, 5.5], [0, 0], color=GREY, lw=0.5)
for x0 in [-1, 1]:
    ax.annotate("", xy=(x0, 0.15), xytext=(x0, 4), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))
    ang = np.deg2rad(50)
    ax.annotate("", xy=(x0 + 3.6 * np.sin(ang), 3.6 * np.cos(ang)), xytext=(x0, 0.15),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))
ax.plot([-1, 1], [-0.45, -0.45], color="black"); ax.text(-0.15, -0.9, "d", fontsize=11)
ax.text(-4.6, 3.4, "incident electrons\n(54 eV)", fontsize=9, color=BLUE)
ax.text(3.9, 3.0, "strong reflection\nat θ ≈ 50°", fontsize=9, color=RED)
ax.set_xlim(-5.5, 6.5); ax.set_ylim(-1.2, 4.3)
ax.set_title("Nickel surface atoms act like a diffraction grating: d sin θ = λ", fontsize=10)
fig.savefig(OUT + "davisson_germer.png"); plt.close(fig)

# 9. Single-molecule build-up of an interference pattern
rng = np.random.default_rng(11)
xs = np.linspace(-1, 1, 4000); p = np.sinc(xs * 1.6)**2 * np.cos(np.pi * xs * 7)**2; p /= p.sum()
fig, ax = plt.subplots(1, 4, figsize=(9, 2.6))
for a, N in zip(ax, [30, 300, 3000, 30000]):
    xx = rng.choice(xs, N, p=p) + rng.normal(0, 0.006, N); yy = rng.uniform(0, 1, N)
    a.set_facecolor("#1a0500")
    a.scatter(xx, yy, s=0.8 if N > 3000 else 3, color="#ff9a5a", alpha=0.6 if N > 3000 else 1, lw=0)
    a.set_xticks([]); a.set_yticks([]); a.set_xlim(-0.7, 0.7); a.set_title(f"{N:,} molecules", fontsize=10)
fig.savefig(OUT + "molecule_buildup.png"); plt.close(fig)

# 10. Classical collapse of the planetary atom
fig, ax = plt.subplots(figsize=(4, 4))
t = np.linspace(0, 1, 3000); r = (1 - t)**(1 / 3); phi = 70 * (1 - (1 - t)**0.5)
ax.plot(r * np.cos(phi), r * np.sin(phi), color=BLUE, lw=0.8)
ax.add_patch(Circle((0, 0), 0.05, color=RED, zorder=5))
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Classical prediction: the electron\nradiates and spirals in (~10$^{-11}$ s)", fontsize=10)
fig.savefig(OUT + "spiral.png"); plt.close(fig)

# Cover
fig = plt.figure(figsize=(6, 9)); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
fig.patch.set_facecolor("#10123a"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
for n in range(1, 5):
    ax.add_patch(Circle((0.5, 0.42), 0.035 * n**1.3, fill=False, ec="white", alpha=0.35, lw=0.9))
ax.add_patch(Circle((0.5, 0.42), 0.012, color="#ff6b5a"))
for i, n in enumerate(range(3, 7)):
    wl = 1e9 / (R_H * (1 / 4 - 1 / n**2))
    ax.add_patch(Rectangle((0.08 + (wl - 380) / 320 * 0.84, 0.17), 0.006, 0.07, color=wl_to_rgb(wl)))
ax.text(0.08, 0.86, "PHAS0004 · Week 2", color="#f1c40f", fontsize=16)
ax.text(0.08, 0.76, "Atoms and their", color="white", fontsize=26, weight="bold")
ax.text(0.08, 0.70, "Structure", color="white", fontsize=26, weight="bold")
ax.text(0.08, 0.06, "Draft lecture notes\nbased on the Week 2 slides", color="#cfd3ff", fontsize=13)
fig.savefig(OUT + "cover.png", dpi=150, facecolor=fig.get_facecolor(), bbox_inches=None); plt.close(fig)
print("done")
