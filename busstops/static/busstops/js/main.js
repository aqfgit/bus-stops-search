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

const inputFrom = document.getElementById('from');
const inputTo = document.getElementById('to');
const searchButton = document.getElementById('search');
const dataWrap = document.getElementById('tableData');

searchButton.addEventListener('click', makeAJAXRequestToSerachForBusStops)

function makeAJAXRequestToSerachForBusStops() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
        });

    const jsonData = {from: inputFrom.value, to: inputTo.value};
    const formattedJsonData = JSON.stringify(jsonData);

    $.ajax('http://localhost:8000/bus-search', {
        type : 'POST',
        content: 'application/json',
        data : formattedJsonData,
        success: function (data) {
            displayData(data);
        },
        cache: false
    })
}

function createDynamicTableTemplate(row) {
    return `
       <tr>
           <td>${row.time_start}</td>
           <td>${row.time_end}</td>
           <td>${row.info}</td>
       </tr>
    `;
   }

function displayData(data) {
    jsonData = JSON.parse(data)

    if ((jsonData.error_msg !== undefined) && (jsonData.error_msg !== null)) {
        dataWrap.innerHTML = `<h2>${jsonData.error_msg}</h2>`
    } else {
        dataWrap.innerHTML = `
        <h2>Połączenie ${inputFrom.value} - ${inputTo.value}</h2>
        <table>
            <tr>
                <th>Odjazd</th>
                <th>Przyjazd</th>
                <th>Informacje</th>
            </tr>
           ${jsonData.map(createDynamicTableTemplate).join('')}
        </table>
    `;
    }
}

