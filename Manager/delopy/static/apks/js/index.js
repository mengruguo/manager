var searchUrl;
$(document).ready(function () {
    var table = $("#apps_table");
    var dataTable = table.DataTable({
        serverSide: true,
        processing: true,
        ajax: searchUrl,
        language: {
            emptyTable: "APP列表为空",
            info: "当前显示第 _START_ 至 _END_ 项，共 _TOTAL_ 项。",
            infoEmpty: "当前显示第 0 至 0 项，共 0 项。",
            processing: "正在搜索中 ...",
            search: "搜索：",
            lengthMenu: "每页 _MENU_ 项",
            paginate: {
                first: "首页",
                previous: "上页",
                next: "下页",
                last: "末页"
            }
        },
        columns: [{
            data: "id",
            searchable: false
        }, {
            data: "app_id"
        }, {
            data: "name",
        }, {
            data: "version",
        }, {
            data: "update_time"
        }],
        "columnDefs": [ {
            "targets": 5,
            "data": null,
            "defaultContent":"<button id='apps_edit' type='btn btn-primary btn-sx' style='margin-right: 5px'>编辑</button>"+"<button id='apps_delete' type='btn btn-primary btn-sx' style='margin-right: 5px'>删除</button>"
        } ],
    });
    var appsEdit = $("#apps_edit");
    appsEdit.click(function () {
        alert("edit");
    })
});
