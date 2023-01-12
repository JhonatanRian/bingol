$(document).ready(function () {
  $('.js-date').mask('00/00/0000', {
    onComplete(value, event, currentField) {
      if ($(currentField).hasClass('birthday_affiliate')) {
        const validate = ValidateDOB($(currentField));
        const submit = $(currentField).parents('form').find('.js-save-item');
        if (validate.status) {
          submit.removeAttr('disabled');
        } else {
          alert(validate.message);
          $(currentField).val('').focus();
          submit.attr('disabled', '');
        }
      }
    }
  });
  $('#data_nascimento').blur(function () {
    const submit = $(this).parents('form').find('.js-save-item');
    if ($(this).val() === '') {
      $(this).val('').focus();
      submit.attr('disabled', '');
    }
  })
  $('.js-time').mask('00:00:00');
  $('.js-date_time').mask('00/00/0000 00:00:00');

  $('.js-cep').mask('00000-000', {
    onComplete(cep, event, currentField) {
      const replaceCep = cep.replace('.', '').replace('-', '');
      const address = '.js-rua';
      const neighborhood = '.js-bairro';
      const city = '.js-cidade';
      const uf = '.js-estado';
      const number = '.js-numero';
      $.ajax({
        url: `https://viacep.com.br/ws/${replaceCep}/json/`,
        type: 'post',
        dataType: 'jsonp',
        crossDomain: true,
        contentType: 'application/json',
        beforeSend() {
          $(address).attr('disabled', true);
          $(neighborhood).attr('disabled', true);
          $(city).attr('disabled', true);
          $(uf).attr('disabled', true);

          swal({
            'text': 'Aguarde...',
            'button': false
          });
        },
      })
        .always((json) => {
          if (json.erro) {
            swal.close();
            swal(
              'Oops...',
              'O CEP digitado não está correto. Tente novamente!',
              'error',
            );
            $(address).attr('disabled', false);
            $(neighborhood).attr('disabled', false);
            $(city).attr('disabled', false);
            $(uf).attr('disabled', false);
            return false;
          }

          $(address).attr('disabled', false);
          $(neighborhood).attr('disabled', false);
          $(city).attr('disabled', false);
          $(uf).attr('disabled', false);

          $(address).val(json.logradouro);
          $(neighborhood).val(json.bairro);
          $(city).val(json.localidade);
          $(uf).val(json.uf);

          $(number).focus();

          swal.close();
        });
    }
  });
  $('.js-phone').mask('0000-0000');
  $('.js-phone_with_ddd').mask('+00 (00) 00000-0000');
  $('.js-phone_us').mask('(000) 000-0000');
  $('.js-phone_br').mask('(00) 0000-0000');
  $('.js-mixed').mask('AAA 000-S0S');
  $('.js-cpf').mask('000.000.000-00', {reverse: true});
  $('.js-cnpj').mask('00.000.000/0000-00', {reverse: true});
  $('.js-money').mask('000.000.000.000.000,00', {reverse: true});
  $('.js-money-wth-rs').mask('R$ 000.000.000.000.000,00', {reverse: true});
  $('.js-money2').mask("#.##0,00", {reverse: true});
  $('.js-ip_address').mask('0ZZ.0ZZ.0ZZ.0ZZ', {
    translation: {
      'Z': {
        pattern: /[0-9]/, optional: true
      }
    }
  });
  $('.js-ip_address').mask('099.099.099.099');
  $('.js-percent').mask('##0,00%', {reverse: true});
  $('.js-clear-if-not-match').mask("00/00/0000", {clearIfNotMatch: true});
  $('.js-placeholder').mask("00/00/0000", {placeholder: "__/__/____"});
  $('.js-fallback').mask("00r00r0000", {
    translation: {
      'r': {
        pattern: /[\/]/,
        fallback: '/'
      },
      placeholder: "__/__/____"
    }
  });
  $('.js-selectonfocus').mask("00/00/0000", {selectOnFocus: true});

  var SPMaskBehavior = function (val) {
      return val.replace(/\D/g, '').length === 11 ? '+00 (00) 00000-0000' : '+00 (00) 00000-0000';
    },
    spOptions = {
      onKeyPress: function (val, e, field, options) {
        field.mask(SPMaskBehavior.apply({}, arguments), options);
      }
    };

  $('.js-cellphones').mask(SPMaskBehavior, spOptions);
});

function ValidateDOB(element) {  //Get the date from the TextBox.
  var dateString = element[0].value;
  var regex = /(((0|1)[0-9]|2[0-9]|3[0-1])\/(0[1-9]|1[0-2])\/((19|20)\d\d))$/;

  let message = '';
  let status = true;

  //Check whether valid dd/MM/yyyy Date Format.
  if (regex.test(dateString)) {
    var parts = dateString.split("/");
    var dtDOB = new Date(parts[1] + "/" + parts[0] + "/" + parts[2]);
    var dtCurrent = new Date();
    message = "Você deve ter mais de 18."
    if (dtCurrent.getFullYear() - dtDOB.getFullYear() < 18) {
      status = false;
      return {'status': status, 'message': message};
    }

    if (dtCurrent.getFullYear() - dtDOB.getFullYear() == 18) {

      //CD: 11/06/2018 and DB: 15/07/2000. Will turned 18 on 15/07/2018.
      if (dtCurrent.getMonth() < dtDOB.getMonth()) {
        status = false;
        return {'status': status, 'message': message};
      }
      if (dtCurrent.getMonth() == dtDOB.getMonth()) {
        //CD: 11/06/2018 and DB: 15/06/2000. Will turned 18 on 15/06/2018.
        if (dtCurrent.getDate() < dtDOB.getDate()) {
          status = false;
          return {'status': status, 'message': message};
        }
      }
    }
    message = "";
    status = true;
  } else {
    message = "Informe uma data com formato válido dd/mm/YYYY."
    status = false;
  }

  return {'status': status, 'message': message};
}
