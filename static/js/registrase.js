

$(document).ready(function(){
  console.log('->',$('[name=error]').val());
  if($('[name=error]').val() == "1")
  {
    resaltar();

    $('[name=mes-error]').text()
  }
});



function resaltar(){
  $('#Peticiones input').each(
    (a, b) => {if (b.value==""){
      $(b).css("border-color","red");
    }}
  );
  
  
}