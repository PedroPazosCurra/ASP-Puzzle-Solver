

var sendBtn = document.getElementById('enviar_button');
var textBox = document.getElementById('textbox');
var chatContainer = document.getElementById('chatContainer');

// Código inicial. Pregunta preprogramada, ejemplo de uso, info, etc.
setTimeout(() => {
    chatbotEnviarMensaje("Hola, ¿en qué puedo ayudarte?");
  }, "1000");
  
// Funciones

/* Función chatbotEnviarMensaje
*/ 
function chatbotEnviarMensaje(responseMsg){

    var mensaje = document.createElement('div');
    mensaje.classList.add('w-50');
    mensaje.classList.add('float-start');
    mensaje.classList.add('shadow-sm');
    mensaje.style.margin = "10px";
    mensaje.style.padding = "5px";
    mensaje.style.backgroundColor = "hotpink";
    mensaje.style.borderRadius = "20px";

    mensaje.innerHTML = "<span style=" + "margin-top: 10px; padding: 10px;" + ">" + responseMsg + "</span>";

    mensaje.animate([{easing:"ease-in", opacity:0}, {opacity:1}], {duration:500});

    chatContainer.appendChild(mensaje);

    // Scroll hacia el último mensaje enviado
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/* Función userEnviarMensaje
*/ 
function userEnviarMensaje(inputMsg){

    var mensaje = document.createElement('div');
    mensaje.classList.add('w-50');
    mensaje.classList.add('float-end');
    mensaje.classList.add('shadow-sm');
    mensaje.style.margin = "10px";
    mensaje.style.padding = "5px";
    mensaje.style.backgroundColor = "aliceblue";
    mensaje.style.borderRadius = "20px";

    mensaje.innerHTML = "<span style=" + "margin-top: 10px; padding: 10px;" + ">" + inputMsg + "</span>";

    mensaje.animate([{easing:"ease-in", opacity:0}, {opacity:1}], {duration:500});

    chatContainer.appendChild(mensaje);

    // Scroll hacia el último mensaje enviado
    chatContainer.scrollTop = chatContainer.scrollHeight;

}

/* Función procesaMensaje
*/
function procesaMensaje(mensaje){    
    
    // Llamada a la API del LLM
    
    // Comprobación de respuesta, verificación y posible reenvío hasta resultado satisfactorio

    // Envío al solver ASP
 
}

/* Ligar Listener al evento click en el botón ENVIAR
*/ 
sendBtn.addEventListener('click', function(e){

    let inputText = textBox.value;

    if(inputText == ""){
        // Pulsa el botón sin escribir - aviso por pantalla
        alert("No me has escrito nada en el cuadro de texto. ¿Qué quieres decirme?");
    }else{
        // El mensaje se imprime en el chat y se borra la caja de texto
        userEnviarMensaje(inputText);
        textBox.value = "";

        // El mensaje se entrega al modelo para recibir una respuesta.
        procesaMensaje(inputText);
    }
});