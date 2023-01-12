"use strict";
$(document).ready(function () {
  const baseUrl = $('meta[name="base_url"]').attr('content');
  const submitButton = $('.js-save-item');
  const submitButtonConfirm = $('.js-save-item-confirm');
  const sendingText = submitButton.data('feedback') ? submitButton.data('feedback') : 'Aguarde...';
  const submitButtonTextDefault = submitButton.html();
  let target = '';
  let form = '';

  $("#depositoComprovante").on('change', function (el) {
    const fileName = el.target.files[0].name;
    const target = $(this).parent().find('.inputAnexar span:first');
    if (fileName) {
      target.html(fileName);
    } else {
      target.html('Nome do arquivo importado');
    }
  })

  /**
   *
   */
  submitButton.on('click', function (el) {
    sendForm(el);
  });

  submitButtonConfirm.on('click', function (el) {
    sendFormConfirm(el);
  });

  /**
   * Seta novos dados do form do botão apertado
   * @param event
   */
  function setjQueryAttrs(event) {
    event.preventDefault();

    target = $(event.target);
    form = target.parents('form');
  }

  function getCheckData(action, input, value) {
    var response = false;
    const data = {};
    data['action'] = action;
    data[input] = value;
    $.ajax({
      type: "POST",
      async: false,
      url: baseUrl + "/checkData",
      data: data,
      dataType:"html",
      success: function(responseData)
      {
        if (responseData == '0') {
          response = true;
        } else {
          response =  false;
        }
      }
    });
    return response;
  }

  $.validator.addMethod(
    "uniqueNickname",
    function(value, element) {
      if (value.length >= 4 && value.length <= 8) {
        return getCheckData('checkNickname', 'nickname', value);
      }
    },
    "O apelido já está em uso."
  );

  $.validator.addMethod(
    "uniqueEmail",
    function(value, element) {
      if (value.length >= 4) {
        return getCheckData('checkEmail', 'email', value);
      }
    },
    "O e-mail já está em uso."
  );

  $.validator.addMethod(
    "maisDeDezoito",
    function(value, element) {
      var regex = /(((0|1)[0-9]|2[0-9]|3[0-1])\/(0[1-9]|1[0-2])\/((19|20)\d\d))$/;

      //Check whether valid dd/MM/yyyy Date Format.
      if (regex.test(value)) {
        var parts = value.split("/");
        var dtDOB = new Date(parts[1] + "/" + parts[0] + "/" + parts[2]);
        var dtCurrent = new Date();
        if (dtCurrent.getFullYear() - dtDOB.getFullYear() < 18) {
          return false;
        }

        if (dtCurrent.getFullYear() - dtDOB.getFullYear() == 18) {
          //CD: 11/06/2018 and DB: 15/07/2000. Will turned 18 on 15/07/2018.
          if (dtCurrent.getMonth() < dtDOB.getMonth()) {
            return false;
          }
          if (dtCurrent.getMonth() == dtDOB.getMonth()) {
            //CD: 11/06/2018 and DB: 15/06/2000. Will turned 18 on 15/06/2018.
            if (dtCurrent.getDate() < dtDOB.getDate()) {
              return false;
            }
          }
        }
        return true;
      } else {
        return false;
      }
    },
    "Você deve ter mais de 18 anos"
  );


  /**
   * Adiciona novas regras de validação
   * @returns {Boolean|*}
   */
  function validateForm() {
    /**
     * Adicionando regra para validação de checkbox e radio
     */
    form.validate({
      rules: {
        email_confirm: {
          equalTo: "#email"
        },
        pass_confirm: {
          equalTo: "#senha"
        },
        nickname: {
          required: true,
          uniqueNickname: true
        }
      },
      messages: {
        nickname: {
          required: "O apelido é de preenchimento obrigatório",
          uniqueNickname: "Este apelido já está sendo usado."
        }
      },
      onclick: (element, event) => {
        if ($(element).prop('checked')) {
          const el = $(element)
            .parent()
            .parent()
            .find('.error-radio-input');
          el.remove();
        }
      },
      errorPlacement:
        (error, element) => {
          if ((element[0].type === 'radio' || element[0].type === 'checkbox') && element[0].name.length > 0) {
            $(element)
              .parent()
              .css('position', 'relative')
              .after(`<span class='error error-radio-input'>${error.text()}</label>`);
          } else {
            //  default label error
            error.insertAfter(element);
          }
        },
    });

    $("#depositoComprovante").rules('add', {
      required: true,
      accept: "application/pdf, image/jpeg, image/jpg, image/png"
    });


    return form.valid();
  }

  /**
   * Submete o form ao qual o botão submit interage
   * @param event
   */
  function sendForm(event) {
    try {
      setjQueryAttrs(event);

      if (form.valid()) {
        $(event.currentTarget).attr('disabled', true).html(sendingText);
        form.submit();
      }
    } catch (e) {
      console.error('Ocorreu um erro ao criar o item: ' + e);
    }
  }


  function sendFormConfirm(event) {
    setjQueryAttrs(event);
    event.preventDefault();

    try {
      setjQueryAttrs(event);

      if (form.valid()) {
        swal({
          title: "Você tem certeza?",
          text: submitButtonConfirm.data('confirm'),
          icon: "warning",
          buttons: true,
          dangerMode: true,
        })
          .then((accepted) => {
            if (accepted) {
              $(event.currentTarget).attr('disabled', true).html(sendingText);
              form.submit();
            }
          });
      }
    } catch (e) {
      console.error('Ocorreu um erro ao criar o item: ' + e);
    }
  }

  /**
   * Executa ação de questionamento ao tentar deletar
   */
  $('.js-delete').on('click', function (el) {
    const routeDelte = $(this).data('route');
    swal({
      title: "Você tem certeza?",
      text: "Esta ação não poderá ser revertida",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
      .then((willDelete) => {
        if (willDelete) {
          const form = document.createElement("form");
          document.body.appendChild(form);
          form.method = "POST";
          form.action = routeDelte;
          form.submit();
        }
      });
  });

  $('.js-print-data').on('click', function (e) {
    e.preventDefault();
    const telaImpressao = window.open('about:blank');
    telaImpressao.document.write($(`${$(this).data('target')} .modal-body`).html());
    telaImpressao.window.print();
    telaImpressao.window.close();
  })
});
