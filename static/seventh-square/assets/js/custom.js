

function EmailExist(value){
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url : '/user/email-check/',
        type: 'post',
        data: {'email':value,'csrfmiddlewaretoken':token},
        success: function(status){
            if(status === false){
                $('#id_emailError').html('<div class="valid-feedback d-block" id="id_email-error">This email is available!</div>');
            }else{
                $('#id_emailError').html('<div class="invalid-feedback d-block" id="id_email-error">This email already registed in our site !</div>');
            }
        },
    })
}


// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
  })()