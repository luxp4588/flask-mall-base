$(document).ready(function () {
    var $submenu = $('.submenu');//<ul class="submenu">
    var $mainmenu = $('.mainmenu');//<ul class="mainmenu">
    var $active = $('.active_focus')
    $submenu.hide();//所有的都不伸展
    if(!navigator.userAgent.match(/mobile/i)) {
        $active.next('.submenu').delay(100).slideDown(400);
    }
    //点击Basics、Picture等左侧变颜色
    $submenu.on('click', 'li', function () {
        /*
        siblings() 方法返回被选元素的所有同级元素。
        同级元素是共享相同父元素的元素。
        */
        $submenu.siblings().find('li').removeClass('chosen');
        $(this).addClass('chosen');
    });
    //点击Account、Messages等展开子元素
    /*
    next() 方法返回被选元素的后一个同级元素。
    同级元素是共享相同父元素的元素。注意：该方法只返回一个元素。
 
    slideToggle() 方法在被选元素上进行 slideUp() 和 slideDown() 之间的切换。
    该方法检查被选元素的可见状态。如果一个元素是隐藏的，则运行 slideDown()，如果一个元素是可见的，则运行 slideUp() - 这会造成一种切换的效果。
 
    slideUp() 方法以滑动方式隐藏被选元素。
    注意：隐藏的元素不会被完全显示（不再影响页面的布局）。
    */
    $mainmenu.on('click', 'li', function () {
        $(this).next('.submenu').slideToggle().siblings('.submenu').slideUp();
		$(this).siblings().removeClass('list-group-item-success');
		$(this).addClass('list-group-item-success')
    });
    $mainmenu.children('li:last-child').on('click', function () {
        //$mainmenu.fadeOut().delay(500).fadeIn();
    });
});