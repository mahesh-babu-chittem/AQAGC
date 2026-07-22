# 📂 AQAGC Data Repository

<p align="center">

![Datasets](https://img.shields.io/badge/Datasets-4-success?style=for-the-badge)
![Benchmark Graph Sizes](https://img.shields.io/badge/Graph%20Sizes-6-blue?style=for-the-badge)
![Graphs per Size](https://img.shields.io/badge/20%20Graphs-Per%20Size-orange?style=for-the-badge)
![Largest Graph](https://img.shields.io/badge/Largest%20Graph-5000%20Nodes-red?style=for-the-badge)
![Formats](https://img.shields.io/badge/Formats-CSV%20%7C%20GraphML%20%7C%20JSON-purple?style=for-the-badge)

</p>

---

## 📖 Overview

This directory contains the benchmark datasets, processed cybersecurity data, and generated attack graph benchmarks used throughout the **Adaptive Quantum Attack Graph Compiler (AQAGC)** framework.

Since the benchmark repository is several gigabytes in size, it is hosted separately from the GitHub source code repository.

> [!IMPORTANT]
> **Download the complete benchmark repository from Google Drive before running the experiments.**

### 📥 Benchmark Repository

**Google Drive:**  
**🔗 [GOOGLE_DRIVE_LINK](https://drive.google.com/drive/folders/1IPPQhXeiaaQPznsAiWT3s9kYZPNOqC7Y?usp=sharing)**

---

# 🛡️ Benchmark Datasets

AQAGC provides benchmark attack graphs generated from four widely used cybersecurity datasets.

| Dataset | Description | Status |
|:---------|:------------|:------:|
| 🛡️ **CIC-IDS2017** | Enterprise Intrusion Detection Dataset | ✅ |
| 🌐 **CSE-CIC-IDS2018** | Large-scale Enterprise Network Attacks | ✅ |
| 🏭 **ToN-IoT** | Internet of Things & Industrial IoT | ✅ |
| 🔒 **UNSW-NB15** | Modern Network Intrusion Dataset | ✅ |

---

# 🏗️ Repository Structure

```text
data/
│
├── 📁 benchmark/
│   ├── 📁 CIC_IDS2017/
│   ├── 📁 CSE_CIC_IDS2018/
│   ├── 📁 ToN_IoT/
│   └── 📁 UNSW_NB15/
│
└── 📁 processed/
    ├── 📄 CIC_IDS2017_processed.csv
    ├── 📄 CSE_CIC_IDS2018_processed.csv
    ├── 📄 ToN_IoT_processed.csv
    └── 📄 UNSW_NB15_processed.csv
```

---

# 📊 Benchmark Graph Repository

Each benchmark dataset contains attack graphs generated at multiple scales.

```text
benchmark_graphs/
│
├── 📁 50_nodes/
├── 📁 200_nodes/
├── 📁 500_nodes/
├── 📁 1000_nodes/
├── 📁 2000_nodes/
└── 📁 5000_nodes/
```

---

## 🔄 Benchmark Generation Pipeline

```text
               Cybersecurity Dataset
                        │
                        ▼
             AQAGC Benchmark Generator
                        │
                        ▼
             Six Graph Complexity Levels
                        │
                        ▼
        20 Independent Graphs per Level
                        │
                        ▼
          Complete Benchmark Repository
```

---

# 📦 Contents of Each Generated Graph

Every generated benchmark graph contains the following files.

| File | Description |
|------|-------------|
| 📄 **AQAGC_Attack_Graph.graphml** | Complete attack graph in GraphML format |
| 📄 **nodes.csv** | Node attributes and vulnerability information |
| 📄 **edges.csv** | Directed attack relationships |
| 📄 **ground_truth.csv** | Ground-truth critical attack paths |
| ⚙️ **metadata.json** | Benchmark generation metadata |

---

# 📈 Benchmark Statistics

| Property | Value |
|-----------|------:|
| 📚 Benchmark Datasets | **4** |
| 📊 Graph Sizes | **6** |
| 🔁 Graphs per Size | **20** |
| 🕸️ Largest Benchmark | **5000 Nodes** |
| 📄 Supported Formats | **CSV, GraphML, JSON** |

---

# 📁 Processed Dataset Repository

The **processed** directory contains the cleaned and preprocessed versions of each cybersecurity dataset used during benchmark generation.

These datasets serve as the direct input to the AQAGC benchmark construction pipeline and ensure reproducible experimental evaluation.

---

# 🔬 Reproducibility

> [!NOTE]
> Please preserve the original folder hierarchy after downloading the benchmark repository.
>
> The AQAGC framework expects the datasets and benchmark graphs to remain in their original locations. Modifying the directory structure may require updating the dataset paths within the project configuration.

---

# 🧩 Overall Data Organization

```text
                        AQAGC Data Repository
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
  Benchmark Datasets      Processed Data        Benchmark Graphs
        │                        │                        │
        └──────────────┬─────────┘                        │
                       ▼                                  ▼
             Benchmark Construction            Experimental Evaluation
                       │                                  │
                       └──────────────┬───────────────────┘
                                      ▼
                          AQAGC Framework Experiments
```

---

<details>

<summary><b>📌 Notes</b></summary>

- All benchmark graphs were generated using the AQAGC benchmark construction framework.
- Each graph size contains **20 independently generated attack graphs** for statistically reliable evaluation.
- The provided benchmark repository is intended for reproducibility, benchmarking, and comparative evaluation of attack graph analytics algorithms.
- Future benchmark releases may include additional cybersecurity datasets and larger graph scales.

</details>

---

# 📚 Citation

The AQAGC framework and benchmark repository are currently associated with a manuscript **under peer review**.

The complete citation information (including DOI and BibTeX entry) will be provided here once the manuscript has been accepted and officially published.

If you wish to use the benchmark repository prior to publication or have any questions regarding its usage, please contact the repository maintainer or open an issue on GitHub.
```
