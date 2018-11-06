$(document).ready(function () {
   let learnerPoints,
       learnerNextLevel,
       learnerBar,
       avatarPoints;
// $.when(getLearnerInfo()).done(learnerProgressBar(),avatarProgressBar());
  getLearnerInfo();

  function getLearnerInfo(){
  $.ajax({
    type: 'GET',
    url: '/api/xp',
    data: {
      'learner': learner,
    },
    success: function(data) {
      avatarPoints = data.avatar_points.toFixed(2);
      learnerPoints = data.learner_points;
      learnerNextLevel = data.learner_next_level_points;
      learnerBar = learnerPoints / learnerNextLevel;
      learnerBar = learnerBar.toFixed(2);
      learnerProgressBar(learnerPoints, learnerBar);
      avatarProgressBar(avatarPoints);
    },
  });
  };

  function learnerProgressBar(bigNum, barNum){
  let bar = new ProgressBar.Line(progress, {
  strokeWidth: 1,
  easing: 'easeInOut',
  duration: 1400,
  color: 'white',
  trailColor: '#eee',
  trailWidth: 1,

  from: { color: '#FFEA82' },
  to: { color: '#38d430' },
  step: (state, bar) => {
    bar.path.setAttribute('stroke', state.color);
  },
  text: {
    // Initial value for text.
    // Default: null
    value: bigNum,

    style: {
      transform: {
        prefix: true,
        value: 'translateY(-50%)',
      },
    },

    // Class name for text element.
    // Default: 'progressbar-text'
    // className: 'progressbar__label',
  }
});
bar.animate(barNum); // Number from 0.0 to 1.0
  };

  function avatarProgressBar(barNum){
if ($('.avatar-progress').length){
  let avatarBar = new ProgressBar.Line(avatarProgress, {
  strokeWidth: 2,
  easing: 'easeInOut',
  duration: 1400,
  color: 'orange',
  trailColor: '#eee',
  trailWidth: 2,
});

avatarBar.animate(barNum); // Number from 0.0 to 1.0
  }
};

});
