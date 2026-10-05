# Gato al Pez 🐱🐟

Puzzle de plataformas 2D pixelart. Programas un **bucle de hasta 4 acciones**
y el gato las repite al ritmo hasta llegar **exacto** a su pescado.

## Mecánica

Rellena las ranuras con acciones y pulsa **EJECUTAR**. El programa se repite
en bucle:

- **→ MOVER** — avanza 1 casilla.
- **↑ SALTAR** — sube encima de una caja, o cruza 2 casillas de un salto.
- **🐾 ZARPAZO** — rompe la caja, o mata al bicho que tiene enfrente.

Obstáculos:

- **Caja** (`#`): la subes de un salto o la rompes atacando.
- **Pinchos** (`x`): matan si caes sobre ellos.
- **Bicho verde** (`b`): mata al contacto y **no se puede saltar**; solo se mata con el zarpazo.
- **Hueco** (`o`): hay que saltarlo.

Como el salto avanza **2** casillas, puedes pasarte del pez y perder: hay que
llegar **exacto**. Y si le das un **zarpazo al pez**, también pierdes.

## Ranuras

Cada bloque de 10 niveles añade **una ranura de acción** más (de 4 en el nivel 1
hasta 13 en el 100). La complejidad de cada bloque se adapta a ese presupuesto:
la solución mínima crece de ~2 acciones al principio hasta ~8, y los mapas se
alargan hacia el final.

## Cómo jugar

Página web autónoma: abre `index.html` (móvil o escritorio), sin instalación.

- **Táctil:** botones MOVER / SALTAR / ATACAR para llenar el bucle, y EJECUTAR.
- **Teclado:** `→` mover · `↑`/`ESPACIO` saltar · `A` atacar · `ENTER` ejecutar · `RETROCESO` borrar.

## Estructura

- `index.html` — juego completo (canvas + lógica + estilos, sin dependencias).
- 100 niveles en el array `LEVELS`. Cada columna:
  `C` gato · `_` suelo · `o` hueco · `x` pinchos · `b` bicho · `#` caja · `F` pez.

Todos los niveles están verificados por fuerza bruta: tienen solución con un
bucle de 4 acciones o menos.
