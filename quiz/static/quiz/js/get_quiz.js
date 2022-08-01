const API_URL = new URL(window.location).origin
let getQuizResponse
let checked = []
var radioBtns = []
var inputFields = []

const attachMDCEffect = () => {
  let inputs = document.querySelectorAll('.mdc-text-field')
  console.log(inputs)
  inputFields = [...inputs].map((ele) =>
    mdc.textField.MDCTextField.attachTo(ele)
  )
  const chboxes = document.querySelectorAll(
    '.mdc-radio:not(.mdc-radio--disabled)'
  )
  console.log(chboxes)
  radioBtns = [...chboxes].map((ele) => new mdc.radio.MDCRadio.attachTo(ele))
  console.log(radioBtns)
  //   const bars = document.querySelectorAll('.mdc-snackbar')
  //   snackbars = [...bars].map((ele) => new mdc.snackbar.MDCSnackbar.attachTo(ele))
  //   console.log(snackbars)
}

const attachQuizAnsCheckboxes = () => {
  console.log('heheheh')
  $('.play-quiz-checkbox').change((evt) => {
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
  })
}

$('.quiz-card')
  .off()
  .click((evt) => {
    evt.preventDefault()

    const id = parseInt(evt.currentTarget.id)

    fetch(`${API_URL}/get_quiz/${id}`, {
      method: 'GET',
    })
      .then((resp) => resp.json())
      .then((response) => {
        console.log(response)
        getQuizResponse = response
        const parent = $('.play-quiz .quiz-preview-parent')
        parent.empty()
        getQuizResponse.questions.forEach((q, index) => {
          let ele = $('.play-quiz .quiz-question-row.d-none').clone()
          ele.attr('id', `quiz-${q.id}`)
          ele.find('.quiz-no-txt').text(`Q${index + 1}`)
          ele.find('.quiz-question-txt').text(q.question)
          q.answers.forEach((a, ansIndex) => {
            let checkboxClone = $('.play-quiz .ans-radio-btn.d-none').clone()
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
            if (a.is_correct) {
            }
          })

          ele.removeClass('d-none')
          parent.append(ele)
        })
        checked = [...new Array(getQuizResponse.questions.length).fill('')]
        attachQuizAnsCheckboxes()

        $('.play-quiz .quiz-preview-parent').removeClass('d-none')
        if (getQuizResponse.questions.length > 0) {
          $('#save-play-quiz-btn').removeClass('d-none')
        } else {
          $('#save-play-quiz-btn').addClass('d-none')
        }

        attachMDCEffect()
      })
  })

//---- Save quiz answers for performance ----//
const saveQuizData = () => {
  let answers = getQuizResponse.questions.map((c, i) => ({
    question_id: c.id,
    answer_id: checked[i],
  }))

  let data = {
    quiz_id: getQuizResponse.id,
    event_id: parseInt((Math.random() * 10).toFixed(0)),
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
    })
    .catch((err) => {
      console.log(err)
    })
}

$('#save-play-quiz-btn')
  .off()
  .click((evt) => {
    evt.preventDefault()
    saveQuizData()
  })

$(document).ready(() => {
  attachMDCEffect()
})
