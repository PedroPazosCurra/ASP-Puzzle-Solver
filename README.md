# ASP-Puzzle-Solver

Este es el repositorio para mi Trabajo de Fin de Grado en Ingeniería Informática.  

- [ASP-Puzzle-Solver](#asp-puzzle-solver)
  * [¿Qué es?](#qué-es)
  * [¿Cómo funciona?](#cómo-funciona)
  * [Tecnologías Usadas](#tecnologías-usadas)
  * [Instalación](#instalación)
  * [Documentación](#documentación)


## ¿Qué es?
El cometido del proyecto es el desarrollo de una **interfaz Web** que permita a un usuario **resolver diversos tipos de puzzles** interactuando con el programa a través de un cómodo **chat**.  

![enter image description here](https://cdn.kometia-static.com/blog/2017/11/06182228/chatbots.jpg)  

## ¿Cómo funciona?

**El usuario debe introducir, por mensaje, el estado de un puzzle** que desee resolver, así como las diferentes restricciones y reglas aplicadas al rompecabezas en cuestión. A más específico e informativo, mejor. El mensaje es entonces procesado por un **LLM** ([Large Language Model](https://en.wikipedia.org/wiki/Large_language_model)). El modelo de lenguaje tendrá el menester de *traducir* la entrada de lenguaje natural a **ASP** ([Answer Set Programming](https://en.wikipedia.org/wiki/Answer_set_programming)). El programa ASP se encargará de resolver el problema, ya codificado, y el LLM explicará al usuario la salida del **solver**, a través de una respuesta en el chat.  

Este sistema, mediante una aproximación **neuro-simbólica**, simbiotiza la ágil capacidad inferencial de un Modelo de Lenguaje Extenso con el razonamiento fuerte propio de Answer Set Programming.  

![enter image description here](https://cdn.reludi.com/media/post-images/types-of-puzzle-games.jpg)  

## Tecnologías Usadas
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![Express.js](https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

## Instalación

El programa usa [node.js](https://developer.ibm.com/tutorials/learn-nodejs-installing-node-nvm-and-vscode/), por lo que deberá ser instalado en el sistema previamente.

Primero, debes preparar el entorno haciendo doble click en **setup**

Con todo listo, puedes ejecutar el servidor haciendo doble click en run_[Sistema Operativo] según el SO que estés usando.  Se abrirá la consola de comandos con el servidor ejecutándose y una ventana de tu navegador predeterminado con la página de ASP Puzzle Solver lista para que la uses.

## Documentación
A disposición de quien lo considere de interés, dejo un enlace a la memoria del presente trabajo: (...)  



