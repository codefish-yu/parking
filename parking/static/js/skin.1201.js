var skinModel = {
    homeiconsrc: '../../Static/img/nhome/',//Home页icon图片路径 ；视图View的相对路径
    skinimgsrc: '../../Static/img/skin/',  //风格页show预览图片路径 
    skincsssrc: '../../Static/css/skin/',  //风格页css路径 
    options: [
        {
            skinid: 1,
            skinname: '背景色风格-1',
            src: '../../Static/img/skin/skin_01.png',
            css: '../../Static/css/skin/skin-t2-red.css',
            type: 'gradient'//渐变色风格
        }, {
            skinid: 2,
            skinname: '背景色风格-2',
            src: '../../Static/img/skin/skin_02.png',
            css: '../../Static/css/skin/skin-t2-orange.css',
            type: 'gradient'
        }, {
            skinid: 3,
            skinname: '背景色风格-3',
            src: '../../Static/img/skin/skin_03.png',
            css: '../../Static/css/skin/skin-t2-blue.css',
            type: 'gradient'
        }, {
            skinid: 4,
            skinname: '背景色风格-4',
            src: '../../Static/img/skin/skin_04.png',
            css: '../../Static/css/skin/skin-t2-green.css',
            type: 'gradient'
        },
        {
            skinid: 5,
            skinname: '纯色风格-1',
            src: '../../Static/img/skin/skin_05.png',
            css: '../../Static/css/skin/skin-t1-green.css',
            type: 'purity'//纯背景色风格
        }, {
            skinid: 6,
            skinname: '纯色风格-2',
            src: '../../Static/img/skin/skin_06.png',
            css: '../../Static/css/skin/skin-t1-default.css',
            type: 'purity'
        }, {
            skinid: 7,
            skinname: '纯色风格-3',
            src: '../../Static/img/skin/skin_07.png',
            css: '../../Static/css/skin/skin-t1-blue.css',
            type: 'purity'
        }, {
            skinid: 8,
            skinname: '纯色风格-4',
            src: '../../Static/img/skin/skin_08.png',
            css: '../../Static/css/skin/skin-t1-red.css',
            type: 'purity'
        }
        //, {
        //    skinid: 9,
        //    skinname: '背景色风格-5',
        //    src: '../../Static/img/skin/skin_09.png',
        //    css: '../../Static/css/skin/skin-t2-purple.css',
        //    type: 'gradient'
        //}
    ],
    echart: {
        purity: {//渐变色风格相关参数
            textColor: '#000',//图表文字颜色
            lineColor: 'rgba(0,0,0,0.3)',//图表线条颜色
            icons: ['icon6.png', 'icon8.png', 'icon9.png', 'icon10.png', 'icon11.png', 'icon7.png']//Home页icon图片名称
        },
        gradient: {//纯背景色风格相关参数
            textColor: '#fff',//图表文字颜色
            lineColor: 'rgba(255,255,255,0.3)',//图表线条颜色
            icons: ['bai6.png', 'bai4.png', 'bai1.png', 'bai3.png', 'bai08.png', 'bai5.png']//Home页icon图片名称
        }
    }
}