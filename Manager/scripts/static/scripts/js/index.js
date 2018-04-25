var searchUrl;
var editUrl;
var delUrl;
var onlineUrl;
var offlineUrl;
var allUrl;

function redraw(row, data) {
    var op = $("td", row).eq(15).empty();
    var online = $("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        onlineUrl + "?t=" + data.id).text("上线");
    var offline = $("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        offlineUrl + "?t=" + data.id).text("下线");
    if (data.state == 1) {
        op.append(online);
    } else {
        op.append(offline);
    }
    op.append(data.state ? online : offline);
    op.append($("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        editUrl + "?t=" + data.id).text("编辑"));
    op.append($("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        delUrl + "?t=" + data.id).text("删除"));
}
$(document).ready(function () {
    var table = $("#script_table");
    var allOffline = $("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        allUrl).text("全部下线")
    var dataTable = table.DataTable({
        processing: true,
        sortable: true,
        ajax: searchUrl,
        order: [14, 'desc'],
        language: {
            emptyTable: "脚本列表为空",
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
            data: "data_type"
        }, {
            data: "os",
        }, {
            data: "name",
        }, {
            data: "url",
            orderable: "false",
        }, {
            data: "single_issued_limit",
        }, {
            data: "app",
            orderable: "false",
        }, {
            data: "issued_limit_type",
        }, {
            data: "number",
        }, {
            data: "issued_count",
        }, {
            data: "effective_time",
        }, {
            data: "invalid_time",
        }, {
            data: "state",
            render: function (data) {
                switch (data) {
                    case 0:
                        return "上线";
                    case 1:
                        return "下线";
                    case 2:
                        return "定向测试";
                }
            }
        }, {
            data: "update_time",
        }, {
            data: "hot",
        },
            {
                data: null,
                orderable: false,
                searchable: false
            }],
        createdRow: redraw,
    });
    $("#script_table_wrapper").parent().append(allOffline);
});
