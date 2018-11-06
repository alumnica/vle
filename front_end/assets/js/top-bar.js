//top navigation bar behaviour
$('#search-btn').click(function() {
  searchMenuClick();
});

$('#ham-btn').click(function() {
  menuShow();
  notiVisible();
});

$('.menu-cover').on('click', function() {
  menuShow();
});

$('.search-cover').on('click', function() {
  searchMenuClick();
});

function searchMenuClick() {
  notiVisible();
  var menuSatus = $('.main-menu').css('display');
  if (menuSatus == 'block') {
    menuShow();
  }
  $('#search-box').slideToggle();
  $('.search-cover').fadeToggle();
  if ($('#searcher').is(':focus')) {
    $('#searcher').blur();
  } else {
    $('#searcher').focus();
  }
  $('#search-btn').toggleClass('top-active');
}

function menuShow() {
  var searchStatus = $('#search-box').css('display');
  if (searchStatus == 'block') {
    $('#search-box').slideToggle();
    $('.search-cover').fadeToggle();
    $('#search-btn').toggleClass('top-active');
    $('#searcher').blur();
  }
  var menuSatus = $('.main-menu').css('display');
  if (menuSatus == 'block') {
    $('#ham-btn')
      .hide()
      .html(' <i class="fas fa-bars"></i>')
      .fadeIn();
  } else if (menuSatus == 'none') {
    $('#ham-btn')
      .hide()
      .html(' <i class="fa fa-times"></i>')
      .fadeIn();
  }
  $('.main-menu').slideToggle();
  $('.menu-cover').fadeToggle();
}

$('#ham-btn-out').click(function() {
  var menuSatus = $('.out-menu').css('display');
  if (menuSatus == 'block') {
    $('#ham-btn-out')
      .hide()
      .html(' <i class="fas fa-bars"></i>')
      .fadeIn();
  } else if (menuSatus == 'none') {
    $('#ham-btn-out')
      .hide()
      .html(' <i class="fa fa-times"></i>')
      .fadeIn();
  }
  $('.out-menu').slideToggle();
  $('.menu-cover-out').fadeToggle();
});

function notiVisible() {
  var notiStatus = $('.noti-cont').css('display');
  if (notiStatus == 'block') {
    $('.noti-cont').slideToggle(250);
  }
}

var notiCont = $('.noti-cont');

$('#noti-btn').on('click', function() {
  notiCont.slideToggle(250);
  var searchStatus = $('#search-box').css('display');
  if (searchStatus == 'block') {
    $('#search-box').slideToggle();
    $('.search-cover').fadeToggle();
    $('#search-btn').toggleClass('top-active');
    $('#searcher').blur();
  }
  var menuSatus = $('.main-menu').css('display');
  if (menuSatus == 'block') {
    menuShow();
  }
});