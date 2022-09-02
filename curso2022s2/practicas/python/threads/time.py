#!/usr/bin/python3
import _thread
import time


# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: #%s - %s" % ( threadName, count, time.ctime(time.time()) ))
   print ("%s: END ------------------ %s" % ( threadName, time.ctime(time.time()) ))



def main():
   print_time("Thread-1", 0.5)
   print_time("Thread-2", 0.5)


# Código estándar para llamar main() cuando arranxca en programa.
if __name__ == '__main__':
    main()   