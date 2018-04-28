function onChange(list, issued, shield) {
    issued.change(function () {
        var checkValue = issued.val();
        $.each(list, function (index, v) {
            if ($.inArray(v.toString(), checkValue) != -1) {
                if (shield.find("option[value='" + v + "']").length > 0) {
                    shield.find("option[value='" + v + "']").remove();
                    shield.selectpicker('refresh');
                }
            } else {
                if (!shield.find("option[value='" + v + "']").length > 0) {
                    shield.append("<option value='" + v + "'>" + v + "</option>");
                    shield.selectpicker('refresh');
                }
            }
        });
    });
}

$(document).ready(function () {
    var timeLimit = $("#buttonSetTime");
    $('.selectpicker').selectpicker();
    timeLimit.click(function () {
        if ($("#singleLimit").is(":hidden")) {
            $("#singleLimit").show();
            var timeLimitTotal = $("#timeLimit_total");
            $("input[id^='singleTimeLimit_'][type=number]").change(function () {
                var sum = 0;
                $("input[id^='singleTimeLimit_'][type=number]").each(function () {
                    if ($(this).val()) {
                        sum += parseInt($(this).val());
                    }
                });
                timeLimitTotal.val(sum);
            });
        }
        else {
            $("#singleLimit").hide();
        }
    });
    var issuedApp = $("#issuedApp");
    var shieldApp = $('#shieldApp');
    var issuedDevice = $("#issuedDevice");
    var shieldDevice = $("#shieldDevice");
    var issuedSdk = $("#issuedSdk");
    var shieldSdk = $("#shieldSdk");
    var issuedProvince = $("#issuedProvince");
    var shieldProvince = $("#shieldProvince");
    var issuedCity = $("#issuedCity");
    var shieldCity = $("#shieldCity");

    onChange(app, issuedApp, shieldApp);
    onChange(app, shieldApp, issuedApp);
    onChange(device, issuedDevice, shieldDevice);
    onChange(device, shieldDevice, issuedDevice);
    onChange(sdk, issuedSdk, shieldSdk);
    onChange(sdk, shieldSdk, issuedSdk);
    issuedProvince.change(function () {
        var checkValue = issuedProvince.val();
        $.each(province, function (k, v) {
            if ($.inArray(v['id'].toString(), checkValue) != -1) {
                if (shieldProvince.find("option[value='" + v['id'] + "']").length > 0) {
                    shieldProvince.find("option[value='" + v['id'] + "']").remove();
                    shieldProvince.selectpicker("refresh");
                }
            } else {
                if (!shieldProvince.find("option[value='" + v['id'] + "']").length > 0) {
                    shieldProvince.append("<option value='" + v['id'] + "'>" + v['name'] + "</option>");
                    shieldProvince.selectpicker("refresh");
                }
            }
        });
        issuedCity.empty();
        issuedCity.selectpicker("refresh");
        $.each(city, function (k, v) {
            if ($.inArray(v['province'].toString(), issuedProvince.val()) != -1) {
                issuedCity.append('<option value="' + v.id + '">' + v.name + '</option>');
                issuedCity.selectpicker('refresh');
            }
        });
    });

    shieldProvince.change(function () {
        var checkValue = shieldProvince.val();
        $.each(province, function (k, v) {
            if ($.inArray(v['id'].toString(), checkValue) != -1) {
                if (issuedProvince.find("option[value='" + v['id'] + "']").length > 0) {
                    issuedProvince.find("option[value='" + v['id'] + "']").remove();
                    issuedProvince.selectpicker("refresh");
                }
            } else {
                if (!issuedProvince.find("option[value='" + v['id'] + "']").length > 0) {
                    issuedProvince.append("<option value='" + v['id'] + "'>" + v['name'] + "</option>");
                    issuedProvince.selectpicker("refresh");
                }
            }
        });
        shieldCity.empty();
        shieldCity.selectpicker("refresh");
        $.each(city, function (k, v) {
            if ($.inArray(v['province'].toString(), shieldProvince.val()) != -1) {
                shieldCity.append('<option value="' + v.id + '">' + v.name + '</option>');
                shieldCity.selectpicker('refresh');
            }
        });
    });
})
;
