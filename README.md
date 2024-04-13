# ASP-Puzzle-Solver

Este es el repositorio para mi Trabajo de Fin de Grado en Ingeniería Informática.

## ¿Qué es?
El cometido del proyecto es el desarrollo de una **interfaz Web** que permita a un usuario **resolver diversos tipos de puzzles** interactuando con el programa a través de un cómodo **chat**.

![enter image description here](https://cdn.kometia-static.com/blog/2017/11/06182228/chatbots.jpg)
## ¿Cómo funciona?
**El usuario debe introducir, por mensaje, el estado de un puzzle** que desee resolver, así como las diferentes restricciones y reglas aplicadas al rompecabezas en cuestión. A más específico e informativo, mejor. El mensaje es entonces procesado por un **LLM** ([Large Language Model](https://en.wikipedia.org/wiki/Large_language_model)). El modelo de lenguaje tendrá el menester de *traducir* la entrada de lenguaje natural a **ASP** ([Answer Set Programming](https://en.wikipedia.org/wiki/Answer_set_programming)). El programa ASP se encargará de resolver el problema, ya codificado, y el LLM explicará al usuario la salida del **solver**, a través de una respuesta en el chat.
![enter image description here](https://cdn.reludi.com/media/post-images/types-of-puzzle-games.jpg)

