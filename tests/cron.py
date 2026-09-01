from app.utils.run_at_time import run_at_time


def a():
    print("a")


run_at_time(59, func=a)
