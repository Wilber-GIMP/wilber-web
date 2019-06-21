function do_like(asset_id){


  request = $.ajax({
    type: "GET",
    url: "/api/asset/"+asset_id+"/like/",
  });

  request.done(function (response, textStatus, jqXHR){

  alert('Liked');
      });
  request.fail(function (jqXHR, textStatus, errorThrown){

  alert('Erro');
      });

}


function do_unlike(asset_id){


  request = $.ajax({
    type: "GET",
    url: "/api/asset/"+asset_id+"/unlike/",
  });

  request.done(function (response, textStatus, jqXHR){

  alert('Unliked');
      });
  request.fail(function (jqXHR, textStatus, errorThrown){

  alert('Erro');
      });

}
