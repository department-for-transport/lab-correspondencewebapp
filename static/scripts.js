


var slidenumber = 0

function ShowSlide(n){
  slidenumber+=n;
  console.log(slidenumber)
  if (slidenumber<0){slidenumber=0}
  $('#correspondence_img').css("visibility", "hidden")
  $('#correspondence_img').attr("src","")
  console.log('heloooo')
  $('#loader').addClass("loader")
  $('#sender').val("");
  $('#date').val("");
  $('#email').val("");
  $('#post').val("");
  $('#casenumber').val("");
  $('#to').val("");
  $('.form-control').removeClass('correctform');


  $.getJSON(Flask.url_for("getcase"), {number: slidenumber})
  .done(function(data) {
    $('#correspondence_img').attr("src", "https://storage.googleapis.com/chapterimages/"+data.image_name)
    $('#sender').val(data.name);
    if ($('#sender').val().length > 0){
      $('#sender').addClass('correctform')
    };
    $('#date').val(data.date);
    if ($('#date').val().length > 0){
      $('#date').addClass('correctform');
    };
    $('#email').val(data.email);
    if ($('#email').val().length > 0){
      $('#email').addClass('correctform');
    };
    $('#post').val(data.post);
    if ($('#post').val().length > 0){
      $('#post').addClass('correctform');
    };
    $('#to').val(data.to);
    if ($('#to').val().length >0){
      $('#to').addClass('correctform');
    };
    $('#casenumber').val(data.id);
    $('#loader').removeClass("loader");
    $('#correspondence_img').css("visibility", "visible");
  });
};


function grabunit() {
  $('.pqbox').each(function(){
    var div = $(this)
    div.children('.unitbox').remove()
    $.getJSON(Flask.url_for("getunit"), {question: $(this).text()})
    .done(function(data) {
      console.log(div.text())
      console.log(data.unit1)
      console.log(data.unit2)
      div.append("<div class='unitbox'>" +'SGD Classifier: ' + data.unit1 + "</div>")
      div.append("<div class='unitbox'>" +'Neural Net: ' + data.unit2 + "</div>")
    });
  });
};

function checkunit() {
  query = $('#question').val()
  $.getJSON(Flask.url_for("getunit"), {question: query})
    .done(function(data) {
      $('.unitbox').remove()
      console.log(data.unit1)
      console.log(data.unit2)
      $('.pqbox').append("<div class='unitbox'>" +'SGD Classifier: ' + data.unit1 + "</div>")
      $('.pqbox').append("<div class='unitbox'>" +'Neural Net: ' + data.unit2 + "</div>")

    });
};

function getpqs() {
  $('.pqholder').empty();
  $.getJSON(Flask.url_for("getpqs"))
  .done(function(data) {
    pqholder = $('.pqholder')
    for (var key in data){
      console.log('okay')
      pqholder.append("<div class='namebox'>" +key + "</div>");
      pqholder.append("<div class='pqbox'>" +data[key]+ "</div>");
    }
  })
};

function customquestion() {
  $('.pqholder').empty();
  $('.pqholder').append("<div class='form-group pqbox'> <input type='text' class='form-control' id='question' placeholder='Enter question'> <input type='button' class='btn btn-block btn-success' onclick='checkunit()' id ='getpq' value='Get unit'>");
};

$(function(){
  ShowSlide(1);
});
