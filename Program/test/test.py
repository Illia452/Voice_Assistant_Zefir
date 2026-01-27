threads = {}


while True:
    name = input("name: ")
    thread = input("thread: ")
    worker = input("worker ")

    threads[name] = {"thread":thread, "worker":worker}

    print(threads)