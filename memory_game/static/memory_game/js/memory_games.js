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
  const btns = document.querySelectorAll('.mdc-button')

  dialog = new mdc.dialog.MDCDialog(
    document.querySelector('.performance-show-modal')
  )
  formModal = new mdc.dialog.MDCDialog(
    document.querySelector('.create-memory-game-modal')
  )
}

const displayVal = () => {
  if (visible == realDigits.length) {
    clearInterval(id)
    $('.input-memoize-value').removeClass('d-none')
    $('.save-memoize-value-btn').removeClass('d-none')
  } else {
    let parent = $('.memory-number-container')[0]
    let width = parent.clientWidth
    let height = parent.clientHeight

    let elem = document.createElement('div')

    elem.setAttribute('id', 'mydiv')
    elem.textContent = realDigits[visible]
    $(elem).fadeOut(speed)
    elem.style.position = 'absolute'
    elem.style.fontSize = 40 + 'px'

    elem.style.left =
      Math.round(Math.random() * (width - elem.clientWidth)) + 'px'
    elem.style.top =
      Math.round(Math.random() * (height - elem.clientHeight)) + 'px'
    // elem.style.padding = 10 + 'px'
    console.log(elem)
    $('.memory-number-container')[0].append(elem)

    visible++

    // elem.style.left =
    //   Math.round(Math.random() * (width - width / 2) + width / 2) + 'px'
    // elem.style.top =
    //   Math.round(Math.random() * (height - height / 2) + height / 2) + 'px'
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
      client_id: client_id,
      inputnum: parseInt(val),
      displaynum: parseInt(digit),
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
        try {
          let data = {
            type: 'show-score',
            performance: resp.mPerformance,
          }
          socket.send(JSON.stringify({ data }))
          $('.save-memoize-value-btn').prop('disabled', true)
        } catch (error) {
          console.log(error)
        }
      })
      .catch((err) => {
        console.log(err)
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
    show()
  })

const startQuizClientSide = () => {
  show()
}

const setupModalListener = () => {
  var slider = document.getElementById('edit-range')
  var output = document.getElementById('edit-size')
  output.innerHTML = slider.value

  slider.oninput = function () {
    output.innerHTML = this.value
  }
}

$('.create-new-memory-number-btn')
  .off()
  .click((evt) => {
    evt.preventDefault()
    console.log(
      document.querySelector('input[name="inlineRadioOptions"]:checked')
    )
    let checkedEle = document.querySelector(
      'input[name="inlineRadioOptions"]:checked'
    )
    console.log($('#edit-size'))
    let range = $('#edit-size').text()
    console.log(range)

    if (checkedEle == null) {
      $('.error-txt').text('Please select Speed')
      return
    }
    let data = {
      client_id: parseInt(client_id),
      therapist_id: parseInt(therapist_id),
      range: parseInt(range),
      inlineRadioOptions: checkedEle.value,
      room_code: parseInt(room_code),
    }
    console.log(data)
    fetch(`${API_URL}/memory-game/create-memory-game/`, {
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
      .catch((err) => {
        console.log(err)
      })
  })

$('#change-memory-game-btn')
  .off()
  .click((evt) => {
    evt.preventDefault()
    let formContainer = $('.form-fields-container').removeClass('d-none')
    console.log(formContainer)
    $(
      '.create-memory-game-modal .mdc-dialog__container .mdc-dialog__surface'
    ).append(formContainer)
    console.log(therapist_id)
    formModal.open()
    setupModalListener()
  })

const showScoreModal = (performance) => {
  console.log(performance)
  console.log(role)
  if (role === 'Therapist') {
    dialog.open()
    $('.performance-show-modal .score-txt')
      .text(`Client entered:${performance.inputnumber}`)
      .addClass('text-dark')
    $('.performance-show-modal img.success').addClass('d-none')
    $('.performance-show-modal img.failed').addClass('d-none')
    $('#change-memory-game-btn').removeClass('d-none')
  } else if (role === 'Client') {
    if (performance.is_correct) {
      dialog.open()
      $('.performance-show-modal .score-txt')
        .text(`Hurray!! You memorize the number..!`)
        .addClass('text-dark')
      $('.performance-show-modal .success-txt')
        .text(`Number was: ${performance.memory_number}`)
        .addClass('text-dark')
      $('.performance-show-modal img.success').removeClass('d-none')
      $('.performance-show-modal img.failed').addClass('d-none')
    } else {
      dialog.open()
      $('.performance-show-modal .score-txt')
        .text(`Oops!! You entered wrong number.`)
        .addClass('text-dark')
      $('.performance-show-modal .success-txt')
        .text(`Number was: ${performance.memory_number}`)
        .addClass('text-dark')
      $('.performance-show-modal img.success').addClass('d-none')
      $('.performance-show-modal img.failed').removeClass('d-none')
    }
    return true
  }
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
        showScoreModal(payload.performance)
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
  console.log(client_id)
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
