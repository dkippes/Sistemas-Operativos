# Paginación
## Práctica: Esquema de Traducción


## Solucion Ejercicio 2



- Espacio de direcciones lógico: Con 5 bits puedo direccionar 32 bytes
m = **5**


- Tamaño de página: Con 3 bits puedo direccionar 8 bytes o “instrucciones”
n = **3**

p = m - n = **2**

Dirección Lógica: **01100** --> Pagina: **01**     Desplazamiento: **100**

Mirando la Page Table vemos que la página "1" (01 en binario) está cargada en el Frame "3" (11 en binario)     

Dirección Física -->  Frame + Desplazamiento = 11 + 100  = **11100** --> **INST_2**



