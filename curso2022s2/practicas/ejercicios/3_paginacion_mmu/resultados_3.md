# Paginación
## Práctica: Esquema de Traducción


## Solucion Ejercicio 3


- Espacio de direcciones lógico: Con 5 bits puedo direccionar 32 bytes
m = **5**


- Tamaño de página: Con 1 bit puedo direccionar 2 bytes o “instrucciones”
n = **1**

p = m - n = **4**

Dirección Lógica: **00110** --> Pagina: **0011**     Desplazamiento: **0**

Mirando la Page Table vemos que la página "3" (0011 en binario) está cargada en el Frame "13" (1101 en binario)     

Dirección Física -->  Frame + Desplazamiento = 1101 + 0  = **11010** --> **INST_0**



