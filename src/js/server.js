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

// Recibe GET a /
app.get("/", function (req, res) {

  console.log("Recibida petición GET a http://localhost:8080/");
  console.log(__dirname);
  res.sendFile(path.join(__dirname, '../', 'index.html'));

});

// Recibe POST a /procesa-mensaje
app.post('/procesa-mensaje', (req, res) => {

  console.log('LOG: POST /procesa-mensaje ${req}');

  const message = req.body.message; // Get the message from the request body

  // Implementa lógica para procesar el mensaje
  
  //const processedMessage = "Processed message: " + message;
  res.send("Llamada POST a procesa-mensaje");
  //res.json({ processedMessage });
});


/*#################  Inicialización del server  ##################*/

// Escuchar en el puerto
app.listen(port, () => console.log(`Server escuchando en puerto ${port},      http://localhost:${port}`));