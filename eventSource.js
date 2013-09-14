// Run this in browser console:
var eventSource = new EventSource('http://localhost:1234/')
eventSource.addEventListener('message', function(e){console.log(e.data);}, false);

// This should start logging the data pushed from server


// To close the connection:
// eventSource.close()
