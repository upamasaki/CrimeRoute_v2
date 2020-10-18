function today(item_period_id) {
    //今日の日時を表示
    var date = new Date()
    var year = date.getFullYear()
    var month = date.getMonth() + 1
    var day = date.getDate()
    
    var toTwoDigits = function (num, digit) {
        num += ''
        if (num.length < digit) {
        num = '0' + num
        }
        return num
    }
    
    var yyyy = toTwoDigits(year, 4)
    var mm = toTwoDigits(month, 2)
    var dd = toTwoDigits(day, 2)
    var ymd = yyyy + "-" + mm + "-" + dd;
    
    document.getElementById(item_period_id).value = ymd;
}


function tomorrow(item_period_id) {
    var tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate()+1); //翌日の日付を取得
    var yyyy = tomorrow.getFullYear();
    var mm = ("0"+(tomorrow.getMonth()+1)).slice(-2);
    var dd = ("0"+tomorrow.getDate()).slice(-2);
    document.getElementById(item_period_id).value=yyyy+'-'+mm+'-'+dd;
}