import time

debugMode = True  # 调试模式


def log(s):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]\t{str(s)}")


def debug(s):
    if debugMode:
        log("<Debug>" + str(s))
