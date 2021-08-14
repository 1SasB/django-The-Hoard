console.log("inside profileJS")
$document.ready(function(){
    $('#function_btn').click(function(){
        if(confirm("Are you sure you want to delete/add")){
            var id = []
            $(':checkbox:checked').each(function(i){
                id[i] = $(this).val()
            })
            if(id.length()===0){
                alert("You must select item(s) for function")
            }else{
                console.log(id)
            }
        }

    })

})