var version = '2.2.3';
var sp = location.href.lastIndexOf('/');
var ep = location.href.lastIndexOf('.html');
var curPage = sp < ep ? location.href.slice(sp + 1, ep) : 'index';
var enVersion = (location.hash && location.hash.indexOf('-en') != -1)
                || location.href.indexOf('-en') != -1;

var activeClass = {};
var loc = {};
var forkWidth = 149;
curPage = curPage.replace('-en', '');
var isExample = false;
switch (curPage) {
    case 'index' :
        activeClass[curPage] = 'active';
        loc[curPage] = '.';
        loc.feature = './doc';
        loc.example = './doc';
        loc.doc = './doc';
        loc.about = './doc';
        loc.changelog = './doc';
        loc.start = './doc';
        loc.img = './doc';
        break;
    case 'feature' :
    case 'example' :
    case 'doc' :
    case 'about' :
    case 'changelog' :
    case 'start' :
        activeClass[curPage] = 'active';
        loc.index = '..';
        break;
    default :
        isExample = true;
        forkWidth = 60;
        activeClass['example'] = 'active';
        var extSub = location.href.indexOf('extension') != -1 ? '../' : '';
        loc.index = extSub + '../..';
        loc.feature = extSub + '../../doc';
        loc.example = extSub + '../../doc';
        loc.doc = extSub + '../../doc';
        loc.about = extSub + '../../doc';
        loc.changelog = extSub + '../../doc';
        loc.start = extSub + '../../doc';
        loc.img = extSub + '../../doc';
        break;
}

$('#head')[0].innerHTML = 
    '<div class="container">'
        + '<div class="navbar-header">'
        + '</div>'
        + '<div class="navbar-collapse collapse" id="nav-wrap">'
          + '<ul class="nav navbar-nav navbar-right" id="nav" style="max-width:100%;">'
          /*
            + '<li><a href="../"><u>Search Again</u></a></li>'
            + '<li><a href="../../admin"><u>Home</u></a></li>'
          */
          + '</ul>'
        + '</div><!--/.nav-collapse -->'
      + '</div>';
      
function back2Top() {
    $("body,html").animate({scrollTop:0},1000);
    return false;
}

function changeVersion() {
    if (!isExample) {
        window.location = curPage + (enVersion ? '' : '-en') + '.html'
    }
    else {
        window.location = curPage + '.html' + (enVersion ? '' : '#-en'); 
        if (enVersion) {
            window.location.hash = window.location.hash.replace('-en', '');
        }
        window.location.reload();
    }
}


$('#footer')[0].style.marginTop = '50px';
/* The $('#footer')[0].innerHTML  is the bottom of page, I have comment all links */
$('#footer')[0].innerHTML =
     '<div class="container">'
        + '<div class="row" style="padding-bottom:20px;">'
            + '<div class="col-md-3">'
            + '</div>'
            + '<div class="col-md-3">'
            + '</div>'
            + '<div class="col-md-3">'
            + '</div>'
            + '<div class="col-md-3 flogo">'
            + '</div>'
        + '</div>'
    + '</div>';


if (document.location.href.indexOf('local') == -1) {
    var hm = document.createElement("script");
    hm.src = "//hm.baidu.com/hm.js?4bad1df23f079e0d12bdbef5e65b072f";
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(hm, s);
}

function fixFork () {
    var navMarginRight = 0;
    var bodyWidth = document.body.offsetWidth;
    var contnetWidth = $('#nav-wrap')[0].offsetWidth;
    if (bodyWidth < 1440) {
        navMarginRight = 150 - (bodyWidth - contnetWidth) / 2;
    }
    $('#nav')[0].style.marginRight = navMarginRight + 'px';
    $('#fork-image')[0].style.width = (document.body.offsetWidth < 768 ? 1 : forkWidth) + 'px';
};
fixFork();
$(window).on('resize', fixFork);
