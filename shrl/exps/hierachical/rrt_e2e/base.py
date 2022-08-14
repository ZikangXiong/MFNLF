import os
from typing import Dict

import pandas as pd

from shrl.config import get_path
from shrl.envs import get_env
from shrl.envs.difficulty import choose_level
from shrl.evaluation.model import load_model
from shrl.evaluation.simulation import simu
from shrl.plan import Planner
from shrl.plan.common.plot import plot_path_2d

ALGO = "rrt_e2e"


def evaluate(env_name,
             n_rollout: int = 1,
             n_steps: int = 1000,
             level: int = 1,
             planning_algo: str = "rrt*",
             planner_max_iter: int = 200,
             planning_algo_kwargs: Dict = {},  # noqa
             arrive_radius: float = 0.1,
             render: bool = False,
             check_plan: bool = False
             ):
    model = load_model(env_name, algo=ALGO)
    env = get_env(env_name)
    choose_level(env, level)
    planner = Planner(env, planning_algo)

    i = 0
    running_data = {
        "total_step": [],
        "goal_met": [],
        "collision": [],
        "reward_sum": []
    }
    while i < n_rollout:
        env.reset()
        path = planner.plan(planner_max_iter, **planning_algo_kwargs)
        if check_plan:
            plot_path_2d(planner.algo.search_space, path, planner.algo.tree)
        if len(path) == 0:
            continue

        res = simu(env=env,
                   model=model,
                   n_steps=n_steps,
                   path=path,
                   arrive_radius=arrive_radius,
                   render=render)
        for k in res:
            running_data[k].append(res[k])
        i += 1

    stat = pd.DataFrame(running_data)

    res_dir = get_path(robot_name=env.robot_name, algo=ALGO, task="evaluation") + f"/{planning_algo}"
    os.makedirs(res_dir, exist_ok=True)
    stat.to_csv(res_dir + f"/{level}.csv")
    print("results are saved to:", res_dir + f"/{level}.csv")

    print(stat)
    return stat
