
$(document).ready(function () {
  $('#fullpage').fullpage({
    anchors: ['firstPage', 'secondPage', '3rdPage', '4thPage', '5thPage', '6thPage'],
    // sectionsColor: ['#C63D0F', '#1BBC9B', '#7E8F7C'],
    navigation: true,
    navigationPosition: 'left',
    // navigationTooltips: ['First page', 'Second page', 'Third and last page'],
    paddingBottom: '3rem',
    paddingTop: '3rem',
    verticalCentered: false,
  });
});
