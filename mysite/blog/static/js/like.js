// function api_like() {
//     let api_url = '1/api_like/';
//     let btn_txt = document.getElementById("like");
//     let request = new XMLHttpRequest();
//     request.onreadystatechange = function () {
//         if (request.readyState === 4 && request.status === 200) {
//             let received_data = JSON.parse(request.responseText);
//             btn_txt.innerText = received_data.like;
//             }
//         }
//     request.open("GET", api_url);
//     request.send();
// }