function createSelect(data){
    var category_select = $("#category_select")
    var select = document.createElement("select")
    select.options.add(new Option("请选择所属类别", 0))
    for (option in data){
        select.options.add(new Option(data[option][0], data[option][1]))
    }

    select.options[0].selected = true
    select.className="form-control"
    select.onchange=function(){
        parent_id = this.options[this.selectedIndex].value
        $(this).next().remove()
        load_cate(parent_id)
    }
    category_select.append(select)
}

function load_cate(parent_id=0) {

    $.ajax({
        url: category_url+"?parent_id="+parent_id,
        method: "get",
        success: function (data) {
            if (data.length>0){
                createSelect(data)
            }

        }

    })
}

