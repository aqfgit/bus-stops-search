function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



// const jsonData = {from: 'roztropice, mleczarnia', to: 'jaworze, dolne wiarus'}
// var formattedJsonData = JSON.stringify( jsonData  );
const inputFrom = document.getElementById('from')
const inputTo = document.getElementById('to')
const searchButton = document.getElementById('search')

searchButton.addEventListener('click', searchBusStops)

function searchBusStops() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
        });

    const jsonData = {from: inputFrom.value, to: inputTo.value}
    const formattedJsonData = JSON.stringify(jsonData);

    $.ajax('http://localhost:8000/bus-search', {
        type : 'POST',
        contentType : 'application/json',
        data : formattedJsonData,
        success: function (data) {
            console.log(data)
        },
        cache: false
    })
}

