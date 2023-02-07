

function checkFileSize(theInput) {
    let parentDiv = document.getElementById('messageFileSizeDisapproved');
    if (parentDiv.hasChildNodes()){
        parentDiv.removeChild(parentDiv.firstChild);
    }
    
    if (theInput.files[0].size > 582000){
        
        let theP = document.createElement('p');
        theP.innerText = "Your image file is too big. Maximum image size: 582'000 bytes";
        parentDiv.append(theP);
        theInput.value= ""
    } else{
       
        if (parentDiv.hasChildNodes()) {
            parentDiv.removeChild(parentDiv.firstChild);
        }
    }
}
