//$(function () {
//    $("input[type=text]").not(".normal").each(function () {
//        if ($(this).parent().find("label").length > 0 && $(this).hasClass("required")) {
//            var dataValid = $(this).attr("data-valid");
//            var dataError = $(this).attr("data-error");
//            if (dataValid != null && dataError != null && dataValid != "" && dataError != "") {
//                dataValid += "||isSpecial";
//                dataError += "||不能包含特殊字符";
//                $(this).attr("data-valid", dataValid).attr("data-error", dataError);
//            } else {
//                $(this).attr("data-valid", "isSpecial").attr("data-error", "不能包含特殊字符");
//            }
//        }
//    });
//});