$(document).ready(function () {
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
});