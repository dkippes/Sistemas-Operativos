# grupo 1

### Integrantes:

| Nombre y Apellido  | Mail                        | usuario Gitlab |
|--------------------|-----------------------------|----------------|
| Diego Kippes       | kippes.diego@gmail.com      | kippes.diego   |  
| Leandro Tittarelli | leandrotittarelli@gmail.com | tittarelli     |


## Entregas:

### Práctica 1:
Aprobada

### Práctica 2:
Aprobada - Está muy bien

### Práctica 3:
Aprobada
#### Detalles:
- Esta muy bien
- Se podría evitar la duplicacion de código:
  
  La sección de código de [la línea 106 a la 109](https://gitlab.com/so-unq-2022-s2/grupo_1/-/blob/main/practica_3/so.py#L106-109) se repite idéntica a la de [la línea 139 a la 142](https://gitlab.com/so-unq-2022-s2/grupo_1/-/blob/main/practica_3/so.py#L139-142) y lo mismo pasa con el código de [las líneas 121 a la 126](https://gitlab.com/so-unq-2022-s2/grupo_1/-/blob/main/practica_3/so.py#L121-126) y [las líneas 152 a la 157](https://gitlab.com/so-unq-2022-s2/grupo_1/-/blob/main/practica_3/so.py#L152-157).

  Sería buena idea refactorizar ese código para implementarlo una única vez en funciones separadas. Asi los handlers `KillInterruptionHandler` e `IoInInterruptionHandler` usan la función que buscan en la ready queue el siguiente y lo ejecutan, y los handlers `NewInterruptionHandler` y `IoOutInterruptionHandler` revisan si hay proceso ejecutando para decidir si mandar el proceso a la CPU o a la ready queue.
  
  Esto también va a hacer mas fácil la modificación del código en el futuro (por ejemplo para verificar prioridades de procesos en los dos handlers que deben revisarla para saber si hay que expropiar)

### Práctica 4:
Aprobada
#### Detalles:
- Esta bastante bien
- En este caso también hay codigo repetido en los handlers que se podría factorizar.
- Estaría bueno tener distintas maneras de correrlo para probar distintos schedulers.
- Los programas no tienen instrucciones de IO. Quizás habría que probarlos para ver que las interrupciones de IO no generan conflictos con los nuevos sechedulers (y en particular con la interrupcion de TIMEOUT).
- No hay problema en usar lazy initialization para la ready queue, pero la forma de hacerlo tradicionalmente es agregar la creación en el `__init__` de la clase. Ejemplo:

```python
    def __init__(self, quantum):
        super().__init__()
        self._ready_queue = ReadyQueue()
        HARDWARE.timer.quantum = quantum
```
- La forma de hacer aging es un poco básica, ya que solo sube la prioridad del último proceso cada N ticks sin importar cuanto tiempo pasó en la ready queue (por ejemplo, puede que haya ejecutado hasta el tick anterior, entra a la ready queue e inmediatamente se cumple el tick de aging y aumenta la prioridad). Para hacerlo correctamente debería contarse el tiempo que lleva cada proceso individualmente en la ready queue (y resetear cuando sale). Además deberia chequearse en todos los procesos, no solo el último.
- Existe una forma mas sencilla de acceder al ultimo [elemento de una lista](https://gitlab.com/so-unq-2022-s2/grupo_1/-/blob/main/practica_4/so.py#L68). En lugar de:

```python
        return queue[len(queue) - 1]
```

se puede escribir:
```python
        return queue[-1:]
```
- En python el valor de verdad de una lista es `True` si tiene elementos o `False` si es vacía. En la [linea 77](https://gitlab.com/so-unq-2022-s2/grupo_1/-/blob/main/practica_4/so.py#L77-78) se podría hacer:

```python
    def is_empty(self):
        return not self._queue
```

### Práctica 5:
Aprobada. Esta muy bien
#### Detalles:
- No encontré detalles 
