
// some constants
const EMPTY = -1;

// to store inputs
var floorW = EMPTY,
    floorH = EMPTY,
    tileW = EMPTY,
    tileH = EMPTY;

// main function, assembling all the others functions in a single routine
// returns false everytime
function updateInformation(){
    if (!retrieveInputData())
        return false;
    
    // TODO

    return false;
}

// dom functions

// update input variables from the dom form
// returns true if the values are all numerically not empty (see constants list), 
//         false otherwise
function retrieveInputData(){
    floorW = parseInt(document.getElementById("floorW").value);
    floorH = parseInt(document.getElementById("floorH").value);
    tileW  = parseInt(document.getElementById("tileW").value);
    tileH  = parseInt(document.getElementById("tileH").value);
    
    return (floorW > EMPTY) && (floorW > EMPTY) && (floorW > EMPTY) && (floorW > EMPTY);
}

// clear all input field values at dom form and update input variables
// returns false everytime
function clearAllFields(){
    document.getElementById("floorW").value = "";
    document.getElementById("floorH").value = "";
    document.getElementById("tileW").value  = "";
    document.getElementById("tileH").value  = "";

    return false;
}

// calculation functions

// amount of tiles you gonna need
function calcTiles(){

}

// how many of them will be sliced
function calcSlices(){

}

// quantity of slices that can be reused
function calcReusedSlices(){

}

// best orientation for the tiles
function calcBestOrientations(){

}
