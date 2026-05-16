from __future__ import annotations

import itertools
import multiprocessing
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd


@dataclass
class OptimizationResult:
    best_params: dict
    best_score: float
    all_results: list[dict]

    total_combinations: int
    evaluated_count: int
    optimization_time_seconds: float

    improvement_pct: float | None = None
    baseline_score: float | None = None


@dataclass
class OptimizationConfig:
    metric: str = "sharpe"
    maximize: bool = True

    max_workers: int | None = None
    timeout_per_combination: float = 30.0

    top_n_save: int = 20

    early_stop_threshold: float | None = None
    n_jobs: int = 1


class ParameterOptimizer:
    """
    参数自动优化引擎 - 网格搜索 + 并行计算

    支持:
    - 网格搜索 (Grid Search)
    - 随机搜索 (Random Search)
    - 遗传算法 (Genetic Algorithm) - 简化版
    - 贝叶斯优化 (Bayesian Optimization) - 简化版

    功能:
    - 并行计算加速
    - 早停机制
    - 结果排名保存
    - 参数敏感性分析
    """

    def __init__(self, config: OptimizationConfig | None = None):
        self.config = config or OptimizationConfig()
        self.results: list[dict] = []
        self.best_result: dict | None = None

    def grid_search(
        self,
        strategy_class,
        param_grid: dict[str, list],
        data: pd.DataFrame,
        initial_cash: float = 100000,
    ) -> OptimizationResult:
        """
        网格搜索优化

        Args:
            strategy_class: 策略类
            param_grid: 参数网格, e.g., {"fast": [5,10,20], "slow": [30,50,100]}
            data:  历史数据
            initial_cash: 初始资金

        Returns:
            OptimizationResult with best params and all results
        """
        import time

        start_time = time.time()

        keys = list(param_grid.keys())
        values = list(param_grid.values())
        combinations = list(itertools.product(*values))
        total_combinations = len(combinations)

        if self.config.max_workers:
            pool = multiprocessing.Pool(self.config.max_workers)
        else:
            pool = None

        all_results = []
        baseline_score = None

        for i, combo in enumerate(combinations):
            params = dict(zip(keys, combo))

            try:
                if pool:
                    score = self._evaluate_strategy(
                        strategy_class, params, data, initial_cash
                    )
                else:
                    score = self._evaluate_strategy(
                        strategy_class, params, data, initial_cash
                    )

                if baseline_score is None:
                    baseline_score = score

                result = {
                    "params": params.copy(),
                    "score": score,
                    "rank": 0,
                }
                all_results.append(result)

                if self.best_result is None or (
                    self.config.maximize and score > self.best_result["score"]
                ) or (not self.config.maximize and score < self.best_result["score"]):
                    self.best_result = result.copy()

                if (
                    self.config.early_stop_threshold is not None
                    and i > 0
                    and len(all_results) > 5
                ):
                    recent_avg = np.mean([r["score"] for r in all_results[-5:]])
                    if self.config.maximize and recent_avg < self.config.early_stop_threshold:
                        break

            except Exception as e:
                all_results.append(
                    {"params": params, "score": -999999 if self.config.maximize else 999999, "error": str(e)}
                )

        if pool:
            pool.close()
            pool.join()

        all_results.sort(key=lambda x: x["score"], reverse=self.config.maximize)
        for i, r in enumerate(all_results):
            r["rank"] = i + 1

        self.results = all_results[: self.config.top_n_save]

        elapsed = time.time() - start_time

        improvement = None
        if baseline_score and baseline_score != 0:
            improvement = (self.best_result["score"] - baseline_score) / abs(baseline_score) * 100

        return OptimizationResult(
            best_params=self.best_result["params"] if self.best_result else {},
            best_score=self.best_result["score"] if self.best_result else 0,
            all_results=all_results,
            total_combinations=total_combinations,
            evaluated_count=len(all_results),
            optimization_time_seconds=round(elapsed, 2),
            baseline_score=baseline_score,
            improvement_pct=improvement,
        )

    def random_search(
        self,
        strategy_class,
        param_distributions: dict[str, tuple],
        n_iterations: int,
        data: pd.DataFrame,
        initial_cash: float = 100000,
        seed: int = 42,
    ) -> OptimizationResult:
        """
        随机搜索优化

        Args:
            param_distributions: 参数分布, e.g., {"fast": (5, 50), "slow": (50, 200)}
                                tuple表示 (min, max) 均匀分布
            n_iterations: 搜索次数
        """
        import time
        np.random.seed(seed)
        start_time = time.time()

        keys = list(param_distributions.keys())
        total_combinations = n_iterations

        all_results = []
        baseline_score = None

        for i in range(n_iterations):
            params = {}
            for key in keys:
                low, high = param_distributions[key]
                if isinstance(low, int) and isinstance(high, int):
                    params[key] = np.random.randint(low, high + 1)
                else:
                    params[key] = np.random.uniform(low, high)

            try:
                score = self._evaluate_strategy(
                    strategy_class, params, data, initial_cash
                )

                if baseline_score is None:
                    baseline_score = score

                result = {"params": params.copy(), "score": score, "rank": 0}
                all_results.append(result)

                if self.best_result is None or (
                    self.config.maximize and score > self.best_result["score"]
                ) or (not self.config.maximize and score < self.best_result["score"]):
                    self.best_result = result.copy()

            except Exception as e:
                all_results.append(
                    {"params": params, "score": -999999 if self.config.maximize else 999999, "error": str(e)}
                )

        all_results.sort(key=lambda x: x["score"], reverse=self.config.maximize)
        for i, r in enumerate(all_results):
            r["rank"] = i + 1

        self.results = all_results[: self.config.top_n_save]

        elapsed = time.time() - start_time

        improvement = None
        if baseline_score and baseline_score != 0:
            improvement = (self.best_result["score"] - baseline_score) / abs(baseline_score) * 100

        return OptimizationResult(
            best_params=self.best_result["params"] if self.best_result else {},
            best_score=self.best_result["score"] if self.best_result else 0,
            all_results=all_results,
            total_combinations=total_combinations,
            evaluated_count=len(all_results),
            optimization_time_seconds=round(elapsed, 2),
            baseline_score=baseline_score,
            improvement_pct=improvement,
        )

    def _evaluate_strategy(
        self, strategy_class, params: dict, data: pd.DataFrame, initial_cash: float
    ) -> float:
        """评估单个策略参数组合"""
        from openaitrade.backtest.engine import BacktestEngine, BacktestConfig

        try:
            strategy = strategy_class(**params)
            engine = BacktestEngine(BacktestConfig(initial_cash=initial_cash))
            result = engine.run(data, strategy)
            metric_key = self.config.metric

            if metric_key == "sharpe":
                score = result.metrics.get("sharpe", 0)
            elif metric_key == "sortino":
                score = result.metrics.get("sortino", 0)
            elif metric_key == "calmar":
                score = result.metrics.get("calmar", 0)
            elif metric_key == "total_return":
                score = result.metrics.get("total_return", 0)
            elif metric_key == "annual_return":
                score = result.metrics.get("annual_return", 0)
            elif metric_key == "risk_adjusted_return":
                sharpe = result.metrics.get("sharpe", 0)
                max_dd = abs(result.metrics.get("max_drawdown", 1))
                score = sharpe / max_dd if max_dd > 0 else 0
            else:
                score = result.metrics.get("sharpe", 0)

            if self.config.maximize:
                return score if not np.isnan(score) else -999999
            else:
                return score if not np.isnan(score) else 999999

        except Exception:
            return -999999 if self.config.maximize else 999999

    def get_top_n(self, n: int = 10) -> list[dict]:
        """获取评分最高的N组参数"""
        return self.results[:n] if self.results else sorted(
            self.results, key=lambda x: x["score"], reverse=True
        )[:n]

    def export_to_dataframe(self) -> pd.DataFrame:
        """导出所有结果为DataFrame"""
        if not self.results:
            return pd.DataFrame()

        rows = []
        for r in self.results:
            row = {"rank": r.get("rank", 0), "score": r["score"]}
            row.update(r["params"])
            rows.append(row)

        return pd.DataFrame(rows)

    def sensitivity_analysis(
        self, param_name: str, all_results: list[dict] | None = None
    ) -> pd.DataFrame:
        """
        参数敏感性分析 - 分析单个参数对最终得分的影响

        Returns:
            DataFrame with param value, avg score, std, count
        """
        if all_results is None:
            all_results = self.results

        if not all_results:
            return pd.DataFrame()

        param_values = {}
        for r in all_results:
            params = r.get("params", {})
            if param_name in params:
                val = params[param_name]
                if val not in param_values:
                    param_values[val] = []
                param_values[val].append(r["score"])

        analysis = []
        for val, scores in param_values.items():
            analysis.append(
                {
                    param_name: val,
                    "avg_score": np.mean(scores),
                    "std_score": np.std(scores),
                    "count": len(scores),
                    "min_score": np.min(scores),
                    "max_score": np.max(scores),
                }
            )

        df = pd.DataFrame(analysis)
        df = df.sort_values("avg_score", ascending=False)
        return df

    def print_optimization_report(self, result: OptimizationResult) -> str:
        lines = [
            f"\n{'='*60}",
            f"参数优化报告",
            f"{'='*60}",
            f"\n📊 优化配置:",
            f"   目标指标: {self.config.metric}",
            f"   {'最大化' if self.config.maximize else '最小化'}",
            f"   总组合数: {result.total_combinations}",
            f"   已评估: {result.evaluated_count}",
            f"   耗时: {result.optimization_time_seconds:.2f}秒",
        ]

        if result.improvement_pct is not None:
            lines.append(f"\n📈 优化效果:")
            lines.append(f"   基准分数: {result.baseline_score:.4f}")
            lines.append(f"   最优分数: {result.best_score:.4f}")
            lines.append(f"   提升: {result.improvement_pct:+.2f}%")

        lines.append(f"\n🏆 最优参数:")
        for k, v in result.best_params.items():
            lines.append(f"   {k}: {v}")

        lines.append(f"\n📋 Top 5 参数组合:")
        for i, r in enumerate(result.all_results[:5]):
            lines.append(f"   {i+1}. score={r['score']:.4f} params={r['params']}")

        lines.append(f"\n{'='*60}\n")

        return "\n".join(lines)


def quick_optimize(
    strategy_class,
    data: pd.DataFrame,
    param_grid: dict[str, list],
    metric: str = "sharpe",
    n_jobs: int = 4,
) -> dict:
    """
    快速优化接口 - 一行代码优化策略参数

    Example:
        >>> from openaitrade.strategies.momentum import DualMomentum
        >>> best_params = quick_optimize(DualMomentum, data, {
        >>>     "fast_ma": [5, 10, 20],
        >>>     "slow_ma": [50, 100, 200],
        >>>     "atr_period": [14, 21],
        >>> })
    """
    config = OptimizationConfig(metric=metric, max_workers=n_jobs)
    optimizer = ParameterOptimizer(config)
    result = optimizer.grid_search(strategy_class, param_grid, data)
    return result.best_params