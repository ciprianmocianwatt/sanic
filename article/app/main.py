import multiprocessing

from app import get_app

if __name__ == '__main__':
    cpu_cores = multiprocessing.cpu_count()
    sanic_app = get_app()
    sanic_app.run(host="0.0.0.0", port=8000, workers=cpu_cores * 2 + 1)



