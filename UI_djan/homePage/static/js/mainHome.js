 var info = document.getElementById("testInfo");
 var btn = document.getElementById("homeBtn");

// var pageCounter = 1;
// btn.addEventListener('click', function(){
//     var ourRequest = new XMLHttpRequest();
//     ourRequest.open('GET', 'https://learnwebcode.github.io/json-example/animals-'+pageCounter + '.json');
//     ourRequest.onload = function () {
//         var ourData = JSON.parse(ourRequest.responseText);
//         renderHTML(ourData);
//     };
//     ourRequest.send();
//     pageCounter++;
//     if(pageCounter > 3){
//       info.insertAdjacentHTML('beforeend','There has been an error. Try again');
//     }
//     ourRequest.onerror = function(){
//         info.insertAdjacentHTML('beforeend','There has been an error. Try again');
//     };
//
// }) ;
//
// function renderHTML(ourData){
//     var htmlString = "";
//     for(i = 0; i < ourData.length; i++){
//         htmlString += "<p>" + ourData[i].name + " is a " + ourData[i].species + ".</p>";
//     }//for
//     info.insertAdjacentHTML('beforeend', htmlString);
// }


//  -------------------------------------
btn.addEventListener('click', function(){
    var plcholder = document.getElementById('ans').placeholder;
    var btnres = document.getElementById('ans').value;
    if(btnres == '' || btnres == plcholder)
        console.log('you failed');
    else
        // console.log(btnres);
        var result = callpy(btnres);
        console.log(result)

});
function callpy(input){
    var pyres = $.ajax({
        type: "POST",
        url:'/result',
        async: false,
        data: { mydata: input }
    });
    return pyres.responseText;
}
