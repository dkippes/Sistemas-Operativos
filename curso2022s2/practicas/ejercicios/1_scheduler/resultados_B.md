# Resultados del Ejercicio B


| Proceso  | Ráfaga de CPU | Tiempo de Llegada | Prioridad |
| -------- | ------------- | ----------------- | --------- |
| 1        | 6             | 1                 | 4         | 
| 2        | 2             | 2                 | 1         | 
| 3        | 7             | 0                 | 5         | 
| 4        | 5             | 3                 | 2         | 



## FCFS

| Proceso  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|  1       |    |  . |  . |  . |  . |  . |  . |  6 |  5 |  4 |  3 |  2 |  1 |    |    |    |    |    |    |    |    |
|  2       |    |    |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  2 |  1 |    |    |    |    |    |    |
|  3       |  7 |  6 |  5 |  4 |  3 |  2 |  1 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|  4       |    |    |    |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . | 5  | 4  |  3 |  2 |  1 |    |



| Ready Q  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|          |    |  1 |  1 |  1 |  1 |  1 |  1 |  2 |  2 |  2 |  2 |  2 |  2 |  4 |  4 |    |    |    |    |    |    |
|          |    |    |  2 |  2 |  2 |  2 |  2 |  4 |  4 |  4 |  4 |  4 |  4 |    |    |    |    |    |    |    |    |
|          |    |    |    |  4 |  4 |  4 |  4 |    |    |    |    |    |    |

| Proceso  | T. Espera | T. Retorno |
| -------- | --------- | ---------- |
|    1     |     6     |    12      |
|    2     |    11     |    13      |
|    3     |     0     |     7      |
|    4     |    12     |    17      |
| -------- | --------- | ---------- |
| TOTALES  |    29     |     49     |
| PROMEDIO |  **7.25** | **12.25**  |




## SJF

| Proceso  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|    1     |    |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . | 6  | 5  | 4  |  3 |  2 |  1 |    |
|    2     |    |    |  2 |  1 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    | 
|    3     |  7 |  6 |  . |  . |  5 |  4 |  3 |  2 |  1 |    |    |    |    |    |    |    |    |    |    |    |    |
|    4     |    |    |    |  . |  . |  . |  . |  . |  . | 5  | 4  |  3 |  2 |  1 |    |    |    |    |    |    |    |


| Ready Q  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|          |    | 1* |  3 | 3* |  4 |  4 |  4 |  4 |  4 |  3 |  3 |  3 |    |
|          |    |    |  1 |  4 |  1 |  1 |  1 |  1 |  1 |    |    |    |    |
|          |    |    |    |  1 |    |    |    |    |    |    |    |    |    |

*: define FIFO



| Proceso  | T. Espera | T. Retorno |
| -------- | --------- | ---------- |
|    1     |    13     |    19      |
|    2     |     0     |     2      |
|    3     |     2     |     9      |
|    4     |     6     |    11      |
| -------- | --------- | ---------- |
| TOTALES  |    21     |     41     |
| PROMEDIO |  **5.25** | **10.25**  |









## RR (q=3)

| Proceso  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|    1     |    |  . |  . | 6  | 5  | 4  |  . |  . |  . |  . |  . |  . |  . |  . |  3 |  2 |  1 |    |    |    |    |
|    2     |    |    |  . |  . |  . |  . |  2 |  1 |    |    |    |    |    |    |    |    |    |    |    |    |    |
|    3     | 7  | 6  | 5  |  . |  . |  . |  . |  . | 4  |  3 |  2 |  . |  . |  . |  . |  . |  . |  1 |    |    |    |
|    4     |    |    |    |  . |  . |  . |  . |  . |  . |  . |  . | 5  | 4  |  3 |  . |  . |  . |  . |  2 |  1 |    |



| Ready Q  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|          |    |  1 |  1 |  2 |  2 |  2 |  3 |  3 | 4  |  4 | 4  |  1 |  1 |  1 |  3 |  3 |  3 | 4  |    |    |    |
|          |    |    |  2 | 3* |  3 |  3 | 4  |  4 |  1 |  1 |  1 |  3 |  3 |  3 | 4  |  4 | 4  |    |    |    |    |
|          |    |    |    | 4* |  4 |  4 |  1 |  1 |    |    |    |    |    |    |    |    |    |    |    |    |    |

*: asumimos que el contex switch se hace antes de la llegada del nuevo proceso


| Proceso  | T. Espera | T. Retorno |
| -------- | --------- | ---------- |
|    1     |    10     |    16      |
|    2     |     4     |     6      |
|    3     |    11     |    18      |
|    4     |    12     |    17      |
| -------- | --------- | ---------- |
| TOTALES  |    37     |     57     |
| PROMEDIO |  **9.25** | **14.25**  |







## Prio (non-preemptive)


| Proceso  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|    1     |    |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . | 6  | 5  | 4  |  3 |  2 |  1 |    |
|    2     |    |    |  . |  . |  . |  . |  . |  2 |  1 |    |    |    |    |
|    3     | 7  | 6  | 5  | 4  |  3 |  2 |  1 |    |    |    |    |    |    |
|    4     |    |    |    |  . |  . |  . |  . |  . |  . | 5  | 4  |  3 |  2 |  1 |    |    |    |    |    |    |    |


| Ready Q  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|          |    |  1 |  2 |  2 |  2 |  2 |  2 | 4  |  4 |  1 |  1 |  1 |  1 |  1 |    |    |    |    |    |    |    |
|          |    |    |  1 | 4  |  4 | 4  |  4 |  1 |  1 |    |    |    |    |
|          |    |    |    |  1 |  1 |  1 |  1 |    |    |    |    |    |    |


| Proceso  | T. Espera | T. Retorno |
| -------- | --------- | ---------- |
|    1     |    13     |    19      |
|    2     |     5     |     7      |
|    3     |     0     |     7      |
|    4     |     6     |    11      |
| -------- | --------- | ---------- |
| TOTALES  |    24     |     44     |
| PROMEDIO |   **6**   |   **11**   |






## Prio (preemptive)
| Proceso  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|    1     |    | 6  |  . |  . |  . |  . |  . |  . |  . | 5  | 4  |  3 |  2 |  1 |    |    |    |    |    |    |    |
|    2     |    |    |  2 |  1 |    |    |    |    |    |    |    |    |    |
|    3     | 7  |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . |  . | 6  | 5  | 4  |  3 |  2 |  1 |    |
|    4     |    |    |    |  . | 5  | 4  |  3 |  2 |  1 |    |    |    |    |


| Ready Q  |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| -------- |  - |  - |  - |  - |  - |  - |  - |  - |  - |  - | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
|          |    |  3 |  1 | 4  |  1 |  1 |  1 |  1 |  1 |  3 |  3 |  3 |  3 |  3 |    |    |    |    |    |    |    |
|          |    |    |  3 |  1 |  3 |  3 |  3 |  3 |  3 |    |    |    |    |
|          |    |    |    |  3 |    |    |    |    |    |    |    |    |    |



| Proceso  | T. Espera | T. Retorno |
| -------- | --------- | ---------- |
|    1     |     7     |    13      |
|    2     |     0     |     2      |
|    3     |    13     |    20      |
|    4     |     1     |     6      |
| -------- | --------- | ---------- |
| TOTALES  |    21     |     41     |
| PROMEDIO | **5.25**  | **10.25**  |




## Comparación

| Algoritmo                 | T. Espera Promedio | T. Retorno  Promedio |
| ------------------------- | -------------------| -------------------- |
| FCFS                      |       7.25         |      12.50           |
| SJF                       |       5.25         |      10.25           |
| Round Robin (Quantum 3)   |       9.25         |      14.25           |
| Prioridad no-expropiativo |       6            |      11              |
| Prioridad expropiativo    |       5.25         |      10.25           |