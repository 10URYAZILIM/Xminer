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
function formatMyMoney(price) {
  var currency_symbol = "₺"

  var formattedOutput = new Intl.NumberFormat('tr-TR', {
      style: 'currency',
      currency: 'TRY',
      minimumFractionDigits: 2,
    });

  return formattedOutput.format(price).replace(currency_symbol, '')+" ₺"
}
function mesajlar(par) {
     var mesaj="";
       for(var i in par){
            mesaj+=par[i];
            mesaj+='\n';
        }
        swal ("",  mesaj ,  "error" );
}
$(function () {
    // AJAX AYARLARI
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

   // BORSA BİLGİLERİNİ ÇEK
    borsa_cek();

    // MARKET FİYATLARINI MASKELE
    market_fiyatlarini_maskele();

    // TL MASKELE
    $('.tl-maskla').each(function () {
        var para=$(this).text();
        $(this).text(formatMyMoney(parseFloat(para)));
    })
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


// BORSA
// BORSA BİLGİLERİNİ ÇEK
function borsa_cek() {
    $.ajax({
        url:"/ajax/borsa",
        type:"GET",
        beforeSend:function () {
        },
        complete:function () {

        },success:function (cevap) {
            document.getElementById("btc").innerHTML=formatMyMoney(cevap.btc);
            document.getElementById("xrp").innerHTML=formatMyMoney(cevap.xrp);
            document.getElementById("ltc").innerHTML=formatMyMoney(cevap.ltc);
            document.getElementById("eth").innerHTML=formatMyMoney(cevap.eth);

        }
    })
}

// SON BORSA


// MARKET
    function market_fiyatlarini_maskele() {
        $(".machine_fiyat").each(function () {
            fiyat=parseFloat($(this).text());
           $(this).text(formatMyMoney(fiyat));
        })
    }
    function satin_al(thiss,id) {
        var fiyat=$(thiss).attr("fiyat");
        var model=$(thiss).attr("name");
        var csrfmiddlewaretoken=$('input[name="csrfmiddlewaretoken"]').val();

        swal({
          title: model,
          text: model+" Model Cihazı "+fiyat+"₺'ye Almak İstiyor musunuz ?",
          icon: "warning",
          buttons: ["Hayır!", "SATIN AL!"],
        }).then((yanit) => {
          if (yanit) {
              $.ajax({
                 url:"/ajax/machinebuy",
                  data:{'csrfmiddlewaretoken':csrfmiddlewaretoken,'machineid':id},
                  beforeSend:function () {
                         $('.satin_al_buton').attr("disabled", true);
                        loading();
                  },complete:function () {
                        loading_close();
                        $('.satin_al_buton').attr("disabled", false);
                    },
                  success:function (cevap) {
                        if(cevap.durum==1){
                            document.location.href="/app/store";
                        }else{
                           mesajlar(cevap.mesaj);
                        }
                    }
              });
            }
        });


    }
// SON MARKET


// ÖDEME
    function odeme_bildir() {
        var data=$('#odeme_bildiri_formu').serialize();
        $.ajax({
            url:'/ajax/payment',
            data:data,
            beforeSend:function () {
                 document.getElementById("odeme_bildiri_buton").disabled=true;
                loading();
            },complete:function () {
                loading_close();
            },success:function (cevap) {
                if(cevap.durum==1){
                    swal("Ödeme Bildirimi Talebiniz Gönderildi", "", "success");
                    document.getElementById("odeme_bildiri_buton").remove();
                }else{
                   mesajlar(cevap.mesaj)
                   document.getElementById("odeme_bildiri_buton").disabled=false;
                }
            }
        })
    }
// SON ÖDEME