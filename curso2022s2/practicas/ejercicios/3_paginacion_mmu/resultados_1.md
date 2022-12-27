# Paginación
## Práctica: Esquema de Traducción


## Solucion Ejercicio 1


- Espacio de direcciones lógico: Con 5 bits puedo direccionar 32 bytes
m = **5**


- Tamaño de página: Con 2 bits puedo direccionar 4 bytes o “instrucciones”
n = **2**

p = m - n = **3**

Dirección Lógica: **01101** --> Pagina: **011**     Desplazamiento: **01**

Mirando la Page Table vemos que la página "3" (011 en binario) está cargada en el Frame "1" (001 en binario)     

Dirección Física -->  Frame + Desplazamiento = 001 + 01  = **00101** --> **INST_f**


