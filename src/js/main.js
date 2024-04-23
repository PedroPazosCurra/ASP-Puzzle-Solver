var sendBtn = document.getElementById('enviar_button');
var textBox = document.getElementById('textbox');
var chatContainer = document.getElementById('chatContainer');
var imgPrueba = "https://www.udc.es/export/sites/udc/identidadecorporativa/_galeria_imgs/logoUDC375x250.png_820558358.png"
var imgFlecha = "../resources/img/flecha.png";

// Código inicial. Pregunta preprogramada, ejemplo de uso, info, etc.
setTimeout(() => {
    chatbotEnviarMensaje("Hola, ¿en qué puedo ayudarte?");
    chatbotEnviarImagen(imgPrueba);
  }, "1000");


// Funciones

/* Función chatbotEnviarMensaje
*/ 
function chatbotEnviarMensaje(responseMsg){

    // Creación del elemento mensaje
    var mensaje = document.createElement('div');
    mensaje.classList.add('w-50');
    mensaje.classList.add('float-start');
    mensaje.classList.add('shadow-sm');
    mensaje.style.margin = "10px";
    mensaje.style.padding = "5px";
    mensaje.style.backgroundColor = "hotpink";
    mensaje.style.borderRadius = "20px";
    mensaje.innerHTML = "<span style=" + "margin-top: 10px; padding: 10px;" + ">" + responseMsg + "</span>";

    // Animación del mensaje al entrar en el chat
    mensaje.animate([{easing:"ease-in", opacity:0}, {opacity:1}], {duration:500});

    // Añade mensaje y scroll hacia el último mensaje enviado
    chatContainer.appendChild(mensaje);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/* Función chatbotEnviarImagen
*/ 
function chatbotEnviarImagen(responseImg){

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
    imagen1.src = responseImg;
    imagen1.style.width = "250px";
    imagen1.style.borderRadius = "20px";

    var flecha = document.createElement('img');
    flecha.src = imgFlecha;
    flecha.classList.add('flecha');
    flecha.style.marginInline = "20px";
    flecha.style.width = "50px";

    var imagen2 = document.createElement('img');
    imagen2.src = responseImg;
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
function userEnviarMensaje(inputMsg){

    var mensaje = document.createElement('div');
    mensaje.classList.add('w-50');
    mensaje.classList.add('float-end');
    mensaje.classList.add('shadow-sm');
    mensaje.style.margin = "10px";
    mensaje.style.padding = "5px";
    mensaje.style.backgroundColor = "aliceblue";
    mensaje.style.borderRadius = "20px";

    mensaje.innerHTML = "<span style=" + "margin-left: 10px; margin-top: 10px; padding: 10px;" + ">" + inputMsg + "</span>";

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