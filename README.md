# Sistema de Inferencia Difusa (MFIS)

Proyecto realizado para la asignatura de **Inteligencia Artificial** en el segundo curso del Grado en Ingeniería Informática de la **Universidad Carlos III de Madrid**.

**Colaboradores**: Diego San Román Posada, Belén Herranz Campusano e Izan Sánchez Álvaro.

## Descripción

Este repositorio contiene una implementación básica de un *Minimal Fuzzy Inference System* (MFIS). El sistema evalúa el riesgo de concesión de préstamos utilizando lógica difusa. A partir de los valores de cada solicitud y de un conjunto de reglas, el programa calcula el grado de pertenencia de las distintas variables, aplica las reglas y obtiene un nivel de riesgo defuzzificado.

El código carga automáticamente los conjuntos difusos, las reglas y las solicitudes desde ficheros de texto. El resultado de cada solicitud se almacena en `Results.txt`.

## Instalación

1. Instala Python 3.
2. Instala las dependencias necesarias:
   ```bash
   pip install numpy scikit-fuzzy matplotlib
   ```

## Uso

Ejecuta el script principal:

```bash
python main.py
```

Se generará un archivo `Results.txt` con el nivel de riesgo de cada solicitud. También puedes probar el archivo `D06_Source_code.py.py`, que incluye una versión alternativa con reglas más complejas.

## Estructura del proyecto

- `main.py` – Motor principal del sistema difuso.
- `D06_Source_code.py.py` – Versión opcional con evaluación de reglas más elaborada.
- `MFIS_Classes.py` – Definición de clases para conjuntos difusos, reglas y aplicaciones.
- `MFIS_Read_Functions.py` – Funciones de lectura de ficheros (`InputVarSets.txt`, `Risks.txt`, `Applications.txt` y `Rules.txt`).
- `MFIS_Read_Functions_Op.py` – Variante para `Rules_Optional.txt`.
- Ficheros de datos:
  - `InputVarSets.txt` – Conjuntos difusos de entrada (edad, ingresos, etc.).
  - `Risks.txt` – Conjuntos difusos del riesgo de salida.
  - `Applications.txt` – Solicitudes de prueba.
  - `Rules.txt` y `Rules_Optional.txt` – Reglas del sistema.
  - `Results.txt` – Salida generada tras la ejecución.

## Ejemplo de ejecución

Al ejecutar `main.py`, el resultado de la primera solicitud puede tener la siguiente forma (dependiendo de las reglas y valores):

```
Application 0001, Defuzzified Risk Level: <valor>
```

## Contribución

Este proyecto se desarrolló como práctica académica y no está abierto a contribuciones externas, pero puedes usar el código como referencia educativa.

## Licencia

Código disponible únicamente con fines docentes.
