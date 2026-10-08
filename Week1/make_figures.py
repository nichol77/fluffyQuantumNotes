import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, Wedge

plt.rcParams.update({"font.size": 11, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False,
                     "savefig.dpi": 160, "savefig.bbox": "tight"})
BLUE, RED, GREY, GOLD = "#3b3b98", "#c0392b", "#7f8c8d", "#f1c40f"
OUT = "fig/"
import os; os.makedirs(OUT, exist_ok=True)

h, c, k = 6.62607015e-34, 2.99792458e8, 1.380649e-23

# 1. Superposition: constructive and destructive
t = np.linspace(0, 3, 600)
fig, ax = plt.subplots(3, 2, figsize=(8, 4.2), sharex=True, sharey=True)
for col, (phi, title) in enumerate([(0, "In phase: constructive"), (np.pi, "Antiphase: destructive")]):
    y1 = np.sin(2*np.pi*t); y2 = np.sin(2*np.pi*t + phi)
    for r, (y, lab) in enumerate([(y1, "wave 1"), (y2, "wave 2"), (y1+y2, "sum")]):
        a = ax[r, col]
        a.plot(t, y, color=BLUE if r < 2 else RED, lw=2)
        a.axhline(0, color=GREY, lw=0.6)
        a.set_ylim(-2.3, 2.3); a.set_yticks([]); a.set_xticks([])
        if col == 0: a.set_ylabel(lab)
    ax[0, col].set_title(title)
ax[2, 0].set_xlabel("time"); ax[2, 1].set_xlabel("time")
fig.savefig(OUT + "superposition.png"); plt.close(fig)

# 2. Single vs double slit pattern (Fraunhofer)
x = np.linspace(-1, 1, 2000)
a_w, d, lam, L = 20e-6, 100e-6, 600e-9, 1.0  # slit width, separation
theta = x*0.08
beta = np.pi*a_w*np.sin(theta)/lam
env = np.sinc(beta/np.pi)**2
dbl = env*np.cos(np.pi*d*np.sin(theta)/lam)**2
fig, ax = plt.subplots(2, 1, figsize=(7, 4), sharex=True)
for a, y, lab in [(ax[0], env, "One slit"), (ax[1], dbl, "Two slits")]:
    a.plot(theta*1e3, y, color=RED, lw=1.6)
    a.fill_between(theta*1e3, y, color=RED, alpha=0.15)
    a.set_ylabel("intensity"); a.set_yticks([]); a.set_title(lab, loc="left", fontsize=11)
ax[1].plot(theta*1e3, env, "--", color=GREY, lw=1, label="single-slit envelope")
ax[1].legend(frameon=False, fontsize=9)
ax[1].set_xlabel("angle from centre (mrad)")
fig.savefig(OUT + "slits.png"); plt.close(fig)

# 3. Amplitude vs intensity
t = np.linspace(0, 3, 600); E = np.sin(2*np.pi*t)
fig, ax = plt.subplots(1, 2, figsize=(8, 2.8))
ax[0].plot(t, E, color=BLUE, lw=2); ax[0].axhline(0, color=GREY, lw=.6)
ax[0].annotate("", xy=(0.25, 1), xytext=(0.25, 0), arrowprops=dict(arrowstyle="<->"))
ax[0].text(0.32, 0.4, "amplitude $E_0$", fontsize=9, bbox=dict(fc="white", ec="none")); ax[0].set_title("Electric field $E(t)$")
ax[0].set_xlabel("time"); ax[0].set_yticks([-1, 0, 1]); ax[0].set_yticklabels(["$-E_0$", "0", "$E_0$"])
ax[1].plot(t, E**2, color=RED, lw=2); ax[1].axhline(0.5, ls="--", color=GREY)
ax[1].text(3.05, 0.45, "time average\n$= E_0^2/2$", fontsize=9)
ax[1].set_title("$E(t)^2$ (proportional to intensity)"); ax[1].set_xlabel("time"); ax[1].set_yticks([0, 1]); ax[1].set_yticklabels(["0", "$E_0^2$"])
fig.savefig(OUT + "amplitude_intensity.png"); plt.close(fig)

# 4. Mach-Zehnder schematic
def mz(fname, top_label, right_label, block=False, photon=False):
    fig, ax = plt.subplots(figsize=(6.4, 4.4)); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-2.2, 6.2); ax.set_ylim(-1.2, 5.2)
    kw = dict(color="black", lw=1.6)
    ax.plot([-2, 0], [0, 0], color="black", lw=4)  # incident
    ax.text(-2.1, 0.2, "single photon" if photon else "incident light", fontsize=10)

    ax.plot([0, 4], [0, 0], **kw); ax.plot([0, 0], [0, 4], **kw)
    ax.plot([4, 4], [0, 4], **kw)
    if not block:
        ax.plot([0, 4], [4, 4], **kw); 
    else:
        ax.plot([2.3, 0], [4, 4], **kw); #y-end or y-start,  #x-end, x-start

    for (px, py, col, lab, dx, dy) in [(0, 0, BLUE, "BS1", 0.45, -0.6), (4, 4, BLUE, "BS2", 0.45, -0.6),
                                       (0, 4, "black", "mirror", -1.3, 0.25), (4, 0, "black", "mirror", 0.35, -0.4)]:
        ax.plot([px-.45, px+.45], [py-.45, py+.45], color=col, lw=3.5)
        ax.text(px+dx, py+dy, lab, fontsize=10)
    ax.annotate("", xy=(4, 5), xytext=(4, 4.05), arrowprops=dict(arrowstyle="->", ls="--", lw=1.5))
    ax.annotate("", xy=(5.1, 4), xytext=(4.05, 4), arrowprops=dict(arrowstyle="->", ls="--", lw=1.5))
    ax.add_patch(Rectangle((3.6, 4.95), 0.8, 0.25, color=GOLD)); ax.text(3.2, 5.3, "D$_{top}$: " + top_label, fontsize=10)
    ax.add_patch(Rectangle((5.1, 3.6), 0.25, 0.8, color=GOLD)); ax.text(5.45, 3.9, "D$_{right}$:\n" + right_label, fontsize=10)
    ax.text(0.6, 4.15, "upper path", fontsize=9, color=GREY); ax.text(1.4, -0.35, "lower path", fontsize=9, color=GREY)
    if block:
        ax.add_patch(Rectangle((2.3, 3.7), 0.6, 0.6, color="#2e86c1")); ax.text(2.15, 3.35, "blocker", fontsize=9)
    fig.savefig(OUT + fname); plt.close(fig)
mz("mz.png", "0 W", "10 W")
mz("mz_blocked.png", "2.5 W", "2.5 W", block=True)
mz("mz_photon.png", "never clicks", "always clicks", photon=True)

# 5. Blackbody spectra + Wien
lam = np.linspace(50e-9, 3000e-9, 2000)
def planck(l, T, hh=h):  # spectral exitance, W m^-3
    return 2*np.pi*hh*c**2/(l**5*(np.expm1(hh*c/(l*k*T))))
fig, ax = plt.subplots(figsize=(7, 4))
cols = ["#8e44ad", "#2c3e50", "#27ae60", "#d4ac0d", "#c0392b"]
for T, col in zip([5500, 5000, 4500, 4000, 3500], cols):
    I = planck(lam, T); ax.plot(lam*1e9, I/1e13, color=col, lw=2, label=f"T = {T} K")
    lm = 2.898e-3/T; ax.plot(lm*1e9, planck(lm, T)/1e13, "o", color=col, ms=4)
ax.axvspan(380, 750, color="#f9e79f", alpha=0.35, lw=0); ax.text(400, 7.8, "visible", fontsize=9)
ax.set_xlabel("wavelength λ (nm)"); ax.set_ylabel(r"$I(\lambda,T)$  ($10^{13}$ W m$^{-3}$)")
ax.legend(frameon=False); ax.set_xlim(0, 3000)
fig.savefig(OUT + "blackbody.png"); plt.close(fig)

# 6. Rayleigh-Jeans vs Planck
T = 5000
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(lam*1e9, planck(lam, T)/1e13, color=RED, lw=2.2, label="Planck (matches experiment)")
rj = 2*np.pi*c*k*T/lam**4
ax.plot(lam*1e9, rj/1e13, color=BLUE, lw=2, ls="--", label="Rayleigh–Jeans (classical)")
ax.set_ylim(0, 6); ax.set_xlim(0, 3000)
ax.annotate("diverges as λ → 0:\n'ultraviolet catastrophe'", xy=(1230, 5.8), xytext=(1450, 5.3),
            arrowprops=dict(arrowstyle="->"), fontsize=10)
ax.set_xlabel("wavelength λ (nm)"); ax.set_ylabel(r"$I(\lambda,T)$  ($10^{13}$ W m$^{-3}$)")
ax.set_title("T = 5000 K", loc="left"); ax.legend(frameon=False, loc="center right")
fig.savefig(OUT + "rayleigh_jeans.png"); plt.close(fig)

# 7. Planck with different h
fig, ax = plt.subplots(figsize=(7, 4))
for hh, ls in [(6.0e-34, ":"), (7.2e-34, "--")]:
    ax.plot(lam*1e9, planck(lam, T, hh)/1e13, color=RED, ls=ls, lw=2, label=f"h = {hh/1e-34:.1f}×10$^{{-34}}$ J s")
ax.plot(lam*1e9, planck(lam, T)/1e13, color="black", lw=2.2, label="h = 6.63×10$^{-34}$ J s (fits data)")
ax.set_xlim(0, 3000); ax.set_xlabel("wavelength λ (nm)"); ax.set_ylabel(r"$I(\lambda,T)$  ($10^{13}$ W m$^{-3}$)")
ax.set_title("T = 5000 K: fitting Planck's law to data fixes h", loc="left", fontsize=11); ax.legend(frameon=False, fontsize=9)
fig.savefig(OUT + "planck_h.png"); plt.close(fig)

# 8. Photoelectric: Kmax vs f
eV = 1.602176634e-19
fig, ax = plt.subplots(figsize=(6.5, 3.8))
for phi, name, col in [(2.3, "sodium (φ ≈ 2.3 eV)", BLUE), (4.3, "zinc (φ ≈ 4.3 eV)", RED)]:
    f0 = phi*eV/h; f = np.linspace(f0, 2e15, 100)
    ax.plot(f/1e14, (h*f/eV - phi), color=col, lw=2, label=name)
    ax.plot([0, f0/1e14], [0, 0], color=col, lw=2, ls=":")
    ax.plot(f0/1e14, 0, "o", color=col); ax.text(f0/1e14, 0.25, "$f_0$", color=col, ha="center")
ax.set_xlabel("frequency f ($10^{14}$ Hz)"); ax.set_ylabel("$K_{max}$ (eV)")
ax.set_xlim(0, 20); ax.set_ylim(-0.3, 6)
ax.text(13.5, 0.4, "slope = h/e\nfor every metal", fontsize=10)
ax.legend(frameon=False, loc="upper left")
fig.savefig(OUT + "photoelectric.png"); plt.close(fig)

# 9. Photoelectric apparatus + energy level
fig, ax = plt.subplots(1, 2, figsize=(8, 3.2), gridspec_kw=dict(width_ratios=[1.2, 1]))
a = ax[0]; a.axis("off"); a.set_xlim(0, 10); a.set_ylim(0, 7); a.set_aspect("equal")
a.add_patch(Rectangle((2, 2.2), 0.4, 3.5, color="#2e86c1")); a.text(1.2, 1.5, "metal plate", fontsize=9)
a.add_patch(Rectangle((7, 2.2), 0.3, 3.5, color="black")); a.text(6.5, 6.1, "collector", fontsize=9)
for yy in [5.9, 5.3]:
    a.annotate("", xy=(2.45, yy-1.1), xytext=(0.6, yy+0.6), arrowprops=dict(arrowstyle="->", color=GOLD, lw=2))
a.text(0.1, 4.2, "light", fontsize=10)
for yy in [3.2, 4.0]:
    a.annotate("", xy=(6.9, yy), xytext=(2.6, yy), arrowprops=dict(arrowstyle="->", color=GREY))
a.text(3.8, 4.3, "e$^-$", fontsize=11)
a.plot([2.2, 2.2, 4.3], [2.2, 0.8, 0.8], "k"); a.plot([7.15, 7.15], [0.8, 2.2], "k")
a.plot([4.3, 4.3], [0.4, 1.2], "k", lw=2); a.plot([4.6, 4.6], [0.6, 1.0], "k", lw=4); a.plot([4.3,5.0],[0.8,0.8],color="white",lw=0)
a.plot([4.6,5.0],[0.8,0.8],"k"); a.add_patch(Circle((5.6, 0.8), 0.35, fill=False)); a.text(5.45, 0.65, "A", fontsize=9); a.plot([5.95,7.15],[0.8,0.8],"k")
b = ax[1]; b.set_xlim(0, 4); b.set_ylim(-3.2, 2.2); b.set_xticks([]); b.set_ylabel("energy (eV)")
b.axhline(0, color="black", ls="--", lw=1); b.text(0.3, 0.12, "free (escaped)", fontsize=9)
b.plot([0.3, 3.7], [-2.3, -2.3], color="#2e86c1", lw=4); b.text(0.3, -2.85, "most weakly bound electrons", fontsize=9)
b.annotate("", xy=(1.0, 0), xytext=(1.0, -2.3), arrowprops=dict(arrowstyle="<->"))
b.text(1.1, -1.3, "work function φ", fontsize=9)
b.annotate("", xy=(2.1, 1.5), xytext=(2.1, -2.3), arrowprops=dict(arrowstyle="->", color=GOLD, lw=2.5))
b.text(2.2, 0.6, "hf", fontsize=10); b.annotate("", xy=(3.2, 1.5), xytext=(3.2, 0), arrowprops=dict(arrowstyle="<->"))
b.text(3.3, 0.6, "$K_{max}$", fontsize=10)
fig.savefig(OUT + "photoelectric_setup.png"); plt.close(fig)

# 10. Compton geometry and shift vs angle
lc = h/(9.1093837e-31*c)
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4), gridspec_kw=dict(width_ratios=[1.1, 1]))
a = ax[0]; a.axis("off"); a.set_xlim(-4, 4); a.set_ylim(-2.5, 2.5); a.set_aspect("equal")
a.annotate("", xy=(-0.25, 0), xytext=(-3.8, 0), arrowprops=dict(arrowstyle="->", lw=1.8, color=BLUE))
a.text(-3.8, 0.25, "incident photon\nλ, p = h/λ", fontsize=9)
a.add_patch(Circle((0, 0), 0.22, color=GOLD, ec="black")); a.text(-0.2, -0.6, "e$^-$", fontsize=10)
th = np.deg2rad(40)
a.annotate("", xy=(3.2*np.cos(th), 3.2*np.sin(th)), xytext=(0.2*np.cos(th), 0.2*np.sin(th)),
           arrowprops=dict(arrowstyle="->", lw=1.8, color=RED))
a.text(1.9, 2.1, "scattered photon\nλ′ > λ", fontsize=9)
a.annotate("", xy=(1.5, -1.9), xytext=(0.15, -0.2), arrowprops=dict(arrowstyle="->", lw=1.5, color=GREY))
a.text(1.6, -2.2, "recoiling electron", fontsize=9)
a.plot([0, 3], [0, 0], color=GREY, ls=":"); a.add_patch(Wedge((0, 0), 1.0, 0, 40, fill=False))
a.text(1.05, 0.25, "θ", fontsize=11)
b = ax[1]; th = np.linspace(0, 180, 200)
b.plot(th, lc*(1-np.cos(np.deg2rad(th)))*1e12, color=RED, lw=2)
b.set_xlabel("scattering angle θ (degrees)"); b.set_ylabel("Δλ = λ′ − λ (pm)"); b.set_xticks([0, 45, 90, 135, 180])
b.axhline(2*lc*1e12, color=GREY, ls=":", lw=1); b.text(5, 2*lc*1e12+0.1, "max = 2h/m$_e$c ≈ 4.85 pm", fontsize=9)
fig.savefig(OUT + "compton.png"); plt.close(fig)

# 11. Single-photon build-up of double-slit pattern
rng = np.random.default_rng(3)
xs = np.linspace(-1, 1, 4000); p = np.sinc(xs*2.2)**2*np.cos(np.pi*xs*9)**2; p /= p.sum()
fig, ax = plt.subplots(1, 4, figsize=(9, 2.6))
for a, N in zip(ax, [20, 200, 2000, 50000]):
    xx = rng.choice(xs, N, p=p) + rng.normal(0, 0.004, N); yy = rng.uniform(0, 1, N)
    a.set_facecolor("black"); a.scatter(xx, yy, s=0.6 if N > 2000 else 3, color="white", alpha=0.6 if N > 2000 else 1, lw=0)
    a.set_xticks([]); a.set_yticks([]); a.set_xlim(-0.6, 0.6); a.set_title(f"{N:,} photons", fontsize=10)
fig.savefig(OUT + "buildup.png"); plt.close(fig)

# 12. Beam splitter photon statistics
fig, ax = plt.subplots(figsize=(6.5, 2.6))
N = 40; r = rng.integers(0, 2, N)
ax.eventplot([np.where(r == 0)[0], np.where(r == 1)[0]], lineoffsets=[1, 0], colors=[BLUE, RED], linelengths=0.7)
ax.set_yticks([0, 1]); ax.set_yticklabels(["reflected\ndetector", "transmitted\ndetector"])
ax.set_xlabel("photon number (one photon sent at a time)")
ax.set_title(f"Each photon clicks exactly one detector; here {int((r==0).sum())} vs {int((r==1).sum())} of {N}", fontsize=10, loc="left")
fig.savefig(OUT + "bs_clicks.png"); plt.close(fig)

# Cover
fig = plt.figure(figsize=(6, 9)); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.set_facecolor("#10123a"); fig.patch.set_facecolor("#10123a")
xx = np.linspace(0, 1, 800)
for i in range(18):
    ax.plot(xx, 0.42 + 0.02*i/18 + 0.12*np.exp(-((xx-0.55)/0.18)**2)*np.sin(2*np.pi*(xx*9 + i/18)), color="white", alpha=0.25, lw=0.8)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.text(0.08, 0.86, "PHAS0004 · Week 1", color="#f1c40f", fontsize=16)
ax.text(0.08, 0.76, "Waves as Particles:", color="white", fontsize=26, weight="bold")
ax.text(0.08, 0.70, "The Photon", color="white", fontsize=26, weight="bold")
ax.text(0.08, 0.14, "Draft lecture notes\nbased on the Week 1 slides", color="#cfd3ff", fontsize=13)
fig.savefig(OUT + "cover.png", dpi=150, facecolor=fig.get_facecolor(), bbox_inches=None); plt.close(fig)
print("done")
