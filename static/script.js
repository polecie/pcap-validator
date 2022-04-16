const burst = new mojs.Burst({
    radius: {0:100},
    count: 20
  })

const timeline = new mojs.Timeline({
    repeat: 999
  })

    .add(burst)
    .play()