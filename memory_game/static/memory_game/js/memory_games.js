const API_URL = new URL(window.location).origin
const host = new URL(window.location).host

var id

var digits = num.toString().split('')
var digit = num.toString()

var realDigits = digits.map(Number)
var visible = 0

const attachMDCEffect = () => {
  //   const radioboxes =
  //     role === 'Therapist'
  //       ? document.querySelectorAll('.mdc-radio.mdc-radio--disabled')
  //       : document.querySelectorAll('.mdc-radio:not(.mdc-radio--disabled)')
  //   console.log(radioboxes)
  //   radioBtns = [...radioboxes].map((ele) => new mdc.radio.MDCRadio.attachTo(ele))
  const bars = document.querySelectorAll('.mdc-snackbar')
  snackbars = [...bars].map((ele) => new mdc.snackbar.MDCSnackbar.attachTo(ele))

  //   dialog = new mdc.dialog.MDCDialog(
  //     document.querySelector('.performance-show-modal')
  //   )
}

const displayVal = () => {
  if (visible == realDigits.length) {
    clearInterval(id)
    $('.input-memoize-value').removeClass('d-none')
    $('.save-memoize-value-btn').removeClass('d-none')
  } else {
    var fullWidth = window.innerWidth
    var fullHeight = window.innerHeight
    console.log($('.memory-number-container'))
    let parent = $('.memory-number-container')[0]
    let width = parent.clientWidth
    let height = parent.clientHeight

    var elem = document.createElement('div')

    elem.setAttribute('id', 'mydiv')
    elem.textContent = realDigits[visible]
    $(elem).fadeOut(speed)
    elem.style.position = 'absolute'
    elem.style.fontSize = 50 + 'px'
    elem.style.left =
      Math.round(Math.random() * (width - width / 2) + width / 2) + 'px'
    elem.style.top =
      Math.round(Math.random() * (height - height / 2) + height / 2) + 'px'
    elem.style.margin = 'auto'
    elem.style.padding = 10 + 'px'
    $('.memory-number-container')[0].append(elem)
    // document.body.appendChild(elem)

    visible++
  }
}
const show = () => {
  $('.memory-number-container-height').removeClass('d-none')
  id = setInterval(displayVal, speed)
}

const setupClientUI = () => {
  $('.memory-number-container-height').removeClass('d-none')
}

const setupRoomJoined = (payload) => {
  //---- only Therapist should get notified about client joined ----//
  console.log(payload)
  if (
    role === 'Therapist' &&
    (payload.role === 'Client') & (payload.status === 1)
  ) {
    const snackbar = snackbars.find((ele) =>
      $(ele.root).hasClass('quiz-join-snackbar')
    )
    console.log(snackbar)
    snackbar.timeoutMs = 4000
    snackbar.labelText = 'Client has joined'
    snackbar.open()
    // setupTherapistUI()
  }
}

$('.save-memoize-value-btn')
  .off()
  .click((evt) => {
    evt.preventDefault()
    const val = $('.input-memoize-value').val()
    console.log(val)
    let data = {
      client_id: id,
      inputnum: parseInt(val),
      room_code: parseInt(room_code),
      event_id: parseInt((Math.random() * 10).toFixed(0)),
    }
    console.log(document.cookie.split('=')[1])
    fetch(`${API_URL}/memory-game/performance/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.cookie.split('=')[1],
      },
      body: JSON.stringify(data),
    })
      .then((resp) => resp.json())
      .then((resp) => {
        console.log(resp)
      })
  })

$('#start-memory-game-btn')
  .off()
  .click((evt) => {
    let data = {
      type: 'start-quiz',
      start: true,
    }
    socket.send(JSON.stringify({ data }))
  })

const startQuizClientSide = () => {
  show()
}

const startWebsocketConnection = () => {
  console.log(room_code)
  console.log(role)
  socket = new WebSocket(`ws://${host}/ws/game/${room_code}`)
  console.log(socket)
  socket.onopen = (e) => {
    if (role === 'Client') {
      console.log('Client Joined---------')
      let data = {
        type: 'room-joined',
        role: 'Client',
        status: 1,
      }
      socket.send(JSON.stringify({ data }))
      setupClientUI()
    }
  }

  socket.onmessage = (m) => {
    console.log(m.data)
    // let payload = JSON.parse(m.data)
    let payload = JSON.parse(m.data).payload
    switch (payload.type) {
      case 'room-joined':
        setupRoomJoined(payload)
        break
      case 'start-quiz':
        role === 'Client' && startQuizClientSide()
        break
      case 'start-quiz-timer':
        startTimer()
        break
      case 'chosen-ans':
        role === 'Therapist' && updateTherapistUI(payload)
        break
      case 'show-score':
        role === 'Therapist' && showScoreModal(payload.percent)
        break
      case 'end-quiz':
        endQuiz()
        break
      default:
        break
    }
  }

  socket.onclose = (e) => {
    if (e.wasClean) {
      console.log(
        `connection closed cleanly with code=${e.code}, reason=${e.reason}`
      )
    } else {
      console.info('connection died')
    }
  }

  socket.onerror = (error) => {
    console.error(error)
  }
  return
}

$(document).ready(() => {
  console.log(num)
  console.log(speed)
  console.log(room_code)
  console.log(role)
  //   let url = new URL(window.location.href)
  //   let params = new URLSearchParams(url.search)

  //   event_id =
  //     role === 'Therapist'
  //       ? parseInt((Math.random() * 10).toFixed(0))
  //       : params.get('event_id')
  if (role === 'Client') startWebsocketConnection()
  console.log($('.memory-game div.link-to-copy'))
  attachMDCEffect()
  $('.memory_game .link-to-copy').val(
    `${API_URL}/memory-game/get-memory-num/${room_code}`
  )
})

$('.share-play-memory-game-btn')
  .off()
  .click((evt) => {
    evt.preventDefault()
    const link = `${API_URL}/memory-game/get-memory-num/${room_code}`
    if (navigator.clipboard) {
      navigator.clipboard.writeText(link).then(
        (val) => {
          const snackbar = snackbars.find((ele) =>
            $(ele.root).hasClass('quiz-link-cpy-snackbar')
          )
          snackbar.timeoutMs = 4000
          startWebsocketConnection()
          snackbar.open()
        },
        (err) => {
          console.error(err)
        }
      )
    } else {
      const snackbar = snackbars.find((ele) =>
        $(ele.root).hasClass('quiz-link-cpy-snackbar')
      )
      snackbar.labelText =
        "Can't copy to clipboard.Please manually copy the link."
      snackbar.timeoutMs = 4000
      snackbar.open()
      startWebsocketConnection()
    }
  })
