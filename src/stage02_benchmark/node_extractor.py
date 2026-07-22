"""
===========================================================================
AQAGC

Stage 2
Dataset-specific Node Extraction

Each dataset is converted into a common graph representation while
preserving its native semantics.

Supported datasets

1. CIC_IDS2017 (CAN)
2. UNSW_NB15
3. CSE_CIC_IDS2018
4. ToN_IoT

===========================================================================

"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List

import pandas as pd


# =======================================================================
# Graph Node
# =======================================================================

@dataclass
class GraphNode:

    node_id: int

    node_type: str

    identifier: str

    dataset: str

    metadata: dict


# =======================================================================
# Node Extractor
# =======================================================================

class NodeExtractor:

    def __init__(self):

        self.nodes = {}

        self.node_counter = 0

    ####################################################################
    # Public API
    ####################################################################

    def extract(

        self,

        dataframe: pd.DataFrame,

        dataset_name: str,

    ):

        self.nodes = {}

        self.node_counter = 0

        dataset = dataset_name.upper()

        if dataset == "TON_IOT":

            self._extract_toniot(dataframe)

        elif dataset == "UNSW_NB15":

            self._extract_unsw(dataframe)

        elif dataset == "CSE_CIC_IDS2018":

            self._extract_cse(dataframe)

        elif dataset == "CIC_IDS2017":

            self._extract_can(dataframe)

        else:

            raise ValueError(

                f"Unsupported dataset : {dataset}"

            )

        return self.to_dataframe()

    ####################################################################
    # Generic
    ####################################################################

    def _insert(

        self,

        node_type,

        identifier,

        dataset,

        **metadata,

    ):

        key = (

            node_type,

            identifier,

        )

        if key in self.nodes:

            return

        self.node_counter += 1

        self.nodes[key] = GraphNode(

            node_id=self.node_counter,

            node_type=node_type,

            identifier=identifier,

            dataset=dataset,

            metadata=metadata,

        )

    ####################################################################
    # ToN-IoT
    ####################################################################
    def _extract_toniot(self, df):

    ############################################################
    # Unique Hosts
    ############################################################

        hosts = pd.unique(
            pd.concat(
                [
                    df["src_ip"],
                    df["dst_ip"],
                ],
                ignore_index=True,
            ).astype(str)
        )

        for host in hosts:
            self._insert(
                "HOST",
                host,
                "ToN_IoT",
                ip=host,
            )

        ############################################################
        # Unique Services
        ############################################################

        services = (
            df[
                [
                    "dst_ip",
                    "dst_port",
                    "proto",
                    "service",
                ]
            ]
            .astype(str)
            .drop_duplicates()
        )

        for row in services.itertuples(index=False):

            dst, port, proto, service = row

            self._insert(
                "SERVICE",
                f"{dst}:{port}:{proto}:{service}",
                "ToN_IoT",
                host=dst,
                port=port,
                protocol=proto,
                service=service,
            )

    ####################################################################
    # UNSW
    ####################################################################

    def _extract_unsw(self, df):

        columns = {

            "src": df.columns[0],

            "sport": df.columns[1],

            "dst": df.columns[2],

            "dport": df.columns[3],

            "proto": df.columns[4],

            "service": df.columns[13],

        }

        for _, row in df.iterrows():

            src = str(row[columns["src"]])

            dst = str(row[columns["dst"]])

            dport = str(row[columns["dport"]])

            proto = str(row[columns["proto"]])

            service = str(row[columns["service"]])

            self._insert(

                "HOST",

                src,

                "UNSW_NB15",

                ip=src,

            )

            self._insert(

                "HOST",

                dst,

                "UNSW_NB15",

                ip=dst,

            )

            self._insert(

                "SERVICE",

                f"{dst}:{dport}:{proto}:{service}",

                "UNSW_NB15",

                host=dst,

                port=dport,

                protocol=proto,

                service=service,

            )

    ####################################################################
    # CSE-CIC-IDS2018
    ####################################################################

    def _extract_cse(self, df):

        for _, row in df.iterrows():

            port = str(row["Dst Port"])

            proto = str(row["Protocol"])

            self._insert(

                "SERVICE",

                f"{port}:{proto}",

                "CSE_CIC_IDS2018",

                port=port,

                protocol=proto,

            )

    ####################################################################
    # CIC IDS2017 CAN
    ####################################################################

    def _extract_can(self, df):

        for _, row in df.iterrows():

            can_id = str(row["ID"])

            payload = "_".join(

                [

                    str(row[f"DATA_{i}"])

                    for i in range(8)

                ]

            )

            self._insert(

                "CAN_NODE",

                can_id,

                "CIC_IDS2017",

                can_id=can_id,

            )

            self._insert(

                "CAN_FRAME",

                payload,

                "CIC_IDS2017",

                payload=payload,

            )

    ####################################################################
    # DataFrame
    ####################################################################

    def to_dataframe(self):

        rows = []

        for node in self.nodes.values():

            row = {

                "node_id": node.node_id,

                "node_type": node.node_type,

                "identifier": node.identifier,

                "dataset": node.dataset,

            }

            row.update(node.metadata)

            rows.append(row)

        return pd.DataFrame(rows)

    ####################################################################
    # Statistics
    ####################################################################

    def statistics(self):

        df = self.to_dataframe()

        return {

            "nodes": len(df),

            "types":

                df["node_type"]

                .value_counts()

                .to_dict(),

        }