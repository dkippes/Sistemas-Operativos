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
    scheduler = RoundRobinScheduler(2)
    kernel = Kernel(scheduler, 4)

    # Ahora vamos a intentar ejecutar 3 programas a la vez
    ##################
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(1)])
    prg2 = Program("prg2.exe", [ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(2)])

    kernel.file_system.write(prg1.name, prg1)
    kernel.file_system.write(prg2.name, prg2)
    kernel.file_system.write(prg3.name, prg3)

    # execute all programs "concurrently"
    kernel.run(prg1.name, 1)
    kernel.run(prg2.name, 2)
    kernel.run(prg3.name, 2)




