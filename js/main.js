

var sendBtn = document.getElementById('enviar_button');
var textBox = document.getElementById('textbox');
var chatContainer = document.getElementById('chatContainer');


chatbotSendMessage("Hola, ¿en qué puedo ayudarte?");

function chatbotSendMessage(responseMsg){

    var messageElement = document.createElement('div');
    messageElement.classList.add('w-50');
    messageElement.classList.add('float-start');
    messageElement.classList.add('shadow-sm');
    messageElement.style.margin = "10px";
    messageElement.style.padding = "5px";
    messageElement.style.backgroundColor = "hotpink";
    messageElement.style.borderRadius = "20px";

    messageElement.innerHTML = "<span>Bot:  </span>" + 
      "<span style=" + "margin-top: 10px; padding: 10px;" + ">" + responseMsg + "</span>";

    chatContainer.appendChild(messageElement);
}


function sendMessage(inputMsg){

    var messageElement = document.createElement('div');
    messageElement.classList.add('w-50');
    messageElement.classList.add('float-end');
    messageElement.classList.add('shadow-sm');
    messageElement.style.margin = "10px";
    messageElement.style.padding = "5px";
    messageElement.style.backgroundColor = "aliceblue";
    messageElement.style.borderRadius = "20px";

    messageElement.innerHTML = "<span>Yo:</span>" + 
      "<span style=" + "margin-top: 10px; padding: 10px;" + ">" + inputMsg + "</span>";

    chatContainer.appendChild(messageElement);

}

sendBtn.addEventListener('click', function(e){

    let inputText = textBox.value;

    if(inputText == ""){
        alert("No me has escrito nada en el cuadro de texto. ¿Qué quieres decirme?");
    }else{
        sendMessage(inputText);
        inputText.value = "";
    }
});