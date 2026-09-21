# ACLDQ: The Unified Principle Across Information and Physical Layers

## Addressed Coherent Lattice Data Quantum — A Single Format Principle at Three Layers

**Author:** Babatope Jesse Afolabi
**Affiliation:** Aevov Research / cr8OS Foundation / WPWakanda, LLC
**Status:** Architecture clarification
**Date:** September 2026

---

## Abstract

ACLDQ appears in three distinct contexts across the AUF architecture: as a phase-coherent mesh protocol (replacing TCP/IP), as a quantum state container format (for cr8OS information-layer data), and as a matter-manifestation blueprint format (for Aura MER physical-layer deployment). This document establishes that these are not three separate formats sharing an acronym — they are three instantiations of a single principle: **addressed coherence patterns in chunked binary encoding.**

At every layer, ACLDQ carries the same semantic: "what should be coherent, where, and by how much." The difference between layers is what "coherence" denotes.

---

## 1. The Unifying Definition

**ACLDQ** — Addressed Coherent Lattice Data Quantum — is a binary encoding principle for addressed coherence patterns. An ACLDQ document is a sequence of typed chunks, each carrying addressed data weighted by a coherence parameter, within a header that establishes the lattice context (mesh ID, compression mode, authorization tier).

The principle is layer-agnostic. What changes between layers is the interpretation of:
- The header fields (what "lattice context" means)
- The chunk types (what "addressed data" means)
- The coherence parameter (what "coherence" means)

---

## 2. Layer Instantiations

### 2.1 ACLDQ as Protocol Stack (Layers L1-L4)

**Context:** Planetary mesh communication, replacing TCP/IP with phase-coherent routing.

| Field | Meaning at Protocol Layer |
|-------|--------------------------|
| Header | Mesh identity, protocol version, routing tier |
| Chunks | Phase-coherent data units with lattice addresses |
| Coherence | Kuramoto order parameter K of the transmission path |
| Addressing | Q3 non-local co-indexing (not IP addresses) |

**Layers:**
- L1 (Lattice Physical): SPU-Core manages Z_M modulation and biophoton synchronization
- L2 (Manifestation Tunnels): High-density informational corridors from coherent node overlap
- L3 (Non-Local Routing): Q3 addressing plane — data co-indexed, not transmitted
- L4 (Application): Senton lattice coupling — the receiving engine's state

**Source:** auf-papers Chapter 15

### 2.2 ACLDQ as Information Format (cr8OS Layer)

**Context:** Quantum state container for simulation data, circuit descriptions, and mesh metadata.

| Field | Meaning at Information Layer |
|-------|-----------------------------|
| Header (128 bytes) | Magic 0x51444C43, version, compression mode, state encoding, qubit count, gate count, content hash (SHA-256), mesh CID, consensus metadata |
| Chunks | STATE (amplitudes), CIRCUIT (gate sequences), MEASURE (results), METADATA (JSON), MESH (peer info), CONSENSUS (Raft state), CHECKPOINT, SIGNATURE |
| Coherence | State encoding fidelity (dense/sparse/MPS/stabilizer) |
| Compression | AVIF-LL, WebP-L, JXL-L, Zstd (layer-appropriate) |

**Source:** `aura_rpp_private_core/cr8OS-2.0/quantum-supercomputer/acldq/include/acldq.h`

### 2.3 ACLDQ as Blueprint Format (Aura MER Layer)

**Context:** Matter-manifestation blueprint carrying geometry, density, phase, and cascade-control instructions.

| Field | Meaning at Physical Layer |
|-------|--------------------------|
| Header (64 bytes) | Magic "ACLD", version, density class, authorization tier |
| Chunks | Geometry (0x01-0x0F), Density/Phase (0x10-0x12), Mirror-State refs, MER_SELF_BLUEPRINT (0x20), CHILD_TIER_DOWNRANK (0x21) |
| Coherence | Field density ρ_A and phase angle φ for transducer projection |
| Density classes | Info (∞ B/g), Bio (10 GB/g), Engineered (1 MB/g), Bulk (1 KB/g) |

**Source:** `aura_rpp_private_core/README.md §5.2`, `hardware/aft_e_retrofit/docs/ACLDQ_BLUEPRINT_FORMAT.md`

---

## 3. The Common Structure

All three instantiations share this structure:

```
┌─────────────────────────────────────────┐
│  HEADER                                  │
│  • Magic (identifies ACLDQ)             │
│  • Version                               │
│  • Lattice context (mesh ID / encoding)  │
│  • Authorization / tier                  │
│  • Integrity (hash / CRC)               │
├─────────────────────────────────────────┤
│  CHUNK SEQUENCE                          │
│  ┌─────────────────────────────────┐    │
│  │ Chunk Header                     │    │
│  │ • Type (what kind of data)       │    │
│  │ • Size                           │    │
│  │ • Address (where in lattice)     │    │
│  ├─────────────────────────────────┤    │
│  │ Chunk Payload                    │    │
│  │ • Addressed data                 │    │
│  │ • Coherence weight               │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │ ... more chunks ...              │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

The header establishes *context* (which lattice, what authorization). The chunks carry *content* (what data, at what address, with what coherence).

---

## 4. The Unification Theorem

**Statement:** The three ACLDQ instantiations are related by a functor F that maps the interpretation domain while preserving the chunked-binary structure.

| Aspect | Protocol | Information | Physical |
|--------|----------|-------------|----------|
| Address space | Q3 mesh addresses | Qubit indices / mesh CIDs | Spatial coordinates / transducer cells |
| Coherence meaning | Kuramoto K of path | State encoding fidelity | Field density ρ_A |
| Authorization | Routing tier | Consensus term | Capability/tier byte |
| Data semantics | Routing instructions | Quantum amplitudes | Geometry/phase/blueprint |

The functor F preserves:
- The chunked binary structure (header + typed chunks)
- The addressing principle (every datum has a lattice address)
- The coherence weighting (every datum has a coherence parameter)
- The authorization context (every document has a tier/capability)

What changes is the *interpretation* of these preserved structures.

---

## 5. Resolution of the Dual-Definition Problem

The `acldq.h` C header currently implements only the information-layer chunk types (STATE, CIRCUIT, MEASURE, METADATA, MESH, CONSENSUS, CHECKPOINT, SIGNATURE). The physical-layer chunk types (0x10-0x12 for bio/phase, 0x20-0x21 for cascade control) exist only in documentation.

**Resolution:** The C header should be extended with the physical-layer chunk types, unified under a single ACLDQ specification. The chunk type space should be partitioned:

```
0x00        — HEADER
0x01-0x0F   — Information-layer chunks (state, circuit, measure, metadata, mesh, consensus)
0x10-0x1F   — Physical-layer chunks (geometry, density, phase, Mirror-State, bio-lock)
0x20-0x2F   — Cascade-control chunks (MER_SELF_BLUEPRINT, CHILD_TIER_DOWNRANK)
0x30-0xEF   — Reserved for future layers
0xF0-0xFE   — Extension chunks (layer-specific custom data)
0xFF        — SIGNATURE (cryptographic verification)
```

This preserves backward compatibility (existing information-layer code continues to work) while adding the physical-layer and cascade-control chunks in their designated ranges.

---

## 6. Relationship to the Empress Seed Format

The Empress seed format (`{coordinate, fh, files, mc, v}`) used by cr8OS is a *special case* of ACLDQ at the information layer, optimized for the specific use case of file compression and storage:

| Empress Field | ACLDQ Equivalent |
|---------------|-----------------|
| coordinate | Mesh CID / content address |
| fh (file headers) | Chunk headers with metadata |
| files (file list) | Chunk sequence |
| mc (moth coordinates) | Chunk payloads (GRM fold residuals) |
| v (version) | Version field |

The Empress format is to ACLDQ what JSON is to a general serialization format — a specific instantiation optimized for a specific use case, but structurally compatible with the general principle.

---

## 7. Summary

ACLDQ is one principle with three instantiations. The principle is: **addressed coherence patterns in chunked binary encoding.** The three instantiations are the protocol layer (mesh routing), the information layer (quantum state containers), and the physical layer (matter-manifestation blueprints).

The C codec (`acldq.h`) should be extended to cover all three instantiations under a single unified chunk-type space. The Empress seed format is a special case of ACLDQ optimized for file compression.

This unification resolves the apparent duplication and establishes ACLDQ as a single, layer-spanning format principle within the AUF architecture.

---

*Part of the Unified Layered Architecture series. See also: `architecture-unified-layers-auf-senton.md`*
