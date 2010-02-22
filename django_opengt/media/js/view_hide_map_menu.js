    $(function(){
        $("#max").click(function(){
            $("#body").css("display", "block");
            $("#min").css("display", "block");
            $("#max").css("display", "none")
        });
        $("#min").click(function(){
            $("#body").css("display", "none");
            $("#min").css("display", "none");
            $("#max").css("display", "block")
        })
    });