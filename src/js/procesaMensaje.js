const spawn = require("child_process");

/* Función procesaMensaje
*/
function procesaMensaje(mensaje){    
    
    // Crea un proceso hijo para controlar el código Python. Establece 3 canales [ entrada, salida, error ]
    const pythonProcess = spawn('python', ['procesa_mensaje.py'], { stdio: [ 'pipe', 'pipe', 'pipe' ] });

    // Envía el mensaje al programa Python
    pythonProcess.stdin.write(mensaje);

    // Recibe la respuesta del programa Python y la envía al usuario
    pythonProcess.stdout.on('data', (data) => {

      const response = data.toString();
      console.log('Respuesta del programa Python: ', response);
      chatbotEnviarMensaje(response);

    });
  
    // Caso de error
    pythonProcess.stderr.on('data', (data) => {
      console.error('Python error:', data.toString());
    });
  
    // Cierra el programa Python
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error('Python script exited with error code:', code);
      }
    });

    // Envía imágenes de principio y final
    // chatbotEnviarImagenes(startImg, endImg);
 
}

module.exports = { procesaMensaje };