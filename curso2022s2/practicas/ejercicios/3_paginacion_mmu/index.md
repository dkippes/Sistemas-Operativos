# Paginación
## Práctica: Esquema de Traducción


- [Ejercicios Prácticos](./practica.md)




Dada la siguiente configuración:


Administración de Memoria : **Paginación**

Memoria Física de **16 Bytes** (cada instrucción ocupa 1 Byte)

Memoria Principal (física)

| Celda  |  Valor | 
| -----  | ------ | 
| 0000   | INST_a | 
| 0001   | INST_b | 
| 0010   | INST_c | 
| 0011   | INST_d | 
| 0100   | INST_e | 
| 0101   | INST_f | 
| 0110   | INST_g | 
| 0111   | INST_h | 
| 1000   | INST_i | 
| 1001   | INST_j | 
| 1010   | INST_k | 
| 1011   | INST_l | 
| 1100   | INST_m | 
| 1101   | INST_n | 
| 1110   | INST_o | 
| 1111   | INST_p | 


Frame Size: **2  Bytes**

Page Table del proceso en CPU

| Frame |
| ---   |
|  010  |
|  001  |
|  011  |
|  000  |


si el PC del CPU es **0101**

Que instruccion se ejecutara en el próximo ciclo (tick) ?


## Solución:


- Espacio de direcciones lógico: Con 4 bits puedo direccionar 16 bytes
m = **4**


- Tamaño de página: Con 1 bit puedo direccionar 2 bytes o “instrucciones”
n = **1**

p = m - n = **3**

Dirección Lógica: **0101** --> Pagina: **010**     Desplazamiento: **1**

Mirando la Page Table vemos que la página "2" (010 en binario) está cargada en el Frame "3" (011 en binario)     

Dirección Física -->  Frame + Desplazamiento = 011 + 1  = **0111** --> **INST_h**
