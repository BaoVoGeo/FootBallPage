
$(function runFilter(){
    // $('.alert').delay(3000).fadeOut();
    // $('#delete_success').delay(3000).fadeOut();
    $("input[name=filter]").on('keyup keypress', function(e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
        e.preventDefault();
        return false;
        }
    });
    $(".search").keyup(function(){
        
		var url = '/filter'; // Backend url
		var params = {'q':$("input[name=filter]").val(), 'sorttitle':$("input[name=sorttitle]").val(), 'sortviews':$("input[name=sortviews]").val(), 'sortdate':$("input[name=sortdate]").val(), 'click':$("input[name=click]").val()}; // Search field value
        fetchData(url, params); // Backend call for filtered data
	});
    
    $(".search").keyup();
    
    
});
var Dem = 1;
function fetchData(url, params) {
    console.log("Lap lan thu ")
    console.log(Dem)
    Dem = Dem + 1;
    var sortbytitle = $("#sortbytitle").val();
    var sortbyviews = $("#sortbyviews").val();
    var sortbydate = $("#sortbydate").val();
    $.get(url, params)
    .done(function(data){
        // Put the data into target div
        
        $("#results").html(data);
        // var sortbytitle = $("#sortbytitle").val();
        // Sign
            sortbychartitle = sortbytitle.substring(0,1)
            sortbycharviews = sortbyviews.substring(0,1)
            sortbychardate = sortbydate.substring(0,1)
            if(sortbychartitle=="-")
            {
                    $(".title").removeClass("main");
            }
            else
            {
                    $(".title").toggleClass("main");
            }
            if(sortbycharviews=="-")
            {
                    $(".views").removeClass("main");
            }
            else
            {
                    $(".views").toggleClass("main");
            }
            if(sortbychardate=="-")
            {
                    $(".date").removeClass("main");
            }
            else
            {
                    $(".date").toggleClass("main");
            }

            $(".title").click(function(){
                $(".title").toggleClass("main");
                var sortbytitle = $("#sortbytitle").val();
                var click = $("#click").val(1);
                sortbychartitle = sortbytitle.substring(0,1)
                
                if(sortbychartitle=="-")
                {
                    sortbytitle = sortbytitle.substring(1);
                    $("#sortbytitle").val(sortbytitle);
                    $("#click").val(1);
                }
                else
                {
                    sortbytitle = "-" + sortbytitle;
                    $("#sortbytitle").val(sortbytitle);
                    $("#click").val(1);
                }
                var url = '/filter/';
                var params = {'q':$("input[name=filter]").val(),'sorttitle':$("input[name=sorttitle]").val(),'sortviews':$("input[name=sortviews]").val(),'click':$("input[name=click]").val(), 'sortdate':$("input[name=sortdate]").val()};
                console.log(sortbychartitle);
                console.log("Chay vao title");
                console.log($("#sortbytitle").val())
                fetchData(url, params);
                
            });
                $(".views").click(function(){
                $(".views").toggleClass("main");
                var sortbyviews = $("#sortbyviews").val();
                sortbycharviews=sortbyviews.substring(0,1)
                if(sortbycharviews=="-")
                {
                    sortbyviews=sortbyviews.substring(1);
                    $("#sortbyviews").val(sortbyviews);
                    $("#click").val(2);
                }
                else{
                    sortbyviews = "-" + sortbyviews;
                    $("#sortbyviews").val(sortbyviews);
                    $("#click").val(2);
                }
                var url = '/filter/'; // Backend url
                var params = {'q':$("input[name=filter]").val(),'sorttitle':$("input[name=sorttitle]").val(),'sortviews':$("input[name=sortviews]").val(), 'sortdate':$("input[name=sortdate]").val(), 'click':$("input[name=click]").val()}; // Search field value
                fetchData(url, params);

            });
            $(".date").click(function(){
                $(".date").toggleClass("main");
                var sortbydate = $("#sortbydate").val();
                sortbychardate = sortbydate.substring(0,1)
                if(sortbychardate=="-")
                {
                    sortbydate = sortbydate.substring(1);
                    $("#sortbydate").val(sortbydate);
                    $("#click").val(3);
                }
                else{
                    sortbydate = "-" + sortbydate;
                    $("#sortbydate").val(sortbydate);
                    $("#click").val(3);
                }
                var url = '/filter/'; // Backend url
                var params = {'q':$("input[name=filter]").val(),'sorttitle':$("input[name=sorttitle]").val(),'sortviews':$("input[name=sortviews]").val(), 'sortdate':$("input[name=sortdate]").val(), 'click':$("input[name=click]").val()}; // Search field value
                fetchData(url, params);

            });
            
                
        }
    );
};
// function showdelete(name,id)
// {
//     $('#autoid').val(id);
//     $('#deleting_field').html(name);
//     $('#myModal').modal('show');
// }

// function deleteemp()
// {
//     var deleteid= $('#autoid').val();
//     url='/delete/'+deleteid;
//     $.ajax({
//             type: 'GET',
//             url:url,
//             dataType: 'json',

//             success: function(data) {

//             if(data.message ==0)
//             {
//                 alert('Something Went Wrong');
//             }
//             else
//             {
//                 $('#myModal').modal('hide');
//                 $("#delete_success").show();
//                 $('#delete_success').delay(3000).fadeOut();

//                 $("input[name=filter]").keyup(function(){
//                     var url = '/list';
//                     var params = {'filter':$("input[name=filter]").val()};
//                     fetchData(url, params);
//                 }).trigger('keyup');
//             }
//             },
//             error: function(data) { // if error occured
//                 alert("Error occured.please try again");
//             }
//     });
// }