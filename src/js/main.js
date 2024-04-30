
// Variables
var sendBtn = document.getElementById('enviar_button');
var textBox = document.getElementById('textbox'); 
var dropdownPuzzle = document.getElementById("dropdownPuzzle");
var chatContainer = document.getElementById('chatContainer');
var imgPrueba = "http://localhost:8080/img/logo_udc_horizontal.png";
var imgFlecha = "http://localhost:8080/img/flecha.png";
var selectedPuzzle = "none";

// Código inicial. Pregunta preprogramada, ejemplo de uso, info, etc.
textBox.value = "";

// Ejemplos de mensajes
setTimeout(() => {
    chatbotEnviarMensaje("Hola, ¿en qué puedo ayudarte?");
    chatbotEnviarImagenes(imgPrueba, "http://localhost:8080/img/logo_fic.jpg");
    userEnviarMensaje("Mensaje de prueba Lorem Ipsum Dolor Sit Amet");
  }, "1000");


//########################   Funciones de chat   ############################

/* Función chatbotEnviarMensaje
*/ 
function chatbotEnviarMensaje(responseMsg){
  var mensaje = creaMensaje("Bot");
  enviaMensaje(mensaje);
  actualizaMensaje(mensaje, responseMsg);
}

/* Función chatbotEnviarImagenes
*/ 
function chatbotEnviarImagenes(startImg, endImg){

    // Creación del elemento mensaje
    var mensaje = document.createElement('div');
    mensaje.classList.add('w-60');
    mensaje.classList.add('float-start');
    mensaje.classList.add('shadow-sm');
    mensaje.style.margin = "10px";
    mensaje.style.padding = "5px";
    mensaje.style.width = "auto";
    mensaje.style.maxWidth = "100%";
    mensaje.style.backgroundColor = "hotpink";
    mensaje.style.borderRadius = "20px";

    // Creación de elementos imagen (estado inicio -> estado final)
    var imagen1 = document.createElement('img');
    imagen1.classList.add('imagen-inicial');
    imagen1.src = startImg;
    imagen1.style.width = "250px";
    imagen1.style.borderRadius = "20px";

    var flecha = document.createElement('img');
    flecha.src = imgFlecha;
    flecha.classList.add('flecha');
    flecha.style.marginInline = "20px";
    flecha.style.width = "50px";

    var imagen2 = document.createElement('img');
    imagen2.src = endImg;
    imagen2.classList.add('imagen-final');
    imagen2.style.width = "250px";
    imagen2.style.borderRadius = "20px";

    // Creación del divisor para ambas imágenes
    var divisor = document.createElement('div');
    divisor.classList.add('divisor_imagenes');
    divisor.appendChild(imagen1);
    divisor.appendChild(flecha);
    divisor.appendChild(imagen2);
    mensaje.appendChild(divisor);

    // Animación del mensaje al entrar en el chat
    mensaje.animate([{easing:"ease-in", opacity:0}, {opacity:1}], {duration:500});

    // Añade mensaje y scroll hacia el último mensaje enviado
    chatContainer.appendChild(mensaje);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/* Función userEnviarMensaje
*/ 
async function userEnviarMensaje(inputMsg){

  // Se coloca el mensaje en el chat
  var mensajeElemUser = creaMensaje("User", inputMsg);
  enviaMensaje(mensajeElemUser);

  // Mientras se recibe, mensaje de carga ...
  var mensajeElemBot = creaMensaje("Bot");
  enviaMensaje(mensajeElemBot);

  // Envía petición AJAX a backend Express
  peticionProcesaMensaje(inputMsg).then((valor) => { 

    // Recibe correctamente, actualiza el mensaje
    actualizaMensaje(mensajeElemBot, valor);

  });


}


//########################   Funciones auxiliares   ############################

/* Función creaMensaje

  Argumentos:
              lado: "User" / "Bot"
              msg: String con mensaje a enviar
*/
function creaMensaje(lado, msg ){


  mensajeElem = document.createElement('div');

  // Estilos comunes
  mensajeElem.classList.add('shadow-sm');
  mensajeElem.classList.add('w-50');
  mensajeElem.style.margin = "10px";
  mensajeElem.style.padding = "5px";
  mensajeElem.style.width = "auto";
  mensajeElem.style.borderRadius = "20px";
  mensajeElem.animate([{easing:"ease-in", opacity:0}, {opacity:1}], {duration:500});

  // Variaciones
  if (lado == "User"){      // Caso Usuario

    mensajeElem.classList.add('float-end');
    mensajeElem.style.backgroundColor = "aliceblue";
    mensajeElem.innerHTML = '<span class="text-end" style="margin: 20px; color: #6f5471">' + msg + '</span>';

  }
  else if (lado == "Bot"){  // Caso Bot
                            // Nota: Por defecto, se dice que está cargando (esta función es síncrona !) Actualizar después de enviar.

    mensajeElem.classList.add('float-start');
    mensajeElem.style.backgroundColor = "hotpink";
    mensajeElem.innerHTML = '<span class="text-start" style= "margin: 20px; padding: 20px; color: #fdb7ff;">Cargando...</span>';

  }

  return mensajeElem;
}

function actualizaMensaje(elementoMensaje, msg){

  try{
    elementoMensaje.classList.add('float-start');
    elementoMensaje.style.backgroundColor = "hotpink";
    elementoMensaje.innerHTML = '<span class="text-start" style= "margin: 20px; padding: 20px; color: #fef0ff;">'+ msg +'</span>';
    elementoMensaje.animate([{easing:"ease-in", opacity:0.4}, {opacity:1}], {duration:500});
  } catch(e){ console.error('ERROR CAPTURADO: actualizaMensaje()\n\t' + e)}
}

function enviaMensaje(elementoMensaje){
  try{

  // Añade mensaje y scroll hacia último mensaje enviado
  chatContainer.appendChild(elementoMensaje);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  } catch(e){ console.error('ERROR CAPTURADO: enviaMensaje()\n\t' + e)}
}

async function peticionProcesaMensaje(mensaje){

  return fetch('/procesa-mensaje', {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message : mensaje,
      puzzle : selectedPuzzle
    })
  }).then(response => { // Caso exitoso

    return response.json();

  }).catch(error => {   // Caso de error -> Aviso

    alert("...Ha habido un error procesando el mensaje, lo sentimos.\n" + error);

  });

}


//#############################   Eventos    ######################################

// Click en el botón ENVIAR 
sendBtn.addEventListener('click', function(evento){

    var inputText = textBox.value;

    if(inputText == ""){            // Input vacío -> aviso
    
      alert("No me has escrito nada en el cuadro de texto. ¿Qué quieres decirme?");
      
    }else{                  

      if(selectedPuzzle == "none"){  // Puzzle sin elegir -> aviso

        alert("Selecciona un puzzle, por favor");
        dropdownPuzzle.style.border="5px solid white";
        dropdownPuzzle.style.transition = "border-color 0.5s ease-in-out";

      }else{                        // El mensaje se envía y se borra el input 

        dropdownPuzzle.style.border="5px transparent";
        userEnviarMensaje(inputText, selectedPuzzle);
        textBox.value = "";
        evento.preventDefault();

      }
    }
});

// Enter en el input -> se envía el texto.
textBox.addEventListener("keyup", function(evento){

    if(evento.key === "Enter"){
        document.getElementById('enviar_button').click();
        evento.preventDefault();
    }

});

// Click opción del dropdown -> se cambia el texto y variable selectedPuzzle
function changeSelectedPuzzle(item) {
  opcion = item.textContent.trim();
  dropdownPuzzle.innerHTML = opcion;
  selectedPuzzle = opcion;
}

