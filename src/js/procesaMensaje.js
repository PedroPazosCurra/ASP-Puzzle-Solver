const { spawn } = require("child_process");

/* Función asíncrona procesaMensaje
*/
async function procesaMensaje(mensaje, puzzle){    
    
  console.log( "Mensaje:\t%s\nPuzzle:\t%s\n", mensaje, puzzle);

  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("Hola que tal tardé 2 secs");
    }, 2000);
  });

  // Envía imágenes de principio y final
  // chatbotEnviarImagenes(startImg, endImg);
}

module.exports = { procesaMensaje };