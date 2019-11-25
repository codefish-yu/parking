/** 
 *
 * var picker = new CarnoPicker(
 *      target: '#targetID',           目标元素ID（如：文本框，该值为城市名称）
 * );
 *
 * picker.init();
 */
; var CarnoPicker = function (target) {

    this.template = $('<div id="laycarno_box" class="laycarno_box" style="position: absolute;"><ul class="laycarno_province" id="laycarno_province"><li>京</li><li>津</li><li>沪</li><li>冀</li><li>豫</li><li>云</li><li>辽</li><li>黑</li>'
        + '<li>湘</li><li>皖</li><li>鲁</li><li>新</li><li>苏</li><li>浙</li><li>赣</li><li>鄂</li><li>桂</li><li>甘</li><li>晋</li><li>蒙</li><li>陕</li><li>吉</li><li>闽</li><li>贵</li><li>粤</li><li>川</li><li>青</li><li>藏</li>'
        + '<li>琼</li><li>宁</li><li>渝</li></ul><ul class="laycarno_char" id="laycarno_char" style="display: none;"><li>A</li><li>B</li><li>C</li><li>D</li><li>E</li><li>F</li><li>G</li><li>H</li><li>I</li><li>J</li><li>K</li>'
        + '<li>L</li><li>M</li><li>N</li><li>O</li><li>P</li><li>Q</li><li>R</li><li>S</li><li>T</li><li>U</li><li>V</li><li>W</li><li>X</li><li>Y</li><li>Z</li></ul></div>');

    this.province = $('#laycarno_province', this.template);
    this.char = $('#laycarno_char', this.template);
    this.target = $(target);
};

CarnoPicker.prototype = {
    init: function () {
        var that = this;

        $(window).click(function (event) { 
            that.template.remove();
        });
         
        that.targetEvent();
    },
     
    provinceEvent: function () {
        var that = this;

        that.province.off('click').on('click', 'li', function (event) {
            event.preventDefault();
            event.stopPropagation();
              
            $(this).parent().hide();
            $(this).parent().next().show();

            that.target.val($(this).html());
            
            return false;
        });
    },

    charEvent: function () {
        var that = this;

        that.char.off('click').on('click', 'li', function (event) {
            event.preventDefault();
            event.stopPropagation();
            
            that.target.val(that.target.val() + $(this).html()).focus();
             
            that.template.remove();

            return false;
        });
         
    },
     
    targetEvent: function () {
        var that = this;
        
        that.target.off('click').click(function (event) {
            event.preventDefault();
            event.stopPropagation();

            that.province.show();
            that.char.hide();
            that.provinceEvent();
            that.charEvent();

            var _this = $(this);
            var offset = _this.offset();
            var top = offset.top + _this.outerHeight();

            that.template.css({
                'left': offset.left,
                'top': top
            });

            $('body').append(that.template);

            return false;

        }).blur(function (event) {
             
            $(this).val($(this).val().toUpperCase());
        });

    }
};