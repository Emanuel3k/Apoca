$(document).ready(function() {
    $('#vertical-menu-btn').click(function() {
        sessionStorage.setItem('classes', $('body').attr('class'));
        $('#sidebar-logo').toggleClass('logo-sidebar-collapsed')
        sessionStorage.setItem('logo', $('#sidebar-logo').attr('class'));
    });
    $('body').addClass(sessionStorage.getItem('classes'));
    $('#sidebar-logo').addClass(sessionStorage.getItem('logo'));
});
