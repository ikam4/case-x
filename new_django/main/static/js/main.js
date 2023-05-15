let reg_pass = document.getElementById('id_password'), rep_pass = document.getElementById('rep_pass'), p_check = document.getElementById('pass_check');
let btn = document.getElementById('reg_form_btn');
function check_pass() {
    if (reg_pass.value.length < 8 && reg_pass.value.length > 0) {
        p_check.textContent = 'Пароль слишком короткий';
        btn.disabled = true;
    }
    else if (reg_pass.value != rep_pass.value && rep_pass.value.length > 0 && reg_pass.value.length > 0) {
        p_check.textContent = "Пароли не совпадают";
        btn.disabled = true;
    }
    else {
        p_check.textContent = '';
        btn.disabled = false;
    }
}
if ((reg_pass != null) && (rep_pass != null)){
    reg_pass.oninput = check_pass;
    rep_pass.oninput = check_pass;
}
