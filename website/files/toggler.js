function show_points(filename, i) {
    document.getElementById("show-"+i).style.display = "none";
    document.getElementById("hide-"+i).style.display = "unset";
    document.getElementById("point-detail-"+i).style.height = "0px";
    var ajax;
    if(window.XMLHttpRequest){
        ajax=new XMLHttpRequest();
    } else {
        ajax=new ActiveXObject('Microsoft.XMLHTTP');
    }
    ajax.onreadystatechange=function(){
        if(ajax.readyState==4 && ajax.status==200){
            var dummy = document.getElementById("point-detail-dummy")
            var detail = document.getElementById("point-detail-"+i)
            dummy.innerHTML = ajax.responseText;
            detail.innerHTML = ajax.responseText;
            detail.style.height = dummy.clientHeight + "px";
        }
    }
    ajax.open('GET',filename,true);
    ajax.send();
}

function hide_points(i) {
    document.getElementById("show-"+i).style.display = "unset";
    document.getElementById("hide-"+i).style.display = "none";
    document.getElementById("point-detail-"+i).style.height = "0px";
}
