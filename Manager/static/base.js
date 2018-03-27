function adjustFooterPosition() {
    var footer = $("footer");
    footer.removeClass("navbar-fixed-bottom");
    if (document.body.clientHeight < $(window).height()) {
        footer.addClass("navbar-fixed-bottom");
    }
}

function onElementHeightChange(e, callback) {
    var lastHeight = e.clientHeight, newHeight;
    (function run() {
        newHeight = e.clientHeight;
        if (lastHeight != newHeight)
            callback();
        lastHeight = newHeight;

        if (e.onElementHeightChangeTimer)
            clearTimeout(e.onElementHeightChangeTimer);

        e.onElementHeightChangeTimer = setTimeout(run, 200);
    })();
}

function addReadyEvent() {
    $(document).ready(function () {
        adjustFooterPosition();
        onElementHeightChange(document.body, adjustFooterPosition);
        var im = $(".im");
        im.find(".im-close").click(function () {
            im.css("height", "0");
            im.find(".im-main").hide();
            im.find(".im-open").show();
        });
        im.find(".im-open").click(function () {
            im.css("height", "272");
            im.find(".im-main").show();
            $(this).hide();
        });
        im.find(".go-top").click(function () {
            $(window).scrollTop(0);
        });
        var wechat = im.find(".im-wechat");
        wechat.mouseenter(function () {
            $(".wechat-panel").show();
        });
        wechat.mouseleave(function () {
            $(".wechat-panel").hide();
        });
    });
}

(function () {
    'use strict';

    function emulatedIEMajorVersion() {
        var groups = /MSIE ([0-9.]+)/.exec(window.navigator.userAgent);
        if (groups === null) {
            return null;
        }
        var ieVersionNum = parseInt(groups[1], 10);
        return Math.floor(ieVersionNum);
    }

    var ua = window.navigator.userAgent;
    if (ua.indexOf('Opera') > -1 || ua.indexOf('Presto') > -1) {
        addReadyEvent();
        return; // Opera, which might pretend to be IE
    }
    var emulated = emulatedIEMajorVersion();
    if (emulated === null) {
        addReadyEvent();
        return; // Not IE
    }
    if (emulated < 9) {
        window.onload = function () {
            document.getElementsByTagName("body")[0].innerHTML = "<p align='center'>您的浏览器版本太低</p>";
        };
    } else {
        addReadyEvent();
    }
})();
