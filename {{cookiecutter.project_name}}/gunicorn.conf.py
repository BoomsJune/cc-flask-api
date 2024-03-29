import multiprocessing

bind = '0.0.0.0:5000'
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)

accesslog = '-'
timeout = 60
