# 🚀 AQAGC  
# Adaptive Quantum-Walk-Inspired Attack Graph Compiler

<p align="center">

<img src="https://img.shields.io/badge/Quantum%20Computing-AQAGC-blue?style=for-the-badge">
<img src="https://img.shields.io/badge/Cybersecurity-Attack%20Graphs-red?style=for-the-badge">
<img src="https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge">
<img src="https://img.shields.io/badge/Reproducible-Research-orange?style=for-the-badge">

</p>


<p align="center">

<b>
An Adaptive Hybrid Quantum-Classical Framework for Intelligent Attack Graph Analysis, Risk Prioritization, and Explainable Cybersecurity Decision Making
</b>

</p>


---

# 🌟 Overview

AQAGC (**Adaptive Quantum-Walk-Inspired Attack Graph Compiler**) is a hybrid quantum-classical cybersecurity framework designed for:

- Attack graph construction
- Vulnerability-aware quantum encoding
- Adaptive quantum walk exploration
- Risk-aware attack path prioritization
- Explainable security analytics
- Large-scale benchmark evaluation


The framework integrates:

```
Cybersecurity Data
        |
        v
Attack Graph Construction
        |
        v
Vulnerability-Aware Quantum Encoding
        |
        v
Adaptive Hybrid Quantum Exploration
        |
        v
Risk Prioritization
        |
        v
Benchmark Evaluation
        |
        v
Statistical Validation
```


---

# 🧠 Core Contributions


## ⚛️ 1. Vulnerability-Aware Quantum Encoding

AQAGC introduces vulnerability-guided encoding of attack graph states.

Components:

- Feature extraction
- Node encoding
- Quantum state preparation
- Graph Hamiltonian construction


---

## 🔄 2. Adaptive Hybrid Quantum Scheduler

AQAGC combines:

- Discrete-Time Quantum Walk (DTQW)
- Continuous-Time Quantum Walk (CTQW)


with an adaptive scheduler controlling exploration behavior.


```
Local Exploration
       |
       |
       v

DTQW

       |
 Adaptive Scheduler

       |
       v

CTQW

       |
       v

Global Propagation
```


---

## 🔐 3. Risk-Aware Attack Prioritization

The framework evaluates:

- Node risk
- Edge risk
- Attack path risk
- Critical asset importance


---

## 🔎 4. Explainable Security Analytics

AQAGC provides:

- Node attribution
- Edge attribution
- Path attribution
- Risk explanations


---

# 🏗️ Repository Architecture


```
AQAGC/

│
├── src/
│
│
├── stage01_preprocessing/
│
├── stage02_benchmark/
│
├── stage03_vaqe/
│
├── stage04_hybrid_scheduler/
│
├── stage05_risk_prioritization/
│
├── stage06_benchmarking/
│
└── stage07_results_generation/

```


---

# 🔬 Complete Pipeline


## Stage 01
# 📂 Data Preprocessing


Purpose:

- Dataset loading
- Cleaning
- Feature preparation
- Dataset normalization


Supported datasets:

- CICIDS2017
- CSE-CIC-IDS2018
- TON_IoT
- UNSW-NB15


Pipeline:

```
Raw Dataset

     |

Cleaning

     |

Feature Processing

     |

Processed Dataset
```


---

# Stage 02
# 🕸️ Attack Graph Benchmark Construction


Purpose:

Convert cybersecurity datasets into benchmark attack graphs.


Components:

```
Node Extraction

Edge Construction

Edge Weighting

Graph Normalization

Graph Sampling

Ground Truth Generation

Graph Export
```


Generated artifacts:

```
nodes.csv

edges.csv

ground_truth.csv

graphml files

metadata.json
```


---

# Stage 03
# ⚛️ Vulnerability-Aware Quantum Encoding (VAQE)


Purpose:

Convert attack graph properties into quantum-compatible representations.


Components:

```
feature_encoder.py

node_encoding.py

quantum_encoder.py

vaqe_circuit.py

graph_hamiltonian.py
```


Workflow:

```
Attack Node Features

        |

Vulnerability Encoding

        |

Quantum State Representation
```


---

# Stage 04
# 🔄 Hybrid Quantum Scheduler


Core AQAGC exploration engine.


Components:


```
dtqw_walk.py

ctqw_walk.py

hybrid_scheduler.py

probability_propagator.py

hamiltonian_evolution.py
```


Hybrid exploration:

```
Attack Graph

     |

DTQW Exploration

     |

Adaptive Scheduling

     |

CTQW Propagation

     |

Attack Probability Distribution
```


---

# Stage 05
# 🎯 Risk Prioritization


Responsible for cybersecurity decision intelligence.


Modules:


```
node_risk_calculator.py

edge_risk_calculator.py

path_risk_calculator.py

priority_ranker.py
```


Computes:

- Node risk
- Edge risk
- Path risk
- Critical assets
- Attack priority ranking


---

# Stage 06
# 📊 Benchmarking Framework


AQAGC evaluation against classical and quantum baselines.


Implemented methods:


| Method | Category |
|---|---|
| BFS | Classical Search |
| DFS | Classical Search |
| A* | Heuristic Search |
| Markov | Probabilistic |
| DTQW | Quantum Walk |
| CTQW | Quantum Walk |
| QAGC | Hybrid Quantum |
| AQAGC | Proposed Framework |


Evaluation includes:

- Runtime analysis
- Ranking performance
- Quantum efficiency
- Scalability


---

# Stage 07
# 📈 Results Generation


Automatically generates manuscript-ready results.


Generated analyses:


## Attack Path Discovery

Metrics:

- APDT
- QSEG


---

## Attack Path Ranking

Metrics:

- Precision@10
- Recall@10
- F1@10
- MAP
- NDCG
- CPC@10
- APRS


---

## Scalability

Evaluates:

- Runtime growth
- Memory consumption


Graph sizes:

```
50

200

500

1000

2000

5000 nodes
```


---

## Quantum Exploration Dynamics


Metrics:

- Amplitude Concentration Score
- Entropy
- Risk Concentration Index
- Scheduler coefficient


---

## Ablation Analysis


Variants:

```
AQAGC

AQAGC-NoVE

AQAGC-NoAS

AQAGC-NoER

AQAGC-FixedAS

AQAGC-UniformInit
```


---

## Hyperparameter Sensitivity


Parameters:


```
η

ω1

ω2

θ1-θ4

K
```


---

## Explainability Evaluation


Metrics:


| Metric | Description |
|-|-|
| NAS | Node Attribution Score |
| EAS | Edge Attribution Score |
| PAS | Path Attribution Score |


---

## Statistical Validation


Methods:


- Paired t-test
- Wilcoxon Signed Rank Test
- Holm-Bonferroni Correction
- Cohen's d Effect Size


---

# 📂 Installation


Clone repository:


```bash
git clone https://github.com/mahesh-babu-chittem/AQAGC.git

cd AQAGC
```


Create environment:


```bash
conda create -n aqagc python=3.10

conda activate aqagc
```


Install dependencies:


```bash
pip install -r requirements.txt
```


---

# ▶️ Running AQAGC


## Run preprocessing


```bash
python src/stage01_preprocessing/run.py
```


---

## Generate attack graphs


```bash
python src/stage02_benchmark/run_graph_construction.py
```


---

## Run vulnerability-aware encoding


```bash
python src/stage03_vaqe/run.py
```


---

## Run hybrid quantum scheduler


```bash
python src/stage04_hybrid_scheduler/scheduler_pipeline.py
```


---

## Run risk prioritization


```bash
python src/stage05_risk_prioritization/risk_prioritization_pipeline.py
```


---

## Run benchmarking


```bash
python src/stage06_benchmarking/run.py
```


---

## Generate manuscript results


```bash
python src/stage07_results_generation/run_stage07.py
```


---

# 📊 Output Structure


After execution:


```
outputs/

│
├── graphs/

├── benchmarks/

├── figures/

├── tables/

└── manuscript_results/
```


Generated files include:


- LaTeX tables
- Publication figures
- Statistical reports
- Benchmark summaries


---

# 🔁 Reproducibility Workflow


```
1. Download datasets

          ↓

2. Run preprocessing

          ↓

3. Generate attack graphs

          ↓

4. Execute AQAGC pipeline

          ↓

5. Run benchmark comparison

          ↓

6. Generate manuscript results
```


---

# 📦 Key Dependencies


Main libraries:


```
Python

NumPy

Pandas

NetworkX

SciPy

Scikit-learn

Qiskit

Matplotlib
```


---

# 🧪 Research Evaluation


AQAGC evaluates:


| Category | Evaluation |
|-|-|
| Efficiency | APDT, Runtime |
| Ranking | Precision, MAP, NDCG |
| Scalability | Memory, Growth |
| Quantum Behaviour | ACS, Entropy |
| Robustness | Statistical Testing |
| Explainability | NAS, EAS, PAS |


---

# ⭐ Acknowledgements


AQAGC integrates concepts from:

- Quantum walks
- Attack graph analysis
- Vulnerability modelling
- Explainable AI


---

# 📜 License


This project is released for academic and research purposes.


---

<p align="center">

🚀 <b>AQAGC — Bridging Quantum Computing and Cybersecurity Intelligence</b> 🚀

</p>
