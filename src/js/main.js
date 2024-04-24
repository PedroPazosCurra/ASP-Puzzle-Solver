var sendBtn = document.getElementById('enviar_button');
var textBox = document.getElementById('textbox');
var chatContainer = document.getElementById('chatContainer');
var imgPrueba = "../resources/img/logo_udc_horizontal.png";
var imgFlecha = "../resources/img/flecha.png";

// Código inicial. Pregunta preprogramada, ejemplo de uso, info, etc.
setTimeout(() => {
    chatbotEnviarMensaje("Hola, ¿en qué puedo ayudarte?");
    chatbotEnviarImagenes(imgPrueba, imgPrueba);
    userEnviarMensaje("Mensaje de prueba Lorem Ipsum Dolor Sit Amet");
  }, "1000");

  setTimeout(() => {
    chatbotEnviarMensaje("Mensaje de prueba");
  }, "1000");


// Funciones

/* Función chatbotEnviarMensaje
*/ 
function chatbotEnviarMensaje(responseMsg){

    // Creación del elemento mensaje
    var mensaje = document.createElement('div');
    mensaje.classList.add('float-start');
    mensaje.classList.add('shadow-sm');
    mensaje.classList.add('w-50');
    mensaje.style.margin = "10px";
    mensaje.style.padding = "5px";
    mensaje.style.width = "auto";
    mensaje.style.backgroundColor = "hotpink";
    mensaje.style.borderRadius = "20px";
    mensaje.innerHTML = '<span style= "margin-left: 20px; padding: 20px; color: white;">' + responseMsg + '</span>';

    // Animación al entrar en el chat
    mensaje.animate([{easing:"ease-in", opacity:0}, {opacity:1}], {duration:500});

    // Añade mensaje y scroll hacia último mensaje enviado
    chatContainer.appendChild(mensaje);
    chatContainer.scrollTop = chatContainer.scrollHeight;
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
function userEnviarMensaje(inputMsg){

    // Creación de elemento mensaje
    var mensaje = document.createElement('div');

    mensaje.classList.add('float-end');
    mensaje.classList.add('shadow-sm');
    mensaje.classList.add('w-50');
    mensaje.style.margin = "10px";
    mensaje.style.padding = "5px";
    mensaje.style.backgroundColor = "aliceblue";
    mensaje.style.borderRadius = "20px";
    mensaje.innerHTML = '<p class="text-end" style="margin-right: 70px;">' + inputMsg + '</p>';


    // Animación al entrar en chat
    mensaje.animate([{easing:"ease-in", opacity:0}, {opacity:1}], {duration:500});

    // Añade mensaje y scroll hacia el último mensaje enviado
    chatContainer.appendChild(mensaje);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/* Función procesaMensaje
*/
function procesaMensaje(mensaje){    
    
    // Llamada a la API del LLM
    
    // Comprobación de respuesta, verificación y posible reenvío hasta resultado satisfactorio

    // Envío al solver ASP

    // Envía imágenes de principio y final
    // chatbotEnviarImagenes(startImg, endImg);
 
}

// Ligar Listener al evento click en el botón ENVIAR 
sendBtn.addEventListener('click', function(evento){

    let inputText = textBox.value;

    if(inputText == ""){    // Pulsa el botón sin escribir - aviso por pantalla
        
        alert("No me has escrito nada en el cuadro de texto. ¿Qué quieres decirme?");

    }else{                  // El mensaje se envía, se borra el input y se envía al modelo
        
        userEnviarMensaje(inputText);
        textBox.value = "";
        procesaMensaje(inputText);

    }
});

// Si se pulsa enter en el input, se envía.
textBox.addEventListener("keyup", function(evento){

    if(evento.key === "Enter"){
        document.getElementById('enviar_button').click();
        evento.preventDefault();
    }

});