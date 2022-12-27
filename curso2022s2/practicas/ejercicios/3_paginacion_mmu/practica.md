# Paginación
## Práctica: Esquema de Traducción


Dada la siguiente configuración:

Administración de Memoria : **Paginación**

Memoria Física de **32 Bytes** (cada instrucción ocupa 1 Byte)

Memoria Principal (física)

| Celda   |  Valor | 
| -----   | ------ | 
| 00000   | INST_a | 
| 00001   | INST_b | 
| 00010   | INST_c | 
| 00011   | INST_d | 
| 00100   | INST_e | 
| 00101   | INST_f | 
| 00110   | INST_g | 
| 00111   | INST_h | 
| 01000   | INST_i | 
| 01001   | INST_j | 
| 01010   | INST_k | 
| 01011   | INST_l | 
| 01100   | INST_m | 
| 01101   | INST_n | 
| 01110   | INST_o | 
| 01111   | INST_p | 
| 10000   | INST_q | 
| 10001   | INST_r | 
| 10010   | INST_s | 
| 10011   | INST_t | 
| 10100   | INST_u | 
| 10101   | INST_v | 
| 10110   | INST_w |
| 10111   | INST_x | 
| 11000   | INST_y | 
| 11001   | INST_z | 
| 11010   | INST_0 | 
| 11011   | INST_1 | 
| 11100   | INST_2 | 
| 11101   | INST_3 |
| 11110   | INST_4 | 
| 11111   | INST_5 | 




## Ejercicio 1


Frame Size: **4  Bytes**

Page Table del proceso en CPU

| Frame |
|  ---- |
|  010  |
|  011  |
|  000  |
|  001  |


si el PC del CPU es **01101**

Que instruccion se ejecutara en el próximo ciclo (tick) ?


- [Resultados del Ejercicio 1](./resultados_1.md)


## Ejercicio 2

Frame Size: **8  Bytes**

Page Table del proceso en CPU

| Frame |
|  ---- |
|   10  |
|   11  |
|   00  |
|   01  |


si el PC del CPU es **01100**

Que instruccion se ejecutara en el próximo ciclo (tick) ?


- [Resultados del Ejercicio 2](./resultados_2.md)



## Ejercicio 3



Frame Size: **2  Bytes**

Page Table del proceso en CPU

| Frame |
|  ---- |
|  0010 |
|  0101 |
|  1000 |
|  1101 |


si el PC del CPU es **00110**

Que instruccion se ejecutara en el próximo ciclo (tick) ?


- [Resultados del Ejercicio 3](./resultados_3.md)
