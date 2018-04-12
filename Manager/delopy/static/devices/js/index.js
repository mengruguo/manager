/**
 * Created by nubia on 2018/3/31.
 */
var searchUrld;
var editUrld;
var delUrld;

function redraw(row, data) {
    var op = $("td", row).eq(5).empty();
    op.append($("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        editUrld + "?t=" + data.id).text("编辑"));
    op.append($("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        delUrld + "?t=" + data.id).text("删除"));
}
$(document).ready(function () {
    var table = $("#devices_table");
    var dataTable = table.DataTable({
        processing: true,
        sortable: true,
        ajax: searchUrld,
        language: {
            emptyTable: "设备列表为空",
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
            data: "manufacturer"
        }, {
            data: "model", defaultContent: "",
        }, {
            data: "version", defaultContent: "",
        }, {
            data: "update_time"
        }, {
            data: null,
            orderable: false,
            searchable: false
        }],
        createdRow: redraw,
    });
});