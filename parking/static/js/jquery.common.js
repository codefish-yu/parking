$.fn.outer = function () {
    return $('<div></div>').append(this.eq(0).clone()).html();
};

jQuery.extend(
 {
     evalJSON: function (strJson) {
         return eval("(" + strJson + ")");
     },
     toJSON: function (object) {
         var type = typeof object;
         if ('object' == type) {
             if (Array == object.constructor)
                 type = 'array';
             else if (RegExp == object.constructor)
                 type = 'regexp';
             else
                 type = 'object';
         }
         switch (type) {
             case 'undefined':
             case 'unknown':
                 return;
                 break;
             case 'function':
             case 'boolean':
             case 'regexp':
                 return object.toString();
                 break;
             case 'number':
                 return isFinite(object) ? object.toString() : 'null';
                 break;
             case 'string':
                 return '"' + object.replace(/(\\|\")/g, "\\$1").replace(/\n|\r|\t/g,
       function () {
           var a = arguments[0];
           return (a == '\n') ? '\\n' :
                       (a == '\r') ? '\\r' :
                       (a == '\t') ? '\\t' : ""
       }) + '"';
                 break;
             case 'object':
                 if (object === null) return 'null';
                 var results = [];
                 for (var property in object) {
                     if (object[property] != null) {
                         var value = jQuery.toJSON(object[property]);
                         if (value !== undefined) {
                             results.push(jQuery.toJSON(property) + ':' + value);
                         }
                     } else {
                         results.push(property + ':null');
                     }
                 }
                 return '{' + results.join(',') + '}';
                 break;
             case 'array':
                 var results = [];
                 for (var i = 0; i < object.length; i++) {
                     var value = jQuery.toJSON(object[i]);
                     if (value !== undefined) results.push(value);
                 }
                 return '[' + results.join(',') + ']';
                 break;
         }
     }
 });

/* 获取表单的字段值 */
$.fieldValue = function (el, successful) {
    var n = el.name, t = el.type, tag = el.tagName.toLowerCase();
    if (typeof successful == 'undefined') successful = true;

    if (successful && (!n || el.disabled || t == 'reset' || t == 'button' ||
        t == 'radio' && !el.checked ||
        (t == 'submit' || t == 'image') && el.form && el.form.clk != el ||
        tag == 'select' && el.selectedIndex == -1))
        return null;

    if (tag == 'select') {
        var index = el.selectedIndex;
        if (index < 0) return null;
        var a = [], ops = el.options;
        var one = (t == 'select-one');
        var max = (one ? index + 1 : ops.length);
        for (var i = (one ? index : 0) ; i < max; i++) {
            var op = ops[i];
            if (op.selected) {
                var v = op.value;
                if (!v)
                    v = (op.attributes && op.attributes['value'] && !(op.attributes['value'].specified)) ? op.text : op.value;
                if (one) return v;
                a.push(v);
            }
        }
        return a;
    }
    if (t == "checkbox") {
        if (el.checked)
            return "1";
        else
            return "0";
    }
    return $.trim(el.value);
};
/* 设置表单的字段值 */
$.fn.setFieldValue = function (sValue) {
    return this.each(function () {
        var t = this.type, tag = this.tagName.toLowerCase(), eEl = this;
        if (tag == "span" || tag == "div") {
            this.innerHTML = sValue;
            return;
        }
        switch (t) {
            case 'hidden':
            case 'text':
            case 'file':
            case 'password':
            case 'number':
            case 'textarea':
                this.value = sValue;
                break;
            case 'checkbox':
                var oReg = new RegExp('(^|,) + eEl.value + (,|$)', 'g');
                eEl.checked = oReg.test(sValue);
                break;
            case 'radio':
                if (eEl.value == sValue)
                    eEl.checked = true;
                break;
            case 'select-one':
                //console.log(eEl.options.length);
                //console.log(sValue + "===");
                for (var j = 0; j < eEl.options.length; j++) {
                    //console.log(eEl.options[j].value);
                    if ( eEl.options[j].value!="" && eEl.options[j].value == sValue) {
                        eEl.options[j].selected = true;
                        break;
                    }
                }
                break;
        }
    });
};
/* 重置表单 */
$.fn.clearForm = function () {
    return this.each(function () {
        $('input,select,textarea', this).clearFields();
    });
};

$.fn.clearFields = $.fn.clearInputs = function () {
    return this.each(function () {
        var t = this.type, tag = this.tagName.toLowerCase();
        if (t == 'text' || t == 'hidden' || t == 'password' || tag == 'textarea')
            this.value = '';
        else if (t == 'checkbox' || t == 'radio')
            {this.checked = false;}
        else if (tag == 'select')
            this.selectedIndex = 0;
    });
};

$.fn.resetForm = function () {
    return this.each(function () {
        if (typeof this.reset == 'function' || (typeof this.reset == 'object' && !this.reset.nodeType))
            this.reset();
    });
};

/*  将单选框，复选框，下拉框设为选中状态 */
$.fn.selected = function (select) {
    if (select == undefined) select = true;
    return this.each(function () {
        var t = this.type;
        if (t == 'checkbox' || t == 'radio')
            this.checked = select;
        else if (this.tagName.toLowerCase() == 'option') {
            var $sel = $(this).parent('select');
            if (select && $sel[0] && $sel[0].type == 'select-one') {
                $sel.find('option').selected(false);
            }
            this.selected = select;
        }
    });
};

/* 为表单绑定键盘事件，点击回车提交表单 */
$(function() {
    $('.search-btn, .commit-btn').keypress(function(event) {
        if (event.keyCode == 13) {
            $(this).find('button').click();
        }
    });
});

$.validConfigs = {
    className: ['.required', '.email', '.plusdecimal', '.plusnumber', '.decimal', '.number', '.username', '.url', '.mobile', '.tel'],
    classTip: ['必填', '必须是正确的邮件地址', '必须是数字(正整数[小数])', '必须是数字(正整数)', '必须是数字(正负(整数)小数)', '必须是数字(正负整数)', '长度不对或者含有特殊字符', '网址输入有误', '手机号码错误', '电话号码格式不对']
};
/**
* @constructor $(this).formDisabled
* @description 禁用文本框工具
* @example $(this).formDisabled();
*/
$.fn.formDisabled = function () {
    return this.each(function () {
        if ($(this).is(":visible") && ($(this).attr('readonly') || $(this).attr('disabled'))) {
            if ($(this)[0].tagName.toUpperCase() == "SELECT") {
                $(this).removeAttr('readonly').removeAttr('disabled').addClass('g_input_d').unbind().bind('change', function () {
                    this.selectedIndex = this.defOpt;
                }).bind('focus', function () {
                    this.defOpt = this.selectedIndex;
                });
            } else {
                // .removeAttr('readonly').removeAttr('disabled')
                $(this).addClass('g_input_d').bind('change', function () { return false; }).bind('contextmenu', function (evt) { return false; }).bind('keydown', function (evt) { return false; });
            }
        } else {
            //            if ($(this)[0].tagName.toUpperCase() == "SELECT") {
            //                $(this).removeClass('g_input_d').unbind();
            //            } else {
            //                $(this).removeClass('g_input_d').unbind('contextmenu').unbind('keydown').unbind('change');
            //            }
        }
    });
}

/*
* @constructor $("form").validFileds('组名')
* @description 对组名进行非空验证等
* @example $(this).validFileds('组名');
* @param gType:组名(任意组名),可为空
*/
$.fn.validFileds = function (gType) {
    $(".tip_errmsg").remove();
    var bFlag = true, options = {
        groupType: gType || ""
    };
    $.each($.validConfigs.className, function (i, n) {
        var oClassName = $(n + ":not([groupType])");
        if (options.groupType) {
            oClassName = $(n + "[groupType='" + options.groupType + "']");
        }

        if (oClassName.length > 0) {
            oClassName.each(function () {
                $(this).trigger('validSubmit');
                bFlag = $(".tip_errmsg").length == 0;
                if (!bFlag) { return false; }
            });
        }
    });
    return bFlag;
}
/**
* @constructor $(this).formToJSON
* @description 返回JSON实体
* @example $('form').formToJSON(true,function(){});
* @param 参数 gType:验证方式,组名|true|false(不验证), callback:对返回实体回调操作
*/
$.fn.formToJSON = function (gType, callback) {
    var oEntity = {};
    if (this.length == 0) { alert("查找panel,form元素失败"); return false; }
    if (gType || gType === true) {
        if (gType === true) { gType = null; }
        var a = $(this).validFileds(gType);
        if (a === false) { return false; }
    }

    var els = $("input,select,textarea", this[0]);
    for (var i = 0, max = els.length; i < max; i++) {
        var aValue = $.fieldValue(els[i]);
        if (aValue === null || typeof aValue == 'undefined' || aValue == '' || ($.isArray(aValue) && !aValue.length)) {
            continue;
        }

        aValue = $.trim(aValue);
        var aCondition = els[i].name.split('__');
        if (aCondition.length == 2) {
            if (!oEntity[aCondition[0]]) {
                oEntity[aCondition[0]] = {}
            }
            oEntity[aCondition[0]][aCondition[1]] = (!oEntity[aCondition[0]][aCondition[1]]) ? aValue : oEntity[aCondition[0]][aCondition[1]] + "," + aValue;
        } else {
            oEntity[els[i].name] = (!oEntity[els[i].name]) ? aValue : oEntity[els[i].name] + "," + aValue;
        }
    }
    if ($.isFunction(callback)) {
        oEntity = callback(oEntity);
    }
    return $.isPlainObject(oEntity) ? oEntity : false;
}

/* 填充表单值 */
$.fn.fillForm = function (model, callback, fillParam) {

    this.each(function() {
        if (model == null) model = {}
        var els = $("input,textarea,span,div,select,number", this);

        for (var i = 0, max = els.length; i < max; i++) {
            var sValue = model[$(els[i]).attr("name")];
            if (typeof sValue == 'undefined') continue;
            if (els[i].type && els[i].type == "checkbox") {
                if (sValue==1) {

                    if (els[i].nextSibling.className== "iCheck-helper") {
                        $(els[i]).iCheck('check');
                    }
                    else {
                        $(els[i]).attr("checked", "checked");
                    }
                    
                } else {

                    if (els[i].nextSibling.className== "iCheck-helper") {
                        $(els[i]).iCheck('uncheck');
                    } 
                    else {
                        $(els[i]).removeAttr("checked");
                    }
                }
            } else {
                if (fillParam && fillParam[$(els[i]).attr("name")]) {
                    sValue = fillParam[$(els[i]).attr("name")](sValue);
                }

                $(els[i]).setFieldValue(sValue).triggerHandler("change");
            }
        }
    });
    var t = setTimeout(function () {
        if ($.isFunction(callback)) {
            callback(model);
        }
        t = null;

    }, 300);
};

/*
批量操作
*/
$.fn.batchRequest = function (options) {
    var configs = {
        handler: function (paramList, thisVal) {
            alert('未实现');
        },
        target: null
    };
    $.extend(configs, options);
    var thisVal = $(this).val();
    if (thisVal && thisVal !== "") {
        configs.target = $(configs.target);
        var targetVal = [];
        configs.target.each(function () {
            if ($(this).attr("checked")) {
                targetVal.push($(this).val());
            }
        });
        if (targetVal && targetVal.length > 0) {
            configs.handler(targetVal, thisVal);
        } else {
            alert("未选择操作项目,请选择操作项");
        }
    }
};
//全选
$.fn.selectAll = function () {
    var inputs = $(this).parents("table").find("tbody>tr>td> :checkbox");
    if (inputs.length > 0) {
        var b = $(this).attr("checked");
        inputs.each(function () {
            if (b) {
                $(this).attr('checked', b);
            } else {
                $(this).removeAttr('checked');
            }
        });
    }
};
//全选控制按钮
$.fn.bindSelectAll = function () {
    $(this).unbind('click').bind('click', function () {
        $(this).selectAll();
    });
}
/*
* @constructor $.fn.bindSelect 
* @description 提示信息集合
* @example $("#ddlUserType").bindSelect(true,enumClass.EnumMemUserType,function(item){return true;});
* @param 参数 empty:是否加上请选择,data:enumClass对象参数, predicate:过滤方法,可以为空
*/
$.fn.bindSelect = function (empty, data, predicate) {
    var query = $(this).html("");
    if (empty) {
        query.html("<option value=''>--请选择--</option>");
    }
    if (data) {
        $.each(data, function (i, item) {
            if (predicate && $.isFunction(predicate)) {
                if (predicate(item)) {
                    query.append("<option value=\"" + item["n"] + "\">" + item["v"] + "</option>");
                }
            } else {
                query.append("<option value=\"" + item["n"] + "\">" + item["v"] + "</option>");
            }
        });
    }
}

//绑定select 并指定要绑定的字段
//* @example  $("#ParkID").bindSelect(false, json.Data, "id", "name");
$.fn.bindSelect = function (empty, data, value, text, predicate) {
    var query = $(this).html("");
    if (empty) {
        query.html("<option value=''>--请选择--</option>");
    }
    if (data) {
        $.each(data, function (i, item) {
            if (predicate && $.isFunction(predicate)) {
                if (predicate(item)) {
                    query.append("<option value=\"" + item[value] + "\">" + item[text] + "</option>");
                }
            } else {
                query.append("<option value=\"" + item[value] + "\">" + item[text] + "</option>");
            }
        });
    }
}

//设置表单读写
$.fn.readonly = function (bool) {
    if (bool) {
        $(this).attr("readonly", "readonly");
    }else
        $(this).removeAttr("readonly"); 
}

/* 启用表单 */
$.fn.enable = function (b) {
    if (b == undefined) b = true;
    return this.each(function () {
        this.disabled = !b;
    });
};

//设置表单禁用
$.fn.disabled = function (bool) {
    if (bool) {
        $(this).attr("disabled", "disabled");
    } else
        $(this).removeAttr("disabled");
}

//获取页面参数
jQuery.getUrlParam = function (name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return r[2]; return null;
}


// 对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符， 
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字) 
// 例子： 
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423 
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18 
//var time1 = new Date().Format("yyyy-MM-dd");
//var time2 = new Date().Format("yyyy-MM-dd HH:mm:ss");
Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
// 获取当前时间年月日时分秒
function getCNDateTime() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hour = date.getHours();
    var minute = date.getMinutes();
    var second = date.getSeconds();

    if (hour <= 9) {
        hour = "0" + hour;
    }
    if (minute <= 9) {
        minute = "0" + minute;
    }
    if (second <= 9) {
        second = "0" + second;
    }
    return year + '年' + month + '月' + day + '日 ' + hour + ':' + minute + ':' + second;
}

///适用于前端的Cookie
function setCookie(name, value) {
    var Days = 365;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}
function getCookie(name) {
    var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
    if (arr != null) {
        return unescape(arr[2]);
    } else {
        return null;
    }
}

//全局处理AJAX清求SESSION超时自动弹出登录
//关联Parking.Framework.ParkPower.PowerCheck
if (typeof ($) != "undefined") {
    $.ajaxSetup({
        complete: function (XMLHttpRequest, textStatus) {
            var sessionstatus = XMLHttpRequest.getResponseHeader("Session-Status");
            if (sessionstatus === "Timeout") {
                layer.closeAll();
                //设置无刷新，并弹出
                window.top.$("#LoginForm").attr("data-reload", "").click();
            } else if (sessionstatus == "OftenRequest") {
                layer.closeAll();
                window.layer.msg("频繁访问 请等待一分钟后再操作", { icon: 0, time: 2000 });
            }
        }
    });
}

