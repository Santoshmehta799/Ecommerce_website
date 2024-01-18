
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

// validators
jQuery.validator.addMethod("alpha", function(value, element) {
  return this.optional(element) || /^[A-Za-z ]+$/i.test(value);
}, "Letters, and space only please");

jQuery.validator.addMethod("alphanumeric", function(value, element) {
  return this.optional(element) || /^[A-Za-z0-9 ]+$/i.test(value);
}, "Letters, Number and space only please");


jQuery.validator.addMethod("numeric", function(value, element) {
  return this.optional(element) || /^[0-9]+$/i.test(value);
}, "Invalid, Number only please");

jQuery.validator.addMethod('filesize', function (value, element, param) {
  return this.optional(element) || (element.files[0].size <= param * 1000000)
}, 'File size must be less than {0} MB');

jQuery.validator.addMethod("panregex", function(value, element) {
  return this.optional(element) || /^[A-Z]{3}[PCHABGJLFT][A-Z][0-9]{4}[A-Z]$/i.test(value);
}, "Invalid Pan Number. Validation Failed.");

jQuery.validator.addMethod("gstregex", function(value, element) {
  return this.optional(element) || /^[0-9][1-9][A-Z]{3}[PCHABGJLFT][A-Z][0-9]{4}[A-Z][0-9][Z][a-zA-Z0-9]$/i.test(value);
}, "Invalid GST Number. Validation Failed.");



// functions
function EmailExist(value){
  var token = $("input[name=csrfmiddlewaretoken]").val();
  if(value.length >= '2'){
    $.ajax({
        url : '/user/email-check/',
        type: 'post',
        data: {'email':value, 'csrfmiddlewaretoken':token},
        success: function(status){
            if(status === false){
              $('#id_emailError').html('<div class="valid-feedback d-block" id="id_email-error"></div>');
                
            }else{
              $('#id_emailError').html('<div class="invalid-feedback d-block" id="id_email-error">This email already registed in our site !</div>');
            }
        },
    });
  }
}


function SendOtpToContactNunber(value){
  var mobileNumber = document.getElementById("id_mobile_number").value;
  var mobileSendOtp = document.getElementById("id_mobile_send_otp");
  var token = $("input[name=csrfmiddlewaretoken]").val();
  var buttonSubmit = document.getElementById("submit-basic-form");
  var entermobileotp = document.getElementById("id_mobile_otp");
  var mobileNumberParentElement = entermobileotp.parentNode;

  if (/^\d{10}$/.test(mobileNumber)) {
    $.ajax({
      url : '/user/auth/signin-otp/',
      type: 'post',
      data: {'contact_number':mobileNumber, 'csrfmiddlewaretoken':token},
      success(data){
        console.log(data);
        if(data.status == true){
          $('#id_mobile_numberError').html('<div class="valid-feedback d-block" id="id_mobile_numberError">'+data.msg+'</div>');
          if(mobileNumber.length == '10'){
              mobileSendOtp.disabled = true;
              entermobileotp.setAttribute("type", "text");
              if (mobileNumberParentElement) {
                mobileNumberParentElement.classList.add('mb-3');
                mobileNumberParentElement.classList.remove('mb-0');
            }
            }else{
            mobileSendOtp.disabled = false; 
          }
          
        }else{
            mobileSendOtp.disabled = false;
            $('#id_mobile_numberError').html('<div class="invalid-feedback d-block" id="id_mobile_numberError">'+data.msg+'</div>');
        }
      },
    });
    buttonSubmit.disabled = true;

  } else {
    buttonSubmit.disabled = false;
      document.getElementById("id_mobile_number").focus();
      alert("Mobile number must have exactly 10 digits.");
  }
}

function VerifySendedContactNunber(value){
  result = value.replace(/[^0-9]/g,'');
  document.getElementById("id_mobile_otp").value = result;
  var mobileNumber = document.getElementById("id_mobile_number").value;
  var entermobileotp = document.getElementById("id_mobile_otp");
  var token = $("input[name=csrfmiddlewaretoken]").val();

  var mobileSendOtp = document.getElementById("id_mobile_send_otp");
  var buttonSubmit = document.getElementById("submit-basic-form");

  if (/^\d{6}$/.test(value)) {
    //alert('enter if condition with validation of 6 digit');
    $.ajax({
      url : '/user/auth/verify-signin-otp/',
      type: 'post',
      data: {'contact_number':mobileNumber, 'otp_number':value, 'csrfmiddlewaretoken':token},
      success(data){
        console.log(data);
        if(data.status == true){
          // alert('enter if condition');
          if(mobileNumber.length == '10'){
            $('#id_mobile_numberError').html('<div class="valid-feedback d-block" id="id_mobile_numberError">'+data.msg+'</div>');
            entermobileotp.setAttribute("readonly", "true");
            entermobileotp.setAttribute("type", "hidden");
            entermobileotp.focus();
            document.getElementById("id_mobile_number").setAttribute("readonly", "true");
            mobileSendOtp.disabled = true;
            buttonSubmit.disabled = false;
          }else{
            mobileSendOtp.disabled = false;
            buttonSubmit.disabled = true;
          }
            
          }else{
            // alert('enter else condition');
            mobileSendOtp.disabled = false;
            $('#id_mobile_numberError').html('<div class="invalid-feedback d-block" id="id_mobile_numberError">'+data.msg+'</div>');
        }
      },
    });
  }
}


function PhoneNumberExist(value){
  result = value.replace(/[^0-9]/g,'');
  document.getElementById("id_mobile_number").value = result;
  var mobileSendOtp = document.getElementById("id_mobile_send_otp");
  var token = $("input[name=csrfmiddlewaretoken]").val();
  var buttonSubmit = document.getElementById("submit-basic-form");

  if(value.length >= '6'){
    $.ajax({
        url : '/user/phone-number-check/',
        type: 'post',
        data: {'contact_number':value, 'csrfmiddlewaretoken':token},
        success(data){
          if(data == true){
            $('#id_mobile_numberError').html('<div class="valid-feedback d-block" id="id_mobile_numberError"></div>');
            if(value.length == '10'){
                mobileSendOtp.disabled = false;
              }else{
              mobileSendOtp.disabled = true; 
            }
            
          }else{
              //alert('enter else does not get');
              mobileSendOtp.disabled = true;
              $('#id_mobile_numberError').html('<div class="invalid-feedback d-block" id="id_mobile_numberError">Contact Number is Already Exist Please try another.</div>');
          }
        },
    });
  }
}

function handleSubCategoryChange(selectElement){
  var category_id = selectElement.value; 
  var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  console.log("url");

  $.ajax({
      url: '/inventory/add/load-subcategory/',
      type: 'POST',
      data: {'category_id':category_id,'csrfmiddlewaretoken':token},
      success: function(data){
          console.log('complete successfully.', data);
          if (data.status == true){
              var productType = document.getElementById('productType');
              $("#id_product_type").html(data.data); 
          }
          else{
              $("#id_product_type").html(data.data); 
          }
      },
      error: function(data){
          console.log('Check backend is not responding ....');
      },
  });
}

function handleCityChange(selectElement){
  var state_id = selectElement.value; 
  var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  console.log("url");

  $.ajax({
      url: '/dashboard/load-city/',
      type: 'POST',
      data: {'state_id':state_id,'csrfmiddlewaretoken':token},
      success: function(data){
          console.log('complete successfully.', data);
          if (data.status == true){
            console.log(data.data);
              //var productType = document.getElementById('productType');
              $("#id_city").html(data.data); 
          }
          else{
              $("#id_city").html(data.data); 
          }
      },
      error: function(data){
          console.log('Check backend is not responding ....');
      },
  });
}


function handleWarehouseAddCityChange(selectElement){
  var state_id = selectElement.value; 
  var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  console.log("url");

  $.ajax({
      url: '/dashboard/load-city/',
      type: 'POST',
      data: {'state_id':state_id,'csrfmiddlewaretoken':token},
      success: function(data){
          console.log('complete successfully.', data);
          if (data.status == true){
            console.log(data.data);
              //var productType = document.getElementById('productType');
              $("#id_add_warehouse_city").html(data.data); 
          }
          else{
              $("#id_add_warehouse_city").html(data.data); 
          }
      },
      error: function(data){
          console.log('Check backend is not responding ....');
      },
  });
}


function handleDataIdCityChange(selectElement, id){
  var state_id = selectElement.value; 
  var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  console.log("url");

  $.ajax({
      url: '/dashboard/load-city/',
      type: 'POST',
      data: {'state_id':state_id,'csrfmiddlewaretoken':token},
      success: function(data){
          console.log('complete successfully.', data);
          if (data.status == true){
            console.log(data.data);
              //var productType = document.getElementById('productType');
              $("#id_edit_warehouse_city_"+ id).html(data.data); 
          }
          else{
              $("#id_edit_warehouse_city_"+ id).html(data.data); 
          }
      },
      error: function(data){
          console.log('Check backend is not responding ....');
      },
  });
}