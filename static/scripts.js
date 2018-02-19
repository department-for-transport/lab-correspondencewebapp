


var slidenumber = 0

function ShowSlide(n){
  slidenumber+=n;
  console.log(slidenumber)
  if (slidenumber<0){slidenumber=0}
  $('.mySlides').css("visibility", "hidden")
  $('.loader').css("visibility", "visible")
  $('#sender').val("");
  $('#date').val("");
  $('#email').val("");
  $('#post').val("");
  $('#caseid').html("");

  $.getJSON(Flask.url_for("getcase"), {number: slidenumber})
  .done(function(data) {
    console.log('done')
    console.log(data.name)
    console.log($('#correspondence_img'))
    $('#correspondence_img').attr("src", "https://storage.googleapis.com/chapterimages/"+data.image_name)
    $('#sender').val(data.name);
    $('#date').val(data.date);
    $('#email').val(data.email);
    $('#post').val(data.post);
    $('#caseid').html("Case " + data.id);
    $('.loader').css("visibility", "hidden");
    $('.mySlides').css("visibility", "visible");
  });
};


function grabunit() {
  query = $('#parliamentaryquestion').val()
  $.getJSON(Flask.url_for("getunit"), {question: query})
  .done(function(data) {
    $('#unit1').val(data.unit1)
    $('#unit2').val(data.unit2)
  })
};

$(function(){
  ShowSlide(1);
});
