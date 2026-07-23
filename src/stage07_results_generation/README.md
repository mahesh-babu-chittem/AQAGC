# 🚀 AQAGC Stage 07  
# 📊 Manuscript Results Generation Pipeline

<p align="center">

<img src="https://img.shields.io/badge/AQAGC-Stage%2007-blue?style=for-the-badge">
<img src="https://img.shields.io/badge/Purpose-Results%20%26%20Discussion-purple?style=for-the-badge">
<img src="https://img.shields.io/badge/Framework-Python-green?style=for-the-badge">
<img src="https://img.shields.io/badge/Experiments-Reproducible-orange?style=for-the-badge">

</p>


<p align="center">

<b>
Adaptive Quantum-Walk-Inspired Attack Graph Compiler (AQAGC)
</b>

<br>

Automated generation of all manuscript evaluation tables,
figures, and statistical analysis results.

</p>


---

# 🌟 Overview

AQAGC Stage 07 is the final evaluation layer of the framework.

It does **not retrain models**.

Instead, it:

```
Benchmark Dataset
        |
        |
        v
Results Loader
        |
        |
        v
Stage 06 Benchmark Models
        |
        |
        v
Stage 07 Evaluation Modules
        |
        |
        v
Publication Ready Results
```

The pipeline automatically generates:

✅ Latex tables  
✅ Publication figures  
✅ Statistical reports  
✅ Ablation results  
✅ Sensitivity analysis  
✅ Explainability evaluation  
✅ Manuscript numerical values  


---

# 🏗️ Stage 07 Architecture


```
stage07_results_generation/

│
├── run_stage07.py
│
├── results_loader.py
│
├── apdt_analysis.py
│
├── ranking_analysis.py
│
├── scalability_analysis.py
│
├── quantum_dynamics_analysis.py
│
├── ablation_analysis.py
│
├── hyperparameter_analysis.py
│
├── explainability_analysis.py
│
├── statistical_analysis.py
│
│
└── outputs/
    |
    ├── apdt/
    ├── ranking/
    ├── scalability/
    ├── quantum_dynamics/
    ├── ablation/
    ├── hyperparameter/
    ├── explainability/
    └── statistical/
```

---

# 🔗 Pipeline Connectivity


## 📂 Data Layer

Stage 07 loads:

```
data/
 |
 └── benchmark/
      |
      └── CSE_CIC_IDS2018/

            ├── benchmark_graphs/
            │
            ├── nodes.csv
            │
            ├── edges.csv
            │
            ├── ground_truth.csv
            │
            └── metadata.json
```

The loader provides:

- Attack graphs
- Ground truth nodes
- Vulnerability information
- Benchmark metadata


---

# 🧠 Stage 06 Model Integration


Stage 07 imports benchmark models from Stage 06.


Supported models:


| Category | Models |
|---|---|
| Classical | BFS |
| Classical | DFS |
| Classical | A* |
| Probabilistic | Markov |
| Quantum Walk | DTQW |
| Quantum Walk | CTQW |
| Hybrid Quantum | QAGC |
| Proposed Framework | AQAGC |


All evaluations use the same attack graph inputs.

---

# ⚙️ Main Execution


## ▶️ Run Complete Pipeline


```bash
python run_stage07.py
```


Execution order:


```
1. Attack Path Discovery Performance

2. Attack Path Ranking Performance

3. Scalability Evaluation

4. Quantum Exploration Dynamics

5. Ablation Study

6. Hyperparameter Sensitivity

7. Explainability Analysis

8. Statistical Significance Analysis
```


---

# 📈 Evaluation Modules


---

# 1️⃣ Attack Path Discovery Performance


## Metrics


| Metric | Description |
|---|---|
| APDT | Attack Path Discovery Time |
| QSEG | Quantum Simulation Efficiency Gain |


Generated outputs:


```
outputs/apdt/

├── tables/
│
│   └── apdt_results.tex
│
├── figures/
│
│   ├── apdt_comparison_publication.png
│   └── qseg_growth_publication.png
│
└── values/
```


---

# 2️⃣ Attack Path Ranking Performance


Evaluates:


```
Precision@10

Recall@10

F1@10

MAP

NDCG

CPC@10

APRS
```


Outputs:


```
outputs/ranking/

├── tables/

│    └── ranking_results.tex


└── values/
```


---

# 3️⃣ Scalability Evaluation


Evaluates:


## Memory

```
Peak Memory Consumption (PMC)
```


## Runtime

```
Runtime Growth Factor
```


Graph sizes:


```
50

200

500

1000

2000

5000 nodes
```


Outputs:


```
outputs/scalability/

├── tables/

│    ├── memory_results.tex
│    └── runtime_growth_results.tex


├── figures/

│    └── AQAGC_Scalability_Heatmap.png
```


---

# 4️⃣ Quantum Exploration Dynamics


Analyzes quantum behaviour:


| Metric | Purpose |
|-|-|
| ACS | Amplitude Concentration Score |
| Entropy | Exploration uncertainty |
| RCI | Risk Concentration Index |
| αt | Scheduler adaptation |


Outputs:


```
outputs/quantum_dynamics/

├── tables/

│
├── figures/
│
└── values/
```


---

# 5️⃣ Ablation Study


Evaluated variants:


```
AQAGC

AQAGC-NoVE

AQAGC-NoAS

AQAGC-NoER

AQAGC-FixedAS

AQAGC-UniformInit
```


Purpose:


| Component | Removed Feature |
|-|-|
| NoVE | Vulnerability Encoding |
| NoAS | Adaptive Scheduler |
| NoER | Explainable Risk Attribution |
| FixedAS | Fixed scheduling |
| UniformInit | Uniform quantum initialization |


Outputs:


```
outputs/ablation/

├── tables/

│    └── ablation_results.tex


└── values/
```


---

# 6️⃣ Hyperparameter Sensitivity Analysis


Parameters:


```
η

ω1

ω2

θ1-θ4

K
```


Metric:


```
MAP
```


Outputs:


```
outputs/hyperparameter/

├── tables/

│   └── hyperparameter_sensitivity.tex

└── values/
```


---

# 7️⃣ Explainability and Attribution Analysis


Computes:


| Metric | Meaning |
|-|-|
| NAS | Node Attribution Score |
| EAS | Edge Attribution Score |
| PAS | Path Attribution Score |


Additional analysis:


```
CVSS correlation

Exploitability correlation

Path risk correlation

Case study
```


Outputs:


```
outputs/explainability/

├── tables/

│
│── explainability_results.tex
│── explainability_case.tex
│── cvss_correlation.tex
```


---

# 8️⃣ Statistical Significance Analysis


Runs:


```
20 Independent executions
```


Statistical tests:


✅ Paired t-test

✅ Wilcoxon Signed Rank Test

✅ Holm-Bonferroni correction

✅ Cohen's d effect size


Outputs:


```
outputs/statistical/

├── tables/

│    └── statistical_results.tex


└── values/
```


---

# 📦 Generated Publication Assets


After execution:


```
outputs/stage07/

│
├── Latex Tables
│
├── PNG Figures
│
├── JSON Manuscript Values
│
└── Experimental Summaries
```


These files can directly support:


```
Results Section

Discussion Section

Supplementary Material

Reproducibility Package
```


---

# 🔬 Reproducibility Workflow


```
Clone Repository

        ↓

Install Requirements

        ↓

Prepare Benchmark Data

        ↓

Ensure Stage 06 Models Available

        ↓

Run:

python run_stage07.py

        ↓

Collect Outputs

        ↓

Compile Manuscript
```


---

# 🛠️ Requirements


```bash
pip install pandas

pip install numpy

pip install scipy

pip install scikit-learn

pip install networkx

pip install matplotlib

pip install statsmodels
```


---

# 📊 Final Pipeline Summary


<p align="center">


| Component | Status |
|-|-|
| Dataset Loading | ✅ |
| Stage 06 Model Integration | ✅ |
| Benchmark Evaluation | ✅ |
| Ranking Analysis | ✅ |
| Scalability Testing | ✅ |
| Quantum Dynamics | ✅ |
| Ablation Experiments | ✅ |
| Hyperparameter Analysis | ✅ |
| Explainability | ✅ |
| Statistical Validation | ✅ |


</p>


---

# 🏆 AQAGC Stage 07


<p align="center">

<img src="https://img.shields.io/badge/Status-Research%20Ready-success?style=for-the-badge">

<img src="https://img.shields.io/badge/Output-Publication%20Ready-blueviolet?style=for-the-badge">

</p>


**Automated. Reproducible. Manuscript-ready.**
