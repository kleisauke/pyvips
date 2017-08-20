$(document).ready(function() {
    // Default to collapsed
    $('dl.staticmethod, dl.method').addClass('collapsed')

    $('dl.staticmethod > dt, dl.method > dt').click(function(e) {
        $(this).parent().toggleClass('collapsed');
    });

    // Attaching the hashchange event listener
    $(window).on('hashchange', function() {
        base = window.location.hash.replace(/\./g, '\\.');
        base = $(base);
        base.parent().removeClass('collapsed');
    });

    // Manually tiggering it if we have hash part in URL
    if (window.location.hash) {
        $(window).trigger('hashchange')
    }
});