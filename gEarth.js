// Run in console
// This will move gEarth camera
function moveCamera(evt){
    var ge = tst.ispatial.Canvas.getEarth(),
        lookAt = ge.getView().copyAsLookAt(ge.ALTITUDE_RELATIVE_TO_GROUND),
        movement = evt.data,
        dLat, dLon;

    switch(movement)
    {
        case "Right":
            dLon = 1.0;
            break;
        case "Left":
            dLon = -1.0;
            break;
        case "Up":
            dLat = +1.0;
            break;
        case "Down":
            dLat = -1.0;
            break;
        default:
            return;
    }

    if (dLat)
        lookAt.setLatitude(lookAt.getLatitude() + dLat*5);
    if (dLon)
        lookAt.setLongitude(lookAt.getLongitude() + dLon*5);

    ge.getView().setAbstractView(lookAt);
}

var eventSource = new EventSource('http://localhost:1234/')
eventSource.addEventListener('message', moveCamera, false);

// To close the connection:
// eventSource.close()
