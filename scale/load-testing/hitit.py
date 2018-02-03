"""
Stress the solution with lots of survey submissions.
"""

from os import fork
from time import sleep
from .models import Surveyee()




def main() -> None:
    for i in range(10):
        child_pid = fork()

        if not child_pid:  # child
            pass
        else:  # parent
            sleep(0.25)


if __name__ == '__main__':
    main()
