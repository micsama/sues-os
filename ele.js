function queryElecDistricts() {
    var elcarea = $("#elcarea").val();
    var elcsysid = $("#elcsysid").val();
    $("#elcdistrict").empty();
    var elcdistrict = $("#elcdistrict");
    //ajax跳转到后台查询楼栋
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/epay/electric/queryelectricdistricts",
        data: {
            "sysid": elcsysid,
            "area": elcarea
        },
        success: function (data) {
            for (var i = 0; i < data.districts.length; i++) {
                var district = data.districts[i];
                elcdistrict.append("<option value=" + district["districtId"] + ">"
                    + district["districtName"] + "</option>");
            }
            queryElecBuis();
        },
        error: function (data) {
            alert("查询错误，请稍后重试");
        }
    });
}

function queryElecBuis() {
    var elcsysid = $("#elcsysid").val();
    var elcarea = $("#elcarea").val();
    var elcdistrict = $("#elcdistrict").val();
    $("#elcbuis").empty();
    var elcbuis = $("#elcbuis");
    //ajax跳转到后台查询楼栋
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/epay/electric/queryelectricbuis",
        data: {
            "sysid": elcsysid,
            "area": elcarea,
            "district": elcdistrict
        },
        success: function (data) {
            for (var i = 0; i < data.buils.length; i++) {
                var buil = data.buils[i];
                elcbuis.append("<option value=" + buil["buiId"] + ">"
                    + buil["buiName"] + "</option>");
            }
            queryElecFloors();
        },
        error: function (data) {
            alert("查询错误，请稍后重试");
        }
    });
}
function queryElecFloors() {
    var elcsysid = $("#elcsysid").val();
    var elcarea = $("#elcarea").val();
    var elcdistrict = $("#elcdistrict").val();
    var elcbuis = $("#elcbuis").val();
    $("#elcfloor").empty();
    var elcfloor = $("#elcfloor");
    //ajax跳转到后台查询楼栋
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/epay/electric/queryelectricfloors",
        data: {
            "sysid": elcsysid,
            "area": elcarea,
            "district": elcdistrict,
            "build": elcbuis
        },
        success: function (data) {
            for (var i = 0; i < data.floors.length; i++) {
                var floor = data.floors[i];
                elcfloor.append("<option value=" + floor["floorId"] + ">"
                    + floor["floorName"] + "</option>");
            }
            queryElecRooms();
        },
        error: function (data) {
            alert("查询错误，请稍后重试");
        }
    });
}
function queryElecRooms() {
    var elcsysid = $("#elcsysid").val();
    var elcarea = $("#elcarea").val();
    var elcdistrict = $("#elcdistrict").val();
    var elcbuis = $("#elcbuis").val();
    var elcfloor = $("#elcfloor").val();
    $("#elcroom").empty();
    var elcroom = $("#elcroom");
    //ajax跳转到后台查询楼栋
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/epay/electric/queryelectricrooms",
        data: {
            "sysid": elcsysid,
            "area": elcarea,
            "district": elcdistrict,
            "build": elcbuis,
            "floor": elcfloor
        },
        success: function (data) {
            for (var i = 0; i < data.rooms.length; i++) {
                var room = data.rooms[i];
                elcroom.append("<option value=" + room["roomId"] + ">"
                    + room["roomName"] + "</option>");
            }
        },
        error: function (data) {
            alert("查询错误，请稍后重试");
        }
    });
}


function queryElectricBill() {
    var elcsysid = $("#elcsysid").val();
    var elcarea = $.trim($("#elcarea").val());
    var elcbuis = $.trim($("#elcbuis").val());
    var roomNo = $.trim($("#elcroom").val());
    var roomName = $.trim($("#elcroom option:selected").text());
    if (null == elcarea || "" == elcarea || undefined == elcarea) {
        alert("没有校区信息!");
        return;
    }
    if (null == elcbuis || "" == elcbuis || undefined == elcbuis) {
        alert("没有楼栋信息!");
        return;
    }
    if (null == roomNo || "" == roomNo || undefined == roomNo) {
        alert("请输入房间号!");
        return;
    }
    //ajax跳转到后台查询电费度数
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/epay/electric/queryelectricbill",
        data: {
            "sysid": elcsysid,
            "roomNo": roomNo,
            "elcarea": elcarea,
            "elcbuis": elcbuis
        },
        success: function (data) {
            if (data != null) {
                if (data.retcode == 0) {
                    if (data.multiflag) {
                        //一房多表
                        $("#multidpsStr").val("");
                        $("#mroomInNo").val(roomNo);
                        $("#mroomInName").val(roomName);
                        $("#tab-data").empty();
                        for (var i = 0; i < data.elecRoomData.length; i++) {
                            var temp = data.elecRoomData[i];
                            var rowStr = "<tr style=\"height: 45px;\"><td style=\"width: 100px;font-weight: bold;\">" + temp.name + " - 剩余电量：</td><td style=\"width: 31%;\"><div class=\"input-group\" style=\"margin-left: 5px;\"><input type=\"text\" class=\"form-control\" id=\"mid_" + temp.elecode + "\" value=\"" + temp.restElecDegree + "\" readonly=\"true\"/><div class=\"input-group-addon\">度</div></div></td>";
                            rowStr += "<td style=\"width: 130px;text-align: right;font-weight: bold;\">" + temp.name + " - 转账金额：</td><td style=\"width: 30%;\"><div class=\"input-group\"><input type=\"text\" class=\"form-control\" id=\"mamt_" + temp.elecode + "\" value=\"0\" onkeyup=\"if(checkAmount(value))execCommand('undo')\" onafterpaste=\"if(checkAmount(value))execCommand('undo')\" /><div class=\"input-group-addon\">元</div></div></td><td>&nbsp;</td></tr>";
                            $("#tab-data").append(rowStr);
                        }
                        $("#queryDiv").hide();
                        $("#queryMultiDiv").show();
                    } else {
                        //一房一表
                        $("#roomInNo").val(roomNo);
                        $("#roomInName").val(roomName);
                        $("#dumpEnergy").val(data.restElecDegree);
                        $("#queryDiv").hide();
                        $("#queryIntoDiv").show();
                    }
                } else {
                    alert(data.retmsg);
                }
            } else {
                alert("未找到该房间信息，请仔细核对房间号！");
            }
        },
        error: function (data) {
            alert("查询错误，请稍后重试");
        }
    });
}

//检测是否空值
function checkEmpty(str) {
    if (undefined == str || null == str || "" == str || "" == ("" + str).replace(/ /g, "")) {
        return true;
    }
    return false;
}

function checkAmount(money) {
    var patt1 = /^\d+(\.)?(\.\d{1,2})?$/;
    if (!patt1.test(money)) {
        return true;
    }
    return false;
}

//返回查询的菜单
function returnQueryBill() {
    $("#queryIntoDiv").hide();
    $("#queryMultiDiv").hide();
    $("#queryDiv").show();
}

//电量过少进行缴费/跳转到缴费的页面
function paidElectricBill() {
    $("#payarea").val($("#elcarea").val());
    $("#paybui").val($("#elcbuis").val());
    $("#payroom").val($("#elcroom").val());
    if ("" == $.trim(document.getElementById("paidMoney").value)) {
        alert("缴费金额不能为空！");
    } else {
        document.stForm.action = "load4paidelectricbill";
        document.stForm.submit();
    }
}

function paidNewElectricBill() {
    $("#msysid").val($("#elcsysid").val());
    $("#mpayarea").val($("#elcarea").val());
    $("#mpaybui").val($("#elcbuis").val());
    $("#mpayroom").val($("#elcroom").val());

    var transamt = $("input[id^='mamt_']");
    if (undefined == transamt || null == transamt || transamt.length == 0) {
        alert("请先填写转账金额");
    }
    var tempStr = [];
    var checflag = false;
    for (var i = 0; i < transamt.length; i++) {
        var elecode = transamt[i].id.replace("mamt_", "");
        var dpsamt = transamt[i].value;
        var restamt = $("#mid_" + elecode).val();
        if (!checkEmpty(dpsamt) && parseFloat(dpsamt) > 0) {
            var dt = {
                "elecode": elecode,
                "dumpEnergy": restamt,
                "dpsamt": dpsamt
            }
            tempStr.push(dt);
        }
    }
    if (tempStr.length < 1) {
        alert("至少要填写一项电控转账金额");
        return;
    }
    $("#multidpsStr").val(JSON.stringify(tempStr));
    document.mstForm.submit();
}



$(document).ready(function () {
    var elcareas = $("#elcarea");
    var elcdistrict = $("#elcdistrict");
    var elcbuis = $("#elcbuis");
    var elcfloor = $("#elcfloor");
    var elcroom = $("#elcroom");
    var elcsysid = $("#elcsysid").val();
    if (undefined == elcsysid || null == elcsysid || "" == elcsysid) {
        alert("未找到电控区域配置信息！");
        return;
    }

    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/epay/electric/queryelectricarea",
        data: {
            "sysid": elcsysid
        },
        success: function (data) {
            if (data.areas.length > 0) {
                for (var i = 0; i < data.areas.length; i++) {
                    var area = data.areas[i];
                    elcareas.append("<option value=" + area["areaId"] + ">"
                        + area["areaName"] + "</option>");
                }
            } else {
                document.getElementById("areamsg").innerHTML = data.errmsg;
            }
            if (data.districts.length > 0) {
                for (var i = 0; i < data.districts.length; i++) {
                    var district = data.districts[i];
                    elcdistrict.append("<option value=" + district["districtId"] + ">"
                        + district["districtName"] + "</option>");
                }
            } else {
                document.getElementById("distmsg").innerHTML = data.errmsg;
            }
            if (data.buils.length > 0) {
                for (var i = 0; i < data.buils.length; i++) {
                    var buil = data.buils[i];
                    elcbuis.append("<option value=" + buil["buiId"] + ">"
                        + buil["buiName"] + "</option>");
                }
            } else {
                document.getElementById("buimsg").innerHTML = data.errmsg;
            }
            if (data.floors.length > 0) {
                for (var i = 0; i < data.floors.length; i++) {
                    var floor = data.floors[i];
                    elcfloor.append("<option value=" + floor["floorId"] + ">"
                        + floor["floorName"] + "</option>");
                }
            } else {
                document.getElementById("floormsg").innerHTML = data.errmsg;
            }
            if (data.rooms.length > 0) {
                for (var i = 0; i < data.rooms.length; i++) {
                    var room = data.rooms[i];
                    elcroom.append("<option value=" + room["roomId"] + ">"
                        + room["roomName"] + "</option>");
                }
            } else {
                document.getElementById("roommsg").innerHTML = data.errmsg;
            }
        },
        error: function (data) {
            alert("查询错误，请稍后重试");
        }
    });
});
