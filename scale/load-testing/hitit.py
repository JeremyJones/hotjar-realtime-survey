"""
Stress the solution with lots of survey submissions.
"""

from os import fork
from time import sleep
from models import Surveyee


def submit_survey() -> None:

    surv = Surveyee()
    surv.random_go()


def main() -> None:
    for i in range(10000):
        child_pid = fork()

        if not child_pid:  # child
            submit_survey()
            exit()
        else:  # parent
            sleep(0.55)


if __name__ == '__main__':
    main()
