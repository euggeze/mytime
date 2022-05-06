$("#custom-input-date_from").datepicker({ dateFormat:'dd/mm/yy'});
$("#custom-input-date_to").datepicker({ dateFormat:'dd/mm/yy'});

// ACTIONS
$("input").on("change", function(e) {
  $(this).siblings(".label-error").text("");
  $(this).removeClass("error");
})

$("#custom-input-date_from").on("focusout", function(e) {
  if($(this).val() != '') {
    dateValidation($(this));
  }
})
$("#custom-input-date_to").on("focusout", function(e) {
  if($(this).val() != '') {
    dateValidation($(this));
  }
})
// CHECK
function dateValidation(input) {
  var errorLabel = input.siblings(".label-error");
  var date = input.val();

  input.removeClass("error");
  errorLabel.text("");

  var matches = /^(\d{1,2})[/\/](\d{1,2})[/\/](\d{4})$/.exec(date);
  if (matches == null) {
    input.addClass("error");
  };
  
  var d = matches[1];
  var m = matches[2] - 1;
  var y = matches[3];
  var composedDate = new Date(y, m, d);

  if(composedDate.getDate() == d && composedDate.getMonth() == m && composedDate.getFullYear() == y) {} else {
    input.addClass("error");
    
  }

}
function click_week(){
var curr = new Date;
var first = curr.getDate() - curr.getDay();
var last = first + 6;
var d = new Date(curr.setDate(last));
var curr_date = d.getDate();
var curr_month = d.getMonth() + 1;
var curr_year = d.getFullYear();
if (curr_month<10){
curr_month = "0" + curr_month
}
if (curr_date<10){
curr_date = "0" + curr_date
}
var d0 = new Date(curr.setDate(first));
var start_date = d0.getDate();
var start_month = d0.getMonth() + 1;
if (start_month<10){
start_month = "0" + start_month
}
if (start_date<10){
start_date = "0" + start_date
}
var start_year = d0.getFullYear();
document.getElementById("custom-input-date_from").value = start_date + "/" + start_month + "/" + start_year;
document.getElementById("custom-input-date_to").value = curr_date + "/" + curr_month + "/" + curr_year;
}
function click_2weeks(){
var curr = new Date;
var first = curr.getDate() - curr.getDay()-7;
var last = first + 13;
var d = new Date(curr.setDate(last));
var curr_date = d.getDate();
var curr_month = d.getMonth() + 1;
var curr_year = d.getFullYear();
if (curr_month<10){
curr_month = "0" + curr_month
}
if (curr_date<10){
curr_date = "0" + curr_date
}
var d0 = new Date(curr.setDate(first));
var start_date = d0.getDate();
var start_month = d0.getMonth() + 1;
if (start_month<10){
start_month = "0" + start_month
}
if (start_date<10){
start_date = "0" + start_date
}
var start_year = d0.getFullYear();
document.getElementById("custom-input-date_from").value = start_date + "/" + start_month + "/" + start_year;
document.getElementById("custom-input-date_to").value = curr_date + "/" + curr_month + "/" + curr_year;
}
function click_month(){
var curr = new Date;
var first = curr.getDate() - curr.getDay()-24;
var last = first + 30;
var d = new Date(curr.setDate(last));
var curr_date = d.getDate();
var curr_month = d.getMonth() + 1;
var curr_year = d.getFullYear();
if (curr_month<10){
curr_month = "0" + curr_month
}
if (curr_date<10){
curr_date = "0" + curr_date
}
var d0 = new Date(curr.setDate(first));
var start_date = d0.getDate();
var start_month = d0.getMonth() + 1;
if (start_month<10){
start_month = "0" + start_month
}
if (start_date<10){
start_date = "0" + start_date
}
var start_year = d0.getFullYear();
document.getElementById("custom-input-date_from").value = start_date + "/" + start_month + "/" + start_year;
document.getElementById("custom-input-date_to").value = curr_date + "/" + curr_month + "/" + curr_year;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function delete_func(id_object) {
       $.ajax({
                type: 'POST',
                url: delete_variable,
                data: {'csrfmiddlewaretoken' : getCookie('csrftoken'),  "id": id_object},
                success: function (response) {
                location.reload(true);
                },
                error: function (response) {
                    alert("A deleting data error");
                }
            })
  }


function create_func(id_proj) {
       $.ajax({
                type: 'POST',
                url: create_variable,
                data: {'csrfmiddlewaretoken' : getCookie('csrftoken'),  "id_proj": id_proj},
                success: function (response) {
                location.reload(true);
                },
                error: function (response) {
                    alert("A creating data error");
                }
            })
  }