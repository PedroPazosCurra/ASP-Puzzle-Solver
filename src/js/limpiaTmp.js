const { spawn } = require('child_process');
var path = require('path');

/* Función asíncrona limpiaTmp
*/
async function limpiaTmp(){  

  ejecutaScript(path.join(__dirname, '../py/limpia_tmp.py'));
  
}

/* Función asíncrona ejecutaScript
*/
async function ejecutaScript(path) {

  // Ejecuta el proceso Python
  const procesoPython = spawn('python', [path], {encoding: 'utf-8' });

  // Recoge la salida
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
      if(code === 0){ 

        // Por ahora no me queda otra que gestionar así los status entre Py y JS
        estado_y_salida = data.split("|")
        resolve(estado_y_salida) 

      }
      else{ reject(new Error(`ERROR: Script de Python. (Cód: ${code})`)); }

    });
  });
}

module.exports = {limpiaTmp};