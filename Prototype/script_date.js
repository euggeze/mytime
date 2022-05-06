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