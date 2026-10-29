"""Bir regresyon probleminde YSA meta parametrelerinin performansa etkisinin incelenmesi.

Ağ yapısı : p -> [Dense(n, aktivasyon)] x L -> Dense(1, lineer)
Giriş     : -2 <= p <= 2
Hedef     : y = 1 + sin(pi * p / 4)
Kriterler : MSE / RMSE, R2, süre (sn)

Her deney 300 epoch eğitilir. Rastgele çekirdek (seed) okul numarasının son 2 hanesidir (--seed).

Deney düzeni (--mode):
    ofat  : her tabloda yalnızca incelenen meta parametre değişir, diğerleri Tablo 1'in
            başlangıç ayarında (ReLU, lr 0.1, SGD, normal, 1 katman, 2 nöron) sabit kalır.
    chain : her tabloda önceki tablolarda bulunan en iyi değerler sabit tutulur.

Kullanım:
    uv run main.py                 # tüm deneyler (300 epoch)
    uv run main.py --epochs 20     # hızlı deneme
"""

import argparse
import os
import time

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import keras
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SEED = 29  # --seed ile değiştirilir (okul numarasının son 2 hanesi)
INIT_SCALE = 0.05  # normal: stddev, uniform: [-scale, scale]  (--init-scale)
SNAPSHOT_EPOCHS = (1, 2, 5, 10, 25, 50, 100, 150, 200, 250, 275, 300)

# Başlangıç (baseline) ayarları: Tablo 1'deki sabit parametreler
BASELINE = dict(act="relu", lr=0.1, opt="sgd", init="normal", layers=1, neurons=2)

# (anahtar, tablo başlığı, [(etiket, değer), ...])
EXPERIMENTS = [
    (
        "act",
        "Aktivasyon fonksiyonlarının değişimi",
        [
            ("Lineer", "linear"),
            ("Sigmoid", "sigmoid"),
            ("Hiperbolik Tanjant", "tanh"),
            ("ReLU", "relu"),
            ("LeakyReLU", "leaky_relu"),
            ("ELU", "elu"),
            ("SiLU", "silu"),
        ],
    ),
    ("lr", "Öğrenme oranının değişimi", [("0.1", 0.1), ("0.01", 0.01), ("0.001", 0.001)]),
    (
        "opt",
        "Öğrenme oranı ayar yönteminin değişimi",
        [("SGD", "sgd"), ("RMSProp", "rmsprop"), ("Adam", "adam")],
    ),
    (
        "init",
        "Ağırlık başlangıç değerlerinin olasılık dağılımının değişimi",
        [("Normal", "normal"), ("Uniform", "uniform")],
    ),
    (
        "layers",
        "Gizli katman sayısının değişimi",
        [(str(n), n) for n in (1, 2, 5, 10, 20)],
    ),
    (
        "neurons",
        "Gizli katmandaki nöron sayısının değişimi",
        [(str(n), n) for n in (2, 5, 10, 20, 50)],
    ),
]

PARAM_NAMES = {
    "act": "Aktivasyon",
    "lr": "Öğrenme Oranı",
    "opt": "Ayar Yöntemi",
    "init": "Olasılık dağılımı",
    "layers": "Gizli katman sayısı",
    "neurons": "Gizli katmandaki nöron sayısı",
}


def make_data(n_points=21):
    p = np.linspace(-2.0, 2.0, n_points, dtype="float32").reshape(-1, 1)
    y = (1.0 + np.sin(np.pi * p / 4.0)).astype("float32")
    return p, y


def make_initializer(kind):
    if kind == "normal":
        return keras.initializers.RandomNormal(mean=0.0, stddev=INIT_SCALE, seed=SEED)
    return keras.initializers.RandomUniform(minval=-INIT_SCALE, maxval=INIT_SCALE, seed=SEED)


def make_optimizer(name, lr):
    return {
        "sgd": keras.optimizers.SGD,
        "rmsprop": keras.optimizers.RMSprop,
        "adam": keras.optimizers.Adam,
    }[name](learning_rate=lr)


def build_model(cfg):
    keras.utils.set_random_seed(SEED)
    layers = [keras.Input(shape=(1,))]
    for _ in range(cfg["layers"]):
        layers.append(
            keras.layers.Dense(
                cfg["neurons"],
                activation=cfg["act"],
                kernel_initializer=make_initializer(cfg["init"]),
                bias_initializer="zeros",
            )
        )
    layers.append(
        keras.layers.Dense(1, activation="linear", kernel_initializer=make_initializer(cfg["init"]))
    )
    model = keras.Sequential(layers)
    model.compile(optimizer=make_optimizer(cfg["opt"], cfg["lr"]), loss="mse")
    return model


class EpochMetrics(keras.callbacks.Callback):
    """Her epoch sonunda tüm veri üzerinde MSE ve R2 hesaplar, bazı epochlarda çıkışı saklar."""

    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.ss_tot = float(np.mean((y - y.mean()) ** 2))
        self.mse, self.r2 = [], []
        self.snaps = {}

    def on_epoch_end(self, epoch, logs=None):
        out = self.model(self.x, training=False).numpy()
        mse = float(np.mean((self.y - out) ** 2))
        self.mse.append(mse)
        self.r2.append(1.0 - mse / self.ss_tot)
        if epoch + 1 in SNAPSHOT_EPOCHS:
            self.snaps[epoch + 1] = out


def run_experiment(cfg, x, y, epochs, batch_size):
    model = build_model(cfg)
    cb = EpochMetrics(x, y)
    t0 = time.perf_counter()
    model.fit(x, y, epochs=epochs, batch_size=batch_size, shuffle=True, verbose=0, callbacks=[cb])
    elapsed = time.perf_counter() - t0
    out = model(x, training=False).numpy()
    mse = float(np.mean((y - out) ** 2))
    r2 = 1.0 - mse / cb.ss_tot
    return dict(
        mse=mse,
        rmse=float(np.sqrt(mse)),
        r2=r2,
        time=elapsed,
        mse_hist=np.array(cb.mse),
        r2_hist=np.array(cb.r2),
        out=out,
        snaps=cb.snaps,
    )


def score(res):
    """Seçim ölçütü: en düşük MSE (NaN/inf en kötü sayılır)."""
    return res["mse"] if np.isfinite(res["mse"]) else np.inf


def plot_best(path, title, label, res, x, y):
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    epochs = np.arange(1, len(res["mse_hist"]) + 1)

    axes[0].semilogy(epochs, res["mse_hist"], color="tab:blue")
    axes[0].set(title="Epoch / MSE (log)", xlabel="Epoch", ylabel="MSE")
    axes[0].grid(True, which="both", alpha=0.3)

    axes[1].plot(x, y, "k-", label="Hedef")
    axes[1].plot(x, res["out"], "r--", label="Ağ çıkışı")
    axes[1].set(title="Hedef - Çıkış", xlabel="p", ylabel="y")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(epochs, res["r2_hist"], color="tab:green")
    axes[2].set(title="Epoch / R²", xlabel="Epoch", ylabel="R²")
    axes[2].grid(True, alpha=0.3)

    fig.suptitle(f"{title} - en iyi: {label}  (MSE={res['mse']:.4g}, R²={res['r2']:.4f})")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_snapshots(path, title, label, res, x, y):
    """Epoch / Hedef-Çıkış: ağ çıkışının seçili epochlardaki hali."""
    epochs = sorted(res["snaps"])
    cols = 4
    nrows = int(np.ceil(len(epochs) / cols))
    fig, axes = plt.subplots(nrows, cols, figsize=(16, 3.4 * nrows), sharex=True, sharey=True)
    axes = np.atleast_1d(axes).reshape(-1)
    for ax, ep in zip(axes, epochs):
        ax.plot(x, y, "k-", lw=2, label="Hedef")
        ax.plot(x, res["snaps"][ep], "r-", lw=1.8, label="Ağ çıkışı")
        ax.set_title(f"Epoch {ep}  (MSE={res['mse_hist'][ep - 1]:.4g})", fontsize=10)
        ax.grid(True, alpha=0.3)
    for ax in axes[len(epochs):]:
        ax.set_visible(False)
    axes[0].legend(fontsize=8)
    fig.suptitle(f"{title} - Epoch / Hedef-Çıkış (en iyi: {label})")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_comparison(path, title, rows, x, y):
    """Tablodaki tüm değerleri aynı eksenlerde üst üste çizer."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    axes[1].plot(x, y, "k-", lw=2.5, label="Hedef")
    for label, res in rows:
        epochs = np.arange(1, len(res["mse_hist"]) + 1)
        axes[0].semilogy(epochs, res["mse_hist"], label=label)
        axes[1].plot(x, res["out"], "--", label=label)
        axes[2].plot(epochs, res["r2_hist"], label=label)

    axes[0].set(title="Epoch / MSE (log)", xlabel="Epoch", ylabel="MSE")
    axes[1].set(title="Hedef - Çıkış", xlabel="p", ylabel="y")
    axes[2].set(title="Epoch / R²", xlabel="Epoch", ylabel="R²", ylim=(-0.1, 1.02))
    for ax in axes:
        ax.grid(True, which="both", alpha=0.3)
    axes[1].legend(fontsize=8)
    fig.suptitle(f"{title} - tüm değerlerin karşılaştırması")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def fmt_value(key, value):
    return {"relu": "ReLU", "sgd": "SGD", "rmsprop": "RMSProp", "adam": "Adam"}.get(value, str(value))


def fmt_cfg(cfg, vary):
    parts = [f"{PARAM_NAMES[k]}: {fmt_value(k, v)}" for k, v in cfg.items() if k != vary]
    return ", ".join(parts)


def markdown_table(idx, title, cfg, vary, rows, best_label):
    lines = [f"### Tablo {idx}. {title}", "", f"({fmt_cfg(cfg, vary)})", ""]
    lines.append("| | MSE | R2 | Süre (sn) |")
    lines.append("|---|---|---|---|")
    for label, res in rows:
        mse_text = np.format_float_positional(res["mse"], precision=6, unique=False, fractional=False, trim="-")
        cells = [label, mse_text, f"{res['r2']:.6f}", f"{res['time']:.2f}"]
        if label == best_label:
            cells = [f"**{c}**" for c in cells]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    global SEED, INIT_SCALE
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--batch-size", type=int, default=0, help="0 = tam batch (epoch başına 1 güncelleme)")
    ap.add_argument("--points", type=int, default=21, help="[-2, 2] aralığındaki örnek sayısı")
    ap.add_argument("--seed", type=int, default=SEED, help="okul numarasının son 2 hanesi")
    ap.add_argument("--init-scale", type=float, default=INIT_SCALE, help="başlangıç ağırlık ölçeği")
    ap.add_argument("--mode", choices=("ofat", "chain"), default="chain")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    SEED, INIT_SCALE = args.seed, args.init_scale

    os.makedirs(args.out, exist_ok=True)
    x, y = make_data(args.points)
    batch_size = args.batch_size or len(x)
    cfg = dict(BASELINE)
    if args.mode == "ofat":
        note = "Her tabloda yalnızca ilgili meta parametre değiştirilmiş, diğerleri Tablo 1'in ayarında (ReLU) sabit tutulmuştur."
    else:
        note = "Her tabloda önceki tablolarda bulunan en iyi değerler sabit tutulmuştur."
    md = [
        "# Bir Regresyon Probleminde Ağ Meta Parametrelerinin Ağ Performansına Etkisinin İncelenmesi",
        "",
        f"Epoch: {args.epochs}, batch size: {batch_size}, örnek sayısı: {args.points}, seed: {SEED}, "
        f"başlangıç ağırlık ölçeği: {INIT_SCALE}. En iyi (en düşük MSE) değer kalın yazılmıştır. {note}",
        "",
    ]
    best_overall = []

    for idx, (key, title, values) in enumerate(EXPERIMENTS, start=1):
        print(f"\n=== Tablo {idx}: {title} ===")
        rows = []
        for label, value in values:
            run_cfg = dict(cfg, **{key: value})
            res = run_experiment(run_cfg, x, y, args.epochs, batch_size)
            rows.append((label, res))
            print(
                f"  {label:<20} MSE={res['mse']:.6g} RMSE={res['rmse']:.6g} "
                f"R2={res['r2']:.5f} süre={res['time']:.2f}s"
            )

        best_label, best_res = min(rows, key=lambda r: score(r[1]))
        best_value = dict(values)[best_label]
        md.append(markdown_table(idx, title, cfg, key, rows, best_label))
        md.append("")
        md.append(f"En iyi: **{best_label}**.")
        md.append("")
        md.append(f"{title} ait yorumlar: _(öğrenci tarafından yazılacak)_")
        md.append("")

        plot_path = os.path.join(args.out, f"tablo{idx}_{key}_en_iyi.png")
        plot_best(plot_path, f"Tablo {idx}: {title}", best_label, best_res, x, y)
        md.append(f"![Tablo {idx} en iyi sonuç grafikleri]({os.path.basename(plot_path)})")
        md.append("")

        snap_path = os.path.join(args.out, f"tablo{idx}_{key}_hedef_cikis_epoch.png")
        plot_snapshots(snap_path, f"Tablo {idx}: {title}", best_label, best_res, x, y)
        md.append(f"![Tablo {idx} Epoch / Hedef-Çıkış grafiği]({os.path.basename(snap_path)})")
        md.append("")

        cmp_path = os.path.join(args.out, f"tablo{idx}_{key}_karsilastirma.png")
        plot_comparison(cmp_path, f"Tablo {idx}: {title}", rows, x, y)
        md.append(f"![Tablo {idx} karşılaştırma grafikleri]({os.path.basename(cmp_path)})")
        md.append("")

        if args.mode == "chain":
            cfg[key] = best_value
        best_overall.append((title, best_label))

    md.append("## Her tablonun en iyi değeri")
    md.append("")
    for title, label in best_overall:
        md.append(f"- {title}: {label}")
    md.append("")
    md.append("Bütün deneylere ait genel yorumlar: _(öğrenci tarafından yazılacak)_")
    md.append("")

    report_path = os.path.join(args.out, "rapor.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"\nRapor: {report_path}")


if __name__ == "__main__":
    main()
