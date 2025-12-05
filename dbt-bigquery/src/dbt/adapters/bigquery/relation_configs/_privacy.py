from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from dbt_common.dataclass_schema import dbtClassMixin, StrEnum


class JoinCondition(StrEnum):
    JOIN_ALL = "JOIN_ALL"
    JOIN_ANY = "JOIN_ANY"
    JOIN_BLOCKED = "JOIN_BLOCKED"
    JOIN_NOT_REQUIRED = "JOIN_NOT_REQUIRED"


@dataclass
class JoinRestrictionPolicyConfig(dbtClassMixin):
    join_condition: JoinCondition
    join_allowed_columns: List[str] = field(default_factory=list)


@dataclass
class AggregationThresholdPolicyConfig(dbtClassMixin):
    threshold: int
    privacy_unit_column: str


@dataclass
class DifferentialPrivacyPolicyConfig(dbtClassMixin):
    privacy_unit_column: str
    max_epsilon_per_query: float
    epsilon_budget: float
    delta_per_query: float
    delta_budget: float
    max_groups_contributed: Optional[int] = None


@dataclass
class PrivacyPolicyConfig(dbtClassMixin):
    aggregation_threshold_policy: Optional[AggregationThresholdPolicyConfig] = None
    differential_privacy_policy: Optional[DifferentialPrivacyPolicyConfig] = None
    join_restriction_policy: Optional[JoinRestrictionPolicyConfig] = None
