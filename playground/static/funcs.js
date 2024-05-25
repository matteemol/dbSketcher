//test function for mock buttons
function callfuncs() {
    alert("Click!");
}

// When form is submitted, execute the /sketch route in the python app
function handleSubmit(event) {
    event.preventDefault();
// get the form data as a JSON object
    const data = new FormData(event.target);
    const value = Object.fromEntries(data.entries())
    console.log(value);
// call the python function, passing the form data as a JSON object
    fetch('/sketch', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(value)
    }).then(response => response.json()) //receive a JSON object
        .then(data => {
            console.log(data['uml']);
// replace the text of the second textarea with the uml Output
            document.getElementById("uml").value = data['uml'];
});
}

// Adjust the size of the generated PNG to the cell
function adjust_size(elementId) {
    document.getElementById(elementId).style.width="100%";
    document.getElementById(elementId).style.height="100%";
    document.getElementById(elementId).style.objectFit="contain";
}

// Generate the PlantUML link to work with
function generate_link() {
    text = document.getElementById('uml').value;
    // console.log("text="+text);
    cjCall("com.plantuml.api.cheerpj.v1.Info", "encode", text).then((res) => {
        console.log("res="+res);
        url = "https://www.plantuml.com/plantuml/uml/" + res;
        document.getElementById('plant-link').setAttribute('href', url);
    });
}

// Create the PNG image out from the umlOutput text
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
// Visualize the buttons and sketch
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

// Load the PlantUML Engine
function loadEngine() {
    cheerpjInit({disableLoadTimeReporting:false,disableErrorReporting:false}).then( (val0) => {
        cheerpjRunMain("com.plantuml.api.cheerpj.v1.RunInit", "/app/static/plantuml-core.jar", "/app/static/", "debugjava").then ( (val1) => {
            console.log("Engine started");
            document.getElementsByClassName('loading-state')[0].style.visibility="hidden";
        });
    });
}