
// some constants
const EMPTY = -1;

// to store inputs
var floorW = EMPTY,
    floorH = EMPTY,
    tileW = EMPTY,
    tileH = EMPTY;

// main function, assembling all the others functions in a single routine
function updateInformation(){
    if (!retrieveInputData())
        return false;
    
    // TOOD

    return false;
}

// update input variables from the html form
// returns true if the values are all numerically not empty (see constants list), 
//         false otherwise
function retrieveInputData(){
    floorW = parseInt(document.getElementById("floorW").value);
    floorH = parseInt(document.getElementById("floorH").value);
    tileW  = parseInt(document.getElementById("tileW").value);
    tileH  = parseInt(document.getElementById("tileH").value);
    
    return (floorW > EMPTY) && (floorW > EMPTY) && (floorW > EMPTY) && (floorW > EMPTY);
}
