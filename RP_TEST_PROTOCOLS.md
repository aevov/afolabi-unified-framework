# Resonance Physics Experimental Test Protocols
## RP-1, RP-2, RP-3 — Native Aevov Mesh Implementation

**Status:** Pre-deployment specification — ready for execution when QPU/RPU mesh is live  
**Platform:** Luci QPU (Q3 Mesh) · Luci RPU (Resonon Mesh)  
**DOI reference:** 10.5281/zenodo.18913463  
**Contact:** research@cr8os.com

---

## Why the Aevov Mesh Is the Correct Platform

External QPU hardware (IBM, Google) forces RP predictions into a mismatched architecture:
- No native qudit support (d>2 forced to qubit approximations)
- No direct 𝕄 measurement — you infer coherence from destructive tomography
- No MESH_SYNC primitive — collective scaling must be approximated with GHZ circuits
- RP-2 (HRV coupling) is physically impossible via cloud access

On the Aevov mesh, every RP prediction maps to a **native primitive**:

| RP Prediction | External QPU | Aevov QPU Mesh | Aevov RPU Mesh |
|---|---|---|---|
| RP-1: Structured state T2 > random T2 | Approximated via Hahn echo on qubits | Native: qudit state preparation + coherence decay measurement | **Native + superior:** READ_M non-destructive — track 𝕄(t) directly |
| RP-2: HRV coherence reduces quantum noise floor | Physically impossible (cloud) | Not applicable | **Native:** F_TUNE gate drives HRV frequency into resonon; MESH_CHECK measures noise floor response |
| RP-3: N² collective coherence scaling | GHZ approximation — lossy at scale | Native: MESH_SYNC on N qudits + collective coherence tomography | **Native + exact:** MESH_CHECK returns C_collective = `sqrt((1/N²)Σᵢⱼ Lᵢⱼ²)`  |

---

## RP-1: Coherence-Extended Decoherence

### Prediction
> Organized (structured) quantum states exhibit longer coherence times than random states of equal size.  
> **Threshold:** Structured states show >15% longer T2 (qudit) or 𝕄-decay half-life (resonon).  
> **Falsification:** No significant difference across 20+ trial pairs at 95% confidence.

### Physical basis
In RP, coherence time is not purely a hardware property — it is a function of the informational structure of the state. A state that is phase-organized (low Z_M gradient across the register) couples to the Afolabi Field more efficiently, reducing the rate at which environmental noise perturbs the register. Random states have no preferred phase structure — they couple to environmental noise incoherently, degrading faster.

This is distinct from standard decoherence theory, which predicts T2 as a function of hardware coupling constants alone, independent of state content. RP-1 is the test that distinguishes these.

### QPU Mesh Implementation (ACL 3.0)

```acl
# RP-1 QPU TEST — COHERENCE DECAY COMPARISON
# Run at N = 4, 8, 16, 32 qudits, d = 4 (ququarts)
# Each condition: 50 trials structured, 50 trials random
# Metric: T2 = time for register fidelity to drop below 1/e

# ── STRUCTURED STATE PREPARATION ─────────────────────────────
PROCEDURE rp1_structured(N, d):
  ALLOC q[N], d=d                    # N ququarts
  FOR i IN range(N):
    H_d(q[i])                        # Hadamard-d: uniform superposition
    PHASE(q[i], phi = 2*pi*i/N)      # Structured phase gradient: φᵢ = 2πi/N
  ENTANGLE_CHAIN(q)                  # Sequential CZ-d gates: nearest-neighbor entanglement
  RETURN q

# ── RANDOM STATE PREPARATION ─────────────────────────────────
PROCEDURE rp1_random(N, d):
  ALLOC q[N], d=d
  FOR i IN range(N):
    H_d(q[i])                        # Hadamard-d: uniform superposition
    PHASE(q[i], phi = RANDOM(0, 2*pi))   # Random phase per qudit
  ENTANGLE_CHAIN(q)                  # Same entanglement topology
  RETURN q

# ── COHERENCE DECAY MEASUREMENT ──────────────────────────────
PROCEDURE measure_T2(q, t_max, dt):
  fidelity_trace = []
  t = 0
  initial = TOMOGRAPHY(q)            # Full state snapshot at t=0
  WHILE t < t_max:
    IDLE(q, dt)                      # Free evolution — hardware decoherence
    current = TOMOGRAPHY(q)
    F = FIDELITY(initial, current)
    fidelity_trace.append((t, F))
    t += dt
    IF F < 0.05: BREAK               # Stop at noise floor
  T2 = EXTRACT_T2(fidelity_trace)    # Fit to F(t) = exp(-t/T2)
  RETURN T2

# ── MAIN TEST LOOP ────────────────────────────────────────────
FOR N IN [4, 8, 16, 32]:
  T2_structured_trials = []
  T2_random_trials     = []

  FOR trial IN range(50):
    q_s = rp1_structured(N, d=4)
    T2_s = measure_T2(q_s, t_max=500us, dt=10us)
    T2_structured_trials.append(T2_s)

    q_r = rp1_random(N, d=4)
    T2_r = measure_T2(q_r, t_max=500us, dt=10us)
    T2_random_trials.append(T2_r)

  mean_s = MEAN(T2_structured_trials)
  mean_r = MEAN(T2_random_trials)
  pct_diff = (mean_s - mean_r) / mean_r * 100

  RECORD:
    N           = N
    T2_struct   = mean_s ± STDERR(T2_structured_trials)
    T2_random   = mean_r ± STDERR(T2_random_trials)
    delta_pct   = pct_diff
    p_value     = T_TEST(T2_structured_trials, T2_random_trials)
    result      = PASS if pct_diff > 15 AND p_value < 0.05 else FAIL
```

### RPU Mesh Implementation (ACL RP 3.0)

The RPU gives a **superior test** for RP-1. Because READ_M is non-destructive, you can track 𝕄(t) in real time without disturbing the state — unlike QPU tomography which requires preparing a fresh state for each measurement point.

```acl
# RP-1 RPU TEST — 𝕄 DECAY COMPARISON
# Non-destructive: same register tracked through full decay
# Metric: 𝕄-half-life τ = time for 𝕄 to decay to 𝕄₀/2

# ── STRUCTURED RESONON STATE ──────────────────────────────────
PROCEDURE rp1_rpu_structured(N):
  ◬ N ρ                              # create N-resonon register at |ground⟩
  FOR i IN range(N):
    ⧈ H_RP ρ[i]                      # |ground⟩ → |seed⟩ (𝕄=0.5)
    ⧈ R_RP(2*pi*i/N) ρ[i]           # structured phase gradient
    ⧈ C_UP(0.4) ρ[i]                # 𝕄 → 0.9
  ⊕ ρ                                # MESH_SYNC: phase-lock all resonons
  RETURN ρ, ℳ ρ                      # return register and initial 𝕄₀

# ── RANDOM RESONON STATE ──────────────────────────────────────
PROCEDURE rp1_rpu_random(N):
  ◬ N ρ
  FOR i IN range(N):
    ⧈ H_RP ρ[i]
    ⧈ R_RP(RANDOM(0, 2*pi)) ρ[i]    # random phase — no structure
    ⧈ C_UP(0.4) ρ[i]                # same initial 𝕄 = 0.9
  # NO MESH_SYNC — random phases cannot phase-lock
  RETURN ρ, ℳ ρ

# ── NON-DESTRUCTIVE DECAY TRACKING ───────────────────────────
PROCEDURE track_M_decay(ρ, M_0, t_max, dt):
  decay_trace = [(0, M_0)]
  t = 0
  WHILE t < t_max:
    IDLE(ρ, dt)                      # free evolution
    M_t = ℳ ρ                        # READ_M — NON-DESTRUCTIVE
    decay_trace.append((t, M_t))
    t += dt
    IF M_t < 0.05: BREAK
  tau = EXTRACT_HALFLIFE(decay_trace)  # fit to M(t) = M_0 * exp(-t/tau)
  RETURN tau

# ── MAIN TEST LOOP ────────────────────────────────────────────
FOR N IN [8, 64, 256, 1024]:          # RPU scales — larger N than QPU test
  tau_s_trials = []
  tau_r_trials = []

  FOR trial IN range(50):
    ρ_s, M0_s = rp1_rpu_structured(N)
    tau_s = track_M_decay(ρ_s, M0_s, t_max=10ms, dt=100us)
    tau_s_trials.append(tau_s)

    ρ_r, M0_r = rp1_rpu_random(N)
    tau_r = track_M_decay(ρ_r, M0_r, t_max=10ms, dt=100us)
    tau_r_trials.append(tau_r)

  RECORD:
    N           = N
    tau_struct  = MEAN(tau_s_trials) ± STDERR(tau_s_trials)
    tau_random  = MEAN(tau_r_trials) ± STDERR(tau_r_trials)
    delta_pct   = (MEAN(tau_s_trials) - MEAN(tau_r_trials)) / MEAN(tau_r_trials) * 100
    p_value     = T_TEST(tau_s_trials, tau_r_trials)
    result      = PASS if delta_pct > 15 AND p_value < 0.05 else FAIL
```

### RP-1 Pass/Fail Criteria

| N | Minimum delta_pct | Required p-value | Notes |
|---|---|---|---|
| 4 | >15% | <0.05 | Baseline — small N, signal may be weak |
| 8 | >15% | <0.05 | Should begin to see consistent signal |
| 16 | >20% | <0.01 | N² amplification should increase separation |
| 32 / 256 (RPU) | >25% | <0.001 | Full confirmation at scale |

**Strong confirmation:** All N ≥ 8 conditions pass. Delta increases with N (consistent with N² amplification of structured advantage).  
**Partial confirmation:** N=4 borderline, N≥8 pass. Rerun N=4 with 200 trials.  
**Falsification:** No condition reaches >15% at p<0.05 after 200 trials.

---

## RP-2: HRV-Field Coherence Coupling

### Prediction
> High-ℜ biological subjects (HRV coherence >0.7) reduce the quantum noise floor in resonant systems.  
> **Threshold:** >10% noise reduction correlated with ℜ, r > 0.5.  
> **Falsification:** Zero correlation across 20+ paired trials.

### Why RP-2 Is Testable on the RPU (Not External QPU)

External QPU: **physically impossible.** Cloud access; hardware is in a dilution refrigerator in a data center. No biological proximity.

RPU mesh: **natively designed for this.** The F_TUNE gate (`F_TUNE(f)`) is the explicit biological-interface primitive — it drives a resonon's phase into alignment with a biological oscillator at frequency f. The HRV coherence band (0.04–0.15 Hz, peak ~0.1 Hz) is the target. The resonon's 𝕄 response to F_TUNE input is the measurement.

This is not an approximation or analogy. NRT states that biological observers couple to the Afolabi Field via coherent HRV oscillations. The RPU's resonon mesh is a physical instantiation of that field. F_TUNE is the coupling primitive. RP-2 is a native test.

### RPU Mesh Implementation (ACL RP 3.0)

```acl
# RP-2 RPU TEST — HRV-RESONON NOISE FLOOR COUPLING
# Requires: HRV sensor input stream at 0.04–0.15 Hz
# ℜ (coherence) = spectral power in HRV band / total HRV power
# Conditions: HIGH-ℜ (>0.7), LOW-ℜ (<0.3), BASELINE (no F_TUNE)

# ── NOISE FLOOR MEASUREMENT ───────────────────────────────────
# Baseline: measure 𝕄 variance on a decohering register (no F_TUNE)
# This establishes the hardware noise floor for each trial

PROCEDURE measure_noise_floor(N, t_window):
  ◬ N ρ
  FOR i IN range(N):
    ⧈ H_RP ρ[i]
    ⧈ C_UP(0.3) ρ[i]               # 𝕄 = 0.8 starting state
  M_readings = []
  FOR t IN RANGE(0, t_window, dt=100ms):
    M_readings.append(ℳ ρ)          # READ_M — non-destructive
  noise_floor = VARIANCE(M_readings)
  RETURN noise_floor

# ── F_TUNE COUPLING PROCEDURE ─────────────────────────────────
PROCEDURE rp2_coupled(N, hrv_stream, t_window):
  ◬ N ρ
  FOR i IN range(N):
    ⧈ H_RP ρ[i]
    ⧈ C_UP(0.3) ρ[i]               # 𝕄 = 0.8 starting state
  ⊕ ρ                               # MESH_SYNC

  M_readings = []
  FOR t IN RANGE(0, t_window, dt=100ms):
    f_hrv = hrv_stream.current_frequency()  # live HRV input (0.04–0.15 Hz)
    coherence_R = hrv_stream.coherence()    # ℜ at current t
    FOR i IN range(N):
      ⧈ F_TUNE(f_hrv) ρ[i]         # couple resonon phase to HRV frequency
    M_readings.append(ℳ ρ)

  noise_floor_coupled = VARIANCE(M_readings)
  RETURN noise_floor_coupled, coherence_R

# ── MAIN TEST LOOP ────────────────────────────────────────────
# Protocol:
# Phase A (5 min): subject in LOW-ℜ state (normal breathing, no biofeedback)
# Phase B (5 min): subject in HIGH-ℜ state (resonance frequency breathing ~0.1 Hz,
#                  biofeedback confirmed ℜ > 0.7)
# Each phase: 30 trials of noise floor measurement, F_TUNE coupled vs baseline

RESULTS = []
FOR condition IN [LOW_R, HIGH_R]:
  hrv_stream = HRV_INPUT(subject=subject_id, condition=condition)
  R_mean = hrv_stream.mean_coherence()

  noise_baseline = []
  noise_coupled  = []

  FOR trial IN range(30):
    nf_base = measure_noise_floor(N=256, t_window=10s)
    nf_coup, R = rp2_coupled(N=256, hrv_stream, t_window=10s)
    noise_baseline.append(nf_base)
    noise_coupled.append(nf_coup)

  reduction_pct = (MEAN(noise_baseline) - MEAN(noise_coupled)) / MEAN(noise_baseline) * 100

  RESULTS.append({
    condition:        condition,
    R_mean:           R_mean,
    noise_baseline:   MEAN(noise_baseline) ± STDERR(noise_baseline),
    noise_coupled:    MEAN(noise_coupled)  ± STDERR(noise_coupled),
    reduction_pct:    reduction_pct,
    p_value:          T_TEST(noise_baseline, noise_coupled)
  })

# ── CORRELATION ANALYSIS ──────────────────────────────────────
# Across all subjects and conditions, compute:
r_correlation = PEARSON_R(
  x = [result.R_mean for result in ALL_RESULTS],
  y = [result.reduction_pct for result in ALL_RESULTS]
)

RECORD:
  r_hrv_noise = r_correlation
  result = PASS if (HIGH_R.reduction_pct > 10
                    AND HIGH_R.p_value < 0.05
                    AND r_hrv_noise > 0.5) else FAIL
```

### RP-2 Requirements Before Running

1. **HRV sensor integration** into RPU mesh — live F_TUNE input requires a real-time HRV stream (sampling rate ≥ 4 Hz)
2. **Minimum subjects:** 20 subjects × 2 conditions × 30 trials = 1,200 data points for statistical power
3. **Blinding:** RPU operator should be blind to ℜ condition during measurement
4. **Controls:** Same subject, same session, LOW-ℜ → HIGH-ℜ within-subject design minimizes hardware variance

### RP-2 Pass/Fail Criteria

| Metric | Threshold | Notes |
|---|---|---|
| Noise reduction (HIGH-ℜ) | >10% vs baseline | Primary metric |
| Noise reduction (LOW-ℜ) | <3% vs baseline | Controls for F_TUNE effect alone |
| r(ℜ, reduction) | >0.5 | Dose-response: higher ℜ = more reduction |
| p-value (HIGH-ℜ) | <0.05 | Across 30 trials per subject |

**Falsification:** HIGH-ℜ condition shows <3% reduction, indistinguishable from LOW-ℜ. This would confirm F_TUNE is a null gate with respect to biological input — which would significantly challenge NRT layer.

---

## RP-3: N² Collective Coherence Scaling

### Prediction
> Distributed resonant systems exhibit N² coherence bandwidth scaling, not linear N scaling.  
> **Threshold:** Measured collective coherence C_collective = C_single × N² (Kuramoto derivation).  
> **Falsification:** Linear scaling observed — C_collective ∝ N.

### Physical Basis
In standard quantum systems, N entangled qubits span a 2^N Hilbert space but the effective coherence bandwidth per node remains constant. In RP, once a resonon mesh enters MESH_SYNC (all nodes phase-locked within π/4), the collective coherence is the integral of all pairwise coupling terms L(i,j) — which grows as N² by the Kuramoto mean-field derivation. The MESH_CHECK primitive directly measures this: `sqrt((1/N²)Σᵢⱼ Lᵢⱼ²)`.

RP-3 is the most decisive test because it distinguishes RP from all other quantum frameworks — QPU Hilbert space scaling (2^N) and classical parallelism (linear N) are both fundamentally different predictions from RP's N².

### QPU Mesh Implementation (ACL 3.0)

```acl
# RP-3 QPU TEST — COLLECTIVE COHERENCE SCALING
# Platform: Luci QPU Q3 Mesh
# Metric: Effective coherence bandwidth B(N) vs N
# Prediction: B(N) = B_single × N²

PROCEDURE measure_single_coherence(d):
  ALLOC q[1], d=d
  H_d(q[0])
  C_UP(q[0], delta=0.4)             # set 𝕄 = 0.9 equivalent in qudit
  B_single = COHERENCE_BANDWIDTH(q[0])   # measure bandwidth of single node
  RETURN B_single

PROCEDURE measure_collective_coherence(N, d):
  ALLOC q[N], d=d
  FOR i IN range(N):
    H_d(q[i])
    C_UP(q[i], delta=0.4)
  MESH_SYNC(q)                       # phase-lock all N qudits
  B_collective = COLLECTIVE_COHERENCE_BANDWIDTH(q)
  RETURN B_collective

# ── SCALING MEASUREMENT ───────────────────────────────────────
FOR d IN [2, 4, 8]:                  # qubit, ququart, qutrit(octal)
  B_1 = measure_single_coherence(d)

  scaling_data = [(1, B_1)]
  FOR N IN [2, 4, 8, 16, 32, 64, 128]:
    B_N_trials = []
    FOR trial IN range(30):
      B_N = measure_collective_coherence(N, d)
      B_N_trials.append(B_N)
    B_N_mean = MEAN(B_N_trials)
    scaling_data.append((N, B_N_mean))

  # Fit scaling exponent: B(N) = B_1 × N^alpha
  alpha = FIT_POWER_LAW(scaling_data)

  RECORD:
    d           = d
    B_single    = B_1
    alpha       = alpha ± FIT_ERROR
    scaling     = "N²" if 1.85 < alpha < 2.15 else "linear" if 0.85 < alpha < 1.15 else "other"
    result      = PASS if 1.85 < alpha < 2.15 else FAIL
```

### RPU Mesh Implementation (ACL RP 3.0)

The RPU is the **canonical** platform for RP-3. MESH_CHECK is the exact measurement primitive derived from the N² law — it returns `sqrt((1/N²)Σᵢⱼ Lᵢⱼ²)`, the collective 𝕄 across all pairwise couplings. The test is direct: does MESH_CHECK output scale as N² × single-node baseline, or linearly?

```acl
# RP-3 RPU TEST — N² SCALING LAW DIRECT MEASUREMENT
# This is the canonical test: native primitives, exact prediction

# ── SINGLE NODE BASELINE ──────────────────────────────────────
PROCEDURE rp3_single_baseline():
  ◬ 1 ρ
  ⧈ H_RP ρ[0]
  ⧈ C_UP(0.4) ρ[0]                  # 𝕄 = 0.9
  M_single = ℳ ρ                     # READ_M — non-destructive
  B_single = COHERENCE_BANDWIDTH(ρ)  # bandwidth of isolated resonon
  RETURN M_single, B_single

# ── COLLECTIVE MESH MEASUREMENT ───────────────────────────────
PROCEDURE rp3_collective(N):
  ◬ N ρ
  FOR i IN range(N):
    ⧈ H_RP ρ[i]
    ⧈ C_UP(0.4) ρ[i]                # identical starting 𝕄 = 0.9 per node
  ⊕ ρ                                # MESH_SYNC — activates N² scaling
  M_collective = ⊠ ρ                 # MESH_CHECK = sqrt((1/N²)Σᵢⱼ Lᵢⱼ²)
  B_collective = COHERENCE_BANDWIDTH(ρ)
  RETURN M_collective, B_collective

# ── SCALING SWEEP ─────────────────────────────────────────────
M_1, B_1 = rp3_single_baseline()
scaling_data = [(1, B_1, M_1)]

FOR N IN [2, 4, 8, 16, 64, 256, 1024, 10000]:  # RPU scale advantage
  B_N_trials = []
  M_N_trials = []

  FOR trial IN range(50):
    M_N, B_N = rp3_collective(N)
    B_N_trials.append(B_N)
    M_N_trials.append(M_N)

  scaling_data.append((N, MEAN(B_N_trials), MEAN(M_N_trials)))

# ── SCALING LAW VALIDATION ────────────────────────────────────
# Fit: B(N) = B_1 × N^alpha
alpha_B = FIT_POWER_LAW([(N, B) for N, B, M in scaling_data])

# Direct N² check: ratio test
FOR N, B_N, M_N IN scaling_data[1:]:           # skip N=1
  predicted_N2  = B_1 * N * N
  predicted_N1  = B_1 * N
  ratio_to_N2   = B_N / predicted_N2            # should ≈ 1.0
  ratio_to_N1   = B_N / predicted_N1            # should ≈ N (large deviation from linear)

  RECORD:
    N               = N
    B_N             = MEAN ± STDERR
    ratio_to_N2     = ratio_to_N2               # 0.9–1.1 = confirmation
    ratio_to_N1     = ratio_to_N1               # should diverge with N
    M_collective    = M_N

RECORD FINAL:
  alpha           = alpha_B ± FIT_ERROR
  N2_confirmed    = ALL(0.85 < r < 1.15 for r in ratio_to_N2 WHERE N >= 8)
  result          = PASS if N2_confirmed AND 1.85 < alpha_B < 2.15 else FAIL

# ── KURAMOTO CROSS-VALIDATION ─────────────────────────────────
# Theoretical N² coefficient from Kuramoto: K = coupling_strength / N
# Expected: C_collective = C_single × N²  with K at MESH_SYNC threshold
# Compare measured alpha to Kuramoto prediction at known coupling strength
K_measured = EXTRACT_KURAMOTO_K(scaling_data)
K_theoretical = KURAMOTO_MEAN_FIELD(coupling_constant=MESH_SYNC_COUPLING)
K_agreement = ABS(K_measured - K_theoretical) / K_theoretical * 100

RECORD:
  K_measured      = K_measured
  K_theoretical   = K_theoretical
  K_agreement_pct = K_agreement     # should be < 10% for strong confirmation
```

### RP-3 Pass/Fail Criteria

| Test | Threshold | Significance |
|---|---|---|
| Power law exponent α | 1.85 < α < 2.15 | Core: N² confirmed |
| ratio_to_N2 at N≥8 | 0.85–1.15 for all N | N² holds across scale range |
| K agreement (Kuramoto) | <10% deviation | Theoretical mechanism confirmed, not just phenomenology |
| Falsification | α < 1.3 across N≥16 at 200 trials | Linear or sub-quadratic — falsifies RP-3 |

**Why the Kuramoto cross-validation matters:** Passing the scaling law alone (α≈2) could in principle be coincidental — any strongly coupled collective system might show superlinear scaling. But if the Kuramoto coupling constant K extracted from the scaling data matches the theoretical prediction from the MESH_SYNC coupling strength, that confirms the *mechanism*, not just the exponent. That is the difference between a correlated result and a causally confirmed prediction.

---

## Combined Validation Impact

If all three tests pass with strong confirmation:

| Prediction | Layer it validates | AUF validation δ |
|---|---|---|
| RP-1 confirmed | Core RP: structured states have intrinsically longer coherence life. Information structure affects physical coherence — Axiom I direct. | +8–12% weighted |
| RP-2 confirmed | NRT biological coupling layer. F_TUNE is a real coupling, not a null gate. HRV-field interaction is measurable. | +12–15% weighted |
| RP-3 confirmed | N² Scaling Law. Kuramoto derivation validated in hardware. N² coefficient matches theory. | +10–14% weighted |
| All three confirmed | AUF weighted total: **~88–93%** (up from ~57% post-Chénier) | **+31–36%** |

RP-3 with Kuramoto cross-validation would be the single most significant result — it validates the mathematical mechanism that underlies both the RPU architecture and NRT's collective coherence model. If K_measured matches K_theoretical, that is not a correlation — that is causal confirmation.

---

## Execution Priority

| Priority | Test | Platform | Readiness |
|---|---|---|---|
| 1 | RP-3 RPU N² scaling | Luci RPU mesh | Run on day 1 of RPU availability — MESH_SYNC + MESH_CHECK are launch primitives |
| 2 | RP-1 RPU 𝕄-decay | Luci RPU mesh | Same session — READ_M non-destructive, low cost per trial |
| 3 | RP-1 QPU qudit | Luci QPU mesh | Run in parallel — validates d>2 generalization |
| 4 | RP-2 RPU HRV | Luci RPU mesh | Requires HRV sensor integration — Phase 2 |
| 5 | RP-3 QPU scaling | Luci QPU mesh | Validates ACL 3.0 side, cross-check with RPU result |

---

*These protocols are pre-registered as of DOI: 10.5281/zenodo.18913463.*  
*Pre-registration establishes that pass criteria were defined before data collection.*  
*Aevov Research / cr8OS Foundation / WPWakanda, LLC*  
*Contact: research@cr8os.com*
