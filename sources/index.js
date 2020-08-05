import $ from 'jquery';
import 'bootstrap';
import 'popper.js';
import moment from 'moment';

import './js/vendor/bootstrap-datepicker';

// SCSS or SASS here
import './main.scss';
import '@fortawesome/fontawesome-free/js/all';

// Images
import './img/logo.png';
import './img/avatar_male.png';
import './img/avatar_female.png';
// import './img/logo.svg';
// import './img/favicon.ico';

// Fonts

// Javascripts
window.jQuery = $;
window.$ = $;
window.moment = moment;

$(function() {
    $('[data-toggle="tooltip"]').tooltip();
    
    // Bootstrap Datepicker
    $('.datetimepicker').datetimepicker();
    // $('.datepicker').datepicker();
    // $('.timepicker').timepicker();
});