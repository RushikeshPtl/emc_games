const API_URL = new URL(window.location).origin
// let checked = []
// var radioBtns = []
// var snackbars = []
// var socket = ''
// var dialog
// var event_id = ''
// var quizQuestions = []
// let intervalId

const attachMDCEffect = () => {
  const radioboxes =
    role === 'Therapist'
      ? document.querySelectorAll('.mdc-radio.mdc-radio--disabled')
      : document.querySelectorAll('.mdc-radio:not(.mdc-radio--disabled)')
  console.log(radioboxes)
  radioBtns = [...radioboxes].map((ele) => new mdc.radio.MDCRadio.attachTo(ele))
  const bars = document.querySelectorAll('.mdc-snackbar')
  snackbars = [...bars].map((ele) => new mdc.snackbar.MDCSnackbar.attachTo(ele))

  dialog = new mdc.dialog.MDCDialog(
    document.querySelector('.performance-show-modal')
  )
}

const getQuizData = async () => {
  try {
    return fetch(`${API_URL}/get_questions/${quiz_id}`, {
      method: 'GET',
    })
      .then((resp) => resp.json())
      .then((resp) => resp.questions)
  } catch (error) {
    console.error(error)
    return []
  }
}

const attachQuizAnsCheckboxes = () => {
  console.log('heheheh')
  $('.play-quiz-checkbox').change((evt) => {
    const id = evt.currentTarget.id
    const questionIndex = evt.currentTarget.id.split('-')[1]
    console.log(questionIndex)
    const radioSelected = radioBtns.filter(
      (r) => r.root.id === evt.currentTarget.id
    )[0]
    console.log(radioSelected.value)
    console.log(checked)
    let cpy = [...checked]
    cpy[questionIndex] = radioSelected.value
    checked = cpy
    let data = {
      type: 'chosen-ans',
      ans: id,
    }
    socket.send(JSON.stringify({ data }))
  })
}

//---- create Therapist side UI ----//
const setupTherapistUI = async () => {
  $('.start-quiz-btn').removeClass('d-none')
  const questions = await getQuizData()
  console.log(questions)
  if (questions.length > 0) {
    $('.quiz-title').text(title)
    questions.forEach((q, index) => {
      let ele = $('.quiz-question-row.d-none').clone()
      ele.attr('id', `quiz-${q.id}`)
      ele.find('.quiz-no-txt').text(`Q${index + 1}`)
      ele.find('.quiz-question-txt').text(q.question)
      q.answers.forEach((a, ansIndex) => {
        let checkboxClone = $('.ans-radio-btn.d-none').clone()
        checkboxClone
          .find('.mdc-radio')
          // .removeClass('mdc-radio--disabled')
          .attr('id', `ans-${index}-${ansIndex}`)
        checkboxClone
          .find('.mdc-radio__native-control')
          .attr('id', `ans-${index}-${ansIndex}`)
          .prop('name', `ans-radios-${index}`)
          .prop('disabled', false)
          .addClass('play-quiz-checkbox')
          .removeClass('mdc-radio--disabled')
          .val(a.id)
        checkboxClone
          .find('label')
          .attr('for', `ans-${ansIndex}`)
          .text(a.answer)

        checkboxClone.removeClass('d-none')
        ele.find('.ans-options').append(checkboxClone)
      })
      ele.removeClass('d-none')
      $('.play-quiz-content').append(ele)
    })
    $('.play-quiz-content').removeClass('d-none')
  }
}

//---- create Client side UI ----//
const setupClientUI = async () => {
  const questions = await getQuizData()
  quizQuestions = questions
  if (questions.length > 0) {
    $('.quiz-title').text(title)
    $('.quiz-helper').text(
      'questions will be visible when Therapist allows you to play.'
    )
    questions.forEach((q, index) => {
      let ele = $('.quiz-question-row.d-none').clone()
      ele.attr('id', `quiz-${q.id}`)
      ele.find('.quiz-no-txt').text(`Q${index + 1}`)
      ele.find('.quiz-question-txt').text(q.question)
      q.answers.forEach((a, ansIndex) => {
        let checkboxClone = $('.ans-radio-btn.d-none').clone()
        checkboxClone
          .find('.mdc-radio')
          .removeClass('mdc-radio--disabled')
          .attr('id', `ans-${index}-${ansIndex}`)
        checkboxClone
          .find('.mdc-radio__native-control')
          .attr('id', `ans-${index}-${ansIndex}`)
          .prop('name', `ans-radios-${index}`)
          .prop('disabled', false)
          .addClass('play-quiz-checkbox')
          .val(a.id)
        checkboxClone
          .find('label')
          .attr('for', `ans-${ansIndex}`)
          .text(a.answer)

        checkboxClone.removeClass('d-none')
        ele.find('.ans-options').append(checkboxClone)
      })
      ele.removeClass('d-none')
      $('.play-quiz-content').append(ele)
    })
    checked = [...new Array(questions.length).fill('')]

    $('.play-quiz-content').removeClass('d-none').addClass('blur')
  }
}

$('.start-quiz-btn')
  .off()
  .click((evt) => {
    console.log('start')
    let data = {
      type: 'start-quiz',
      start: true,
    }
    socket.send(JSON.stringify({ data }))
    $('.start-quiz-btn').prop('disabled', true)
  })

const startQuizClientSide = () => {
  $('.play-quiz-content').removeClass('blur')
  attachQuizAnsCheckboxes()
  attachMDCEffect()
  $('#save-quiz-btn').removeClass('d-none')
  let data = {
    type: 'start-quiz-timer',
  }
  socket.send(JSON.stringify({ data }))
}

const startTimer = () => {
  let deadline = moment().add(1, 'minute').add(1, 'seconds').toDate().getTime()

  role === 'Therapist' && attachMDCEffect()
  const countDown = () => {
    let now = moment().toDate().getTime()
    let t = deadline - now
    let seconds = parseInt(t / 1000)

    $('.timer')
      .removeClass('d-none')
      .text(
        moment
          .utc(moment.duration(seconds, 'seconds').as('milliseconds'))
          .format('mm:ss')
      )
    if (t < 0) {
      clearInterval(intervalId)
      saveQuizData()
    }
  }
  intervalId = setInterval(() => {
    countDown()
  }, 1000)
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
    setupTherapistUI()
  }
}

const updateTherapistUI = (data) => {
  const id = data.ans
  const questionIndex = id.split('-')[1]

  const radioSelected = radioBtns.filter((r) => r.root.id === id)[0]

  radioSelected.checked = true
  let cpy = [...checked]
  cpy[questionIndex] = radioSelected.value
}

//---- save Quiz answers ----//
const saveQuizData = () => {
  clearInterval(intervalId)
  let answers = quizQuestions.map((c, i) => ({
    question_id: c.id,
    answer_id: checked[i],
  }))
  console.log(quizQuestions)
  let data = {
    quiz_id: parseInt(quiz_id),
    event_id: parseInt(event_id),
    user_id: parseInt((Math.random() * 10).toFixed(0)),
    answers: answers,
  }
  console.log(data)
  console.log(document.cookie)
  fetch(`${API_URL}/performance/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.cookie.split('=')[1],
    },
    body: JSON.stringify(data),
  })
    .then((resp) => resp.json())
    .then((response) => {
      console.log(response)
      let data = {
        type: 'show-score',
        percent: response.percent,
      }
      socket.send(JSON.stringify({ data }))
      showScoreModal(response.percent)
    })
    .catch((err) => {
      console.log(err)
    })
}

const showScoreModal = (data) => {
  role === 'Therapist' && clearInterval(intervalId)
  $('.performance-show-modal .score-txt').text(`Score- ${data}`)

  if (data === 100) {
    role === 'Client' &&
      $('.performance-show-modal .success-txt').text('Hurray!! You won!')
    $('.performance-show-modal img.success').removeClass('d-none')
    $('.performance-show-modal img.failed').addClass('d-none')
  } else if (data < 90) {
    role === 'Client' &&
      $('.performance-show-modal .success-txt').text('Not Bad!! keep trying!')
    $('.performance-show-modal img.success').addClass('d-none')
    $('.performance-show-modal img.failed').removeClass('d-none')
  }
  dialog.open()
}

$('#save-quiz-btn')
  .off()
  .click((evt) => {
    evt.preventDefault()
    saveQuizData()
  })

const startWebsocketConnection = () => {
  console.log(quiz_id)
  console.log(room_code)
  console.log(role)
  socket = new WebSocket(`ws://127.0.0.1:8000/ws/game/${room_code}`)
  socket.onopen = (e) => {
    if (role === 'Client') {
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
  console.log(quiz_id)
  console.log(room_code)
  console.log(role)
  console.log(window.location.href)
  let url = new URL(window.location.href)
  let params = new URLSearchParams(url.search)
  console.log(params.has('room'))
  //---- check if URL has room code , if it's then Student has logged-in----//
  if (params.has('room')) {
    startWebsocketConnection()
    console.log(socket)
  }
  event_id = params.get('event_id')
  attachMDCEffect()
})

$('.share-play-quiz-btn')
  .off()
  .click((evt) => {
    evt.preventDefault()
    const link = `${API_URL}/get_room/${quiz_id}?event_id=${event_id}&room=${room_code}`
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
    }
  })
