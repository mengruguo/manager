/**
 * Created by nubia on 2018/4/7.
 */
var searchUrlsc
var allIssuedUrlsc
var editUrlsc
var delUrlsc
var issuedUrlsc

function redraw(row, data) {
    var op = $("td", row).eq(15).empty();
    op.append($("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        issuedUrlsc + "?t=" + data.id).text("下线"));
    op.append($("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        editUrl + "?t=" + data.id).text("编辑"));
    op.append($("<a></a>").addClass("btn btn-primary btn-xs").attr("type", "button").attr("href",
        delUrl + "?t=" + data.id).text("删除"));
}
$(document).ready(function () {
    var table = $("#scripts_table");
    var dataTable = table.DataTable({
        processing: true,
        sortable: true,
        ajax: searchUrlsc,
        ajax: allIssuedUrlsc,
        language: {
            emptyTable: "脚本管理列表为空",
            info: "当前显示第 _START_ 至 _END_ 项，共 _TOTAL_ 项。",
            infoEmpty: "当前显示第 0 至 0 项，共 0 项。",
            processing: "正在搜索中 ...",
            search: "搜索：",
            allissued: "全部下线",
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
            data: "scriptType"
        }, {
            data: "osVer",
        }, {
            data: "scriptName",
        }, {
            data: "url"
        }, {
            data: "oneIssuedCount"
        }, {
            data: "appId"
        }, {
            data: "issuedType"
        }, {
            data: "scriptNumber"
        }, {
            data: "issuedCount"
        }, {
            data: "effective_time"
        }, {
            data: "dead_time"
        }, {
            data: "scriptSate"
        }, {
            data: "update_time"
        }, {
            data: "scriptHot"
        }, {
            data: null,
            orderable: false,
            searchable: false
        }],
        createdRow: redraw,
    });
});