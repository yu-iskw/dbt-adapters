import pytest
from dbt.tests.util import run_dbt

MODEL_SQL = """
{{ config(materialized='view') }}
select * from {{ ref('seed') }}
"""

AGG_THRESHOLD_POLICY = {
    "aggregation_threshold_policy": {
        "threshold": 3,
        "privacy_unit_column": "id",
    },
    "join_restriction_policy": {
        "join_condition": "JOIN_ANY",
        "join_allowed_columns": ["id"],
    },
}

DIFF_PRIVACY_POLICY = {
    "differential_privacy_policy": {
        "privacy_unit_column": "id",
        "max_epsilon_per_query": 1000.0,
        "epsilon_budget": 10000.1,
        "delta_per_query": 0.01,
        "delta_budget": 0.1,
        "max_groups_contributed": 2,
    }
}

class TestPrivacyPolicy:
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "view_with_agg_threshold.sql": MODEL_SQL,
            "view_with_diff_privacy.sql": MODEL_SQL,
        }

    @pytest.fixture(scope="class")
    def seeds(self):
        return {
            "seed.csv": "id,name\n1,a\n2,b\n3,c",
        }

    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
            "models": {
                "test": {
                    "view_with_agg_threshold": {
                        "+privacy_policy": AGG_THRESHOLD_POLICY
                    },
                    "view_with_diff_privacy": {
                        "+privacy_policy": DIFF_PRIVACY_POLICY
                    }
                }
            }
        }

    def test_privacy_policy(self, project):
        run_dbt(["seed"])
        results = run_dbt(["run"])
        assert len(results) == 2
