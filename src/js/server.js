/*
  Server

  Descripción:   Código encargado de manejar la interfaz del backend. Se encarga de abrir un puerto 
                  para escuchar y recibir las peticiones HTTP del front-end.
*/

//  Imports y variables
const procesador = require("./procesaMensaje")
const limpiador = require("./limpiaTmp")
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

  // Llama a la función asíncrona externa procesaMensaje (espera por el valor)
  return await procesador.procesaMensaje(msg, puzzle);
}

async function limpiar(){

  // Llama a la función externa limpiaTmp()
  limpiador.limpiaTmp();
}


/*########################  Rutas  ##########################*/

// Routing para elementos estáticos
app.use('/img', express.static(path.join(__dirname, '../../resources/img')));
app.use('/tmp', express.static(path.join(__dirname, '../../resources/tmp')));
app.use('/css',express.static(path.join(__dirname, '../css')));
app.use('/js',express.static(__dirname));

// Recibe GET a '/'
app.get("/", function (req, res) {

  // LOG + Envía html 
  console.log("LOG: GET /");
  res.sendFile(path.join(__dirname, '../html/', 'index.html'));

});

// Recibe GET a '/ayuda'
app.get("/ayuda", function (req, res) {

  // LOG + Envía html 
  console.log("LOG: GET /ayuda");
  res.sendFile(path.join(__dirname, '../html/', 'ayuda.html'));

});

// Recibe GET a '/about'
app.get("/about", function (req, res) {

  // LOG + Envía html 
  console.log("LOG: GET /about");
  res.sendFile(path.join(__dirname, '../html/', 'about.html'));

});

// Recibe GET a '/imagen-inicial'
app.get("/imagen-inicial", function (req, res) {

  // LOG + Envía html 
  console.log("LOG: GET /imagen-inicial");
  res.sendFile(path.join(__dirname, '../../resources/tmp/', 'estado_inicial.png'));

});

// Recibe GET a '/imagen-final'
app.get("/imagen-final", function (req, res) {

  // LOG + Envía html 
  console.log("LOG: GET /imagen-final");
  res.sendFile(path.join(__dirname, '../../resources/tmp/', 'solucion.png'));

});

// Recibe DELETE a '/tmp'
app.delete("/tmp", function (req, res) {

  // LOG
  console.log("LOG: DELETE /tmp");
  limpiar();

});

// Recibe POST a '/procesa-mensaje'
app.post('/procesa-mensaje', (req, res) => {

  // Coge mensaje del cuerpo del JSON + LOG
  const msg = req.body.message; 
  const puzzle = req.body.puzzle;
  console.log("LOG: POST /procesa-mensaje: \"%s\" para puzzle: %s ", msg, puzzle);

  // Se procesa el mensaje recibido (nota: es asíncrono) y se responde
  procesar(msg, puzzle).then((valor) => {
    res.send(JSON.stringify(valor));
  });

});


/*#################  Inicialización del server  ##################*/

// Escuchar en el puerto
app.listen(port, () => console.log(`LOG: Server escuchando en puerto ${port}\thttp://localhost:${port}`))
  .on('error', function(err) {
    if (err.code === 'EADDRINUSE') {
      console.log('ERROR puerto :%d ocupado', port);   
    } 
    else {
        console.log("ERROR no manejado: ", err);   
    } 
  });