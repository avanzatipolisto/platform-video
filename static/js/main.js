document.getElementById("image").addEventListener("change", function(event) {
    let file = event.target.files[0]; // Obtiene el archivo seleccionado
    let divImage = document.getElementById("divImage")
    if (file) {
        let fileName = file.name.toLowerCase(); // Convierte el nombre del archivo a minúsculas
        divImage.textContent =  file.name; 
        let validExtensions = /(\.jpg|\.jpeg|\.png)$/i; // Expresión regular para validar las extensiones
        
        if (!validExtensions.test(fileName)) {
            divImage.innerHTML="<p>Invalid format. Only JPG, JPEG and PNG images are allowed.</p>";
            event.target.value = ""; // Limpia el input file
            return;
        }

        let reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("imageFile").src = e.target.result; // Cambia el src de la imagen
        };
        reader.readAsDataURL(file); // Convierte la imagen a Base64
    }
});
