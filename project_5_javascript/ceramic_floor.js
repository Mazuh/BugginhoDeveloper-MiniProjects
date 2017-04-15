
// constants here
const EMPTY = -1;

// to store some input data
var floorW = EMPTY,
    floorH = EMPTY,
    tileW  = EMPTY,
    tileH  = EMPTY;

// to store information
var eachTileArea = tileW  * tileH,
    floorArea    = floorW * floorH;

// main function, assembling all the others functions in a single routine
// returns false everytime
function updateInformation(){
    if (!retrieveInputData())
        return false;
    
    calcAreas();
    
    // TODO
    calcTiles();

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

// calculation functions, they're all assuming that stored variables are already sanitized

// calculate and store in global variables the areas of the whole and each tile
function calcAreas(){
    eachTileArea = tileW  * tileH;
    floorArea    = floorW * floorH;
}

// amount of tiles you gonna need
// also update dom output fields
function calcTiles(){
    // TODO: can it be converted into a closed form instead of a loop? maybe using ceiling or floor
    var n = 0;
    while(n*eachTileArea < floorArea){
        n++;
    }

    document.getElementById("tilesQtt").innerHTML = n;
}

// how many of them will be sliced
function calcSlices(){
    //var tilesQtt = parseInt(document.getElementById("tilesQtt").innerHTML);
}

// quantity of slices that can be reused
function calcReusedSlices(){

}

// best orientation for the tiles
function calcBestOrientations(){

}
