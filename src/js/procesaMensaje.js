const { spawn } = require('child_process');
var path = require('path');

/* Función asíncrona procesaMensaje
*/
async function procesaMensaje(mensaje, puzzle){  

  const respuesta = await ejecutaScript(path.join(__dirname, '../procesa_mensaje.py'), mensaje, puzzle);
  return(respuesta);
  
}

/* Función asíncrona ejecutaScript
*/
async function ejecutaScript(path, mensaje, puzzle) {

  const procesoPython = spawn('python', [path, mensaje, puzzle]);

  var data = '';
  procesoPython.stdout.on('data', (stdout) => {
    data += stdout.toString();
  });

  // Error
  procesoPython.stderr.on('data', (stderr) => {
    console.error(`stderr: ${stderr}`);
  });

  // Script finalizado
  return new Promise((resolve, reject) => {
    procesoPython.on('close', (code) => {

      // Debug
      console.log(`LOG: Proceso hijo Python finaliza con cód. ${code}`);
      console.log('La salida del programa python es: ' + data);

      // Retorno con gestión de errores
      if(code === 0){ resolve(data) }
      else{ reject(new Error(`ERROR: Script de Python. (Cód: ${code})`)); }

    });
  });

}

module.exports = { procesaMensaje };