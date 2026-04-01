import re # regex tokenizer

class SQLComplexityAnalyzer:
    complexity_score = {
        "num_conditions":0.5,
        "num_joins": 1.0, "num_group_by": 1.0, "nesting_depth": 1.0,
        "num_ctes": 2.0, "num_subqueries": 2.0, "num_window_functions": 2.0
    }

    antipattern_penalties = {
        "too_many_joins": 2.0,
        "high_nesting": 1.5, "missing_where": 1.5,
        "uses_select_star": 1.0, "unbounded_order_by": 1.0
    }

    # Rough fix. @TODO
    ANTIPATTERN_KEYS = { "uses_select_star", "missing_where", "too_many_joins", "has_subquery_no_join", 
                        "unbounded_order_by", "high_nesting",  "many_window_functions" }
    FEATURE_KEYS = {"num_joins", "num_ctes", "num_group_by", "num_window_functions", "num_subqueries", "num_conditions", "nesting_depth",
                    "estimated_operator_count", "estimated_plan_depth", "actual_operator_count", "actual_plan_depth", "complexity_score", "sql_token_count"}
        
    def count_sql_features(self, sql: str) -> dict:
        sql_upper = sql.upper()

        return {
            "num_joins": sql_upper.count("JOIN"),
            "num_ctes": sql_upper.count("WITH"),
            "num_group_by": sql_upper.count("GROUP BY"),
            "num_window_functions": sql_upper.count("OVER"),
            "num_subqueries": max(sql_upper.count("SELECT") - 1, 0),
            "num_conditions": sql_upper.count("WHERE") + sql_upper.count("CASE"),
            "nesting_depth": self._estimate_nesting_depth(sql_upper),
        }

    def score_sql_features(self, features: dict) -> float:
        score = 0.0
        for k, weight in self.complexity_score.items():  # fixed name
            score += features.get(k, 0) * weight
        return round(score, 4)

    # Matches SQL identifiers, numbers, operators, punctuation, and keywords
    def count_tokens(self, sql: str) -> int:
        tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+|[<>!=]=|[<>]|[\(\),.*]", sql)
        return len(tokens)

    def analyze(self, sql: str) -> dict:
        features = self.count_sql_features(sql)
        score = self.score_sql_features(features)
        tokens = self.count_tokens(sql)

        plan_metrics = self._estimate_plan_metrics(sql)
        anti_patterns = self.detect_anti_patterns(sql)
        antipatt_score = self.score_anti_patterns(anti_patterns)

        return {
            "features": {**features, **plan_metrics, "complexity_score": score, "sql_token_count": tokens},
            "antipatterns": {**anti_patterns, "antipattern_penalty": antipatt_score}
        }
    
    def detect_anti_patterns(self, sql: str) -> dict:
        sql_upper = sql.upper()

        return {
            "uses_select_star": "SELECT *" in sql_upper, # Scans unnecessary columns, kills column pruning
            "missing_where": ( # (excluding aggregations) Scanning entire dataset 
                "WHERE" not in sql_upper and
                "GROUP BY" not in sql_upper and
                not any(agg in sql_upper for agg in ["COUNT(", "SUM(", "AVG(", "MIN(", "MAX("])
            ),
            "too_many_joins": sql_upper.count("JOIN") > 3,  # Causes exponential blow-up risk
            "has_subquery_no_join": sql_upper.count("SELECT") > 1 and "JOIN" not in sql_upper, # Less efficient than join
            "unbounded_order_by": "ORDER BY" in sql_upper and "LIMIT" not in sql_upper, # 
            "high_nesting": self._estimate_nesting_depth(sql_upper) > 3,
            "many_window_functions": sql_upper.count("OVER") > 2,
        }
    
    def score_anti_patterns(self, patterns: dict) -> float:
        score = 0.0
        for k, v in patterns.items():
            if v:
                score += self.antipattern_penalties.get(k, 0)

        return score

    # -------------------------------------
    # Helpers

    '''
    Estimates are guessed roughly based on heuristic operators
    Not accurate, but is consistent across engines. Useful for:
    - relative comparisons
    - when the engine doesn't support runtime metrics
    '''

    def _estimate_nesting_depth(self, sql_upper: str) -> int:
        depth = max_depth = 0
        for char in sql_upper:
            if char == "(":
                depth += 1
                max_depth = max(max_depth, depth)
            elif char == ")":
                depth -= 1
        return max_depth
    
    def _estimate_plan_metrics(self, sql: str) -> dict:
        sql_upper = sql.upper()

        operator_count = (
            sql_upper.count("JOIN") +
            sql_upper.count("WHERE") +
            sql_upper.count("GROUP BY") +
            sql_upper.count("ORDER BY") +
            sql_upper.count("UNION") +
            sql_upper.count("OVER") +        # window ops
            sql_upper.count("DISTINCT") +
            1  # base scan
        )

        plan_depth = self._estimate_nesting_depth(sql_upper)

        return {
            "estimated_operator_count": operator_count,
            "estimated_plan_depth": plan_depth
        }
    
    # Helpers END
    # -------------------------------------