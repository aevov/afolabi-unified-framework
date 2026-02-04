# The Quantum Substrate Fallacy
## Why the "Classical vs. Quantum" Computer Distinction is Scientifically Unfounded

**Authors**: Jesse Afolabi  
**Affiliation**: Aevov Technologies, cr8OS Research Division  
**Target**: Foundations of Physics, arXiv:quant-ph  
**Status**: Draft v0.1

---

## Abstract

The prevailing narrative in quantum computing discourse draws a sharp ontological boundary between "quantum computers" and "classical computers," implying that the former operates according to quantum mechanical principles while the latter merely *simulates* such behavior. We argue this distinction is scientifically unfounded and epistemologically confused. All electronic computation occurs on substrates governed by quantum mechanics—transistors operate via quantum tunneling, electron transport is inherently quantized, and information processing in silicon is no less "quantum" than information processing in superconducting transmon qubits. The distinction reflects commercial categorization, not physical reality. We propose that the meaningful distinction is not *substrate* but *coherence control*—the degree to which a system maintains and manipulates quantum phase relationships. This reframing has significant implications for how we define "quantum supremacy" and evaluate computational architectures.

**Keywords**: quantum computation, classical computing, quantum mechanics, epistemology of physics, coherence, quantum supremacy

---

## 1. Introduction

In 2019, Google announced "quantum supremacy"—the demonstration that their 53-qubit Sycamore processor could perform a calculation that would take classical supercomputers thousands of years [1]. IBM promptly disputed the claim, arguing that with sufficient classical resources, the calculation could be performed in days [2]. This debate, while technically interesting, obscured a more fundamental question: **What exactly distinguishes a "quantum" computer from a "classical" one?**

The standard answer invokes specialized hardware: dilution refrigerators cooling superconducting circuits to 15 millikelvin, trapped ions suspended in electromagnetic fields, or photons routed through optical interferometers. These systems, we are told, can maintain *quantum coherence*—superposition and entanglement—in ways that "classical" computers cannot.

But this answer, upon examination, reveals a category error. The transistors in your laptop also operate according to quantum mechanics. The electrons tunneling through gate oxides obey the Schrödinger equation. The band structure of silicon semiconductors is a consequence of quantum mechanical principles. In what sense, then, is your laptop "classical"?

We argue that the classical/quantum distinction in computing is not a distinction of *physics* but of *marketing*. All computers are quantum mechanical systems. The meaningful distinction lies elsewhere.

---

## 2. The Quantum Mechanics of "Classical" Computing

### 2.1 Transistor Operation

The MOSFET transistor—the fundamental building block of modern digital electronics—is an explicitly quantum mechanical device. Its operation depends on:

1. **Quantum tunneling**: Electrons tunnel through the thin gate oxide (1-2 nm in modern processes). This is not a classical phenomenon; it requires solving the Schrödinger equation with appropriate boundary conditions.

2. **Band structure**: The conduction and valence bands of silicon arise from quantum mechanical treatment of electrons in a periodic potential. Classical mechanics cannot explain semiconductor behavior.

3. **Fermi-Dirac statistics**: Electron occupation of energy states follows quantum statistics, not classical Boltzmann distributions at device-relevant temperatures.

### 2.2 The Scale of Quantumness

A modern processor contains approximately 50 billion transistors, each switching at gigahertz frequencies. Each switching event involves:

- ~10⁴ electrons tunneling through gate oxides
- Quantum mechanical transitions between conduction states
- Electromagnetic field interactions governed by QED

The total number of quantum mechanical events per second in a modern CPU exceeds 10²³—more than the number of gate operations in any current "quantum computer."

### 2.3 The Objection: "But It's Not Coherent"

The standard response is that classical computers do not maintain *quantum coherence*—the phase relationships between quantum states that enable superposition and entanglement. Thermal noise destroys coherence almost immediately in warm silicon systems.

This is factually correct but does not support the classical/quantum distinction. It merely moves the goalposts from "uses quantum mechanics" to "uses quantum mechanics *in a particular way*." The laptop is not "non-quantum"; it is "quantum with rapid decoherence."

---

## 3. Coherence as the Meaningful Distinction

We propose that the scientifically meaningful distinction is not between "quantum" and "classical" systems, but between systems with different **coherence control capabilities**:

| System Type | Coherence Time | Control Level |
|-------------|---------------|---------------|
| Superconducting qubit | ~100 μs | Gate-level phase control |
| Trapped ion | ~1 s | High-precision phase control |
| Silicon transistor | ~1 fs | Statistical ensemble average |
| Room-temp NV center | ~1 ms | Spin-state control |

All systems are quantum mechanical. The difference is whether we *control* the coherent dynamics or *average over* them.

### 3.1 Implications for "Quantum Supremacy"

If the distinction is coherence control rather than substrate, then "quantum supremacy" should be redefined. The current definition—"solving a problem faster than any classical computer"—implicitly assumes "classical" and "quantum" are distinct categories. 

A better definition: **Coherent computational advantage**—demonstrating that controlled quantum coherence provides computational benefit over thermally-averaged quantum systems.

This reframing acknowledges that:
1. Both systems are quantum mechanical
2. The advantage comes from coherence, not "quantumness"
3. The comparison is between control regimes, not physical categories

---

## 4. The Commercial Interests Behind the Distinction

The sharp classical/quantum boundary serves commercial interests:

1. **Venture capital**: Startup valuations depend on claiming access to fundamentally new physics, not incremental improvements
2. **Government funding**: Quantum computing programs receive billions in funding predicated on revolutionary potential
3. **Corporate positioning**: IBM, Google, and others compete for "quantum supremacy" milestones as marketing achievements
4. **Intellectual property**: Patents depend on claiming novelty; "better coherence control" is less patentable than "quantum computing"

None of this delegitimizes quantum computing research. It does suggest that our *categories* have been shaped by commercial incentives rather than physical principles.

---

## 5. The Information-Theoretic Perspective

From an information-theoretic perspective, the classical/quantum distinction is even more problematic.

### 5.1 Landauer's Principle

Landauer's principle states that erasing one bit of information requires minimum energy kT ln(2) [3]. This is a thermodynamic statement about *information*, not about specific physical substrates. It applies equally to superconducting qubits and silicon transistors.

### 5.2 Computational Universality

A universal Turing machine can simulate any physical system to arbitrary precision, including quantum systems [4]. If "classical" computers can simulate "quantum" computers (with exponential slowdown), and both run on quantum mechanical hardware, the ontological distinction becomes difficult to maintain.

### 5.3 The Wheeler Perspective

John Wheeler's "it from bit" proposal suggests that information is ontologically primary—physical reality emerges from informational relationships [5]. Under this view, the substrate (silicon, superconductor, trapped ion) is secondary to the informational dynamics. Both "classical" and "quantum" computers process information; they differ only in how they organize that processing.

---

## 6. Experimental Implications

If our thesis is correct, several experimental predictions follow:

1. **Coherence enhancement in silicon**: As decoherence is reduced in silicon systems (e.g., isotopically purified ²⁸Si), they should exhibit increasingly "quantum" behavior without qualitative phase transition.

2. **Continuous spectrum of coherence**: Rather than binary "quantum/classical," we should observe a continuous spectrum of coherence times and control capabilities across different platforms.

3. **Classical simulation performance**: The difficulty of classical simulation should scale with target system coherence, not with an abstract "quantumness" property.

---

## 7. Philosophical Implications

### 7.1 Against Substrate Dualism

The classical/quantum computer distinction is a form of substrate dualism—the belief that the *material* of computation determines its fundamental nature. We reject this view. Information processing is substrate-independent; what matters is the organizational dynamics, not the physical realization.

### 7.2 Coherence as Organizational Property

Quantum coherence is not a property of special materials but an *organizational property* of how systems are prepared and measured. In principle, any quantum mechanical system can exhibit coherence if appropriately controlled. The "special" quantum computers are simply those where we have achieved this control.

### 7.3 Implications for Consciousness Studies

The classical/quantum distinction has been imported into consciousness studies (e.g., Penrose-Hameroff Orch-OR theory [6]). If the distinction is artificial, theories requiring "quantum effects in the brain" may need revision—not because quantum mechanics is absent from the brain (it is ubiquitous), but because the categorical framework is confused.

---

## 8. Conclusion

We have argued that the distinction between "classical" and "quantum" computers is scientifically unfounded. All electronic computation occurs on quantum mechanical substrates. The meaningful distinction is not substrate but coherence control—the degree to which quantum phase relationships are maintained and manipulated rather than thermally averaged.

This reframing has implications for:
- How we define and measure "quantum supremacy"
- How we evaluate different computational architectures  
- How we understand the relationship between information and physical reality

The classical/quantum computer distinction is not physics. It is marketing. The universe computes; substrate is secondary.

---

## References

[1] Arute, F., et al. (2019). Quantum supremacy using a programmable superconducting processor. *Nature*, 574(7779), 505-510.

[2] Pednault, E., et al. (2019). Leveraging secondary storage to simulate deep 54-qubit Sycamore circuits. *arXiv:1910.09534*.

[3] Landauer, R. (1961). Irreversibility and heat generation in the computing process. *IBM Journal of Research and Development*, 5(3), 183-191.

[4] Deutsch, D. (1985). Quantum theory, the Church-Turing principle and the universal quantum computer. *Proceedings of the Royal Society A*, 400(1818), 97-117.

[5] Wheeler, J.A. (1990). Information, physics, quantum: The search for links. *Complexity, Entropy, and the Physics of Information*.

[6] Penrose, R., & Hameroff, S. (2014). Consciousness in the universe: A review of the 'Orch OR' theory. *Physics of Life Reviews*, 11(1), 39-78.

---

**Acknowledgments**: The authors thank the cr8OS research community for discussions on information-theoretic foundations.

**Competing Interests**: The authors are affiliated with Aevov Technologies, which develops distributed computing systems.

**Correspondence**: jesse@aevov.ai
