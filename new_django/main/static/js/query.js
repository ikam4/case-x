let roll_items, case_price, items_shuffle, opened_item;
let roll = false;
function add_roulette(){
    shuffle_items();
    document.querySelectorAll('.roll_item').forEach(e => e.remove());
    for (i = 0; i < 10; i++){
        $('#roulette').append(`
        <div class="roll_item">
            <img src="${items_shuffle[i]['path']}" alt="" class="case_skin_img">
            <p class="case_skin_name">${items_shuffle[i]['name']}</p>
        </div>`);
    }
    
}
$('.case_card').click(function(event){
    if (!roll){
        let id = $(this).attr('id').slice(4);
        $.ajax({
            type: "POST",
            url: "/case/api/get_case_items",
            data: {'id': id},
            success: function (data) {
                $('#case_skins').empty();
                let added_skins = Array();
                roll_items = data['case_items'];
                for (i in data['case_items']) {
                    if (!added_skins.includes((data['case_items'][i]['name']))){
                        $('#case_skins').append(`
                        <div class="case_skin" id="case_skin${i}">
                            <p class="case_skin_dots">...</p>
                            <img src="${data['case_items'][i]['path']}" alt="" class="case_skin_img">
                            <p class="case_skin_name">${data['case_items'][i]['name']}</p>
                        </div>`);
                        added_skins.push(data['case_items'][i]['name']);
                    }
                }
                add_roulette();
                let button_case_price = document.getElementById('amount_roll');
                case_price = data['case_price'];
                button_case_price.textContent = `${case_price}$`;
            }
        });
    }
});
function shuffle(array){
    array.sort(() => Math.random() - 0.5);
};
function shuffle_items(){
    items_shuffle = new Array();
    for (i in roll_items){
        console.log(roll_items[i]['chance']);
        let koef = Number(roll_items[i]['chance'])*1000;
        for (j = 0; j < koef; j++){
            items_shuffle.push(roll_items[i]);
        }
    }
    shuffle(items_shuffle);
};
function roll_animation(){
    let opened_el = $('.roll_item:nth-child(22)');
    console.log(opened_el);
    let line = $('.vertical-line');
    let roll_els = $('.roll_item');
    let op_el_cor = opened_el.offset()['left'], line_cor = line.offset()['left'] - Math.random() * 160 - 5;
    console.log(roll_els);
    setTimeout(function() {
        roll_els.css('left', `-${op_el_cor - line_cor}px`);
    }, 100)
}
$('#roll_btn').click(function(event){
    console.log(roll);
    if (!roll){
        roll = true;
        console.log(roll_items);
        console.log(items_shuffle)
        opened_item = Math.round(Math.random()*999);
        console.log(items_shuffle[opened_item]);
        let a = new Array();
        for (i = opened_item - 10; i < opened_item + 11; i++) {
            if (i < 0) a.push(items_shuffle[items_shuffle.length + i]);
            else if (i > 999) a.push(items_shuffle[i - 999]);
            else a.push(items_shuffle[i]);
            console.log(i);
        }
        console.log(a);
        for (i of a){
            $('#roulette').append(`
            <div class="roll_item">
                <img src="${i['path']}" alt="" class="case_skin_img">
                <p class="case_skin_name">${i['name']}</p>
            </div>`);
        }
        $.ajax({
            type: "POST",
            url: "/case/api/buy_case",
            data: {'case_price': case_price},
            success: function (data) {
                if (data['status'] == 'success'){
                    $('#balance').text(data['balance']);
                    roll_animation();
                    setTimeout(function(){
                        confirm("Продать скин?");
                        add_roulette();
                        roll = false;
                    }, 10000)
                    let element = items_shuffle[opened_item];
                    for (i in roll_items){
                        if (roll_items[i]['name'] == element['name']){
                            $.ajax({
                                type: "POST",
                                url: "/case/api/inv_add_item",
                                data: {
                                    'opened_item': i,
                                    'item_name': roll_items[i]['name'],
                                    'item_price': roll_items[i]['price'], 
                                    'case_price': case_price
                                },
                                success: function (data) {
                                    
                                }
                           
                            });
                            break;
                        }
                    }
                }
                else {
                    alert(data['status_descr']);
                    roll = false;
                }
            }
        });
    }
});