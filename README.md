# Gato al Pez 🐱🐟

Puzzle de plataformas 2D pixelart. Programas un **bucle de hasta 4 acciones**
y el gato las repite al ritmo hasta llegar **exacto** a su pescado.

## Mecánica

Rellena las ranuras con acciones y pulsa **EJECUTAR**. El programa se repite
en bucle:

- **→ MOVER** — avanza 1 casilla.
- **↑ SALTAR** — sube encima de una caja, o cruza 2 casillas de un salto.
- **⚔ ATACAR** — rompe la caja o el bicho que tiene enfrente.

Obstáculos:

- **Caja** (`#`): la subes de un salto o la rompes atacando.
- **Pinchos** (`x`) y **bichos** (`b`): matan si caes sobre ellos.
- **Hueco** (`o`): hay que saltarlo.

Como el salto avanza **2** casillas, puedes pasarte del pez y perder: hay que
llegar **exacto**.

## Cómo jugar

Página web autónoma: abre `index.html` (móvil o escritorio), sin instalación.

- **Táctil:** botones MOVER / SALTAR / ATACAR para llenar el bucle, y EJECUTAR.
- **Teclado:** `→` mover · `↑`/`ESPACIO` saltar · `A` atacar · `ENTER` ejecutar · `RETROCESO` borrar.

## Estructura

- `index.html` — juego completo (canvas + lógica + estilos, sin dependencias).
- 15 niveles en el array `LEVELS`. Cada columna:
  `C` gato · `_` suelo · `o` hueco · `x` pinchos · `b` bicho · `#` caja · `F` pez.

Todos los niveles están verificados por fuerza bruta: tienen solución con un
bucle de 4 acciones o menos.
