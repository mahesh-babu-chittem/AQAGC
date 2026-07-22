"""
===========================================================================
AQAGC

Stage 2

Dataset-specific Edge Construction

===========================================================================

"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import pandas as pd


@dataclass
class GraphEdge:

    edge_id: int

    source: int

    destination: int

    edge_type: str

    dataset: str

    transition_frequency: int

    attack_label: str

    timestamp: str

    #metadata: dict


class EdgeConstructor:

    def __init__(self, node_df):

        self.nodes = node_df

        self.edge_counter = 0

        self.edges = []

        self.lookup = {}

        self._build_lookup()

    ####################################################################

    def _build_lookup(self):

        for _, row in self.nodes.iterrows():

            self.lookup[(row["node_type"], row["identifier"])] = row["node_id"]

    ####################################################################

    def build(

        self,

        dataframe,

        dataset_name,

    ):

        dataset = dataset_name.upper()

        if dataset == "TON_IOT":

            self._toniot(dataframe)

        elif dataset == "UNSW_NB15":

            self._unsw(dataframe)

        elif dataset == "CSE_CIC_IDS2018":

            self._cse(dataframe)

        elif dataset == "CIC_IDS2017":

            self._can(dataframe)

        else:

            raise ValueError(dataset)

        return self.to_dataframe()

    ####################################################################
    # helper
    ####################################################################

    def _add(

        self,

        src,

        dst,

        edge_type,

        dataset,

        attack,

        timestamp,

    ):

        self.edge_counter += 1

        self.edges.append(

            GraphEdge(

                edge_id=self.edge_counter,

                source=src,

                destination=dst,

                edge_type=edge_type,

                dataset=dataset,

                transition_frequency=1,

                attack_label=attack,

                timestamp=str(timestamp),

                #metadata={},

            )

        )

    ####################################################################
    # ToN-IoT
    ####################################################################

    def _toniot(self, df):

        grouped = (

            df.groupby(

                [

                    "src_ip",

                    "dst_ip",

                    "dst_port",

                    "proto",

                    "service",

                    "label",

                ]

            )

            .size()

            .reset_index(name="frequency")

        )

        for _, row in grouped.iterrows():

            src = self.lookup[

                ("HOST", str(row["src_ip"]))

            ]

            dst = self.lookup[

                ("HOST", str(row["dst_ip"]))

            ]

            service = self.lookup[

                (

                    "SERVICE",

                    f"{row['dst_ip']}:{row['dst_port']}:{row['proto']}:{row['service']}"

                )

            ]

            self._add(

                src,

                dst,

                "HOST_COMMUNICATION",

                "ToN_IoT",

                row["label"],

                "",

            )

            self.edges[-1].transition_frequency = int(row["frequency"])

            self._add(

                dst,

                service,

                "HOST_SERVICE",

                "ToN_IoT",

                row["label"],

                "",

            )

    ####################################################################
    # UNSW
    ####################################################################

    def _unsw(self, df):

        for _, row in df.iterrows():

            src = self.lookup[

                ("HOST", str(row[df.columns[0]]))

            ]

            dst = self.lookup[

                ("HOST", str(row[df.columns[2]]))

            ]

            service = self.lookup[

                (

                    "SERVICE",

                    f"{row[df.columns[2]]}:{row[df.columns[3]]}:{row[df.columns[4]]}:{row[df.columns[13]]}"

                )

            ]

            attack = row[df.columns[48]]

            timestamp = row[df.columns[28]]

            self._add(

                src,

                dst,

                "HOST_COMMUNICATION",

                "UNSW_NB15",

                attack,

                timestamp,

            )

            self._add(

                dst,

                service,

                "HOST_SERVICE",

                "UNSW_NB15",

                attack,

                timestamp,

            )

    ####################################################################
    # CSE-CIC
    ####################################################################
    def _cse(self, df):

        """
    Construct temporal service-transition graph for CSE-CIC-IDS2018.

    Since the dataset does not contain source/destination IP addresses,
    services are connected according to the chronological order of
    observed network flows.
    """

    ############################################################
    # Sort chronologically
    ############################################################

        df = df.sort_values(
            "Timestamp"
        ).reset_index(drop=True)

    ############################################################

        for i in range(len(df) - 1):

            current = df.iloc[i]
            nxt = df.iloc[i + 1]

        ########################################################

            current_service = self.lookup[
                (
                    "SERVICE",
                    f"{current['Dst Port']}:{current['Protocol']}"
                )
            ]

            next_service = self.lookup[
                (
                    "SERVICE",
                    f"{nxt['Dst Port']}:{nxt['Protocol']}"
                )
            ]

        ########################################################

            self._add(

                current_service,

                next_service,

                "SERVICE_TRANSITION",

                "CSE_CIC_IDS2018",

                current["Label"],

                current["Timestamp"],

            )

    ############################################################
    # Merge duplicate transitions
    ############################################################

        edges = self.to_dataframe()

        edges = (

            edges.groupby(

                [

                    "source",

                    "destination",

                    "edge_type",

                    "dataset",

                    "attack_label",

                ],

                as_index=False,

            )

            .agg(

                {

                    "transition_frequency": "sum",

                    "timestamp": "first",

                }

            )

        )

        self.edges = []

        self.edge_counter = 0

        for _, row in edges.iterrows():

            self._add(

                int(row["source"]),

                int(row["destination"]),

                row["edge_type"],

                row["dataset"],

                row["attack_label"],

                row["timestamp"],

            )

            self.edges[-1].transition_frequency = int(

                row["transition_frequency"]

            )

  ####################################################################
    # CAN
    ####################################################################

    def _can(self, df):

        ids = list(df["ID"].astype(str))

        labels = list(df["label"])

        for i in range(len(ids) - 1):

            src = self.lookup[

                ("CAN_NODE", ids[i])

            ]

            dst = self.lookup[

                ("CAN_NODE", ids[i + 1])

            ]

            self._add(

                src,

                dst,

                "CAN_TRANSITION",

                "CIC_IDS2017",

                labels[i],

                i,

            )

    ####################################################################

    def to_dataframe(self):

        rows = []

        for edge in self.edges:

            row = asdict(edge)

            #row.update(edge.metadata)

            rows.append(row)

        return pd.DataFrame(rows)