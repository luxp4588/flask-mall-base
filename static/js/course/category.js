function createSelect(data){
    var select = document.createElement("select")
    select.options.add(new Option("请选择所属类别", 0))
    // console.log(data)
    for (option in data){
        // console.log(option)
        select.options.add(new Option(data[option][0], data[option][1]))
    }

    select.options[0].selected = true
    select.className="form-control"
    // select.setAttribute("data-level", level)
    select.onchange=function(){
        parent_id = this.options[this.selectedIndex].value
        // console.log($(this).next())
        $(this).next().remove()
        load_cate(parent_id)
    }
    category_select.appendChild(select)
}

function load_cate(parent_id=0) {

    $.ajax({
        url: category_url+parent_id,
        method: "get",
        success: function (data) {
            if (data.length>0){
                createSelect(data)
            }

        }

    })
}

