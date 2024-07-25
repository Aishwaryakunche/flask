$(document).ready(function () {

    // Initialize error flags
    let usernameError = true;
    let emailError = true;
    let passwordError = true;
    let confirmPasswordError = true;

    // Validate Username
    $('#usercheck').hide();
    $('#usernames').keyup(function () {
        validateUsername();
    });

    function validateUsername() {
        let usernameValue = $('#usernames').val();
        if (usernameValue.length === 0) {
            $('#usercheck').show().text("**Username is required");
            usernameError = false;
        } else if (usernameValue.length < 3 || usernameValue.length > 10) {
            $('#usercheck').show().text("**Length of username must be between 3 and 10 characters");
            usernameError = false;
        } else {
            $('#usercheck').hide();
            usernameError = true;
        }
    }

    // Validate Email
    const email = $('#email');
    email.on('blur', function () {
        validateEmail();
    });

    function validateEmail() {
        let regex = /^([_\-\.0-9a-zA-Z]+)@([_\-\.0-9a-zA-Z]+)\.([a-zA-Z]{2,7})$/;
        let emailValue = email.val();
        if (regex.test(emailValue)) {
            email.removeClass('is-invalid').addClass('is-valid');
            emailError = true;
        } else {
            email.removeClass('is-valid').addClass('is-invalid');
            emailError = false;
        }
    }

    // Validate Password
    $('#passcheck').hide();
    $('#password').keyup(function () {
        validatePassword();
    });

    function validatePassword() {
        let passwrdValue = $('#password').val();
        if (passwrdValue.length === 0) {
            $('#passcheck').show().text("**Password is required");
            passwordError = false;
        } else if (passwrdValue.length < 3 || passwrdValue.length > 10) {
            $('#passcheck').show().text("**Length of password must be between 3 and 10 characters");
            $('#passcheck').css("color", "red");
            passwordError = false;
        } else {
            $('#passcheck').hide();
            passwordError = true;
        }
    }

    // Validate Confirm Password
    $('#conpasscheck').hide();
    $('#conpassword').keyup(function () {
        validateConfirmPassword();
    });

    function validateConfirmPassword() {
        let passwrdValue = $('#password').val();
        let conpasswrdValue = $('#conpassword').val();
        if (conpasswrdValue.length === 0) {
            $('#conpasscheck').show().text("**Please confirm your password");
            confirmPasswordError = false;
        } else if (conpasswrdValue !== passwrdValue) {
            $('#conpasscheck').show().text("**Passwords do not match");
            confirmPasswordError = false;
        } else {
            $('#conpasscheck').hide();
            confirmPasswordError = true;
        }
    }

    // Submit button
    $('#submitbtn').click(function (e) {
        validateUsername();
        validatePassword();
        validateEmail();
        validateConfirmPassword();

        if (usernameError && passwordError && confirmPasswordError && emailError) {
            return true; // Allow form submission
        } else {
            e.preventDefault(); // Prevent form submission
            return false;
        }
    });

});
