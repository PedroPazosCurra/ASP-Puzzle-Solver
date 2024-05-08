const { spawn } = require('child_process');
var path = require('path');

/* Función asíncrona procesaMensaje
*/
async function procesaMensaje(mensaje, puzzle){  

  const respuesta = await ejecutaScript(path.join(__dirname, '../py/proceso.py'), mensaje, puzzle);
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

      // Retorno con gestión de errores
      if(code === 0){ resolve(data) }
      else{ reject(new Error(`ERROR: Script de Python. (Cód: ${code})`)); }

    });
  });

}

module.exports = { procesaMensaje };