from so import *
import log


##
##  MAIN 
##
if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    ## setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(25)

    ## Switch on computer
    HARDWARE.switchOn()

    ## new create the Operative System Kernel
    # "booteamos" el sistema operativo
    scheduler = RoundRobinScheduler(3)
    kernel = Kernel(scheduler)

    # Ahora vamos a intentar ejecutar 3 programas a la vez
    ##################
    prg1 = Program("prg1.exe", [ASM.CPU(6)])
    prg2 = Program("prg2.exe", [ASM.CPU(10)])
    prg3 = Program("prg2.exe", [ASM.CPU(5)])

    # execute all programs "concurrently"
    kernel.run(prg1, 1)
    kernel.run(prg2, 2)
    kernel.run(prg3, 2)




