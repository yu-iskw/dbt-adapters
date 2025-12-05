import unittest
from unittest.mock import Mock, patch
from dbt.adapters.bigquery.impl import BigQueryAdapter
from dbt.adapters.bigquery.relation_configs._privacy import PrivacyPolicyConfig
import dbt.common.exceptions


class TestPrivacyPolicy(unittest.TestCase):
    def setUp(self):
        self.config = Mock()
        self.adapter = BigQueryAdapter(self.config, Mock())

    def test_get_view_options_with_privacy_policy(self):
        config = {
            "privacy_policy": {
                "aggregation_threshold_policy": {
                    "threshold": 3,
                    "privacy_unit_column": "id",
                },
            }
        }
        node = {}
        with patch.object(self.adapter, "get_common_options", return_value={}):
            options = self.adapter.get_view_options(config, node)
            self.assertIn("privacy_policy", options)
            self.assertIsInstance(options["privacy_policy"], str)

    def test_get_table_options_with_privacy_policy(self):
        config = {"privacy_policy": {}}
        node = {}
        with self.assertRaises(dbt.common.exceptions.DbtRuntimeError):
            self.adapter.get_table_options(config, node, False)
