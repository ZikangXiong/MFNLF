from shrl.exps.check_results import print_all_results
from shrl.exps.no_planner.cpo.base import evaluate

ENV_NAME = "Doggo-eval"


def e2e():
    for i in range(1, 4):
        evaluate(ENV_NAME,
                 n_rollout=100,
                 level=i,
                 render=False,
                 n_steps=i * i * 1000)


if __name__ == '__main__':
    # e2e()
    print_all_results(ENV_NAME, "cpo")
