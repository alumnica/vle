import $ from 'jquery';
import whatInput from 'what-input';
window.$ = $;

// fullpage.js
import fullpage from 'fullpage.js';
window.fullpage = fullpage;



//Sweet Alert
import swal from 'sweetalert2';
window.swal = swal;

//masonry grid
import Masonry from 'masonry-layout';
window.Masonry = Masonry;


//jquery ui
import 'jquery-ui/ui/widgets/tooltip';
import 'jquery-ui/ui/widgets/selectable';
import 'jquery-ui/ui/effects/effect-slide';

// flip
import flip from 'flip';


// timeing function for data collection
import TimeMe from 'timeme.js';
window.TimeMe = TimeMe;

// progressbar.js
import ProgressBar from 'progressbar.js';
window.ProgressBar = ProgressBar;



// Foundation
import Foundation from 'foundation-sites';
$(document).foundation();

// initialize counting time spent on page

TimeMe.initialize({
  idleTimeoutInSeconds: 30, // seconds
});