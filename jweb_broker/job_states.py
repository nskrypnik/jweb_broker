'''This module contains constants with job states

    Jobs workflow looks next:

    IDLE -> OPENED -> IN_PROGRESS -> DONE

    When job is created by some agent the state is always IDLE. Then when jobs
    manager adds a job into a jobs queue it changes the state to OPENED. After
    job is assigned to worker it changes a state to IN_PROGRESS and eventually
    when worker finishes task it put state to DONE
'''

IDLE = 0
DONE = 1
OPENED = 2 # is added to jobs queue
IN_PROGRESS = 3
FAILED = 4
