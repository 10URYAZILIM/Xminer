function login(device) {
    if(device=="mobil"){
        var data=$("#oturum_ac_formu2").serialize();
    }else{
        var data=$("#oturum_ac_formu").serialize();
    }
    document.getElementById("giris_buton1").disabled=true;
    document.getElementById("giris_buton2").disabled=true;
    $.ajax({
        url:"/ajax/login",
        data:data,
        type:"POST",
        dataType:"JSON",
        success:function (cevap) {
            if(cevap.durum==1){
                // Giriş Başarılı
                document.location.href="/app/";
            }else{
                // Hatalı Giriş
                var mesaj="";
                   for(var i in cevap.mesaj){
                        mesaj+=cevap.mesaj[i];
                        mesaj+='<br>';
                    }
                    swal ("",  mesaj ,  "error" );
                // HATALI GİRİŞ OLDUĞU İÇİN BUTONLARIN KILIDINI AÇALIM
                document.getElementById("giris_buton1").disabled=false;
                document.getElementById("giris_buton2").disabled=false;
            }

        }
    })

}