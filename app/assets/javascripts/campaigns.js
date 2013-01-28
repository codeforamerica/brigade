$(document).ready(function() {
  function filterPath(string) {
  return string
    .replace(/^\//,'')
    .replace(/(index|default).[a-zA-Z]{3,4}$/,'')
    .replace(/\/$/,'');
  }
  var locationPath = filterPath(location.pathname);
  var scrollElem = scrollableElement('html', 'body');
 
  $('a[href*=#]').each(function() {
    var thisPath = filterPath(this.pathname) || locationPath;
    if (  locationPath == thisPath
    && (location.hostname == this.hostname || !this.hostname)
    && this.hash.replace(/#/,'') ) {
      var $target = $(this.hash), target = this.hash;
      if (target) {
        var targetOffset = $target.offset().top;
        $(this).click(function(event) {
          event.preventDefault();
          $(scrollElem).animate({scrollTop: targetOffset}, 400, function() {
            location.hash = target;
          });
        });
      }
    }
  });
 
  // use the first element that is "scrollable"
  function scrollableElement(els) {
    for (var i = 0, argLength = arguments.length; i <argLength; i++) {
      var el = arguments[i],
          $scrollElement = $(el);
      if ($scrollElement.scrollTop()> 0) {
        return el;
      } else {
        $scrollElement.scrollTop(1);
        var isScrollable = $scrollElement.scrollTop()> 0;
        $scrollElement.scrollTop(0);
        if (isScrollable) {
          return el;
        }
      }
    }
    return [];
  }
  
  $('.collapse').collapse();
  if ($('.collapse').collapse() === true) {
      $('.collapse').collapse();
  }

  $('#pledge-form-learn-more-primary').on('click', function(){
      $('.pledge-form-inner.primary').fadeOut('fast', function(){
          $('.pledge-form-inner.secondary').fadeIn('fast');
      });
      return false;
  });

  $('#pledge-form-learn-more-secondary').on('click', function(){
      $('.pledge-form-inner.secondary').fadeOut('fast', function(){
          $('.pledge-form-inner.primary').fadeIn('fast');
      });
      return false;
  });

  $('#flash-join-form').on('click', function(){
      $('.pledge-form-inner').css('border-color', '#FDB63E');
      return false;
  });
  
  $('#flash-race-form').on('click', function(){
      $('.pledge-form-inner').css('border-color', '#203B7F');
      return false;
  });
 
});