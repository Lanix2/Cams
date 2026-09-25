# Gato al Pez 🐱🐟

Juego de ritmo pixelart en 2D. Un gato tiene que llegar **exacto** hasta su
pescado cruzando huecos y pinchos. En cada beat pulsas la acción correcta:

- **CAMINA →** para avanzar un paso por el suelo.
- **SALTA ↑** para cruzar un hueco o unos pinchos.

Si te equivocas de acción o fallas el ritmo, el gato se queda sin pescado.
Llega al final del nivel para completarlo.

## Cómo jugar

Es una página web autónoma: abre `index.html` en el navegador (móvil o
escritorio). No necesita instalación ni servidor.

- **Táctil:** botones `SALTA` / `CAMINA`.
- **Teclado:** `ESPACIO` o `↑` para saltar · `→` o `ENTER` para caminar.

## Estructura

- `index.html` — el juego completo (canvas + lógica + estilos, sin dependencias).
- Niveles definidos como cadenas al principio del `<script>`:
  `_` suelo · `o` hueco · `x` pinchos. El primer tile es el gato, el último el pez.

## Añadir niveles

Edita el array `LEVELS` en `index.html`. Cada nivel tiene `name`, `bpm`
(velocidad del ritmo) y `map`. Regla: los obstáculos van siempre aislados
(suelo antes y después) para que el salto caiga seguro.
