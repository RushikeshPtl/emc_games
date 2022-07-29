var checkboxes = []
var inputFields = []
var questions = []
var snackbars = []
let quiz_id

const attachMDCEffect = () => {
  let inputs = document.querySelectorAll('.mdc-text-field')
  console.log(inputs)
  inputFields = [...inputs].map((ele) =>
    mdc.textField.MDCTextField.attachTo(ele)
  )
  const chboxes = document.querySelectorAll('.mdc-checkbox')
  checkboxes = [...chboxes].forEach(
    (ele) => new mdc.checkbox.MDCCheckbox.attachTo(ele)
  )
  const bars = document.querySelectorAll('.mdc-snackbar')
  snackbars = [...bars].map((ele) => new mdc.snackbar.MDCSnackbar.attachTo(ele))
  console.log(snackbars)
}

const dialog = new mdc.dialog.MDCDialog(
  document.querySelector('.mdc-dialog.add-question-modal')
)
const select = new mdc.select.MDCSelect(
  document.querySelector('.mdc-select.form-field')
)

console.log(checkboxes)
console.log(snackbars)

$('.mdc-checkbox__native-control').change((evt) => {
  console.log('hehehe')
  console.log(evt)
  console.log(evt.currentTarget.id)
})

dialog.listen('MDCDialog:opened', () => {
  console.log('ehehehe')
  console.log(select)

  // console.log(select.getValue())
  // createAnsRows([...Array(4)].map((v, i) => i)) //---- default is 4 ----//
  // dialog.layout()
})

const attachCheckboxListener = () => {
  $('.mdc-checkbox__native-control.ans-checkbox').change((evt) => {
    const cb = document.querySelectorAll(
      '.mdc-checkbox__native-control.ans-checkbox'
    )

    const id = evt.currentTarget.id
    // const index = id.split('ans-checkbox-')[1]
    // let answerData = questionData.answers.find((a) => a.id === parseInt(index))

    // answerData['is_correct'] = $(evt.currentTarget).prop('checked')
    let filtered = [...cb].filter((c) => c.id !== id)
    filtered.forEach((ele, i) => {
      $(ele).prop('checked', false)
      // let updateInd = $(ele).attr('id').split('ans-checkbox-')[1]
      // questionData.answers[updateInd]['is_correct'] = false
    })
  })
}

const attachAnsTextListener = () => {
  $('.ans-txt').on('input', (evt) => {
    const ele = $(evt.currentTarget)[0].id
    const index = ele.split('-')[1]
    const data = $(evt.currentTarget).val()

    let answerData = questionData.answers.find((a) => a.id === parseInt(index))
    console.log(answerData)
    // answerData.answer = data
  })
}

const createAnsRows = (arr) => {
  $('.ans-container').empty()
  arr.forEach(function (ele, i) {
    let row = $('#ans-row').clone()
    row.attr('id', `row-${i}`).removeClass('d-none').addClass('ans-row')
    row
      .find('input.mdc-text-field__input')
      .attr('id', `input-${i}`)
      .attr('aria-labelledby', `question-${i}`)
    row
      .find('span.mdc-floating-label')
      .attr('id', `answer-${i}`)
      .text(`answer-${i + 1}`)
    row
      .find('input.mdc-checkbox__native-control')
      .attr('id', `ans-checkbox-${i}`)
      .addClass('ans-checkbox')
    row.removeClass('d-none')
    $('.ans-container').append(row)
  })
  $('.answers-section').removeClass('d-none')
  attachMDCEffect()
  attachCheckboxListener()
  // attachAnsTextListener()
}

select.listen('MDCSelect:change', () => {
  console.log(select.selectedIndex, select.value)
  if (select.selectedIndex !== -1) {
    const noOfAns = parseInt(select.value)
    console.log(noOfAns)

    var arr = [...Array(noOfAns)].map((v, i) => i)
    createAnsRows(arr)
    // questionData.answers = [...Array(noOfAns)].map((v, i) => ({
    //   id: i,
    //   answer: '',
    //   is_correct: false,
    // }))
  }
})

// $('#question-txt').on('input', (evt) => {
//   questionData.question = $(evt.currentTarget).val()
//   console.log(questionData)
// })

const createQuizQuestionsPreview = (data) => {
  $('#add-question .spinner-border').removeClass('d-none')
  $('#add-question .mdc-button__label').addClass('d-none')
  console.log(questions)
  fetch('/add_question/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((resp) => resp.json())
    .then((resp) => {
      console.log(resp)
      let parent = $('.quiz-preview-parent')
      $('.quiz-preview-parent').empty()

      questions.forEach((item, i) => {
        let q = $('.quiz-question-row.d-none').clone()
        q.attr('id', `quiz-${i}`)
        q.find('.quiz-no-txt').text(`Q${i + 1}`)
        q.find('.quiz-question-txt').text(item.question)
        item.answers.forEach((ans, index) => {
          let checkboxClone = $('.ans-radio-btn.d-none').clone()
          checkboxClone
            .find('.mdc-radio__native-control')
            .attr('id', `ans-${index}`)
          checkboxClone
            .find('label')
            .attr('for', `ans-${index}`)
            .text(ans.answer)
          checkboxClone.removeClass('d-none')
          q.find('.ans-options').append(checkboxClone)
        })

        q.removeClass('d-none')
        parent.append(q)
      })

      parent.removeClass('d-none')
      dialog.close()
      $('#question-txt').val('')
      select.selectedIndex = -1 //--- reset the select dropdown value ----//
      $('.ans-container').empty()
      $('.answers-section').addClass('d-none')
      $('.subheader-txt').removeClass('err')
      $('.add-more-questions-btn').removeClass('d-none')
      $('#create-quiz-btn').addClass('d-none')
      $('#add-question .spinner-border').addClass('d-none')
      $('#add-question .mdc-button__label').removeClass('d-none')
    })
  // $.post('/add_question/', questions[0], (resp) => {
  //   console.log(resp)
  // })
}

const checkFormFields = () => {
  $('.subheader-txt').removeClass('err')
  if (!$('#question-txt').val().length > 0) {
    const field = inputFields.find((ele) => ele.input.id === 'question-txt')
    field.valid = false
    field.helperTextContent = 'Please enter your question.'
    return
  }

  const ansTexts = [...$('.ans-txt')].filter((ele) => $(ele).attr('id'))
  if (ansTexts.filter((ele) => $(ele).val().length === 0).length > 0) {
    const emptyFields = ansTexts
      .filter((ele) => $(ele).val().length === 0)
      .map((e) => $(e).attr('id'))

    const fields = inputFields.filter(
      (ele) => emptyFields.findIndex((e) => e === ele.input.id) > -1
    )
    console.log(fields)

    fields.forEach((field) => {
      field.valid = false
      field.helperTextContent = 'Please enter answer'
    })
    return
  }
  const ansCheckboxes = [
    ...$('.mdc-checkbox__native-control.ans-checkbox'),
  ].filter((ele) => $(ele).attr('id'))

  if (ansCheckboxes.filter((ele) => $(ele).prop('checked')).length === 0) {
    $('.subheader-txt').addClass('err')
    return
  }

  const quizAnswers = ansTexts.map((ele, index) => ({
    answer: $(ele).val(),
    is_correct: $(ansCheckboxes[index]).prop('checked'),
  }))
  let questionData = {
    question: $('#question-txt').val(),
    difficulty: 'easy',
    quiz_id: quiz_id,
    answers: quizAnswers,
  }
  questions.push(questionData)

  createQuizQuestionsPreview(questionData)
}

const saveQuizData = () => {
  const data = {
    title: $('input[name="title"]').val(),
    category: $('input[name="category"]').val(),
    therapist_id: parseInt($('input[name="therapist_id"]').val()),
  }

  $.post('/create_quiz/', data, (resp) => {
    console.log(resp)
    quiz_id = resp.id
  })
  console.log(data)
}

$('#add-question')
  .off()
  .click((evt) => {
    evt.preventDefault()

    checkFormFields()
  })

$('.add-more-questions-btn')
  .off()
  .click((evt) => {
    evt.preventDefault()
    dialog.open()
  })

$('#create-quiz-btn')
  .off()
  .click((evt) => {
    evt.preventDefault()
    if (
      !(
        $('input[name="title"]').val().length > 0 &&
        $('input[name="category"]').val().length > 0 &&
        $('input[name="therapist_id"]').val().length > 0
      )
    ) {
      const snackbar = snackbars.find((ele) =>
        $(ele.root).hasClass('quiz-err-snackbar')
      )

      snackbar.open()
      return
    }
    dialog.open()
    saveQuizData()
  })

$(document).ready(() => {
  attachMDCEffect()
})
