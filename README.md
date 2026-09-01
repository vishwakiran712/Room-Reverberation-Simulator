# 🏛️ Room Reverberation Simulator

> An interactive room-acoustics simulator for modeling reverberation, acoustic reflections, energy decay, and RT60 behavior under different room and material conditions.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt)
[![NumPy](https://img.shields.io/badge/Numerical-NumPy-orange?logo=numpy)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-orange?logo=matplotlib)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<img width="903" height="478" alt="image" src="https://github.com/user-attachments/assets/ddf2299c-8ded-4fcb-a9a6-792a336ce935" />


---

## 📌 Overview

**Room Reverberation Simulator** is an interactive desktop application for exploring how room geometry, acoustic absorption, reflection density, and reverberation time influence the behavior of sound inside an enclosed space.

The simulator creates a synthetic room-reverberation response and provides visual and numerical feedback on the resulting acoustic decay.

It is designed as a practical laboratory for understanding:

* Room acoustics
* Reverberation
* Acoustic reflections
* Absorption
* Reflection density
* RT60
* Energy decay
* Sound propagation
* Acoustic treatment concepts
* Digital signal processing

The application provides a controlled environment for experimenting with room parameters without requiring a physical acoustic measurement setup.

---

# ✨ Key Features

## 🏠 Room Parameter Modeling

The simulator allows the user to configure fundamental room-acoustic parameters.

These parameters influence the simulated reverberant field and decay characteristics.

```text
Room Geometry
      │
      ▼
Surface / Absorption
      │
      ▼
Reflection Behavior
      │
      ▼
Reverberant Field
      │
      ▼
Energy Decay
```

This provides an intuitive way to understand how physical room characteristics affect acoustic behavior.

---

# 📐 Room Geometry

The room is represented using configurable dimensions:

```text
Length × Width × Height
```

These dimensions define the simulated acoustic space.

Room geometry affects:

* Available acoustic volume
* Reflection paths
* Reverberant behavior
* Acoustic decay

A larger enclosed space generally provides a different reverberation characteristic from a smaller space when other parameters remain unchanged.

---

# 🧱 Acoustic Absorption

The simulator models acoustic energy absorption using an adjustable absorption parameter.

Conceptually:

```text
Incident Sound
      │
      ▼
┌───────────────┐
│ Room Surface  │
└───────┬───────┘
        │
   ┌────┴────┐
   ▼         ▼
Absorbed   Reflected
 Energy      Energy
```

Higher absorption results in more acoustic energy being removed from the reverberant field.

Lower absorption allows more energy to remain available for subsequent reflections.

---

# 🪞 Acoustic Reflection Modeling

Reflected acoustic energy forms the basis of the simulated reverberation.

The simulator represents the transition from:

```text
Direct Sound
     ↓
Early Reflections
     ↓
Dense Reflections
     ↓
Reverberant Field
     ↓
Decay to Noise Floor
```

This provides a simplified representation of how sound persists inside an enclosed room after the direct sound has arrived.

---

# 🌊 Reverberation Modeling

Reverberation is simulated using a decaying acoustic response.

Conceptually:

```text
Amplitude
   │
   │\
   │ \
   │  \
   │   \
   │    \____
   │         \____
   │              \____
   └──────────────────────► Time
```

The reverberant tail represents the gradual reduction of acoustic energy caused by repeated reflections and absorption.

---

# ⏱️ RT60

One of the primary acoustic indicators demonstrated by the simulator is **RT60**.

RT60 is the theoretical time required for the acoustic energy level to decrease by:

```text
60 dB
```

from its initial level.

Conceptually:

```text
  0 dB ─────────●
                \
                 \
 -20 dB           \
                   \
 -40 dB             \
                     \
 -60 dB ──────────────●
              │
              └── RT60 ──► Time
```

RT60 is one of the fundamental parameters used to characterize the reverberation of a room.

---

# 📉 Energy Decay

The simulator visualizes the decrease in acoustic energy over time.

The reverberation envelope can be represented approximately as an exponential decay:

```text
E(t) = E₀ e⁻ᵅᵗ
```

where:

* `E₀` = initial acoustic energy
* `α` = decay coefficient
* `t` = time

This provides a simplified mathematical model for studying reverberant decay.

---

# 🎛️ Reflection Density

Reflection density controls the number or concentration of simulated reflected acoustic contributions.

Conceptually:

```text
Low Density

│     │        │
│  │        │
│       │
└─────────────────► Time


High Density

││││││││││││││││
││││││││││││││││
││││││││││││││││
└─────────────────► Time
```

Increasing reflection density produces a more continuous reverberant field.

This demonstrates the transition from discrete reflections toward a dense reverberation tail.

---

# 🔊 Direct Sound → Reverberant Field

The simulator conceptually divides the acoustic response into several stages:

```text
┌──────────────────────────────────────────────┐
│                 ROOM RESPONSE                │
│                                              │
│  Direct      Early        Late               │
│  Sound       Reflections  Reverberation      │
│    │              │             │            │
│    ▼              ▼             ▼            │
│    ▲        ▲ ▲ ▲ ▲ ▲      ▓▓▓▓▓▓▓▓         │
│    │       ▲ ▲ ▲ ▲ ▲ ▲    ▓▓▓▓▓▓▓▓▓         │
│    │      ▲ ▲ ▲ ▲ ▲ ▲ ▲  ▓▓▓▓▓▓▓▓▓▓         │
└──────────────────────────────────────────────┘
```

This provides an intuitive visualization of how an acoustic event evolves inside a room.

---

# 🧮 Reverberation Mathematics

A simplified exponential decay model can be expressed as:

```text
A(t) = A₀e⁻ᵅᵗ
```

In decibel form:

```text
L(t) = 20 log₁₀(A(t))
```

The simulator uses this type of decay behavior to create the synthetic reverberation response.

---

# 📊 Acoustic Visualization

The application provides graphical feedback for studying the simulated response.

The primary visualization can be used to observe:

* Initial sound arrival
* Reflection behavior
* Reverberant tail
* Decay characteristics
* Noise-floor behavior
* Overall acoustic persistence

This allows users to visually compare different room configurations.

---

# 🧪 Example Experiments

## Experiment 1 — Small vs Large Room

Create two room configurations:

```text
Room A
Small Volume

Room B
Large Volume
```

Keep the absorption and other parameters similar.

Compare the resulting reverberation behavior.

---

## Experiment 2 — Absorptive vs Reflective Room

Compare:

```text
Low Absorption
       vs
High Absorption
```

Expected behavior:

```text
Low Absorption
     ↓
More Reflected Energy
     ↓
Longer Reverberation


High Absorption
     ↓
Less Reflected Energy
     ↓
Shorter Reverberation
```

---

## Experiment 3 — Reflection Density

Compare:

```text
Low Reflection Density
          vs
High Reflection Density
```

Observe how the simulated response changes from relatively sparse reflections toward a denser reverberant field.

---

## Experiment 4 — RT60 Comparison

Configure rooms with different reverberation characteristics and compare their RT60 values.

This demonstrates how room acoustic treatment and geometry influence reverberation time.

---

## Experiment 5 — Acoustic Treatment

Simulate a reflective room and gradually increase absorption.

Observe:

* Reduced reverberant energy
* Faster decay
* Lower reverberation time

This provides a simple conceptual demonstration of acoustic treatment.

---

# 🧠 Room-Acoustics Processing Pipeline

```text
┌───────────────────────────────┐
│        Room Configuration     │
│                               │
│ Length / Width / Height       │
│ Absorption / Reflection       │
│ Reverberation Parameters      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Acoustic Modeling       │
│                               │
│ Direct Sound                  │
│ Reflections                   │
│ Reverberant Field             │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│    Reverberation Generation   │
│                               │
│     Decaying Acoustic Field   │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Energy Decay Analysis   │
│                               │
│          RT60                 │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Acoustic Visualization  │
└───────────────────────────────┘
```

---

# 🖥️ Application Interface

The simulator uses a dark, technical laboratory-style interface.

Conceptually:

```text
┌──────────────────────────────────────────────────────────────┐
│                 ROOM REVERBERATION SIMULATOR                │
├──────────────────────┬───────────────────────────────────────┤
│                      │                                       │
│  ROOM PARAMETERS     │       SIMULATION STATUS               │
│                      │                                       │
│  Room Dimensions     ├───────────────────────────────────────┤
│  Absorption          │                                       │
│  Reflection Density  │       REVERBERATION RESPONSE         │
│  RT60 / Decay        │                                       │
│                      │                                       │
│                      ├───────────────────────────────────────┤
│                      │                                       │
│  SIMULATION CONTROL  │       ACOUSTIC METRICS               │
│                      │                                       │
└──────────────────────┴───────────────────────────────────────┘
```

The desktop interface is implemented using **PyQt5**, with scientific visualization provided through **Matplotlib**.

---

# 🎓 Educational Applications

This simulator can be used to demonstrate:

* Room Acoustics
* Reverberation
* RT60
* Acoustic Absorption
* Acoustic Reflection
* Reflection Density
* Sound Propagation
* Energy Decay
* Reverberant Fields
* Acoustic Treatment
* Room Design
* Audio Engineering
* Signal Processing
* Architectural Acoustics

---

# 🛠️ Technology Stack

| Technology     | Purpose                                   |
| -------------- | ----------------------------------------- |
| **Python**     | Core simulation                           |
| **NumPy**      | Numerical computation and signal modeling |
| **PyQt5**      | Desktop GUI                               |
| **Matplotlib** | Acoustic visualization                    |

---

# 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/vishwakiran712/Room-Reverberation-Simulator.git
cd Room-Reverberation-Simulator
```

### 2. Install dependencies

```bash
pip install numpy matplotlib PyQt5
```

### 3. Run the simulator

```bash
python app.py
```

---

# 📂 Project Structure

```text
Room-Reverberation-Simulator/
│
├── app.py
├── README.md
└── LICENSE
```

---

# 🔭 Possible Future Enhancements

Potential extensions include:

* 3D room visualization
* Source and receiver positioning
* Image-source method
* Ray-tracing acoustic simulation
* Frequency-dependent absorption
* Frequency-dependent RT60
* Octave-band analysis
* Early Decay Time (EDT)
* C50 speech clarity
* C80 music clarity
* D50 definition
* Center Time (Ts)
* Energy Time Curve
* Room impulse-response export
* WAV audio rendering
* Real-time audio playback
* Material database
* Wall/floor/ceiling material selection
* Acoustic treatment placement
* Room-mode analysis
* Room resonance visualization
* Interactive room geometry

---

# 📜 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

# 👨‍💻 Author

**Vishwakiran B.V.S.**

Engineering • Sports Technology • Product Research • Scientific Computing • Acoustics • Signal Processing

GitHub: [@vishwakiran712](https://github.com/vishwakiran712)

---

# ⭐ Project

If you find this project useful for learning, experimentation, or acoustic research, consider giving the repository a ⭐.

**Repository:**
https://github.com/vishwakiran712/Room-Reverberation-Simulator
