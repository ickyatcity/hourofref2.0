
function getParameterByName(name, url) {
    if (!url) {
      url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
   
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
       
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}




var ctrlAddItem = function(){
	var formvalue;
	formvalue = getParameterByName('q')
	console.log(formvalue)
 }();


 function mySubmitFunction()
{
    formvalue = getParameterByName('q')
    if (formvalue == "") {
        alert("Name must be filled out");
        return false;
    }
}