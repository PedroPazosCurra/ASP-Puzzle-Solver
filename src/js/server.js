/*
  Server
*/

//  Requerimientos y constantes
const express = require('express');
const cors = require('cors')
var path = require('path');
const app = express();
const port = 8080;
var router = express.Router();

// Módulos para funcionalidades extra
app.use(express.json());
app.use(cors());

// Routing para elementos estáticos
app.use('/img', express.static(path.join(__dirname, '../../resources/img')));
app.use('/css',express.static(path.join(__dirname, '../css')));
app.use('/js',express.static(__dirname));

/*########################  Rutas  ##########################*/

// Recibe GET a '/'
app.get("/", function (req, res) {

  // LOG + Envía html 
  console.log("LOG: GET /");
  res.sendFile(path.join(__dirname, '../', 'index.html'));

});

// Recibe POST a '/procesa-mensaje'
app.post('/procesa-mensaje', (req, res) => {

  // Coge mensaje del cuerpo del JSON + LOG
  const message = req.body.message; 
  console.log("LOG: POST /procesa-mensaje: \"%s\" ", message);


  // Implementa lógica para procesar el mensaje
  
  // Responde
  res.json({message});
});


/*#################  Inicialización del server  ##################*/

// Escuchar en el puerto
app.listen(port, () => console.log(`Server escuchando en puerto ${port},      http://localhost:${port}`))
  .on('error', function(err) {
    if (err.code === 'EADDRINUSE') {
      console.log('ERROR puerto :%d ocupado', port);   
    } 
    else {
        console.log("ERROR ", err);   
    } 
  });