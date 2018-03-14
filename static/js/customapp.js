$('.cep_tel').mask('(000) 000 00 00');
window.onload = function(e){
     loading_close();
}
function loading() {
    $(".loader").fadeIn("slow");
}
function loading_close() {
     $(".loader").fadeOut("slow");
}
function mesajlar(par) {
     var mesaj="";
       for(var i in par){
            mesaj+=par[i];
            mesaj+='<br>';
        }
        swal ("",  mesaj ,  "error" );
}
$(function () {
   $.ajaxSetup({
      type:"POST",
      dataType:"JSON",
      success:function (cevap) {
            if(cevap.durum==1){
                document.location.reload();
            }else{
               mesajlar(cevap.mesaj);
            }
        },error:function () {
            swal ("TimeOut",  "" ,  "error" );
            document.location.reload();
        }
    });
})

// USER
// PROFILI GUNCELLE
function user_update() {
    var data=$("#update_user_form").serialize();
    $.ajax({
        url:"/ajax/update_user",
        data:data,
        beforeSend:function () {
             document.getElementById("profil_guncelle_buton").disabled=true;
            loading();
        },
        complete:function () {
            loading_close();
            document.getElementById("profil_guncelle_buton").disabled=false;
        }
    })
}
function update_password() {
    var data=$("#update_password_form").serialize();
    $.ajax({
        url:"/ajax/update_password",
        data:data,
        beforeSend:function () {
             document.getElementById("sifre_guncelle_buton").disabled=true;
            loading();
        },complete:function () {
            loading_close();
            document.getElementById("sifre_guncelle_buton").disabled=false;
        }
    })
}

function change_avatar() {
    $.ajax({
        url:"/ajax/update_avatar",
        data:new FormData(document.getElementById("change_avatar_form")),
        contentType: false,
        cache: false,
        processData:false,
    })

}
// SON USER