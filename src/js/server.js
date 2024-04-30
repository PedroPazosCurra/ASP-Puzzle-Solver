/*
  Server
*/

//  Imports y variables
const procesador = require("./procesaMensaje")
const express = require('express');
const cors = require('cors')
var path = require('path');
const app = express();
var router = express.Router();
const port = 8080;


// Módulos Express para funcionalidades extra
app.use(express.json());
app.use(cors());

/*########################  Funciones  ##########################*/

async function procesar(msg, puzzle){

  var mensaje_procesado = await procesador.procesaMensaje(msg, puzzle);

  console.log("Respuesta del procesador (asíncrono):", mensaje_procesado);

  return mensaje_procesado;

}


/*########################  Rutas  ##########################*/

// Routing para elementos estáticos
app.use('/img', express.static(path.join(__dirname, '../../resources/img')));
app.use('/css',express.static(path.join(__dirname, '../css')));
app.use('/js',express.static(__dirname));

// Recibe GET a '/'
app.get("/", function (req, res) {

  // LOG + Envía html 
  console.log("LOG: GET /");
  res.sendFile(path.join(__dirname, '../', 'index.html'));

});

// Recibe POST a '/procesa-mensaje'
app.post('/procesa-mensaje', (req, res) => {

  // Coge mensaje del cuerpo del JSON + LOG
  const msg = req.body.message; 
  const puzzle = req.body.puzzle;
  console.log("LOG: POST /procesa-mensaje: \"%s\" para puzzle: %s ", msg, puzzle);

  // Se procesa el mensaje recibido (nota: es asíncrono) y se responde
  output = procesar(msg, puzzle).then((valor) => {
    res.send(JSON.stringify(output));
  });

});


/*#################  Inicialización del server  ##################*/

// Escuchar en el puerto
app.listen(port, () => console.log(`Server escuchando en puerto ${port},      http://localhost:${port}`))
  .on('error', function(err) {
    if (err.code === 'EADDRINUSE') {
      console.log('ERROR puerto :%d ocupado', port);   
    } 
    else {
        console.log("ERROR no manejado: ", err);   
    } 
  });