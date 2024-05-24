var shortlink = "";

function callfuncs() {
    alert("Click!");
}

function handleSubmit(event) {
    event.preventDefault();

    const data = new FormData(event.target);
//    const value = data.get('csv');
    const value = Object.fromEntries(data.entries())
    console.log(value);

    fetch('/sketch', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(value)
    }).then(response => response.text)
        .then(text => console.log(text) );

        // do something with response here... 
        console.log(response.text())
        console.log(response.umlOutput)
//    });

}

/*
function sketch_it(data) {
  
//    const formData = new FormData(document.forms("form_csv"));
//    console.log($('form')[0][0]);
/*
    fetch("/sketch", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: $('form')
    })
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log(text)
    });
/*

    var request = new XMLHttpRequest();
    request.onload = function() {
        // We could do more interesting things with the response
        // or, we could ignore it entirely
        alert(request.responseText);
        console.log(request.responseText)
//        document.getElementById("uml").value = "Some new text"
    };
    // We point the request at the appropriate command
    request.open("POST", "/sketch", true);
    // and then we send it off
    request.send();
}
*/

function adjust_size(elementId) {
    document.getElementById(elementId).style.width="100%";
    document.getElementById(elementId).style.height="100%";
    document.getElementById(elementId).style.objectFit="contain";
}
    
function generate_link() {
    text = document.getElementById('uml').value;
    // console.log("text="+text);
    cjCall("com.plantuml.api.cheerpj.v1.Info", "encode", text).then((res) => {
        console.log("res="+res);
        shortlink = res;
        url = "https://www.plantuml.com/plantuml/uml/" + res;
        document.getElementById('plant-link').setAttribute('href', url);
    });
}

function createPNG() {
    text = document.getElementById('uml').value;
    console.log("text="+text);
    document.getElementsByClassName('visualizing-state')[0].style.visibility="visible";
    cjCall("com.plantuml.api.cheerpj.v1.Png", "convertToBlob", "light", text, "/files/result.png").then((res) => {
        document.getElementsByClassName('visualizing-state')[0].style.visibility="hidden";
        console.log("png res="+res);
        cjFileBlob("result.png").then((blob) => {
            blob_dir = window.URL.createObjectURL(blob);
            console.log("blob_dir="+blob_dir);
            document.getElementById('render-image').src = blob_dir;
            document.getElementById('diagram').setAttribute('href', blob_dir);
        });
        document.getElementsByClassName('render-text')[0].style.visibility="visible";
        document.getElementsByClassName('render-button')[0].style.visibility="visible";
        adjust_size('render-image');
    });
}

/*
function createSVG() {
    text = document.getElementById('uml').value;
    console.log("text="+text);
    cjCall("com.plantuml.api.cheerpj.v1.Svg", "convert", "light", text).then((res) => {
        console.log("svg res="+res);
        document.getElementById('colb').innerHTML=res;
        document.getElementsByClassName('render-button')[0].style.visibility="visible";
        adjust_size('colb');
    });
}
*/

function loadEngine() {
    cheerpjInit({disableLoadTimeReporting:false,disableErrorReporting:false}).then( (val0) => {
        cheerpjRunMain("com.plantuml.api.cheerpj.v1.RunInit", "/app/static/plantuml-core.jar", "/app/static/", "debugjava").then ( (val1) => {
            console.log("Engine started");
            document.getElementsByClassName('loading-state')[0].style.visibility="hidden";
        });
    });
}