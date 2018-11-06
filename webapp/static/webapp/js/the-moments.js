$(document).ready(function () {
  new fullpage('#moments', {
    verticalCentered: false,
    slidesNavigation: false,
    loopHorizontal: false,
    licenseKey: 'OPEN-SOURCE-GPLV3-LICENSE',
  });

  $('.end-uoda-btn').on('click', function () {
    let timeSpentOnPage = TimeMe.getTimeOnCurrentPageInSeconds();
    let duration = timeSpentOnPage.toString().slice(0, -1);
    duration = `PT${duration}S`;
    console.log(duration);
    $.ajax({
        method: 'POST',
        type: 'POST',
        url: '/api/microodas/' + learner + "," + microoda + "," + duration + "/",
        success: function (data) {
          $('.end-uoda-btn').hide();
          $('.end-scoring').fadeIn()
          $('.end-scoring_btn').attr('href','/odas/'+ data.oda + '/')
          showNum();
        }

      }
    );
  })

  function upCounter() {
  $('.end-scoring_score').toggleClass('show');
  $('.xp-number').each(function() {
    $(this)
      .prop('Counter', 0)
      .animate(
        {
          Counter: $(this).text(),
        },
        {
          duration: 2000,
          easing: 'swing',
          step: function(now) {
            $(this).text(Math.ceil(now));
          },
        }
      );
  });
}


async function showNum() {
  await showBoxes();
  setTimeout(upCounter, 2000);
}

var items = $('.bonus-box');

async function showBoxes() {
  for (var i = 0; i < items.length; i++) {
    // get function in closure, so i can iterate
    var toggleItemMove = getToggleItemMove(i);
    // stagger transition with setTimeout
    setTimeout(toggleItemMove, i * 500);
  }
}

function getToggleItemMove(i) {
  var item = items[i];
  return function() {
    $(item).toggleClass('show');
  };
}
//   $('.end-uoda-btn').click(function () {
//     let timeSpentOnPage = TimeMe.getTimeOnCurrentPageInSeconds();
//     let duration = timeSpentOnPage.toString().slice(0, -1);
//     duration = `PT${duration}S`;
//     console.log(duration);
//     $.ajax({
//         method: 'POST',
//         type: 'POST',
//         url: '/api/microodas/' + learner + "," + microoda + "," + duration + "/",
//         success: function (data) {
//           // window.location.href = "/odas/" + data.oda + "/";
//         }
//
//       }
//     );
//   });
});

