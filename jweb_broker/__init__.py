
# Should have:

# Scheduler which listens to job queue and runs workers

# Main broker class which creates all workers, managers and other stuff
from .broker import Broker

# Manager - the process which checks DB for jobs to be added to queue

# Worker - a class which performs some job

# WorkersPool - a pool of workers available for doing some job

# TaskLookup - an abstract class which performs tasks lookup according to job
# data

# Task - an abstract class to subclass a task a worker should do to complete a job

# Uses MongoDB as primary database using Motor async driver for it
