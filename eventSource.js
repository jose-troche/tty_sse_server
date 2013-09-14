// Run this in browser console
// This should start logging the data pushed from server
var eventSource = new EventSource('http://localhost:1234/')
eventSource.addEventListener('message', function(e){console.log(e.data);}, false);

// To close the connection:
// eventSource.close()

