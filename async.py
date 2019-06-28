from selenium import webdriver
import threading
import time
import inspect
import ctypes

def test_func():
    a = 1

t = threading.Thread(target=test_func, args=())

while True:
    if (t.isAlive() == False):
        t.start()

    t._stop()
